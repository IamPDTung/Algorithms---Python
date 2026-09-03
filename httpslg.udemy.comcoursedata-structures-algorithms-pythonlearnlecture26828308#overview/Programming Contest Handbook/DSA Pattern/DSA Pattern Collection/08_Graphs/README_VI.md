# GRAPHS (ĐỒ THỊ)

## Nó là gì?

Đồ thị là tập các **nút (đỉnh)** nối với nhau bằng **cạnh**. Cạnh có thể:
- **Có hướng** (một chiều) hoặc **vô hướng** (hai chiều).
- **Có trọng số** (chi phí mỗi cạnh) hoặc **không trọng số**.
- Lưu dạng **danh sách kề** `{nút: [các nút kề]}` (phổ biến nhất) hoặc **ma trận**.

Các thuật toán duyệt cốt lõi:
- **DFS** — duyệt sâu (stack / đệ quy).
- **BFS** — duyệt rộng (hàng đợi); cho **đường đi ngắn nhất trên đồ thị không trọng số**.
- **Dijkstra** — đường đi ngắn nhất trên đồ thị có trọng số (heap).
- **Topological Sort** — thứ tự cho DAG (Kahn / DFS).
- **Union Find** — tính liên thông (xem pattern 12).

## Vì sao dùng?

- Dữ liệu thực tế mang tính quan hệ: bạn bè, đường xá, liên kết web, môn học tiên quyết, mạng.
- Nhiều bài toán quy về *"có đến được X không?"*, *"tuyến đường ngắn nhất"*,
  *"có chu trình không?"*, *"thứ tự nào để chạy các tác vụ?"* — tất cả là bài đồ thị.
- Học 5 công cụ này bao phủ phần lớn bài đồ thị trong thi đấu.

## Khi nào dùng?

| Dấu hiệu trong đề bài | Công cụ |
|---|---|
| "Liên thông / đến được / đếm đảo" | DFS hoặc BFS |
| "Đường đi ngắn nhất, không trọng số" | BFS |
| "Đường đi ngắn nhất, có trọng số" | Dijkstra |
| "Thứ tự môn học / tác vụ (DAG)" | Topological Sort |
| "Phát hiện chu trình" | DFS (tô màu) / Kahn / Union Find |
| "Tỉnh / thành phần liên thông" | Union Find hoặc DFS |

## Minh họa — đồ thị vô hướng, danh sách kề

```
    A ─── B
    │     │
    C ─── D

 danh sách kề:
   A: [B, C]
   B: [A, D]
   C: [A, D]
   D: [B, C]

 BFS từ A:  A -> B, C -> D    thứ tự: A, B, C, D
 DFS từ A:  A -> B -> D -> C  thứ tự: A, B, D, C
```

## Minh họa — Dijkstra trên đồ thị có trọng số

```
       1
   A ───── B
   | \     |
  4|  \2   |2
   |   \   |
   C ──3── D

 dist:  A=0, B=1, C=4, D=3
 đường tới D: A -> B -> D  (1 + 2 = 3)
 (trực tiếp A->D = 5, qua C = 4 + 3 = 7, nên qua B là tốt nhất)

 Thuật toán: tham lam - liên tục nới lỏng nút có dist nhỏ nhất (hàng đợi ưu tiên)
```

## Độ phức tạp

- **DFS / BFS:** O(V + E) thời gian, O(V) bộ nhớ
- **Dijkstra:** O((V + E) log V)
- **Topological sort (Kahn):** O(V + E)

## Mẫu code (BFS)

```python
from collections import deque

def bfs(graph, start):
    visited = {start}
    q = deque([start])
    while q:
        node = q.popleft()
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                q.append(neighbor)
```

## Bài tập mẫu trong thư mục này

| Bài toán | File | Ý tưởng |
|---|---|---|
| Number of Islands | `number_of_islands.py` | DFS flood fill |
| Course Schedule | `course_schedule.py` | topological sort / kiểm tra chu trình |
| Clone Graph | `clone_graph.py` | DFS + bảng băm |

## Luyện tập

Thử: Network Delay Time (Dijkstra), Word Ladder (BFS), Alien Dictionary (topo sort),
Number of Provinces (Union Find), Rotting Oranges (BFS nhiều nguồn).
