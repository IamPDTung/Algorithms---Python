# Kiến thức nền tảng về Segment Tree và hình ảnh minh họa

## 1. Mục tiêu

Segment tree là một cây nhị phân mà các lá là các phần tử của mảng và các
nút bên trong lưu giá trị tổng hợp (sum, min, max, ...) trên khoảng chỉ số
của chúng. Vì mọi nút bên trong nhớ giá trị tổng hợp của cả khoảng của
mình, cả truy vấn khoảng lẫn cập nhật điểm đều hoàn thành trong `O(log N)`
thay vì `O(N)`.

Vì sao nó ra đời? Một mảng thường cho phép đọc `O(1)`, nhưng truy vấn
khoảng như `sum(l..r)` phải quét `O(N)` phần tử và cập nhật điểm mất `O(1)`.
Điều đó ổn với dữ liệu tĩnh, nhưng nhiều bài toán trộn truy vấn khoảng với
cập nhật điểm động: ví dụ các bài online judge hỏi "tổng của một khoảng, rồi
đổi một phần tử, rồi hỏi tiếp, ...". Làm mỗi truy vấn khoảng bằng cách quét
tốn `O(N)`, và `M` truy vấn tốn `O(N*M)`, quá chậm với đầu vào lớn. Segment
tree đánh đổi chi phí dựng `O(N)` và bộ nhớ `O(N)` để mọi truy vấn và mọi
cập nhật đều là `O(log N)`.

Cài đặt trong `SegmentTreeBasics.py` cung cấp:

- `SegmentTree`: cây tổng hợp sum với cập nhật điểm và truy vấn khoảng.
- `LazySegmentTree`: cộng khoảng + tổng khoảng với lazy propagation, để
  cập nhật cả một khoảng trong `O(log N)`.
- `draw()`: vẽ cây dạng ASCII kèm khoảng để học.
- Kiểm tra ngẫu nhiên đối chiếu cây với một danh sách tham chiếu thường.

Nguồn tham khảo:

- [Segment Tree Basics and Visualization](https://labuladong.online/en/algo/data-structure-basic/segment-tree-basic/)

## 2. Bối cảnh ứng dụng: vì sao mảng và mảng prefix-suffix thất bại

Dữ liệu tĩnh có thể được phục vụ bằng công cụ đơn giản hơn. Với mảng cố
định, mảng prefix sum trả lời `sum(l..r)` trong `O(1)`:

```text
values:     [1, 3, 5, 7, 9, 11]
prefix:     [1, 4, 9, 16, 25, 36]

sum(2..4) = prefix[4] - prefix[1] = 25 - 4 = 21     O(1)
```

Nhưng ngay khi một phần tử thay đổi, mọi prefix sum sau nó phải tính lại,
tốn `O(N)` cho mỗi cập nhật:

```text
update index 3:  5 -> 8

values:     [1, 3, 5, 8, 9, 11]
prefix:     [1, 4, 9, 17, 26, 37]
                        ^--- must touch indices 3, 4, 5   O(N)
```

Thủ thuật selection sort chỉ dùng prefix và suffix *minimum*, vốn cũng
tĩnh. Nó không thể trả lời "minimum trên khoảng tùy ý [l, r]" sau các cập
nhật:

```text
selection sort:
  find min of [0..N-1]  -> prefix/suffix min works
  find min of [1..N-1]  -> suffix min still works
  find min of [2..N-1]  -> still a suffix ... always the suffix!

arbitrary range [l, r] after updates:
  sum/min over [l, r] where l and r are arbitrary -> prefix array useless
  an update at any index invalidates the whole prefix array -> O(N) fix
```

Vậy bối cảnh đòi hỏi segment tree là: truy vấn khoảng trên các khoảng *tùy
ý* (không chỉ prefix hay suffix) xen kẽ với cập nhật điểm hoặc khoảng động.
Cả hai đều phải nhanh.

## 3. API chính

`SegmentTree` (tổng hợp sum, cập nhật điểm):

```python
tree = SegmentTree(values)

tree.query(l, r)        # inclusive sum over [l, r]     O(log N)
tree.update(i, v)       # values[i] = v                 O(log N)
tree.to_list()          # copy of the underlying values O(N)
tree.size()             # number of elements            O(1)
tree.draw()             # ASCII rendering               O(N)
```

`LazySegmentTree` (cộng khoảng, tổng khoảng):

```python
tree = LazySegmentTree(values)

tree.range_add(l, r, delta)  # values[i] += delta for l<=i<=r   O(log N)
tree.range_sum(l, r)         # inclusive sum over [l, r]         O(log N)
tree.point_get(i)            # current value at index i          O(log N)
```

## 4. Nguyên lý cốt lõi: lá là phần tử, nút trong là khoảng

Với `values = [1, 3, 5, 7, 9, 11]` segment tree trông như thế này. Mỗi nút
được gán nhãn bởi khoảng `[l, r]` và tổng nó lưu:

```text
                 [0,5]=36
                /         \
          [0,2]=9          [3,5]=27
          /     \          /      \
     [0,1]=4   [2,2]=5  [3,4]=16  [5,5]=11
     /     \             /     \
 [0,0]=1 [1,1]=3    [3,3]=7  [4,4]=9

interval [0,5]  covers everything   sum = 1+3+5+7+9+11 = 36
interval [3,5]  covers 7, 9, 11     sum = 27
interval [3,4]  covers 7, 9         sum = 16
leaf    [0,0]  element 1
```

Hai quy tắc bất biến:

```text
1. A leaf holds exactly one element:  tree[leaf] = values[i]
2. An internal node is the merge of its children:
   tree[node] = tree[left_child] + tree[right_child]
```

Hình dạng tương tự áp dụng cho min/max/gcd: chỉ phép hợp nhất đổi khác.

## 5. Dựng cây

Dựng đệ quy: chia khoảng tại `mid`, dựng hai con, rồi hợp nhất. Cây được
lưu trong một mảng phẳng kích thước `4*N` theo layout heap: con của `node`
là `2*node` và `2*node+1`, gốc tại `1`.

```python
def _build(node, start, end):
    if start == end:
        tree[node] = values[start]      # leaf: one element
        return
    mid = (start + end) // 2
    _build(2 * node, start, mid)        # left half
    _build(2 * node + 1, mid + 1, end)  # right half
    tree[node] = tree[2 * node] + tree[2 * node + 1]  # merge
```

Đệ quy cho `[1, 3, 5, 7, 9, 11]`:

```text
_build(1, 0, 5)            interval [0,5]
 |-- _build(2, 0, 2)       interval [0,2]
 |    |-- _build(4, 0, 1)  interval [0,1]
 |    |    |-- _build(8, 0, 0)   -> tree[8] = 1
 |    |    |-- _build(9, 1, 1)   -> tree[9] = 3
 |    |    `-- tree[4] = 1 + 3 = 4
 |    |-- _build(5, 2, 2)  -> tree[5] = 5
 |    `-- tree[2] = 4 + 5 = 9
 |-- _build(3, 3, 5)       interval [3,5]
 |    |-- _build(6, 3, 4)  interval [3,4]
 |    |    |-- _build(12, 3, 3)  -> tree[12] = 7
 |    |    |-- _build(13, 4, 4)  -> tree[13] = 9
 |    |    `-- tree[6] = 7 + 9 = 16
 |    |-- _build(7, 5, 5)  -> tree[7] = 11
 |    `-- tree[3] = 16 + 11 = 27
 `-- tree[1] = 9 + 27 = 36

node indices follow the heap layout: 1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 13
```

Chi phí dựng: `O(N)` nút được ghé, mỗi nút làm `O(1)`.

## 6. Truy vấn: vì sao O(log N)

Truy vấn khoảng đi xuống từ gốc. Tại mỗi nút có ba trường hợp:

```text
case 1  no overlap:   right < start or end < left    -> return 0
case 2  full overlap: left <= start and end <= right -> return tree[node]
case 3  partial:      descend into both children and add the results
```

Truy vấn `[2, 4]` trên `[1, 3, 5, 7, 9, 11]` (kỳ vọng `5+7+9 = 21`). Các
nút được phủ được đánh dấu `[*]`:

```text
                 [0,5]=36
                /         \
          [0,2]=9         [3,5]=27
          /     \          /      \
     [0,1]=4   [2,2]=5* [3,4]=16* [5,5]=11
     /     \             /     \
 [0,0]=1 [1,1]=3    [3,3]=7  [4,4]=9

[0,5]  partial  -> descend
[0,2]  partial  -> descend
[0,1]  no overlap with [2,4]  -> return 0
[2,2]  full overlap          -> return 5      [*]
[3,5]  partial  -> descend
[3,4]  full overlap          -> return 16     [*]
[5,5]  no overlap with [2,4] -> return 0

answer = 5 + 16 = 21        only 2 full nodes visited
```

Thêm vài khoảng mẫu trên cùng cây:

```text
query [0, 5]:
                 [0,5]=36*   full overlap -> answer 36
   visited nodes: 1

query [3, 3]:
   [0,5] partial -> [3,5] partial -> [3,4] partial -> [3,3]* -> answer 7
   visited nodes: 4 along one path

query [1, 3]:
                 [0,5]=36
                /         \
          [0,2]=9         [3,5]=27
          /     \          /      \
     [0,1]=4   [2,2]=5* [3,4]=16* [5,5]=11
     /     \
 [0,0]=1 [1,1]=3*

   [0,1] partial -> [1,1] full -> 3
   [2,2] full -> 5
   [3,4] partial -> [3,3] full -> 7
   answer = 3 + 5 + 7 = 15

query [0, 2]:
   [0,2] full overlap -> return 9
   visited nodes: 1
```

Vì sao chỉ `O(log N)` nút? Ở mỗi tầng truy vấn ghé nhiều nhất hai nút
"biên" cộng các nút phủ đầy giữa chúng, và một nút phủ đầy dừng đệ quy
ngay. Khoảng chia đôi ở mỗi tầng, nên có `log2(N)` tầng:

```text
level 0   [0,5]                     1 node
level 1   [0,2] [3,5]               2 boundary nodes
level 2   [0,1] [2,2] [3,4] [5,5]   <= 2 boundary + full nodes
level 3   leaves                     only the needed full leaves

total visited nodes per level: <= 4   ->   O(log N) nodes in total
```

## 7. Cập nhật điểm: vì sao O(log N)

Cập nhật điểm chạm đúng một lá rồi tính lại mọi tổ tiên trên đường về gốc.
Đường từ lá lên gốc có `log2(N) + 1` nút.

Cập nhật `update(3, 8)` trên `[1, 3, 5, 7, 9, 11]`. Đường đi được đánh dấu
bằng mũi tên:

```text
before update:

                 [0,5]=36
                /         \
          [0,2]=9         [3,5]=27
          /     \          /      \
     [0,1]=4   [2,2]=5  [3,4]=16  [5,5]=11
     /     \             /     \
 [0,0]=1 [1,1]=3    [3,3]=7  [4,4]=9

after update(3, 8):

                 [0,5]=37
                    ^
          [0,2]=9  |   [3,5]=28
                    ^
     [0,1]=4  |  [2,2]=5 | [3,4]=17  [5,5]=11
                          ^
 [0,0]=1 [1,1]=3    [3,3]=8*  [4,4]=9
                       ^--- the only leaf that changed

only the path nodes are recomputed:
   [3,3]: 7 -> 8
   [3,4]: 16 -> 8 + 9 = 17
   [3,5]: 27 -> 17 + 11 = 28
   [0,5]: 36 -> 9 + 28 = 37
```

Đệ quy đi xuống lá, vẽ dưới dạng đường đi:

```text
_update(1, 0, 5, index=3)
  | 3 > mid=2 -> go right
  +-- _update(3, 3, 5, index=3)
       | 3 <= mid=4 -> go left
       +-- _update(6, 3, 4, index=3)
            | 3 <= mid=3 -> go left
            +-- _update(12, 3, 3, index=3)   leaf: tree[12] = 8
            +-- recompute tree[6] = 8 + 9 = 17
       +-- recompute tree[3] = 17 + 11 = 28
  +-- recompute tree[1] = 9 + 28 = 37

path length: 4 nodes = log2(6) + 1  ->  O(log N)
```

## 8. Lazy propagation: cập nhật khoảng trong O(log N)

Cộng khoảng ngây thơ sẽ ghé mọi lá trong khoảng, tốn `O(N)`. Lazy
propagation sửa điều đó: khi khoảng của một nút được phủ hoàn toàn, ta
không đi xuống chút nào. Ta cập nhật tổng của nút, cất delta vào tag `lazy`,
và bỏ mặc các con. Tag chỉ được đẩy xuống khi một thao tác sau này thực sự
cần các con.

```python
def _update_range(node, start, end, left, right, delta):
    if right < start or end < left:
        return
    if left <= start and end <= right:      # full cover: lazy park
        tree[node] += delta * (end - start + 1)
        lazy[node] += delta
        return
    _push(node, start, end)                  # push before descending
    mid = (start + end) // 2
    _update_range(2 * node, start, mid, left, right, delta)
    _update_range(2 * node + 1, mid + 1, end, left, right, delta)
    tree[node] = tree[2 * node] + tree[2 * node + 1]

def _push(node, start, end):
    if lazy[node] == 0 or start == end:
        return
    delta = lazy[node]
    mid = (start + end) // 2
    tree[2 * node] += delta * (mid - start + 1)
    tree[2 * node + 1] += delta * (end - mid)
    lazy[2 * node] += delta
    lazy[2 * node + 1] += delta
    lazy[node] = 0                            # tag cleared
```

`range_add(1, 4, 10)` trên `[1, 3, 5, 7, 9, 11]` phải cộng 10 vào các chỉ
số 1..4, tạo ra `[1, 13, 15, 17, 19, 11]`. Chỉ hai nút được phủ hoàn toàn,
nên chỉ chúng bị chạm:

```text
                 [0,5]=36
                /         \
          [0,2]=9         [3,5]=27
          /     \          /      \
     [0,1]=4   [2,2]=5  [3,4]=16  [5,5]=11
     /     \             /     \
 [0,0]=1 [1,1]=3    [3,3]=7  [4,4]=9

step 1: [0,1] is partial for [1,4] -> descend to [1,1]
        [1,1] full cover -> tree[1,1] = 3 + 10 = 13, lazy[1,1] += 10
step 2: [2,2] full cover -> tree[2,2] = 5 + 10 = 15, lazy[2,2] += 10
step 3: [3,4] full cover -> tree[3,4] = 16 + 20 = 36, lazy[3,4] += 10
        (10 for each of the 2 elements -> +20)
step 4: recompute ancestors: [0,2] = 4 + 15 = 19, [0,5] = 19 + 47 = 66

after the update (lazy tags shown in brackets):

                 [0,5]=66
                /         \
          [0,2]=19        [3,5]=47
          /     \          /      \
     [0,1]=4   [2,2]=15* [3,4]=36* [5,5]=11
     /     \    lazy+10   lazy+10
 [0,0]=1 [1,1]=13*
         lazy+10

children of the lazy nodes were NOT visited: that is the saving
```

Giờ một truy vấn sau đó buộc phải push. `range_sum(2, 3)` đi xuống qua
`[0,5]` -> `[0,2]` -> `[2,2]` (phủ đầy, trả về 15) và `[3,5]` -> `[3,4]`
(phủ một phần, phải push trước):

```text
range_sum(2, 3):
                 [0,5]=66
                /         \
          [0,2]=19        [3,5]=47
          /     \          /      \
     [0,1]=4   [2,2]=15* [3,4]=36  [5,5]=11
                          |   \-- partial: push lazy before descending
                          |       [3,3] = 7+10 = 17, lazy+10
                          |       [4,4] = 9+10 = 19, lazy+10
                          `-- [3,4] lazy cleared -> 0
answer = 15 + 17 = 32     (= 5+10 + 7+10)

the push happened on demand, only along the query path
```

Một thao tác push, vẽ từng bước:

```text
before _push(node=[3,4], start=3, end=4):
   tree[3,4] = 36,  lazy[3,4] = 10
   tree[3,3] = 7    lazy[3,3] = 0
   tree[4,4] = 9    lazy[4,4] = 0

after _push:
   delta = 10
   tree[3,3] += 10*1 -> 17   lazy[3,3] += 10
   tree[4,4] += 10*1 -> 19   lazy[4,4] += 10
   lazy[3,4] = 0
```

Tóm tắt lazy: cộng khoảng đỗ một tag tại `O(log N)` nút biên thay vì chạm
`O(N)` lá, và mỗi tag được push đúng một lần, khi một truy vấn/cập nhật sau
đó cần các con.

## 9. Segment tree động cho khoảng chỉ số khổng lồ hoặc thưa

Khi khoảng chỉ số khổng lồ (ví dụ `[0, 10^9]`) nhưng ít phần tử thực sự bị
chạm, dựng mảng `4*N` là bất khả thi. Segment tree động chỉ cấp phát nút
khi cần: các con được tạo theo nhu cầu và vắng mặt khi khoảng chưa từng bị
ghé.

```text
static tree, N = 10^9:    4*10^9 array slots -> out of memory

dynamic tree (sparse):    only visited intervals exist as real nodes

                       [0,10^9]          created on first query
                      /         \
                [0,5*10^8]    [5*10^8+1,10^9]   created on demand
                /     \
          [0,2.5e8]  [2.5e8+1,5e8]
                       /      \
                 [..]   [..]  ... nodes only where operations land

memory used: O(k * log U), k = number of distinct touched positions
```

Đệ quy hoàn toàn giống nhau; chỉ phần lưu trữ đổi: thay vì `self.tree[node]`,
các con được giữ trong hai con trỏ khởi tạo là `None` và được cấp phát bên
trong lời gọi đệ quy khi một lần ghé một phần cần chúng.

## 10. Tóm tắt độ phức tạp

| Thao tác | Mảng tĩnh | Prefix sums | Segment tree | Lazy segment tree |
|:---|:---:|:---:|:---:|:---:|
| Dựng | `O(N)` | `O(N)` | `O(N)` | `O(N)` |
| Cập nhật điểm | `O(1)` | `O(N)` | `O(log N)` | `O(log N)` |
| Tổng khoảng `[l,r]` | `O(N)` quét | `O(1)` (tĩnh) | `O(log N)` | `O(log N)` |
| Cộng khoảng `[l,r]` | `O(N)` | `O(N)` | `O(N)` ngây thơ | `O(log N)` lazy |
| Bộ nhớ | `O(N)` | `O(N)` | `O(4N)` | `O(4N)` |

Vì sao chiều cao là `O(log N)`: khoảng chia đôi ở mỗi tầng, nên số tầng là
`log2(N)`:

```text
level 0   [0, N-1]                     size N
level 1   [0, N/2-1] [N/2, N-1]        size N/2
level 2   four intervals of size N/4
level 3   eight intervals of size N/8
  ...
level k   intervals of size N / 2^k
  ...
level log2(N)   leaves of size 1

stop when N / 2^k = 1  ->  k = log2(N) levels
```

## 11. Demo từng bước

Chạy:

```text
python SegmentTreeBasics.py
```

Đầu tiên cây cơ bản được dựng từ `[1, 3, 5, 7, 9, 11]` và bản vẽ ASCII của
nó được in ra. Rồi các kiểm tra tất định:

```text
query(0,5) = 36       full range
query(2,4) = 21       5 + 7 + 9
query(0,0) = 1        single element
query(3,3) = 7        single element
query(1,3) = 15       3 + 5 + 7
update(3, 8)          values become [1, 3, 5, 8, 9, 11]
query(2,4) = 22       5 + 8 + 9
query(0,5) = 37       new total
```

Rồi 200 thao tác ngẫu nhiên trên mảng 30 phần tử so sánh `query` với
`sum(reference[l:r+1])` của một danh sách tham chiếu; mọi kết quả phải khớp.

Cây lazy khởi đầu từ cùng các giá trị:

```text
range_add(1, 4, 10)   values become [1, 13, 15, 17, 19, 11]
range_sum(0,5) = 76
range_sum(2,3) = 32   15 + 17
range_sum(0,0) = 1
range_add(0, 0, 5)    values become [6, 13, 15, 17, 19, 11]
range_sum(0,2) = 34   6 + 13 + 15
```

Lại 200 lần cộng khoảng và tổng khoảng ngẫu nhiên được đối chiếu với danh
sách tham chiếu, và toàn bộ demo kết thúc bằng `All assertions passed.`

## 12. Hạn chế và tổng kết

Hạn chế:

- Cây tĩnh cần `O(4N)` bộ nhớ kể cả khi nhiều nút không bao giờ hữu dụng;
  biến thể động sửa điều đó cho khoảng thưa/khổng lồ.
- Mỗi cây chỉ một giá trị tổng hợp; kết hợp sum và min trong một cây đòi
  hỏi lưu cả hai mỗi nút (hoặc một struct hợp nhất tùy biến).
- Cài đặt đệ quy có thể chạm giới hạn độ sâu đệ quy với kích thước cực lớn;
  các phiên bản lặp tồn tại nhưng khó đọc hơn.
- Lazy tag chỉ hợp với các giá trị tổng hợp hấp thụ được thao tác khoảng
  (sum += delta*len; min/max cần xử lý cẩn thận, max với cộng khoảng cần
  thêm sổ sách).

Tổng kết:

```text
plain array      range query O(N), point update O(1)
prefix sums      range query O(1), point update O(N)
segment tree     range query O(log N), point update O(log N)
lazy seg tree    range query O(log N), range update O(log N)
```

Segment tree là câu trả lời kinh điển bất cứ khi nào khối lượng công việc
là hỗn hợp truy vấn khoảng và cập nhật trên một mảng động. Chi phí thật sự
chỉ là dựng `O(N)` và bộ nhớ `O(4N)`, và thủ thuật lazy mở rộng nó sang
cập nhật khoảng với cùng chi phí logarit.

## 13. Nguồn

- [Segment Tree Basics and Visualization](https://labuladong.online/en/algo/data-structure-basic/segment-tree-basic/)