
---

# Trường hợp sử dụng của DFS và BFS

## 1. Mục tiêu

Trong các bài toán thuật toán thực tế, DFS thường được dùng để liệt kê mọi
đường đi, còn BFS thường được dùng để tìm đường đi ngắn nhất. Tài liệu này
giải thích lý do, lấy LeetCode 111 Minimum Depth of Binary Tree làm ví dụ
chạy xuyên suốt, rồi tổng quát hóa lập luận cho đồ thị không trọng số.

Cài đặt trong `DfsBfsUseCases.py` cung cấp:

- `min_depth_bfs` và `min_depth_dfs` cho LeetCode 111.
- `dfs_all_paths` và `bfs_all_paths` để liệt kê đường đi từ gốc tới lá.
- `bfs_shortest_path` và `dfs_graph_paths` cho đồ thị không trọng số.
- Kiểm tra ngẫu nhiên chứng minh BFS và DFS cho cùng đáp án.

Nguồn tham khảo:

- [Use cases of DFS and BFS](https://labuladong.online/en/algo/data-structure-basic/use-case-of-dfs-bfs/)
- [Binary Tree Recursive/Level Traversal](https://labuladong.online/en/algo/data-structure-basic/binary-tree-traverse-basic/)

## 2. Hai quy tắc kinh nghiệm

Hai câu hỏi mà bài viết này trả lời:

```text
Vì sao BFS thường được dùng để tìm đường đi ngắn nhất?
Vì sao DFS thường được dùng để tìm mọi đường đi?
```

Duyệt đệ quy và duyệt theo tầng của cây nhị phân là hai dạng đơn giản nhất
của DFS và BFS. Cả hai quy tắc đều quan sát được trong bối cảnh đơn giản này.

## 3. Vì sao BFS thường được dùng để tìm đường đi ngắn nhất

Duyệt theo tầng chính là BFS trên cây. Cấu trúc cốt lõi của nó là:

```text
xử lý tầng 0 (gốc)
xử lý tầng 1
xử lý tầng 2
...
```

Nút ở tầng `d` cách gốc đúng `d` bước. Vì vậy lần đầu BFS chạm tới nút đích,
biến đếm tầng chính là khoảng cách nhỏ nhất. BFS duyệt các nút theo thứ tự
khoảng cách tăng dần, nên đích tìm thấy đầu tiên tự động là đích gần nhất.

BFS lan tỏa như các gợn nước, mỗi lần một vòng:

```text
               (gốc) ............. vòng 0  (khoảng cách 0)
              /      \
          (a)          (b) ...... vòng 1  (khoảng cách 1)
         /  \          /  \
       (c)  (d)      (e)  (f) .. vòng 2  (khoảng cách 2)

  bất kỳ đích nào ở vòng 1 đều gần hơn mọi đích ở vòng 2,
  nên vòng đầu tiên chứa đích chính là đáp án.
```

DFS không có tính chất này. Nó lao thẳng xuống một lá nhanh nhất có thể và
chỉ trả kết quả cho một đường đi. Nó không biết nhánh khác có đích gần hơn
hay không cho tới khi cũng phải xét nhánh đó.

## 4. BFS giải LeetCode 111: Độ sâu nhỏ nhất

Bài toán là độ sâu nhỏ nhất của cây nhị phân: số nút trên đường đi ngắn nhất
từ gốc tới lá gần nhất.

```python
def min_depth_bfs(root, trace=None):
    if root is None:
        return 0

    queue = deque([root])
    depth = 1

    while queue:
        level_size = len(queue)
        for _ in range(level_size):
            node = queue.popleft()

            if node.left is None and node.right is None:
                return depth

            if node.left is not None:
                queue.append(node.left)
            if node.right is not None:
                queue.append(node.right)

        depth += 1

    return depth
```

Với cây `[3, 9, 20, None, None, 15, 7]`:

```text
        3
       / \
      9   20
         /  \
        15   7
```

Từng bước, hàng đợi BFS tiến hóa như sau (một lá được tìm thấy ở tầng 2):

```text
bước 1   hàng đợi: [3]           duyệt 3          depth = 1
         thêm con của nó là 9, 20

bước 2   hàng đợi: [9, 20]       duyệt 9          depth = 2
         9 là lá  ->  trả về 2  (xong, 20 không bao giờ được duyệt)
```

Cùng cây đó dưới BFS với thứ tự duyệt được đánh dấu:

```text
   duyệt 1: (3) ..................... tầng 1
           /  \
duyệt 2: (9)  (20) .................. tầng 2
               /  \
            (15)   (7)             (không bao giờ tới)
```

BFS xử lý tầng 1 (`3`), rồi tầng 2 (`9`, `20`). Nút `9` là lá, nên đáp án là
`2`. Các nút `15` và `7` không bao giờ được ghé thăm. Demo in vết duyệt
`[3, 9]` của BFS so với `[3, 9, 20, 15, 7]` của DFS.

## 5. Vì sao DFS không thể dừng ở lá đầu tiên

Phiên bản DFS của LeetCode 111 phải xét mọi nhánh:

```python
def min_depth_dfs(root, trace=None):
    if root is None:
        return 0

    if root.left is None and root.right is None:
        return 1

    if root.left is None:
        return min_depth_dfs(root.right, trace) + 1

    if root.right is None:
        return min_depth_dfs(root.left, trace) + 1

    return min(
        min_depth_dfs(root.left, trace),
        min_depth_dfs(root.right, trace),
    ) + 1
```

Lá đầu tiên DFS gặp chưa chắc là lá nông nhất, nên DFS phải giữ giá trị nhỏ
nhất chạy qua mọi nhánh. Trong bài toán này nó luôn duyệt cả cây. Đáp án thì
giống nhau, nhưng bảo đảm "tìm thấy đầu tiên là ngắn nhất" khiến BFS tự
nhiên với bài toán này lại không tồn tại với DFS.

Thứ tự duyệt của DFS trên cùng cây cho thấy mọi nút đều được chạm tới:

```text
  duyệt 1: ①(3)
          /    \
  duyệt 2: ②(9)   ③(20)
                  /    \
         duyệt 4: ④(15)   ⑤(7)
```

DFS lao xuống `9` trước, nhưng vẫn phải đi ngược lên và kiểm tra cả nhánh
`20` trước khi chắc chắn rằng `2` là giá trị nhỏ nhất.

## 6. Chi phí bộ nhớ của BFS

BFS giữ nguyên cả một tầng trong hàng đợi cùng lúc. Cây nhị phân đầy đủ có
khoảng `N / 2` lá, nên hàng đợi có thể chứa `O(N)` nút.

DFS chỉ giữ ngăn xếp đệ quy của đường đi hiện tại, tức là `O(height)`, hay
`O(log N)` với cây cân bằng.

Đây là sự đánh đổi: BFS mua bảo đảm đường ngắn nhất bằng bộ nhớ rộng hơn,
còn DFS chỉ lưu một đường đi tại một thời điểm.

## 7. Vì sao DFS thường được dùng để tìm mọi đường đi

DFS kết hợp quay lui mang đường đi hiện tại trên ngăn xếp đệ quy. Khi tìm
kiếm tới một lá, ngăn xếp đúng bằng một đường đi từ gốc tới lá. Sao chép nó
là ghi lại đường đi mà không cần sổ sách gì thêm.

BFS cũng liệt kê được mọi đường đi, nhưng hàng đợi của nó chứa các nút độc
lập, không phải cấu trúc đường đi. Mỗi phần tử trong hàng đợi phải mang theo
bản sao đầy đủ đường đi của riêng nó, gây tốn bộ nhớ và phức tạp hóa code.

## 8. DFS với quay lui liệt kê mọi đường đi

```python
def dfs_all_paths(root):
    paths = []
    path = []

    def backtrack(node):
        if node is None:
            return

        path.append(node.val)

        if node.left is None and node.right is None:
            paths.append(list(path))
        else:
            backtrack(node.left)
            backtrack(node.right)

        path.pop()

    backtrack(root)
    return paths
```

Với cây `[1, 2, 3, None, 5]` kết quả là:

```text
[[1, 2, 5], [1, 3]]
```

Cây và ngăn xếp đường đi dùng chung trong lúc quay lui:

```text
          1
         / \
        2   3
         \
          5

  dfs(1)        path = [1]
    dfs(2)      path = [1, 2]
      dfs(5)    path = [1, 2, 5]   -> ghi lại [1, 2, 5]
      pop 5     path = [1, 2]
    pop 2       path = [1]
    dfs(3)      path = [1, 3]      -> ghi lại [1, 3]
    pop 3       path = [1]
  pop 1         path = []
```

Danh sách `path` dùng chung hoạt động như một ngăn xếp: đẩy vào khi vào nút,
lấy ra khi rời nút. Vì chỉ có một danh sách đường đi, bộ nhớ sổ sách chỉ là
`O(height)`.

## 9. BFS phải làm gì để liệt kê mọi đường đi

Phiên bản BFS lưu một bản sao đường đi trong mỗi phần tử hàng đợi:

```python
def bfs_all_paths(root):
    if root is None:
        return []

    paths = []
    queue = deque([(root, [root.val])])

    while queue:
        node, path = queue.popleft()

        if node.left is None and node.right is None:
            paths.append(path)
            continue

        if node.left is not None:
            queue.append((node.left, path + [node.left.val]))
        if node.right is not None:
            queue.append((node.right, path + [node.right.val]))

    return paths
```

Nó trả về cùng tập đường đi, nhưng mỗi phần tử hàng đợi nhân bản một tiền tố
của đường đi của nó, nên tổng lưu trữ là `O(số đường đi * độ dài đường)`
thay vì `O(height)` của ngăn xếp DFS. Đó là lý do DFS là lựa chọn quen thuộc
khi cần liệt kê mọi đường đi.

## 10. Cùng quy tắc trên đồ thị tổng quát

Quy tắc không chỉ giới hạn ở cây. Trên đồ thị không trọng số:

```python
def bfs_shortest_path(graph, start, target):
    if start not in graph or target not in graph:
        return None

    queue = deque([start])
    parent = {start: None}

    while queue:
        node = queue.popleft()
        if node == target:
            path = []
            cursor = node
            while cursor is not None:
                path.append(cursor)
                cursor = parent[cursor]
            path.reverse()
            return len(path) - 1, path

        for neighbor in graph[node]:
            if neighbor not in parent:
                parent[neighbor] = node
                queue.append(neighbor)

    return None
```

BFS khám phá các nút theo thứ tự khoảng cách từ điểm xuất phát, nên lần lấy
ra đầu tiên của đích là một đường đi ngắn nhất. Demo kiểm chứng điều này với
hàm tham chiếu `dfs_graph_paths` liệt kê mọi đường đi đơn và lấy độ dài nhỏ
nhất.

Ý tưởng vòng tròn trên đồ thị demo (`A` là điểm xuất phát, `F` là đích):

```text
        A --- B
        |     |
        C --- D --- F
         \   /
          E

  vòng 0: A
  vòng 1: B, C
  vòng 2: D, E
  vòng 3: F        <- vòng đầu tiên chứa đích, khoảng cách = 3
```

Ngược lại, DFS phải liệt kê các đường `A->B->D->F` (dài 3) và `A->C->E->F`
(dài 3), cùng các tuyến dài hơn bị cắt khi không còn là đường đơn, trước khi
lấy giá trị nhỏ nhất.

## 11. So sánh độ phức tạp

Với cây có `N` nút:

| Tác vụ | Thuật toán | Thời gian | Bộ nhớ |
|:---|:---|:---:|:---:|
| Độ sâu nhỏ nhất | BFS | `O(N)` tệ nhất, dừng sớm | `O(N)` hàng đợi |
| Độ sâu nhỏ nhất | DFS | `O(N)` luôn luôn | `O(height)` ngăn xếp |
| Mọi đường đi gốc-lá | DFS quay lui | `O(N)` lời gọi | `O(height)` cộng output |
| Mọi đường đi gốc-lá | BFS chép đường đi | `O(N)` lượt ghé | `O(đường * độ dài)` |
| Đường ngắn nhất đồ thị | BFS | `O(V + E)` | `O(V)` |
| Mọi đường đi đồ thị | DFS quay lui | `O(số đường)` | `O(V)` cộng output |

## 12. Cách chọn giữa DFS và BFS

```text
Khoảng cách ngắn nhất, ít bước nhất, đích gần nhất  -> BFS
Liệt kê mọi đường đi, mọi lời giải, quay lui        -> DFS
Bộ nhớ quan trọng và cây rộng                       -> DFS
Cần thoát sớm khi đáp án ở gần                       -> BFS
```

DFS và BFS cuối cùng ghé cùng tập nút với tìm kiếm vét cạn. Khác biệt là
thứ tự duyệt và hình dạng của bộ nhớ làm việc, và khác biệt đó quyết định mỗi
thuật toán hợp với tác vụ nào.

## 13. API Python công khai

```python
root = build_tree([3, 9, 20, None, None, 15, 7])

min_depth_bfs(root)            # 2, kèm danh sách trace tùy chọn
min_depth_dfs(root)            # 2, kèm danh sách trace tùy chọn

dfs_all_paths(root)            # danh sách các danh sách giá trị
bfs_all_paths(root)            # cùng tập hợp, khác thứ tự

graph = {"A": ["B", "C"], ...}
bfs_shortest_path(graph, "A", "F")   # (khoảng cách, đường đi) hoặc None
dfs_graph_paths(graph, "A", "F")     # mọi đường đi đơn

count_nodes(root)              # helper cho việc kiểm chứng
```

## 14. Ví dụ

Chạy:

```text
python DfsBfsUseCases.py
```

Demo in vết duyệt của LeetCode 111, kết quả liệt kê đường đi của cả hai thuật
toán, một đường đi ngắn nhất trên đồ thị được kiểm chứng với DFS vét cạn, và
kết quả của 200 lần kiểm tra ngẫu nhiên trên cây cùng 200 lần trên đồ thị.

## 15. Nguồn và liên kết LeetCode

- [Use cases of DFS and BFS](https://labuladong.online/en/algo/data-structure-basic/use-case-of-dfs-bfs/)
- [111. Minimum Depth of Binary Tree](https://leetcode.com/problems/minimum-depth-of-binary-tree/)
