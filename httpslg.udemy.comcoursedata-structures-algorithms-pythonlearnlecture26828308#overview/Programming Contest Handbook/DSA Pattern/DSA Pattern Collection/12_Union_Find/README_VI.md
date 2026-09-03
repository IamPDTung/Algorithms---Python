# UNION FIND (DSU - CẤU TRÚC DỮ LIỆU CÁC TẬP RỜI)

## Nó là gì?

Union-Find (Disjoint Set Union, DSU) là cấu trúc dữ liệu quản lý phân hoạch các phần tử
thành các **tập rời nhau**. Nó hỗ trợ hai thao tác:
1. **Find(x)** — x thuộc tập nào? (kèm **nén đường đi - path compression**)
2. **Union(x, y)** — trộn tập chứa x và y. (theo **bậc / kích thước**)

Mỗi tập được biểu diễn bằng một cây; **gốc** là đại diện của tập. Với cả hai tối ưu, mỗi
thao tác chạy gần như **O(1)** khấu hao — **O(α(n))**, hàm Ackermann ngược.

## Vì sao dùng?

- Truy vấn **kết nối** cực nhanh: "A và B có nối với nhau không?"
- **Kết nối động** — cạnh thêm dần theo thời gian; union khi cạnh đến.
- **Phát hiện chu trình trong đồ thị vô hướng**: nếu hai nút đã cùng gốc, cạnh mới tạo chu trình.
- Đếm **thành phần liên thông** bằng cách đếm các gốc phân biệt.

## Khi nào dùng?

| Dấu hiệu trong đề bài | Vì sao |
|---|---|
| "Thành phần liên thông / tỉnh / nhóm" | union các thành viên, đếm gốc |
| "A và B có nối nhau không?" | find(A) == find(B) |
| "Cạnh thừa / chu trình trong vô hướng" | union hai đầu cạnh, phát hiện chu trình |
| "Tài khoản / người hợp nhất" | union các định danh chồng lấn |
| "Kết nối động / trực tuyến" | xử lý union dần |

## Minh họa — union by rank

```
 Ban đầu:  0  1  2  3  4  5        (mỗi phần tử một tập)

 union(0,1):  parent[0] = 1        rank[1] = 1
 union(2,3):  parent[2] = 3        rank[3] = 1
 union(0,3):  0 -> 1,  2 -> 3
              rank bằng nhau -> gắn gốc của một tập dưới tập kia
              parent[1] = 3        rank[3] = 2

 Cây:
   trước union(0,3):    1         3
                       /          /
                      0          2
   sau union(0,3):      3
                        / \
                       1   2
                      /
                     0
   find(0): 0 -> 1 -> 3   (nén đường: 0 giờ trỏ thẳng tới 3)

 Gốc: {3} cho {0,1,2,3}, {4}, {5}  -> 3 thành phần liên thông
```

## Độ phức tạp

- **Thời gian:** O(α(n)) ~ O(1) khấu hao mỗi thao tác
- **Bộ nhớ:** O(n)

## Mẫu code

```python
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):                    # nén đường đi
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, x, y):                # union theo bậc
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False                  # đã nối rồi (chu trình!)
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1
        return True
```

## Bài tập mẫu trong thư mục này

| Bài toán | File | Ý tưởng |
|---|---|---|
| Lớp DSU | `union_find.py` | triển khai tái sử dụng |
| Redundant Connection | `redundant_connection.py` | union các cạnh, cạnh chu trình đầu tiên |
| Number of Provinces | `number_of_provinces.py` | union các thành phố, đếm gốc |

## Luyện tập

Thử: Accounts Merge, Number of Connected Components in an Undirected Graph,
Smallest String With Swaps, Satisfiability of Equality Equations, Regions Cut By Slashes.
