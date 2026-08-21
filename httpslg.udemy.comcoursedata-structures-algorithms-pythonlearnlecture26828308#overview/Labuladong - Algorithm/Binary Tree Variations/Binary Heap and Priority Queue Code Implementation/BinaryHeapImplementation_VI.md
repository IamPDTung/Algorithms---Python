
---

# Binary Heap / Priority Queue Code Implementation

## 1. Goal

**Hàng đợi ưu tiên (priority queue)** là hàng đợi mà phần tử có ưu tiên
cao nhất luôn ra trước. Cách xây dựng kinh điển là dùng cây nhị phân heap:
heap giữ phần tử ưu tiên cao nhất ở gốc, và chỉ cần hai phép sửa cục bộ --
`swim` và `sink` -- để giữ điều đó đúng sau mọi thay đổi.

**Vì sao biểu diễn bằng mảng lại quan trọng ở đây?** Vì cây là *ngầm
định*: không có con trỏ nào cả. Cha và con của một nút chỉ là phép toán
trên chỉ số. Điều đó khiến phần cài đặt nhỏ gọn, nhanh và thân thiện với
bộ nhớ đệm.

Phần cài đặt trong `BinaryHeapImplementation.py` cung cấp:

- Lớp `PriorityQueue` tổng quát với bộ so sánh cắm được (max-heap hoặc
  min-heap), gồm `push`, `pop`, `peek`, `update`, `remove`, `is_valid`.
- Lớp `IndexMinPQ` (hàng đợi ưu tiên có chỉ số) dùng cho thuật toán đồ
  thị, với `insert`, `decrease_key`, `increase_key`, `del_min`,
  `min_index`.
- Demo Dijkstra đường đi ngắn nhất dùng `IndexMinPQ`.

Nguồn tham khảo:

- [Binary Heap/Priority Queue Code Implementation](https://labuladong.online/en/algo/data-structure-basic/binary-heap-implement/)
- [Basic Concept of Binary Heap](https://labuladong.online/en/algo/data-structure-basic/binary-heap-basic/)

## 2. Key Challenges

Hàng đợi ưu tiên dựa trên heap phải trả lời hai câu hỏi ở mọi lần thay
đổi:

```text
challenge 1: the tree is 2D but the array is 1D
  -> map indices: parent(i)=(i-1)//2, left(i)=2i+1, right(i)=2i+2

challenge 2: after insert or delete, the heap order may break
  -> restore it with exactly two local fixes:
       swim : a child became too "big"  -> bubble it up
       sink : a parent became too "small" -> push it down
```

Mọi thứ khác (peek, size, contains) chỉ là sổ sách tầm thường. Làm đúng
`swim` và `sink` chính là toàn bộ trận chiến.

## 3. Insertion: push / swim

Chèn sẽ thêm vào cuối mảng, rồi swim phần tử mới lên cho tới khi cha của nó
không còn nhỏ hơn:

```text
push(7)  into max-heap [9,6,8,5,3,2,1]  (0-indexed: [9,6,8,5,3,2,1])

  append 7 at the end:
     [9,6,8,5,3,2,1,7]
      index:0 1 2 3 4 5 6 7
                        ^

  swim(7): parent = (7-1)//2 = 3  -> 5 < 7, swap
     [9,6,8,7,3,2,1,5]
      index:0 1 2 3 ...
  swim(3): parent = (3-1)//2 = 1  -> 6 < 7, swap
     [9,7,8,6,3,2,1,5]
  swim(1): parent = 0  -> 9 >= 7, stop
```

```text
swim(k):
  while k > 0:
      parent = (k-1)//2
      if parent >= heap[k]: break
      swap(parent, k)
      k = parent
```

## 4. Deletion: pop / sink

Phần tử đỉnh là gốc. Để pop: đưa phần tử cuối lên gốc, rồi sink nó xuống,
luôn đổi chỗ với con lớn hơn:

```text
pop() from [9,6,8,5,3,2,1]  (max = 9)

  save 9; move last element (1) to the root:
     [1,6,8,5,3,2]          9 is returned

  sink(0): children 6,8 -> larger is 8 -> swap
     [8,6,1,5,3,2]
  sink(2): children 3,2 -> larger is 3 -> 1 < 3, swap
     [8,6,3,5,1,2]
  sink(4): no children. done.
```

```text
sink(k):
  while 2k+1 < n:
      j = 2k+1
      if j+1 < n and heap[j] < heap[j+1]: j += 1   # larger child
      if heap[k] >= heap[j]: break
      swap(k, j)
      k = j
```

## 5. Query: peek

Phần tử lớn nhất luôn ở chỉ số 0, nên peek là O(1) và không cần sửa gì cả:

```text
peek() -> heap[0]
```

`is_empty` và `len` chỉ là kiểm tra độ dài mảng.

## 6. Simulating the Binary Tree with an Array

Phần cài đặt này dùng chỉ số **bắt đầu từ 0** (quy ước hơi khác với quy ước
bắt đầu từ 1 trong bài "Basic Concept" -- cả hai đều hợp lệ):

```text
0-indexed array [_, a, b, c, d, e, f, g]:

        a (index 0)
       / \
    b (1) c (2)
   / \   / \
d(3) e(4) f(5) g(6)

  parent(i)  = (i-1)//2
  left(i)    = 2*i+1
  right(i)   = 2*i+2

  check: parent(5)=2 (f's parent is c)          OK
         left(1)=3 (b's left child is d)        OK
         right(1)=4 (b's right child is e)      OK
```

Phép toán chỉ số là "cái cây" duy nhất mà code từng đụng tới -- không có
đối tượng `Node`, không có con trỏ `left`/`right`.

## 7. Code Implementation of the Generic PriorityQueue

Bộ so sánh `less(a, b)` là núm xoay duy nhất giữa max-heap và min-heap:

```python
class PriorityQueue(Generic[T]):
    def __init__(self, less=None):
        self._data = []
        self._less = less if less is not None else (lambda a, b: a < b)
```

```text
default:  less(a,b) = a < b   -> a "smaller" sinks, largest pops first
                                = MAX-heap
pass:     less(a,b) = a > b   -> smallest pops first
                                = MIN-heap
```

API công khai:

```text
push(item)     O(log N)   append + swim
pop()          O(log N)   swap root/last + sink
peek()         O(1)       read heap[0]
update(a, b)   O(N)       replace a with b, then swim + sink
remove(a)      O(N)       remove a, then swim + sink
len / is_empty O(1)
```

`update` và `remove` quét mảng tuyến tính (O(N)) vì heap không có cách nào
tìm phần tử bất kỳ nhanh hơn; một khi đã tìm thấy, việc sửa vẫn chỉ là swim
+ sink.

## 8. Improved Priority Queue: Dynamic Priority and IndexMinPQ

Hàng đợi ưu tiên thường không thể hạ ưu tiên của một phần tử một cách hiệu
quả, vì nó không có tay cầm để tìm phần tử đó. Thuật toán Dijkstra cần
đúng điều này: khi phát hiện đường ngắn hơn tới một đỉnh, khoảng cách của
đỉnh đó phải giảm xuống.

**Hàng đợi ưu tiên có chỉ số (indexed priority queue)** khắc phục bằng cách
đánh khóa các phần tử theo chỉ số nguyên:

```text
IndexMinPQ arrays:
   pq       : the heap itself, holding INDICES
   qp       : index -> its position in pq   (-1 if absent)
   priority : index -> its current priority

   min-heap by priority: pq[0] is the index with the smallest priority.

   decrease_key(i, p): update priority[i], then swim only at qp[i]
                       -> O(log N), no search needed
```

```text
        pq (heap of indices)          priority array
   pos:  0     1     2            idx:  0     1     2     3
         [2]   [0]   [3]               [4.0] [7.0] [1.5] [2.0]
          ^                                 ^
    smallest priority                     qp: [1, -1, 0, 2]
    is index 2 (1.5)
```

Dijkstra trên đồ thị demo dùng `decrease_key` mỗi khi một khoảng cách được
cải thiện:

```text
demo graph (undirected):
        1
  0 --------- 1
  |           |
  | 4      5  |
  |           |
  2 --------- 3
        1

  edge weights: 0-1 = 1, 0-2 = 4, 1-3 = 5, 2-3 = 1
  (the diagonal edge 1-2 = 2 is omitted from the drawing)

  shortest distances from node 0:
        dist[0]=0, dist[1]=1, dist[2]=3, dist[3]=4
```

## 9. Complexity

```text
PriorityQueue            IndexMinPQ
----------------------   ----------------------
push      O(log N)       insert          O(log N)
pop       O(log N)       del_min         O(log N)
peek      O(1)           min_index       O(1)
update    O(N)           decrease_key    O(log N)
remove    O(N)           increase_key    O(log N)
contains  O(N)           contains        O(1)
memory    O(N)           memory          3*O(N)
```

IndexMinPQ đánh đổi một mảng `qp` để có O(1) tra cứu và O(log N)
decrease-key -- chính là lý do Dijkstra chạy trong O(E log V).

## 10. Demo Walkthrough

Chạy `BinaryHeapImplementation.py` in ra:

```text
=== Priority queue demo ===
max-heap pop order: [9, 6, 5, 4, 3, 2, 1, 1]
min-heap pop order: [1, 1, 2, 3, 4, 5, 6, 9]
after update(5,100) and remove(10): [100, 3]

IndexMinPQ basic ops...
IndexMinPQ basic ops passed.

Dijkstra with IndexMinPQ...
shortest distances from node 0: [0.0, 1.0, 3.0, 4.0]
```

Điều demo chứng minh:

```text
- the same pushes give [9,6,5,4,3,2,1,1] with the default max-heap
- flipping the comparator gives the min-heap [1,1,2,3,4,5,6,9]
- update(5,100) reprioritizes and 100 pops first; remove works
- decrease_key/increase_key flip the minimum instantly
- Dijkstra with the IndexMinPQ returns the correct distances
```

## 11. Limitations and Summary

```text
strengths:
  - O(log N) push/pop, O(1) peek, no pointers
  - one comparator turns a max-heap into a min-heap
  - the IndexMinPQ supports O(log N) decrease-key for graph algorithms

trade-offs:
  - arbitrary-item search/update is O(N) in a plain PQ
  - no iteration in sorted order (a heap is not a BST)
  - duplicate items complicate "remove by value" semantics

when to use:
  - repeated push/pop of the current max/min
  - Dijkstra / Prim / A* need the IndexMinPQ form
```

Tóm tắt trong một câu: hàng đợi ưu tiên là một binary heap trong một mảng,
chỉ có hai phép duy trì là swim (khi push) và sink (khi pop), và thêm một
ánh xạ chỉ số sẽ nâng nó thành cấu trúc decrease-key O(log N) mà Dijkstra
cần.
