
---

# Basic Concept of Binary Heap

## 1. Goal

**Cây nhị phân heap (binary heap)** là một cây nhị phân đầy đủ thỏa mãn
**tính chất thứ tự heap**: trong max-heap, mỗi cha luôn lớn hơn hoặc bằng
các con của nó, nên phần tử lớn nhất luôn nằm ở gốc. Vì cây đầy đủ, nó
không cần con trỏ -- nó sống ngay trong một mảng phẳng.

**Vì sao nó ra đời?** Ta thường cần liên tục lấy "phần tử lớn nhất đến giờ"
ra khỏi một tập hợp đang thay đổi. Mảng đã sắp xếp làm việc đó trong O(1)
nhưng chèn tốn O(N). Cây heap là điểm cân bằng: nó giữ các phần tử "được
sắp xếp động" để cả **chèn lẫn xóa-max đều O(log N)** và phần tử lớn nhất
luôn nhìn thấy trong O(1). Nó là động cơ đằng sau hàng đợi ưu tiên và sắp
xếp heap.

Phần cài đặt trong `BinaryHeapBasics.py` cung cấp:

- Lớp `MaxHeap` với `insert`, `del_max`, `peek`, `is_valid`.
- Hai hàm trợ giúp lõi `_swim` và `_sink` duy trì bất biến.
- Hàm `heapify` dựng heap trong O(N) từ mảng bất kỳ (chìm từ dưới lên).
- Hàm `heap_sort` trả về mảng theo thứ tự tăng dần.
- Hàm vẽ ASCII `draw()` tái dựng cây từ mảng.

Nguồn tham khảo:

- [Basic Concept of Binary Heap](https://labuladong.online/en/algo/data-structure-basic/binary-heap-basic/)
- [Binary Heap/Priority Queue Code Implementation](https://labuladong.online/en/algo/data-structure-basic/binary-heap-implement/)

## 2. Two Properties: Complete Tree + Heap Order

Cây nhị phân heap là giao của hai ý tưởng:

```text
1. COMPLETE binary tree:
   every level is full, except possibly the last,
   and the last level is filled left to right.

        (a)                     (a)
       /   \                   /   \
     (b)   (c)   OK          (b)   (c)   NOT complete
     / \   /                / \     \
   (d)(e)(f)              (d)(e)    (f)
                              ^ gap in the middle

2. HEAP ORDER (max-heap):
   parent >= child, recursively.

        (9)                     (9)
       /   \                   /   \
     (6)   (8)    OK         (10)  (8)   broken: 10 > 9
     / \   / \               / \
   (5)(3)(2)(7)            (5)(3)
```

Tính chất cây đầy đủ giúp có thể biểu diễn bằng mảng. Tính chất thứ tự heap
giúp tìm phần tử lớn nhất trong O(1).

## 3. The Array Representation

Một cây đầy đủ ánh xạ lên mảng mà không cần con trỏ. Dùng chỉ số bắt đầu từ
1 (chỉ số 0 là ô giả), công thức là:

```text
parent(i) = i // 2
left(i)   = 2*i
right(i)  = 2*i + 1

        index:      1
                   / \
                 2     3
                / \   / \
               4   5 6   7

  array (index 0 unused):
  [X, a, b, c, d, e, f, g]
   0  1  2  3  4  5  6  7

  check: parent of index 5 (e) is 5//2 = 2 (b)      OK
         left of index 2 (b) is 4 (d)               OK
         right of index 2 (b) is 5 (e)              OK
```

Heap trong demo, vẽ từ mảng của nó:

```text
          9
      6     8
    5   3   2   7
   4  1
```

tương ứng với mảng `[_, 9, 6, 8, 5, 3, 2, 7, 4, 1]`.

## 4. swim: Inserting an Element

Chèn gồm hai bước: thêm vào cuối, rồi **swim (bơi lên)** giá trị mới cho
tới khi cha của nó không còn nhỏ hơn.

```text
insert(7) into [9,6,8,5,3,2,1]:

  step 1: append at the end
          9
       6     8
     5   3  2   1
    7  <- swim starts here

  step 2: swim up (7 vs parent 5 -> swap)
          9
       6     8
     7   3  2   1
    5

  step 3: swim up (7 vs parent 6 -> swap)
          9
       7     8
     6   3  2   1
    5

  step 4: 7 vs parent 9 -> 9 > 7, stop.
  heap order restored, O(log N).
```

`swim` chỉ di chuyển giá trị lên trên dọc theo đường tới gốc:

```text
swim(k):
  while k > 1 and parent(k) < heap[k]:
      swap(k, parent(k))
      k = parent(k)
```

## 5. sink: Deleting the Maximum

Phần tử lớn nhất là gốc. Để xóa nó: đưa phần tử cuối lên gốc, rồi **sink
(chìm xuống)** phần tử đó, luôn đổi chỗ với con lớn hơn.

```text
del_max() from [9,6,8,5,3,2,1]  (max = 9)

  step 1: put the last element (1) at the root
          1
       6     8
     5   3  2  X

  step 2: sink (children 6, 8 -> larger is 8, swap)
          8
       6     1
     5   3  2

  step 3: sink (children 2, X -> larger is 2, swap with 1? 1 < 2)
          8
       6     2
     5   3  X
  stop: no more children. O(log N).
```

`sink` đổi chỗ với con **lớn hơn** để tính chất max-heap được bảo toàn:

```text
sink(k):
  while 2*k <= n:
      j = 2*k
      if j < n and heap[j] < heap[j+1]: j += 1   # pick larger child
      if heap[k] >= heap[j]: break
      swap(k, j)
      k = j
```

## 6. Building a Heap: O(N) heapify

Chèn N phần tử lần lượt tốn O(N log N). Nhưng nếu bắt đầu từ một mảng bất
kỳ, ta có thể sửa nó trong **O(N)** bằng cách chìm mọi nút không phải lá từ
dưới lên:

```text
array (not a heap yet):
  [_, 5, 3, 8, 1, 9, 2, 7, 4, 6]

  bottom-up sink from n//2 = 4 down to 1:

  sink(4): 1 has child 6 -> swap      -> 6
  sink(3): 8 has children 2,7 -> swap with 7 -> 7
  sink(2): 3 has children 6,9 -> swap with 9 -> 9, then 3 sinks again
  sink(1): 5 vs 9/7 -> swap with 9 -> 9, sink 5 down...

  final heap:
            9
        6       8
      5   3   2   7
     4  1
```

Vì sao là O(N)? Hầu hết các nút nằm gần đáy và chỉ chìm một hoặc hai tầng.
Cụ thể, tổng công việc là một chuỗi hình học:

```text
N/2 nodes sink <= 1 level,  N/4 sink <= 2,  N/8 sink <= 3, ...

sum = N/2*1 + N/4*2 + N/8*3 + ... = O(N)
```

## 7. The Most Common Use: Priority Queue

Hàng đợi ưu tiên là hàng đợi mà phần tử có ưu tiên cao nhất ra trước. Cây
heap triển khai nó trực tiếp:

```text
            push               pop
         (insert+swim)     (swap+sink)
   input -------> [max-heap] -------> largest first
                    O(log N)           O(log N)

  peek: look at the root            O(1)
```

Ứng dụng điển hình: đường đi ngắn nhất Dijkstra, lập lịch theo độ khẩn
cấp, trộn K luồng đã sắp xếp, bài toán top-K -- bất cứ thứ gì liên tục hỏi
"phần tử lớn/nhỏ nhất hiện tại là gì?"

## 8. Another Use: Heap Sort

Sắp xếp heap tái sử dụng chính cái heap: dựng heap, rồi lặp lại việc đổi
gốc với phần tử cuối và chìm xuống.

```text
[5,3,8,1,9,2,7,4,6]

  step 1: heapify                    step 2: swap root with last
           9                          1
        6     8                    6     8
      5  3  2  7                  5  3  2  7
     4  1                         4  [9]  <- 9 is now sorted

  step 3: sink the new root, shrink the heap
           8
        6     7
      5  3  2  1
     4  [9]

  repeat ... the "sorted" zone grows from the right end:
  [1,2,3,4,5,6,7,8,9]
```

Tổng chi phí là O(N log N): O(N) để dựng, rồi N-1 lần chìm, mỗi lần O(log
N). Nó sắp xếp tại chỗ, không tốn bộ nhớ thêm.

## 9. Complexity

```text
operation        cost
---------------- ---------
peek (max)       O(1)
insert (push)    O(log N)
del_max (pop)    O(log N)
heapify (build)  O(N)
heap_sort        O(N log N)
memory           O(N), in place (no extra pointers)
```

Chiều cao của cây đầy đủ với N nút đúng bằng floor(log2(N)), giới hạn mọi
đường đi swim/sink.

## 10. Demo Walkthrough

Chạy `BinaryHeapBasics.py` in ra:

```text
=== Binary heap basics demo ===
insert/pop order (max first): [9, 6, 5, 4, 3, 2, 1, 1]

heapify([5,3,8,1,9,2,7,4,6]) tree:
          9
      6     8
    5   3   2   7
   4  1

heap_sort randomized check passed for 50 arrays.
All assertions passed.
```

Điều demo chứng minh:

```text
- inserting 3,1,4,1,5,9,2,6 keeps the heap valid after every insert
- popping returns [9,6,5,4,3,2,1,1], largest first
- heapify produces a valid heap whose root is the maximum
- heap_sort matches Python's sorted() on 50 random arrays
```

## 11. Limitations and Summary

```text
strengths:
  - O(log N) insert AND delete-max, O(1) peek
  - no pointers: cache-friendly flat array
  - in-place heap sort with no extra memory

trade-offs:
  - cannot search for an arbitrary element efficiently (O(N))
  - no locality of keys: it is NOT a sorted structure like a BST
  - no easy merge of two heaps (O(N) unless using a meldable heap)

when to use:
  - you only need the max/min and repeated push/pop
  - for arbitrary-element search, prefer a BST or hash table
```

Tóm tắt trong một câu: cây nhị phân heap là một cây nhị phân đầy đủ nằm
trong một mảng, giữ phần tử lớn nhất ở gốc chỉ bằng hai phép sửa cục bộ --
swim khi chèn và sink khi xóa.
