
---

# Red-Black Trees Basics and Visualization

## 1. Goal

Cây đỏ-đen (red-black tree) là một **cây tìm kiếm nhị phân tự cân bằng**.
Nó giữ chiều cao ở mức O(log N) ở mọi thời điểm, nên các thao tác chèn,
xóa, tìm kiếm và cập nhật đều chạy trong O(log N).

**Vì sao nó ra đời?** Cây tìm kiếm nhị phân thường (như TreeMap ở bài
trước) có một khuyết điểm chí mạng: nó không tự cân bằng. Nếu bạn chèn các
khóa theo thứ tự tăng dần, mỗi khóa mới lại rơi về phía phải và cây thoái
hóa thành một danh sách liên kết. Mọi thao tác khi đó suy biến về O(N). Cây
đỏ-đen khắc phục điều này bằng cách tự động tái cân bằng sau mỗi lần chèn
và xóa, nên chiều cao không bao giờ bị đẩy lên quá cao.

Hướng dẫn này cài đặt biến thể **cây đỏ-đen nghiêng trái (LLRB)**, phiên
bản dễ viết và dễ suy luận nhất.

Phần cài đặt trong `RedBlackTreeBasics.py` cung cấp:

- Lớp `RedBlackTree` ánh xạ các khóa so sánh được sang giá trị, với `put`,
  `get`, `delete`, `delete_min`, `delete_max`, `min`, `max`, `keys`.
- Hàm `height` và hàm vẽ `draw()` bằng ASCII, đánh dấu các liên kết đỏ.
- Hàm `is_valid()` kiểm tra mọi bất biến của cây đỏ-đen.
- Lớp `PlainBST` cố tình không cân bằng, dùng để minh họa sự thoái hóa.
- Các bài kiểm tra ngẫu nhiên chứng minh bất biến giữ vững sau mọi thao tác.

Nguồn tham khảo:

- [Red-Black Trees Basics and Visualization](https://labuladong.online/en/algo/data-structure-basic/rbtree-basic/)
- [TreeMap Structure and Visualization](https://labuladong.online/en/algo/data-structure-basic/tree-map-basic/)

## 2. The Problem: a Plain BST Degrades into a Linked List

Cây tìm kiếm nhị phân chỉ nhanh khi nó còn cân bằng. Chiều cao của nó quyết
định chi phí của mọi thao tác.

Chèn các khóa theo thứ tự tăng dần là ca xấu nhất. Mỗi khóa mới đều lớn hơn
mọi khóa trước, nên nó trở thành con phải của nút ngoài cùng bên phải:

```text
insert 1          insert 2          insert 3          insert 4
  (1)               (1)               (1)               (1)
                     \                 \                 \
                     (2)               (2)               (2)
                                        \                 \
                                        (3)               (3)
                                                           \
                                                           (4)
```

"Tảng cây" thực chất là một danh sách liên kết dài N. Tìm khóa lớn nhất
phải đi qua cả N nút:

```text
plain BST after inserting 1..5 in order:
   height = 4 edges, search(5) visits: 1, 2, 3, 4, 5  (5 steps)

   (1)
     \
     (2)
       \
       (3)
         \
         (4)
           \
           (5)
```

Demo trong `RedBlackTreeBasics.py` chèn `1..15` theo thứ tự vào cả cây BST
thường lẫn cây đỏ-đen:

```text
plain BST : height 14  (a linked list of 15 nodes)
red-black : height  3  (the perfect balanced tree)
```

## 3. Red-Black Tree Properties and the Color Convention

Cây đỏ-đen là cây tìm kiếm nhị phân với thêm một bit cho mỗi nút: màu **đỏ**
hoặc **đen**. Màu lưu trên một nút thực chất là màu của liên kết từ cha của
nó.

```text
black link (default)          red link (marked R)
     (P)                          (P)
      |                            |
     (C) black                  (C) red   <-- parent's left child is red
```

Các quy tắc giữ cây cân bằng:

```text
1. every node is red or black
2. the root is black
3. red links lean left: a red node is always the LEFT child of its parent
4. no node has two red children in a row
5. every path from the root to a null leaf has the SAME number of black links
   (this is the "black height" and it is the true balancing rule)
```

Quy tắc 5 là mấu chốt: nếu mọi đường từ gốc tới lá có cùng số liên kết đen,
cây không thể biến thành một que dài mảnh. Các liên kết đỏ là "khoảng trống"
cho nút tạm phát triển; quy tắc 3 giữ hình dạng chuẩn tắc.

Một cây đỏ-đen hợp lệ với 15 nút, do demo vẽ ra:

```text
       8(B)
      /    \
   4(B)    12(B)
  /   \    /    \
2(B) 6(B) 10(B) 14(B)
  ...  ...
```

## 4. The 2-3-4 Tree Correspondence

Cây đỏ-đen không phải phép màu: nó là mã hóa nhị phân của một **cây 2-3-4**,
một cây tìm kiếm mà mỗi nút có thể chứa một, hai hoặc ba khóa.

```text
2-node                3-node                   4-node
  (a)                 (a|b)                   (a|b|c)
                      /    \                  /  |  \
                   (<a)   (>b)            (<a)(a,b)(>c)
```

Cây đỏ-đen mã hóa cùng cấu trúc bằng cách "dán" các khóa của một nút nhiều
khóa lại với nhau bằng các liên kết đỏ:

```text
2-node (one key, two children):
     (a)
    /   \
  left  right

3-node (two keys, three children)  ==  black parent + red left child:
       (b)
      /   \
    (a)   right
    /  \
 left  mid

4-node (three keys, four children) ==  black parent + two red children:
       (b)
      /   \
    (a)   (c)
    / \   / \
  l1  l2 l3  l4
```

Quy tắc 4 ("không có hai liên kết đỏ liền nhau") và quy tắc 5 ("chiều cao
đen bằng nhau") chính xác là phát biểu rằng cây đỏ-đen là một cây 2-3-4:
liên kết đỏ chỉ dán các nút lại với nhau, còn liên kết đen mới là "cấu trúc
cây" thực sự.

## 5. Rotations and Color Flips

Sự cân bằng được khôi phục bằng ba phép toán cục bộ, không bao giờ làm đổi
thứ tự duyệt giữa (in-order) của các khóa.

**Xoay trái** đưa một con đỏ bên phải lên trên:

```text
     (h)                    (x)
       \                   /   \
      (x)      ==>       (h)  (c)
      /  \                 \
    (a)  (c)              (a)
```

**Xoay phải** là hình ảnh phản chiếu:

```text
       (h)                  (x)
      /                    /   \
    (x)        ==>       (a)  (h)
    /  \                      /
  (a)  (c)                 (c)
```

**Lật màu** tách một 4-node: hai con đỏ hóa đen, cha hóa đỏ, đẩy "tràn" lên
trên:

```text
      (b)  black                (b)  red
     /   \          ==>        /   \
   (a)  (c)  red             (a)  (c)  black
```

## 6. Insert Algorithm

Chèn một khóa vào LLRB là chèn BST thường (luôn tạo nút đỏ mới), tiếp theo
là một lượt `fix_up` trên đường đi lên, áp dụng ba phép toán cục bộ:

```text
put(key, value):
  1. BST-insert a RED node
  2. walk back up, at every node fix_up:
       if right child red and left child black   -> rotate left
       if left child red and left.left red       -> rotate right
       if left child red and right child red     -> flip colors
  3. paint the root black
```

Ví dụ: chèn các khóa `5, 3, 8, 2`.

```text
insert 5            insert 3                insert 8 (fix_up flips):
  (5)                 (5)                     (5)            (5)
                    /                        /   \    ==>   /   \
                  (3)R                    (3)R  (8)R      (3)   (8)

insert 2:
     (5)               (5)
    /   \             /   \
  (3)   (8)   ==>   (3)   (8)
                   /
                 (2)R
```

Từng bước:

```text
1. 5 is the root, painted black.
2. 3 becomes the red left child of 5.
3. 8 becomes the red right child of 5. Now 5 has two red children,
   so fix_up flips colors: 3 and 8 turn black, 5 turns red, and
   the root is repainted black.
4. 2 becomes the red left child of 3. No rotation is needed; the
   final tree has height 2 and black height 2 on every path.
```

Bất biến dễ phát biểu hơn là vẽ ở từng bước: sau `fix_up`, không có liên kết
đỏ nào chỉ sang phải, không có hai liên kết đỏ xếp liền nhau, và không nút
nào có hai con đỏ.

Chèn `1..15` theo thứ tự vào LLRB tạo ra cây cân bằng hoàn hảo toàn đen như
ở mục 3: chiều cao 3 thay vì 14.

## 7. Delete Algorithm

Xóa khỏi cây đỏ-đen khó hơn chèn, vì bỏ một nút có thể phá quy tắc chiều
cao đen bằng nhau. Chiến lược LLRB là "làm đỏ đường đi khi đi xuống": trước
khi xuống một con, đảm bảo con đó (hoặc con của nó) đang đỏ, để việc xóa
khỏi nó không làm đổi chiều cao đen.

```text
delete(key):
  0. if both children of the root are black, paint the root red
  1. descend toward the key:
       if key < h.key  -> ensure h.left is red  (move_red_left)
       else            -> ensure h.right is red (move_red_right)
  2. when the key is found:
       if it has no right child        -> remove it
       else replace it with its
            in-order successor, then
            delete the successor       (delete_min on the right subtree)
  3. fix_up on the way back up
  4. paint the root black
```

Các hàm trợ giúp `move_red_left` / `move_red_right` "mượn" một liên kết đỏ
từ anh em để đường đi xuống luôn "đỏ suốt":

```text
move_red_left(h)  --  h is red, h.left is black:
   h        (h red, left black, right black)
  / \   ==> flip colors -> h black, both children red
(a) (b)     then if b.left is red, rotate right then left, flip again

   result: h.left is now red, so we can safely descend and delete.
```

## 8. Complexity

Vì quy tắc 5 buộc mọi đường đi có cùng số liên kết đen, chiều cao đen tối đa
là log2(N+1), và liên kết đỏ tối đa làm tăng gấp đôi:

```text
height  <=  2 * log2(N+1)

N=1000   ->  height <= 20   (a plain BST could be 1000)
N=1e6    ->  height <= 42
```

Mọi thao tác đều là O(log N):

```text
operation     plain BST (worst)     red-black tree
------------- -------------------  --------------
put           O(N) linked list     O(log N)
get           O(N)                 O(log N)
delete        O(N)                 O(log N)
min / max     O(N)                 O(log N)
height        O(N)                 O(log N)
```

Cái giá là một hằng số nhỏ: mỗi lần chèn/xóa thực hiện tối đa hai phép xoay
và O(log N) phép lật màu.

## 9. Invariant Checking

Phương thức `is_valid()` là một bài kiểm tra đơn vị thu nhỏ chạy ngay trong
demo. Nó xác minh:

```text
check 1: in-order keys are strictly sorted          (BST ordering)
check 2: the root is black
check 3: no red node has a red child                (rule 4)
check 4: no node has a red right child              (rule 3, red leans left)
check 5: every root-to-null path has the same
         number of black links                      (rule 5, black height)
```

Đệ quy trả về chiều cao đen của từng cây con, hoặc -1 khi gặp vi phạm đầu
tiên:

```text
black_height(node):
    if node is None:            return 0
    if node red and has a red child:  return -1
    if node.right is red:       return -1
    L = black_height(node.left)
    R = black_height(node.right)
    if L == -1 or R == -1 or L != R:  return -1
    return L + (0 if node is red else 1)
```

Demo gọi `is_valid()` sau **mỗi** lần chèn và xóa ngẫu nhiên, nên bất kỳ lỗi
nào trong `put`/`delete` sẽ hỏng ngay lập tức.

## 10. Demo Walkthrough

Chạy `RedBlackTreeBasics.py` in ra:

```text
=== Red-Black Tree demo ===
Inserted 1..15 in increasing order.
Plain BST height : 14  (degenerated into a linked list)
Red-black height : 3  (stays logarithmic)

Red-black tree drawn with colors:
       8(B)
      4(B)  12(B)
     2(B)  6(B)  10(B)  14(B)
    1(B)  3(B)  5(B)  7(B)  9(B)  11(B)  13(B)  15(B)

Random insert / delete stress test...
Stress test passed: invariants held after every put/delete.
Final size: 0
```

Điều demo chứng minh:

```text
- the same 15 keys give height 14 in a plain BST but 3 in a red-black tree
- the 1..15 tree is a perfect all-black tree (black height 3)
- 80 random inserts keep every invariant (is_valid after each put)
- 80 random deletes keep every invariant (is_valid after each delete)
- deleting all keys leaves an empty, still-valid tree
```

## 11. Limitations and Summary

```text
strengths:
  - guaranteed O(log N) for every operation, no matter the input order
  - in-order keys stay sorted: min/max/rank/select all available
  - the standard library TreeMap/TreeSet in Java is a red-black tree

trade-offs:
  - more complex than a plain BST or an AVL tree
  - a constant-factor slowdown from rotations and color flips
  - if you only need O(1) lookups, a hash table is still faster

when to use:
  - you need sorted keys AND guaranteed log-time operations
  - you cannot tolerate the worst-case O(N) of a plain BST
```

Tóm tắt trong một câu: cây đỏ-đen là một cây tìm kiếm nhị phân thường tô màu
các liên kết của nó để không bao giờ nghiêng thành danh sách liên kết, giữ
mọi thao tác ở O(log N).
