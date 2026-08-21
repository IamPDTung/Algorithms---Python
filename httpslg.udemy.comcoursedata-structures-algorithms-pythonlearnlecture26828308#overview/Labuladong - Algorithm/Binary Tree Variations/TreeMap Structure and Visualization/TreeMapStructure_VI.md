# Cấu trúc TreeMap và trực quan hóa

## 1. Mục tiêu

TreeMap là một Map có các khóa nằm trong một cây tìm kiếm nhị phân (binary search tree), nên các khóa luôn được sắp xếp. Nó ra đời vì HashMap không thể trả lời các câu hỏi về thứ tự: nó không thể cho biết khóa nhỏ nhất, khóa lớn nhất, các khóa nằm giữa hai biên, hay khóa nhỏ thứ k, bởi mảng bucket của nó không có khái niệm thứ tự. LinkedHashMap chỉ bảo toàn thứ tự chèn, tức là trình tự các khóa được thêm vào, chứ không phải thứ tự theo giá trị khóa. TreeMap trả lời tất cả các câu hỏi có thứ tự đó trong O(logN) bằng cách duyệt một cây BST.

Nguồn tham khảo:

- [TreeMap Structure and Visualization](https://labuladong.online/en/algo/data-structure-basic/tree-map-basic/)

Cài đặt trong `TreeMapStructure.py` cung cấp:

- `BSTNode` lưu khóa, giá trị, và kích thước cây con.
- `TreeMap` đầy đủ với `put`, `get`, `remove`, `contains_key`, `keys`, `first_key`, `last_key`, `floor_key`, `ceiling_key`, `select`, `rank`, và `range_keys`.
- Điều hướng có thứ tự (`first_key`, `floor_key`, ...) dựa trên bất biến của BST.
- `select`/`rank` dựa trên kích thước cây con.
- Helper `search_steps` và `draw` trực quan hóa đường tìm kiếm và hình dạng cây, chứng minh vì sao BST cân bằng thắng BST suy biến.

## 2. Lợi thế của cây BST

Cây tìm kiếm nhị phân là cây nhị phân với một luật thêm vào cho mỗi nút: mọi khóa ở cây con trái nhỏ hơn khóa của nút, và mọi khóa ở cây con phải lớn hơn.

```text
            (8)
           /    \
       (3)        (10)
      /   \      /    \
   (1)    (6)  (9)   (12)
         /   \
      (4)    (7)

   left subtree  : every key < node.key
   right subtree : every key > node.key
```

Luật duy nhất này biến cây thành một cấu trúc được sắp xếp và cho việc tìm kiếm một hướng đi. Cây thường không cho tìm kiếm biết nên rẽ trái hay phải, nên trong trường hợp xấu nhất phải xét từng nút. BST so sánh khóa cần tìm với nút hiện tại và loại bỏ cả một nửa số nút còn lại ở mỗi bước.

```text
   ordinary tree (no order)          BST (ordered)

        (5)                              (8)
       / |  \                          /      \
    (9) (1) (7)                     (3)        (10)
     |     |   |                   /   \      /    \
   (4)   (2) (6)                (1)    (6)  (9)  (12)
                                          / \
   search(6): visits 5, 9, 1, 2, 4      (4) (7)
   ...every node is a candidate...
          O(N)                    search(6): 8 -> 3 -> 6
   worst case                       one path, 3 steps
                                    O(logN) when balanced
```

## 3. TreeMap / TreeSet hoạt động ra sao

Nút TreeMap là nút BST chứa cả khóa lẫn giá trị. Bất biến BST sắp xếp các khóa; giá trị chỉ đi theo mà thôi.

```text
   BSTNode(key=8, value=80)
        +-----------------+
        |  key  = 8       |
        |  value = 80     |      a TreeMap node = key + value + size
        |  size = 3       |
        |  left  -> (7)   |
        |  right -> (9)   |
        +-----------------+
```

Trong Python, nút là một class nhỏ với năm trường đó:

```python
class BSTNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.size = 1
```

TreeSet chính xác là TreeMap bỏ qua giá trị: nó lưu các khóa trong cùng một BST đã sắp xếp và coi giá trị là đồ giả. Trong nhiều thư viện, TreeSet thực chất là một wrapper bọc quanh TreeMap.

```text
   TreeMap<TKey, TValue>   stores (key, value) in the BST
   TreeSet<TKey>           same BST, every value is a dummy
```

Khác biệt quyết định so với HashMap là thứ tự. HashMap rải các khóa lên mảng bucket theo mã băm, nên khóa nhỏ nhất có thể nằm ở đâu cũng được; TreeMap giữ cùng các khóa đó trong một cây luôn được sắp xếp.

```text
   HashMap (bucket array)                  TreeMap (BST)
   keys placed by hash code                keys placed by value

   +------+------+------+------+             (6)
   |      |      |      |      |            /    \
   +------+------+------+------+         (3)      (9)
   hash(1)->bucket 2                     /  \    /   \
   hash(3)->bucket 0                  (1)  (4)(8)  (12)
   hash(6)->bucket 1
   hash(9)->bucket 3

   smallest key?   unknown,             first_key()   = 1
                   must scan all        last_key()    = 12
   keys in [3,9]?  must scan all        range_keys(3,9) = [3,4,6,8,9]
```

## 4. Tổng quan API

| Phương thức | Ý nghĩa | Độ phức tạp (BST cân bằng) |
|:---|:---|:---:|
| `put(key, value)` | chèn hoặc cập nhật; trả về giá trị cũ | `O(logN)` |
| `get(key)` | giá trị của khóa, hoặc `None` | `O(logN)` |
| `remove(key)` | xóa khóa; trả về giá trị cũ | `O(logN)` |
| `contains_key(key)` | khóa có tồn tại hay không | `O(logN)` |
| `keys()` | mọi khóa theo thứ tự tăng dần | `O(N)` |
| `first_key()` | khóa nhỏ nhất | `O(logN)` |
| `last_key()` | khóa lớn nhất | `O(logN)` |
| `floor_key(key)` | khóa lớn nhất <= key | `O(logN)` |
| `ceiling_key(key)` | khóa nhỏ nhất >= key | `O(logN)` |
| `select(k)` | khóa nhỏ thứ k, tính từ 1 | `O(logN)` |
| `rank(key)` | hạng của khóa, tính từ 1 | `O(logN)` |
| `range_keys(low, high)` | khóa đã sắp xếp với low <= key <= high | `O(logN + k)` |

Nhóm `get`/`put`/`remove` có cùng giao diện với HashMap, nên TreeMap dùng được ở bất cứ đâu thay cho HashMap. Nhóm phương thức có thứ tự thứ hai chính là thứ HashMap không thể có.

```text
   HashMap  : get / put / remove / contains   (unordered, O(1) average)
   TreeMap  : get / put / remove / contains   (ordered,  O(logN))
            + first_key / last_key / floor_key / ceiling_key
            + select / rank / range_keys / keys
```

Một ví dụ dùng ngắn gọn:

```python
tm = TreeMap()
tm.put("b", 2)
tm.put("a", 1)
tm.put("c", 3)
tm.keys()              # ['a', 'b', 'c']
tm.first_key()         # 'a'
tm.ceiling_key("bb")   # 'c'
tm.select(2)           # 'b'
tm.rank("b")           # 2
tm.range_keys("a", "b")  # ['a', 'b']
```

## 5. Thao tác cơ bản: Thêm, Xóa, Tìm, Cập nhật

Tìm một khóa là một đường đi có dẫn dắt: so sánh tại mỗi nút, rẽ trái khi khóa nhỏ hơn, rẽ phải khi khóa lớn hơn.

```text
   get(4) on the sample tree

        (5)         4 < 5  -> go left
       /   \
    (3)     (8)     4 > 3  -> go right
   /   \   /   \
 (2)   (4)(7)  (9)  4 == 4 -> found, return value
```

Thêm một khóa đi theo cùng đường đó và gắn nút mới vào ô trống. Mọi tổ tiên trên đường đi sau đó tăng `size` của mình lên.

```text
   put(6) on the sample tree

   step 0   start at root (5), 6 > 5  -> go right
   step 1   node (8),      6 < 8      -> go left
   step 2   node (7),      6 < 7      -> go left
   step 3   empty slot, attach new node (6)

        (5)                              (5)
       /   \                            /   \
    (3)     (8)                      (3)     (8)
   /   \   /   \                    /   \   /   \
 (2)   (4)(7)  (9)                (2)   (4)(7)  (9)
                                      /
                                    (6)

   before insert                    after insert
```

Cập nhật một khóa đã tồn tại là cùng đường đi đó nhưng kết thúc bằng phép ghi thay vì tạo nút mới, nên `size` không đổi.

Xóa là trường hợp khó nhất. Nút lá bị cắt bỏ trực tiếp; nút có một con được thay bằng đúng con đó; nút có hai con được thay bằng kế vị in-order của nó, tức khóa nhỏ nhất của cây con phải.

```text
   remove(5) from the sample tree

   case 1: leaf (2) -> just cut it off

   case 2: one child -> splice the child up

   case 3: two children -> successor deletion
        (5)                  successor = min of right subtree = (7)
       /   \
    (3)     (8)
   /   \   /   \
 (2)   (4)(7)  (9)

   copy (7) over (5), then delete the min from the right subtree
        (7)
       /   \
    (3)     (8)
   /   \     \
 (2)   (4)  (9)
```

## 6. firstKey / lastKey và keys() (Duyệt in-order)

Khóa nhỏ nhất nằm ở nút tận cùng bên trái, khóa lớn nhất nằm ở nút tận cùng bên phải. Cả hai đều là những đường đi thuần túy.

```text
   first_key(): always walk left          last_key(): always walk right

        (5)         <- root                    (5)         <- root
       /   \                                 /   \
    (3)     (8)     (5).left = (3)          (3)     (8)     (5).right = (8)
   /   \   /   \                           /   \   /   \
 (2)   (4)(7)  (9)  (3).left = (2)       (2)   (4)(7)  (9)  (8).right = (9)
   (2).left = None                       (9).right = None
   first_key = 2                         last_key = 9
```

Thu thập mọi khóa theo thứ tự chính là duyệt in-order: duyệt cây con trái, rồi nút, rồi cây con phải. Kết quả tự động được sắp xếp.

```text
   in-order visits:  (2) -> (3) -> (4) -> (5) -> (7) -> (8) -> (9)
   keys() = [2, 3, 4, 5, 7, 8, 9]
```

`floor_key` và `ceiling_key` là những phiên bản có biên của các đường đi này. `floor_key(6)` giữ khóa lớn nhất vẫn nhỏ hơn hoặc bằng 6, `ceiling_key(6)` giữ khóa nhỏ nhất lớn hơn hoặc bằng 6.

```text
   floor_key(6) -> 5       ceiling_key(6) -> 7
   (largest key <= 6)      (smallest key >= 6)

        (5)                     (5)
       /   \                   /   \
    (3)     (8)              (3)     (8)
   /   \   /   \             /   \   /   \
 (2)   (4)(7)  (9)         (2)   (4)(7)  (9)
        ^                       ^
     5 is the closest        7 is the closest
     key below 6             key above 6
```

## 7. select / rank dùng kích thước cây con

Mỗi nút lưu `size`, tổng số nút trong cây con của nó. Con số duy nhất này cho phép `select` và `rank` nhảy tới đáp án mà không cần duyệt hết.

```text
   size = 1 + size(left) + size(right)

        (5) size = 7
       /   \
   (3) sz=3 (8) sz=3
   /   \      /   \
 (2) 1 (4) 1 (7) 1 (9) 1
```

`select(k)` trả về khóa nhỏ thứ k. Tại mỗi nút nó so sánh `k` với kích thước cây con trái: nếu khóa thứ k nằm trong cây con trái thì rẽ trái; nếu đúng là chính nút đó thì dừng; ngược lại trừ phần bên trái rồi rẽ phải.

```text
   select(4) on the sample tree
   root (5): size(left) = 3, k = 4 = 3 + 1  -> the node itself -> 5

   select(6) on the sample tree
   root (5): 6 > 3 + 1  -> go right, k = 6 - 3 - 1 = 2
   node (8): size(left) = 1, k = 2 = 1 + 1   -> the node itself -> 8

   result: select(1)=2, select(4)=5, select(7)=9
```

Hình dạng đệ quy của `_select`:

```python
def _select(node, k):
    if node is None:
        return None
    left_size = size_of(node.left)
    if k == left_size + 1:
        return node.key
    if k <= left_size:
        return _select(node.left, k)
    return _select(node.right, k - left_size - 1)
```

`rank(key)` là phép ngược: số khóa nhỏ hơn hẳn khóa đã cho, cộng thêm một. Mỗi khi tìm kiếm rẽ phải, nó cộng toàn bộ cây con trái và chính nút đó; rẽ trái thì không cộng gì.

```text
   rank(7) on the sample tree
   (5): 7 > 5  -> add size(left)+1 = 3+1 = 4, go right
   (8): 7 < 8  -> go left, add nothing
   (7): 7 == 7 -> add size(left)+1 = 0+1 = 1
   total = 4 + 1 = 5

   rank(2) = 1, rank(5) = 4, rank(9) = 7
```

Vì cây cân bằng, cả hai thao tác đều tốn O(logN) thay vì quét toàn bộ danh sách.

## 8. Tìm kiếm theo khoảng

`range_keys(low, high)` trả về mọi khóa trong `[low, high]` theo thứ tự tăng dần. BST cho phép tìm kiếm cắt tỉa cả những cây con chắc chắn không chứa khóa nào trong khoảng.

```text
   range_keys(3, 8) on the sample tree

        (5)
       /   \
    (3)     (8)
   /   \   /   \
 (2)   (4)(7)  (9)

   (5): low 3 < 5 -> visit left subtree;   3<=5<=8 -> keep 5;  5 < high 8 -> visit right
   (3): low 3 < 3? no -> prune left (2 excluded)
        3<=3<=8 -> keep 3;  3 < high 8 -> visit right
   (4): 3<=4<=8 -> keep 4
   (8): low 3 < 8 -> visit left (7);
        3<=8<=8 -> keep 8;  8 < high 8? no -> prune right (9 excluded)
   (7): 3<=7<=8 -> keep 7

   result = [3, 4, 5, 7, 8]
```

Hai luật cắt tỉa: cây con trái chỉ được duyệt khi `low < node.key` (nếu không mọi khóa ở đó đều dưới khoảng), và cây con phải chỉ được duyệt khi `node.key < high` (nếu không mọi khóa ở đó đều trên khoảng). Các khóa 2 và 9 không bao giờ bị xét đến.

Hình dạng đệ quy của `_range`:

```python
def _range(node, low, high, out):
    if node is None:
        return
    if low < node.key:
        _range(node.left, low, high, out)
    if low <= node.key <= high:
        out.append(node.key)
    if node.key < high:
        _range(node.right, low, high, out)
```

## 9. Vấn đề hiệu năng: BST mất cân bằng suy biến thành O(N)

Mọi lời hứa O(logN) ở trên chỉ đúng khi cây giữ được sự cân bằng. Nếu các khóa được chèn theo thứ tự đã sắp xếp, BST trở thành một danh sách liên kết và mọi lời hứa sụp đổ xuống O(N).

```text
   balanced BST (height 4)            degenerate BST = linked list (height 8)

        (4)                                     (1)
       /   \                                     \
    (2)     (6)                                  (2)
   /   \   /   \                                  \
 (1)   (3)(5)  (7)                                (3)
                   \                               ...
                    (8)                           (8)

   search(8): 4 -> 6 -> 7 -> 8          search(8): 1 -> 2 -> ... -> 8
   4 steps,  O(logN)                    8 steps,  O(N)
```

Chiều cao của cây cân bằng là 4, chiều cao của cây suy biến là 8, và `search_steps(8)` đếm đúng 4 lượt thăm so với 8. Đây là lý do các TreeMap sản xuất không dùng BST trần: chúng dùng biến thể tự cân bằng, cây đỏ-đen, giữ chiều cao bị chặn bởi O(logN) bất kể thứ tự các khóa đến. Tái cân bằng đỏ-đen bảo đảm trường hợp xấu nhất, chứ không chỉ trung bình.

## 10. Demo từng bước

Chạy:

```text
python TreeMapStructure.py
```

Demo trước hết dựng cây `5,3,8,2,4,7,9` với giá trị = key*10 và kiểm tra từng truy vấn có thứ tự bằng tay:

```text
len = 7 | height = 3
keys() = [2, 3, 4, 5, 7, 8, 9]
first_key = 2 | last_key = 9
floor_key(6) = 5 | ceiling_key(6) = 7
select(1) = 2 | select(4) = 5
rank(5) = 4 | rank(2) = 1
range_keys(3, 8) = [3, 4, 5, 7, 8]
```

Sau đó demo thử cập nhật và xóa: `put(5, 999)` ghi đè giá trị tại chỗ, `remove(5)` dùng phép xóa theo kế vị, và xóa nút lá `2` cùng nút `7` vẫn giữ các khóa được sắp xếp.

Cuối cùng nó so sánh cây suy biến (chèn `1..8` theo thứ tự) với cây cân bằng (chèn ưu tiên giữa: `4,2,1,3,6,5,7,8`):

```text
Degenerate BST: height = 8, search_steps(8) = [1, 2, 3, 4, 5, 6, 7, 8]
Balanced BST:   height = 4, search_steps(8) = [4, 6, 7, 8]
```

Cây cân bằng thắng ở cả hai chỉ số, và hình dạng của nó được in ra bằng helper `draw`.

## 11. Giới hạn và tóm tắt

Cài đặt BST trần ở đây mang tính giáo dục: nó đúng, được sắp xếp, và có khả năng truy vấn có thứ tự, nhưng không tự cân bằng. Chèn dữ liệu đã sắp xếp sẽ biến nó thành danh sách liên kết. Các thư viện thực tế giải quyết điều này bằng cây đỏ-đen (Java TreeMap/TreeSet), cây AVL, hoặc cây B.

Tóm tắt những gì đã học:

```text
- A TreeMap is a Map whose keys live in a BST, so keys stay sorted.
- Ordered queries (first/last/floor/ceiling/select/rank/range) come from
  the BST invariant and subtree sizes.
- Subtree sizes turn select/rank into O(logN) operations.
- Range search prunes whole subtrees and never touches out-of-range keys.
- Without balancing, a BST degrades to a linked list and O(N) behavior.
```

## 12. Bảng độ phức tạp

| Thao tác | HashMap | TreeMap (BST cân bằng) |
|:---|:---:|:---:|
| `get` / `contains_key` | `O(1)` trung bình | `O(logN)` |
| `put` | `O(1)` trung bình | `O(logN)` |
| `remove` | `O(1)` trung bình | `O(logN)` |
| `keys()` (đã sắp xếp) | cần sort `O(N logN)` | `O(N)` in-order |
| `first_key` / `last_key` | không hỗ trợ | `O(logN)` |
| `floor_key` / `ceiling_key` | không hỗ trợ | `O(logN)` |
| `select` / `rank` | không hỗ trợ | `O(logN)` |
| `range_keys(low, high)` | không hỗ trợ | `O(logN + k)`, `k` = số kết quả |

## 13. Nguồn và tài liệu tham khảo

- [TreeMap Structure and Visualization](https://labuladong.online/en/algo/data-structure-basic/tree-map-basic/)
