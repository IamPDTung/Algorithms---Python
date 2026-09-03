
---

# Các Thuật toán Cây khung Nhỏ nhất (Minimum Spanning Tree Algorithms)

## 1. Mục tiêu

Một **cây khung nhỏ nhất (MST)** nối mọi nút của một đồ thị vô hướng có trọng
số bằng tổng trọng số cạnh nhỏ nhất có thể — mà không tạo chu trình.

Đây là một bài toán trọng yếu: thiết kế bố trí mạng lưới/rải đường rẻ nhất, nối
dây mạch và lắp đặt đường ống đều quy về nó. Bài viết này bao quát định nghĩa,
vì sao nó tồn tại, và hai thuật toán kinh điển: **Kruskal** và **Prim**.

Nguồn tham khảo:
- https://labuladong.online/en/algo/data-structure-basic/graph-minimum-spanning-tree/

---

## 2. Vì sao Cây khung Nhỏ nhất ra đời

Giả sử bạn phải nối nhiều thành phố bằng đường bộ, và mỗi con đường khả thi có
một chi phí xây dựng. Bạn muốn nối tất cả các thành phố với **tổng chi phí thấp
nhất**.

```text
        A
       /|\
     1/ | \3
     /  |  \
    B  2|   C
     \  |  /
     4\ | /2
       \|/
        D

  connect A, B, C, D as cheaply as possible
```

Cách ngây thơ là thử mọi tập con của các con đường — theo hàm mũ. Các thuật
toán MST ra đời để tìm bố trí liên thông rẻ nhất **hiệu quả** và **chứng minh
được là tối ưu**.

Các ứng dụng thực tế:

```text
  telecommunication  - lay cable to connect all offices at minimum cost
  road / rail        - link all towns with the cheapest network
  circuit wiring     - connect all pins with minimal copper
  pipeline layout    - connect sources to sinks with least pipe
  maze generation    - carve a random connected maze (see below)
```

---

## 3. Cây khung (Spanning Tree) là gì?

Cho một đồ thị vô hướng liên thông `G`, một **cây khung** là một đồ thị con mà:

* chứa **tất cả** các đỉnh của `G`
* là một **cây** — liên thông và không chu trình
* do đó dùng đúng `V - 1` cạnh

```text
  graph G (4 nodes, 5 edges):        one spanning tree (3 edges):

        A---B                              A---B
        |\ /|                              |   |
        | X |                              |   |
        |/ \|                              |   |
        C---D                              C   D
```

Một đồ thị liên thông thường có **nhiều** cây khung khác nhau. Dưới đây là một
vài cây khung của cùng một đồ thị:

```text
  spanning tree #1:                spanning tree #2:
        A---B                           A---B
            |                           |
            |                           |
        C---D                           C---D

  both include all 4 nodes, both use 3 edges, both are acyclic
```

---

## 4. Cây khung Nhỏ nhất (MST) là gì?

Nếu đồ thị có **trọng số**, **cây khung nhỏ nhất** là cây khung có **tổng trọng
số cạnh nhỏ nhất**.

```text
        A
      2/ \3
      B---C
       \ /
        5
      (weights on edges)

  spanning tree {A-B, B-C}: weight 2 + 5 = 7
  spanning tree {A-B, A-C}: weight 2 + 3 = 5   <-- the MST
  spanning tree {B-C, A-C}: weight 5 + 3 = 8
```

MST chọn các cạnh để nối mọi thứ trong khi **tối thiểu hóa tổng**.

```text
  cities + road costs:           MST (cheapest connected network):

     A --5-- B                     A --5-- B
     |      /|                     |
     7    3/ |                     7
     |    /  |                     |
     C --1-- D                     C --1-- D
                                    (A-B=5, A-C=7, C-D=1 => 13)
```

Có đúng một đáp án cho **tổng trọng số**, dù các tập cạnh khác nhau có thể hòa
cho nó.

---

## 5. Hai Thuật toán Kinh điển

Cả hai đều tham lam, nhưng chúng phát triển cây theo cách khác nhau:

| Thuật toán | Phát triển bằng | Công cụ cốt lõi |
|:---|:---|:---|
| **Kruskal** | chọn cạnh rẻ nhất không tạo chu trình | sắp xếp cạnh + Union-Find |
| **Prim** | phát triển một thành phần bằng cạnh biên rẻ nhất | hàng đợi ưu tiên (giống Dijkstra) |

```text
  Kruskal: pick edges globally, cheapest first.
  Prim:    grow a single blob outward, cheapest boundary first.

  both end with the same MST total weight.
```

---

## 6. Thuật toán Kruskal: Sắp xếp + Union-Find

Ý tưởng của Kruskal giản dị đẹp đẽ:

```text
  1. Sort all edges by weight, cheapest first.
  2. Go through them in order.
  3. Add an edge only if it connects two different components
     (i.e. does not form a cycle).
  4. Stop when V-1 edges are in the tree.
```

```text
  edges sorted:  1, 1, 2, 2, 3, 4, 5

  add (0-1, 1)     components: {0,1}
  add (2-5, 1)     {0,1} {2,5}
  add (1-4, 2)     {0,1,4} {2,5}
  add (3-4, 2)     {0,1,3,4} {2,5}
  add (1-2, 3)     connects the two -> {0,1,2,3,4,5}  DONE (5 edges)
  skip (0-3, 4)    already connected (would form a cycle)
  skip (4-5, 5)    already connected
```

Để kiểm tra rẻ "cạnh này có nối hai thành phần khác nhau không?", Kruskal dùng
cấu trúc dữ liệu **Union-Find** (chủ đề của bài viết tiếp theo):

```python
def kruskal(g):
    edges = sorted(g.all_edges(), key=lambda e: e[2])
    uf = UnionFind(g.size())
    mst, total = [], 0.0
    for u, v, w in edges:
        if uf.union(u, v):        # True only if u,v were in different sets
            mst.append((u, v, w))
            total += w
    return total, mst
```

Vì sao bỏ qua chu trình là đúng: thêm một cạnh giữa hai nút đã nằm trong cùng
một thành phần sẽ tạo chu trình, thứ mà một cây không thể chứa.

Độ phức tạp: sắp xếp là `O(E log E)`; Union-Find thêm gần như `O(1)` mỗi cạnh,
nên tổng thể là `O(E log E)`.

---

## 7. Thuật toán Prim: Phát triển Một Thành phần

Prim hoạt động giống Dijkstra (bài viết trước), nhưng thay vì tối thiểu khoảng
cách tới một nguồn, nó tối thiểu chi phí để **phát triển một cây duy nhất**:

```text
  1. Start from any node; it is the tree.
  2. Look at all edges leaving the tree; push them on a min-priority queue.
  3. Pop the cheapest edge; if its other end is already in the tree, skip it.
  4. Otherwise add that node + edge to the tree, then push its edges.
  5. Stop when all nodes are in the tree.
```

```text
  start at 0:
    tree {0};  boundary edges: 0-1(1), 0-3(4)
    pop 0-1(1) -> tree {0,1};  add 1-4(2), 1-2(3)
    pop 1-4(2) -> tree {0,1,4}; add 4-3(2), 4-5(5)
    pop 4-3(2) -> tree {0,1,4,3}
    pop 1-2(3) -> tree {0,1,2,3,4}
    pop 2-5(1) -> tree {0,1,2,3,4,5}   DONE
```

```python
def prim(g, start=0):
    n = g.size()
    in_mst = [False] * n
    pq = []
    in_mst[start] = True
    for v, w in g.neighbors(start):
        heapq.heappush(pq, (w, start, v))
    mst, total = [], 0.0
    while pq:
        w, u, v = heapq.heappop(pq)
        if in_mst[v]:
            continue
        in_mst[v] = True
        mst.append((u, v, w))
        total += w
        for nxt, w2 in g.neighbors(v):
            if not in_mst[nxt]:
                heapq.heappush(pq, (w2, v, nxt))
    return total, mst
```

Hàng đợi ưu tiên luôn chọn cạnh rẻ nhất nối cây với một nút bên ngoài — chính
xác là bước tham lam giữ cho cây tối thiểu.

Độ phức tạp: `O(E log V)` với binary heap (giống Dijkstra).

---

## 8. Kruskal so với Prim

| | Kruskal | Prim |
|:---|:---|:---|
| Phát triển | toàn cục: các cạnh rẻ nhất trước | cục bộ: phát triển một blob |
| Công cụ chính | Union-Find | hàng đợi ưu tiên |
| Đồ thị thưa | tốt (`E log E`) | tốt (`E log V`) |
| Đồ thị dày | ổn | thường tốt hơn |
| Cảm giác | sắp xếp + liên thông | Dijkstra |

Cả hai đều tạo ra một MST hợp lệ. Lựa chọn chủ yếu là cái nào khớp với công cụ
và dữ liệu bạn đã có. Kruskal thường dễ lý luận nhất; Prim cảm giác tự nhiên khi
bạn đã có Dijkstra.

---

## 9. Sinh Mê cung Ngẫu nhiên (Ứng dụng vui)

Với một biến thể nhỏ, các thuật toán MST sinh ra các bản đồ mê cung và hang
động ngẫu nhiên. Tính chất then chốt: một MST nối mọi điểm **không tạo chu
trình** — chính xác thứ một mê cung cần (một đường liên thông, không vòng lặp).

```text
  a grid of cells as a graph (cells = nodes, walls = edges):

     +--+--+--+
     |  |  |  |
     +--+--+--+
     |  |  |  |
     +--+--+--+

  Kruskal:  start with all walls; add random cheap edges -> passageways
            appear in many places at once, then merge into one maze.
  Prim:     start from one cell; carve passageways outward from the blob
            -> the maze grows from a single point.

  both guarantee every cell is reachable (connected) with no loops.
```

Đó là lý do hai thuật toán tạo ra mê cung có đặc điểm thị giác khác nhau:
Kruskal đục nhiều điểm khởi đầu riêng biệt, còn Prim lan tỏa từ một gốc.

---

## 10. Tóm tắt Độ phức tạp

| Thuật toán | Thời gian | Không gian | Công cụ |
|:---|:---:|:---:|:---|
| Kruskal | `O(E log E)` | `O(V + E)` | sắp xếp + Union-Find |
| Prim | `O(E log V)` | `O(V + E)` | hàng đợi ưu tiên |

Trong đó `V` = nút, `E` = cạnh. Cả hai đều hiệu quả và mở rộng được cho các
mạng thực tế.

---

## 11. Những Sai lầm Thường gặp

### Sai lầm 1: Quên quy tắc dừng `V-1`

Một cây khung phải có đúng `V - 1` cạnh. Nếu đồ thị không liên thông, bạn không
thể đạt `V - 1` — hãy phát hiện điều đó (ít cạnh hơn nghĩa là không có cây
khung).

### Sai lầm 2: Thêm một cạnh tạo chu trình

Trong Kruskal, luôn kiểm tra rằng `u` và `v` thuộc các thành phần khác nhau
trước khi thêm. Thêm trong cùng một thành phần tạo chu trình và phá vỡ cây.

### Sai lầm 3: Dùng Prim mà không bỏ qua các nút trong cây

Khi pop khỏi hàng đợi ưu tiên, hãy bỏ qua một cạnh có đầu kia đã nằm trong cây.
Quên điều này làm trùng công việc và có thể làm hỏng kết quả.

### Sai lầm 4: Dùng MST cho các bài toán đường đi ngắn nhất

MST nối mọi thứ rẻ nhưng **không** cho đường đi ngắn nhất giữa hai nút cụ thể.
Đó là những bài toán khác nhau (MST so với đường ngắn nhất). Đừng nhầm lẫn.

### Sai lầm 5: Coi MST là duy nhất

Tổng trọng số của một MST là duy nhất, nhưng tập cạnh có thể không. Hai tập
cạnh khác nhau có thể đều là MST hợp lệ với cùng trọng số.

---

## 12. Chạy Ví dụ

Chạy:

```text
python MinimumSpanningTree.py
```

Đầu ra ổn định mong đợi:

```text
=== The graph (undirected, weighted) ===
  0 - 1  (w=1)
  1 - 2  (w=3)
  0 - 3  (w=4)
  1 - 4  (w=2)
  2 - 5  (w=1)
  3 - 4  (w=2)
  4 - 5  (w=5)

=== Kruskal's algorithm ===
MST edges: [(0, 1, 1.0), (2, 5, 1.0), (1, 4, 2.0), (3, 4, 2.0), (1, 2, 3.0)]
total weight: 9.0

=== Prim's algorithm ===
MST edges: [(0, 1, 1.0), (1, 4, 2.0), (4, 3, 2.0), (1, 2, 3.0), (2, 5, 1.0)]
total weight: 9.0

=== Which edges were chosen? (1 + 1 + 2 + 2 + 3 = 9) ===
chosen edge set (Kruskal): [(0, 1), (1, 2), (1, 4), (2, 5), (3, 4)]
```

Cả hai thuật toán đều chọn 5 cạnh (một cây trên 6 nút) với cùng tổng trọng số
`9`, và tập cạnh được chọn là giống hệt nhau trong ví dụ này.

---

## 13. Bảng Tóm tắt Cuối cùng

```text
    1. Spanning tree = all nodes, connected, acyclic, V-1 edges.
    2. MST = spanning tree with the minimum total weight.
    3. Many spanning trees exist; the MST total is unique.
    4. Kruskal: sort edges, add cheapest that connects two components.
    5. Kruskal uses Union-Find to test connectivity (O(alpha)).
    6. Prim: grow one component by its cheapest boundary edge.
    7. Prim uses a priority queue, like Dijkstra.
    8. Both greedy; both give the same MST total.
    9. Kruskal O(E log E); Prim O(E log V).
    10. MST connects cheaply; it is NOT shortest paths between nodes.
```

**Bước tiếp theo:** Kruskal phụ thuộc vào Union-Find — đúng chủ đề tiếp theo.
Hiểu nó sẽ hoàn thiện câu chuyện MST.
