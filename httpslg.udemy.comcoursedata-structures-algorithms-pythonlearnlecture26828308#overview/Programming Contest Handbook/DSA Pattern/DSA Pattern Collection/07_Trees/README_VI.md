# TREES (CÂY)

## Nó là gì?

Tree là cấu trúc dữ liệu **phân cấp** gồm các **nút** nối với nhau bằng **cạnh**, có một
**gốc** duy nhất. Mỗi nút có các nút con; nút không có con gọi là **lá**. **Cây nhị phân**
(mỗi nút có tối đa 2 con) phổ biến nhất trong bài toán.

Hai cách duyệt cơ bản:
- **DFS** — Preorder (gốc, trái, phải), Inorder (trái, gốc, phải),
  Postorder (trái, phải, gốc).
- **BFS / Level-order** — duyệt theo từng tầng.

## Vì sao dùng?

- Mô hình tự nhiên cho **dữ liệu phân cấp** (hệ thống file, HTML, sơ đồ tổ chức, BST, heap).
- Các bài về **quan hệ cha / con**, **đường đi**, **độ sâu / chiều cao**, **cây con**.
- Nhiều bài phân rã thành: "giải cho gốc dùng kết quả của cây con trái & phải" — mẫu đệ quy
  ghé mỗi nút đúng một lần (**O(n)**).

## Khi nào dùng?

| Dấu hiệu trong đề bài | Vì sao |
|---|---|
| "Cây nhị phân", "BST" | cấu trúc cây được cho |
| "Tổng đường đi / độ sâu / chiều cao / đường kính" | đệ quy đi lên cây |
| "Tổ tiên chung thấp nhất (LCA)" | DFS truyền kết quả lên |
| "Duyệt theo tầng" | BFS với hàng đợi |
| "Cây con / tuần tự hóa" | so sánh đệ quy hoặc làm phẳng |

## Minh họa — thứ tự duyệt

```
            1
          /   \
         2     3
        / \     \
       4   5     6

 Preorder:   1, 2, 4, 5, 3, 6     (gốc, trái, phải)
 Inorder:    4, 2, 5, 1, 3, 6     (trái, gốc, phải)
 Postorder:  4, 5, 2, 6, 3, 1     (trái, phải, gốc)
 BFS:        1, 2, 3, 4, 5, 6     (theo từng tầng)
```

## Minh họa — đường kính cây nhị phân

```
 Đường kính = đường đi dài nhất giữa hai nút bất kỳ (đếm theo cạnh).

            1
           / \
          2   3
         / \
        4   5
       /     \
      6       7

 đường dài nhất: 6 -> 4 -> 2 -> 5 -> 7   (5 cạnh)
 tính: tại nút 2, leftHeight=2, rightHeight=2
       ứng viên = 2 + 2 = 4
       tại nút 1, leftHeight=3, rightHeight=0
       ứng viên = 3 + 0 = 3
 đáp án = max(4, 3) = 4? Không—tính lại đúng:
 height(2) = 3 (qua 6->4->2), height(5) = 2 -> đường qua 2 = 3 + 2 = 5
```

## Độ phức tạp

- **Thời gian:** O(n) — mỗi nút ghé một lần
- **Bộ nhớ:** O(h) — ngăn xếp đệ quy, h = chiều cao (tệ nhất O(n) với cây lệch)

## Mẫu code (DFS đệ quy)

```python
def dfs(node):
    if node is None:
        return 0                    # trường hợp cơ sở
    left = dfs(node.left)
    right = dfs(node.right)
    return combine(left, right, node)   # kết hợp thành đáp án
```

## Bài tập mẫu trong thư mục này

| Bài toán | File | Ý tưởng |
|---|---|---|
| Lowest Common Ancestor | `lowest_common_ancestor.py` | đệ quy truyền lên |
| Diameter of Binary Tree | `diameter_of_binary_tree.py` | leftHeight + rightHeight |
| Serialize & Deserialize | `serialize_deserialize.py` | BFS với marker "null" |

## Luyện tập

Thử: Maximum Path Sum, Binary Tree Level Order Traversal, Validate BST,
Maximum Depth, Same Tree, Invert Tree.
