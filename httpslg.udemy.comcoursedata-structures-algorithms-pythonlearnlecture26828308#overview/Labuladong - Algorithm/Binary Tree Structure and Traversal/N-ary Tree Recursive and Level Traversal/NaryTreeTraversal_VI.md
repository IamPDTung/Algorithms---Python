
---

# Duyệt đệ quy và duyệt theo tầng của cây N-ary

## 1. Mục tiêu

Cây N-ary là mở rộng của cây nhị phân: mỗi nút có thể có bất kỳ số con nào.
Duyệt cây N-ary là mở rộng của duyệt cây nhị phân với đúng hai dạng: duyệt
đệ quy (DFS) và duyệt theo tầng (BFS). Tài liệu này cài đặt cả hai, kèm ba
biến thể chuẩn của duyệt theo tầng, và giải thích khái niệm rừng (forest).

Cài đặt trong `NaryTreeTraversal.py` cung cấp:

- Lớp `Node` có `children` và hàm dựng theo định dạng LeetCode.
- Khung DFS với vị trí pre-order và post-order.
- Duyệt theo tầng Cách Một (hàng đợi đếm kích thước tầng), Cách Hai (DFS
  đệ quy mang theo độ sâu), và Cách Ba (hàng đợi có trọng số mang trạng
  thái độ sâu).
- Helper `forest_preorder` duyệt mọi gốc trong một rừng.
- Kiểm tra ngẫu nhiên chứng minh ba cách duyệt theo tầng khớp nhau.

Nguồn tham khảo:

- [N-ary Tree Recursive/Level Traversal](https://labuladong.online/en/algo/data-structure-basic/n-ary-tree-traverse-basic/)
- [Binary Tree Recursive/Level Traversal](https://labuladong.online/en/algo/data-structure-basic/binary-tree-traverse-basic/)

## 2. Nút N-ary so với nút nhị phân

Nút cây nhị phân có hai con được đặt tên:

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

Nút cây N-ary thay vào đó lưu một danh sách con:

```python
class Node:
    def __init__(self, val, children=None):
        self.val = val
        self.children = children if children is not None else []
```

Đó là khác biệt duy nhất. Cây nhị phân là trường hợp đặc biệt khi danh sách
con có tối đa hai phần tử.

So sánh cạnh nhau:

```text
   nút nhị phân                 nút N-ary
      (v)                        (v)
     /   \                  /   |   |   \
  (trái)(phải)          (c1) (c2) (c3) (c4)
```

## 3. Rừng (Forest)

Rừng là tập hợp nhiều cây N-ary; một cây đơn lẻ là một dạng đặc biệt của
rừng. Trong code nó chỉ là một danh sách các nút gốc:

```python
forest = [root_a, root_b, root_c]
```

Chạy DFS hoặc BFS trên từng gốc sẽ ghé thăm mọi nút của rừng. Thuật toán
Union Find giữ gốc của nhiều cây N-ary, và các gốc đó cùng nhau tạo thành
một rừng.

```python
def forest_preorder(roots):
    visited = []
    for root in roots:
        traverse_dfs(root, on_preorder=lambda node: visited.append(node.val))
    return visited
```

Một rừng với ba gốc:

```text
  gốc:  (A)     (B)      (C)
       /   \     |      /   \
     (a1) (a2) (b1)   (c1)  (c2)

  DFS từng gốc theo thứ tự:
  A, a1, a2,  B, b1,  C, c1, c2
```

## 4. Duyệt đệ quy (DFS): Khung tổng quát

Khung duyệt cây nhị phân là:

```python
def traverse(root):
    if root is None:
        return
    # vị trí pre-order
    traverse(root.left)
    # vị trí in-order
    traverse(root.right)
    # vị trí post-order
```

Khung N-ary thay hai lời gọi đệ quy bằng một vòng lặp:

```python
def traverse_dfs(root, on_preorder=None, on_postorder=None):
    if root is None:
        return

    if on_preorder is not None:
        on_preorder(root)

    for child in root.children:
        traverse_dfs(child, on_preorder, on_postorder)

    if on_postorder is not None:
        on_postorder(root)
```

Vì một nút có thể có bất kỳ số con nào, code không thể gọi tên riêng `left`
và `right`. Vòng lặp qua `children` chính là sự tổng quát hóa của hai lời
gọi đó.

Hai vị trí móc (hook) của khung:

```text
traverse_dfs(root)
  |
  +-- [vị trí pre-order]  duyệt root            <-- trước các con
  |
  +-- với mỗi con c trong root.children:
  |       traverse_dfs(c)          (lặp lại cho từng con)
  |
  +-- [vị trí post-order]  duyệt root           <-- sau các con
```

Cây lời gọi của cây mẫu `1 -> [3, 2, 4], 3 -> [5, 6]`:

```text
                 traverse(1)
                /     |     \
          traverse(3) traverse(2) traverse(4)
           /        \
    traverse(5)  traverse(6)

  duyệt pre-order:  1, 3, 5, 6, 2, 4
  duyệt post-order: 5, 6, 3, 2, 4, 1
```

## 5. Preorder và postorder (LC 589 và 590)

LeetCode 589 thu thập giá trị ở vị trí pre-order:

```python
def preorder(root):
    result = []
    traverse_dfs(root, on_preorder=lambda node: result.append(node.val))
    return result
```

LeetCode 590 thu thập giá trị ở vị trí post-order:

```python
def postorder(root):
    result = []
    traverse_dfs(root, on_postorder=lambda node: result.append(node.val))
    return result
```

Với cây `1 -> [3, 2, 4], 3 -> [5, 6]`:

```text
preorder:  [1, 3, 5, 6, 2, 4]
postorder: [5, 6, 3, 2, 4, 1]
```

## 6. Vì sao không có vị trí in-order

Khung nhị phân có một vị trí ở giữa hai con. Nút N-ary không có đúng hai
con, nên "vị trí giữa" không xác định. Chỉ vị trí pre-order và post-order
tồn tại trong khung N-ary.

Vị trí pre-order chạy trước công việc của cây con, hợp với tác vụ từ trên
xuống như sao chép giá trị. Vị trí post-order chạy sau mọi con, hợp với tác
vụ từ dưới lên như gom kết quả của cây con.

## 7. Tổng quan duyệt theo tầng (BFS)

Duyệt theo tầng ghé thăm cây lần lượt từng tầng một. Có ba cách chuẩn để
cài đặt, liệt kê bên dưới. Cả ba trả về cùng các tầng, nên việc chọn chỉ là
vấn đề phong cách và thói quen.

Với cây `1 -> [3, 2, 4], 3 -> [5, 6]` các tầng là:

```text
[[1], [3, 2, 4], [5, 6]]
```

Minh họa theo tầng:

```text
  tầng 0   (1)
  tầng 1   (3)  (2)  (4)
  tầng 2   (5)  (6)

  1 -> [3, 2, 4]
  3 -> [5, 6]
```

## 8. Cách Một: Hàng đợi đếm kích thước tầng

Khung BFS phổ biến nhất đếm số nút của tầng hiện tại trước khi xử lý:

```python
def level_order_traverse(root):
    if root is None:
        return []

    levels = []
    queue = deque([root])

    while queue:
        level_size = len(queue)
        level = []

        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)
            for child in node.children:
                queue.append(child)

        levels.append(level)

    return levels
```

Ranh giới `level_size` gom đúng một tầng, vì mọi nút của tầng kế tiếp chỉ
vào hàng đợi sau khi cha của nó được xử lý xong.

Sự tiến hóa của hàng đợi cho cây mẫu:

```text
bắt đầu  hàng đợi: [1]
tầng 1   pop 1, thêm 3, 2, 4
         hàng đợi: [3, 2, 4]          tầng = [1]
tầng 2   pop 3, thêm 5, 6
         pop 2, pop 4
         hàng đợi: [5, 6]             tầng = [3, 2, 4]
tầng 3   pop 5, pop 6
         hàng đợi: []                 tầng = [5, 6]
```

## 9. Cách Hai: DFS đệ quy mang theo độ sâu

Cách Hai có cấu trúc là DFS nhưng cho ra kết quả theo tầng. Mỗi lời gọi nối
giá trị của nó vào danh sách ở đúng độ sâu của nó:

```python
def level_order_recursive(root):
    levels = []

    def traverse(node, depth):
        if node is None:
            return

        if len(levels) <= depth:
            levels.append([])
        levels[depth].append(node.val)

        for child in node.children:
            traverse(child, depth + 1)

    traverse(root, 0)
    return levels
```

Tham số độ sâu thay thế ranh giới tầng. Đây là hình dạng kinh điển của các
lời giải LeetCode 429.

Đệ quy với tham số độ sâu:

```text
traverse(1, 0)   -> levels[0] = [1]
  traverse(3, 1) -> levels[1] = [3]
    traverse(5, 2) -> levels[2] = [5]
    traverse(6, 2) -> levels[2] = [5, 6]
  traverse(2, 1) -> levels[1] = [3, 2]
  traverse(4, 1) -> levels[1] = [3, 2, 4]
```

Danh sách kết quả lớn dần từng tầng một, và mỗi giá trị rơi vào danh sách
được đánh chỉ số bởi chính độ sâu của nó.

## 10. Cách Ba: Hàng đợi có trọng số mang trạng thái độ sâu

Cách Ba lưu độ sâu cùng với nút trong hàng đợi:

```python
class LevelState:
    def __init__(self, node, depth):
        self.node = node
        self.depth = depth


def level_order_states(root):
    if root is None:
        return []

    levels = []
    queue = deque([LevelState(root, 0)])

    while queue:
        state = queue.popleft()
        node = state.node
        depth = state.depth

        if len(levels) <= depth:
            levels.append([])
        levels[depth].append(node.val)

        for child in node.children:
            queue.append(LevelState(child, depth + 1))

    return levels
```

Các phần tử hàng đợi tự mang trạng thái của mình, nên các tầng không còn
phụ thuộc kích thước hàng đợi. Ý tưởng hàng đợi có trọng số này tổng quát
hóa sang Dijkstra và các biến thể BFS khác khi trạng thái nhiều hơn một con
số.

Sự tiến hóa của hàng đợi với độ sâu mang bên trong từng phần tử:

```text
bắt đầu  hàng đợi: [(1, 0)]
bước 1   pop (1, 0), thêm (3, 1), (2, 1), (4, 1)
         hàng đợi: [(3, 1), (2, 1), (4, 1)]
bước 2   pop (3, 1), thêm (5, 2), (6, 2)
         hàng đợi: [(2, 1), (4, 1), (5, 2), (6, 2)]
bước 3   pop (2, 1)
bước 4   pop (4, 1)
         hàng đợi: [(5, 2), (6, 2)]
bước 5   pop (5, 2)
bước 6   pop (6, 2)
         hàng đợi: []
```

## 11. Nên dùng cách nào

```text
Cách Một  -> mặc định; vòng lặp đơn giản nhất với ranh giới tầng rõ ràng
Cách Hai  -> khi bạn đã quen suy nghĩ đệ quy và theo dõi độ sâu
Cách Ba   -> khi mỗi phần tử hàng đợi cần thêm trạng thái ngoài tầng
```

Cả ba đều chạy `O(N)`. Cách Một thường là đủ, nhưng biết hai cách còn lại
giúp đọc các bài BFS có trọng số và DFS/BFS lai dễ dàng hơn.

## 12. Độ phức tạp

Với cây N-ary có `N` nút và chiều cao `H`:

| Cách duyệt | Thời gian | Bộ nhớ thêm |
|:---|:---:|:---|
| DFS đệ quy (pre/post) | `O(N)` | `O(H)` ngăn xếp đệ quy |
| Cách Một (hàng đợi + kích thước) | `O(N)` | `O(W)` hàng đợi, `W` = tầng rộng nhất |
| Cách Hai (đệ quy + độ sâu) | `O(N)` | `O(H)` ngăn xếp cộng danh sách tầng |
| Cách Ba (hàng đợi có trọng số) | `O(N)` | `O(N)` hàng đợi trạng thái |
| Duyệt rừng | `O(N)` | giống cách duyệt được dùng |

## 13. API Python công khai

```python
root = Node.from_level_order([1, None, 3, 2, 4, None, 5, 6])

preorder(root)             # [1, 3, 5, 6, 2, 4]       (LC 589)
postorder(root)            # [5, 6, 3, 2, 4, 1]       (LC 590)
level_order_traverse(root) # [[1], [3, 2, 4], [5, 6]] (LC 429, Cách Một)
level_order_recursive(root)   # cùng các tầng (Cách Hai)
level_order_states(root)      # cùng các tầng (Cách Ba)

forest_preorder([root_a, root_b])   # DFS qua mọi gốc

traverse_dfs(root, on_preorder=fn, on_postorder=fn)  # chính khung tổng quát
```

## 14. Ví dụ

Chạy:

```text
python NaryTreeTraversal.py
```

Demo dựng cây mẫu, in preorder, postorder, và kết quả duyệt theo tầng từ cả
ba cách, kiểm tra chúng khớp nhau, duyệt một rừng nhỏ, rồi chạy 200 cây ngẫu
nhiên trong đó ba cách duyệt theo tầng và các kết quả DFS được đối chiếu
chéo.

## 15. Nguồn và liên kết LeetCode

- [N-ary Tree Recursive/Level Traversal](https://labuladong.online/en/algo/data-structure-basic/n-ary-tree-traverse-basic/)
- [589. N-ary Tree Preorder Traversal](https://leetcode.com/problems/n-ary-tree-preorder-traversal/)
- [590. N-ary Tree Postorder Traversal](https://leetcode.com/problems/n-ary-tree-postorder-traversal/)
- [429. N-ary Tree Level Order Traversal](https://leetcode.com/problems/n-ary-tree-level-order-traversal/)
