
---

# Duyệt Đồ thị DFS/BFS (Graph Structure DFS/BFS Traversal)

## 1. Mục tiêu

Duyệt đồ thị là một sự mở rộng của duyệt cây N-ary. Hai phương pháp chính vẫn
là **tìm kiếm theo chiều sâu (DFS)** và **tìm kiếm theo chiều rộng (BFS)**.

Điểm mới duy nhất là các chu trình: cây không có chu trình, nhưng đồ thị có
thể có. Vì vậy chúng ta cần một mảng `visited` để ngăn quá trình duyệt lặp vô
hạn.

Đồ thị phong phú hơn cây, nên việc duyệt có ba hương vị:

```text
  traverse NODES  -> 1D visited[]   (visit each node once)
  traverse EDGES  -> 2D visited[]   (visit each edge once)
  traverse PATHS  -> onPath[]       (record full node sequences)
```

Nguồn tham khảo:
- https://labuladong.online/en/algo/data-structure-basic/graph-traverse-basic/

---

## 2. Vì sao Chu trình buộc phải có mảng `visited`

Cây không có chu trình, nên một đệ quy đơn giản thăm mọi nút rồi dừng.

```text
  tree:
       1
      / \
     2   3

  traverse(1) -> traverse(2), traverse(3)
  no node is ever reached twice.
```

Một đồ thị có thể vòng lại. Xét chu trình nhỏ nhất, một cạnh hai chiều:

```text
  1 <=> 2
```

Nếu không có rào chắn `visited`, bắt đầu từ `1` bạn đi tới `2`, quay lại `1`,
tới `2`, tới `1`, ... mãi mãi:

```text
  1 -> 2 -> 1 -> 2 -> 1 -> 2 -> ...  (infinite recursion)
```

Mảng `visited` khắc phục điều này. Đánh dấu `1` ở lần đầu tiên bạn thấy nó.
Khi tìm kiếm quay lại `1` qua chu trình, nó thấy `visited[1] == True` và trả
về ngay, dừng vòng lặp.

```text
  with visited:
    1 (mark) -> 2 (mark) -> 1? already visited -> return
                              -> no infinite loop
```

---

## 3. Duyệt Cây so với Duyệt Đồ thị cạnh nhau

Cây N-ary và đồ thị chia sẻ gần như cùng một hình dạng đệ quy. Đồ thị thêm
một dòng: phép kiểm tra `visited`.

```text
  N-ary tree:                        graph:

  traverse(node):                    traverse(node):
      if node == null: return            if node == null: return
      print(node)                        if visited[node]: return   <-- extra
      for child in node.children:        visited[node] = True
          traverse(child)                print(node)
                                         for nb in node.neighbors:
                                             traverse(nb)
```

Trong code (`GraphTraversal.py`) điều này trở thành `dfs_nodes`:

```python
def dfs_nodes(g, start=0):
    order = []
    visited = [False] * g.size()
    def dfs(u):
        if visited[u]:
            return
        visited[u] = True
        order.append(u)          # pre-order position
        for v in g.neighbors(u):
            dfs(v)
    dfs(start)
    return order
```

Vì mảng `visited` cắt bớt các lần thăm lại, mọi nút được thăm một lần và mọi
cạnh được thử một lần, nên độ phức tạp là `O(V + E)`.

### Vì sao lại là `O(V + E)` mà không phải `O(V)`?

Số cạnh của một cây xấp xỉ bằng số nút của nó, nên duyệt cây là `O(N + N) =
O(N)`. Trong đồ thị, bất kỳ hai nút nào cũng có thể được nối, nên số cạnh độc
lập với số nút — do đó là `O(V + E)`.

---

## 4. Duyệt toàn bộ NÚT (`visited`)

Mảng `visited` 1D là đủ khi bạn chỉ quan tâm đến việc thăm mỗi nút một lần,
bất kể thứ tự.

```text
  directed graph:

        0 --> 1 --> 3
        |           ^
        v           |
        2 ----------+

  DFS from 0:  0, 1, 3, 2   (go deep, then backtrack)
  BFS from 0:  0, 1, 2, 3   (visit by distance layer)
```

Phiên bản `dfs_nodes_all` ngoài ra còn khởi động lại tìm kiếm từ mọi nút chưa
thăm, giúp bạn bao phủ **mọi thành phần liên thông** của một đồ thị không liên
thông:

```text
  disconnected graph:           DFS all components:
    0 --- 1       3 --- 4         component {0,1}: 0, 1
        |                         component {3,4}: 3, 4
        2                          result: [0, 1, 3, 4]
```

---

## 5. Duyệt toàn bộ CẠNH (ma trận `visited` 2D)

Đôi khi mục tiêu là dùng mỗi **cạnh** đúng một lần (đây là nền tảng của đường
Euler, bài viết tiếp theo). Với mục tiêu đó, mảng nút 1D là không đủ — bạn
phải ghi lại cạnh nào `u -> v` đã được dùng.

Một mảng 2D `visited[u][v]` theo dõi từng cạnh có hướng:

```python
def dfs_edges(g, start=0):
    order = []
    n = g.size()
    visited = [[False] * n for _ in range(n)]
    def dfs(u):
        for v in g.neighbors(u):
            if visited[u][v]:
                continue
            visited[u][v] = True
            order.append((u, v))   # mark + visit the edge
            dfs(v)
    dfs(start)
    return order
```

Chú ý việc đánh dấu xảy ra **bên trong vòng `for`**, không phải trước nó. Một
cạnh được tạo từ hai nút, nên vị trí pre-order phải nằm nơi một cạnh được chọn.

```text
  0 -> 1 -> 2 -> 0   (a triangle cycle)

  edge traversal:  (0,1), (1,2), (2,0)
```

Chi phí cao hơn: `O(E + V^2)` thời gian và `O(V^2)` không gian vì mảng 2D. Bài
viết tiếp theo (đường Euler) trình bày một cách thông minh hơn tránh mảng 2D.

---

## 6. Duyệt toàn bộ ĐƯỜNG ĐI (`onPath`)

Để liệt kê mọi đường đi đầy đủ từ một nguồn đến một đích, ta cần biết không
chỉ "nút này đã được thăm chưa" mà còn "nút này có đang nằm trên **đường đi
hiện tại** không".

Đó chính là nhiệm vụ của `onPath`:

```text
  mark onPath[u] = True   at the pre-order position (entering u)
  mark onPath[u] = False  at the post-order position (leaving u)
```

```python
def all_paths(g, src, dst):
    result, path = [], []
    on_path = [False] * g.size()
    def dfs(u):
        if u == dst:
            result.append(list(path))
            return
        for v in g.neighbors(u):
            if on_path[v]:
                continue
            path.append(v)
            on_path[v] = True
            dfs(v)
            path.pop()
            on_path[v] = False
    path.append(src)
    on_path[src] = True
    dfs(src)
    return result
```

```text
  DAG:  0 -> 1 -> 3
        |         ^
        2 --------+

  all paths 0 -> 3:
     [0, 1, 3]
     [0, 2, 3]
```

`visited` nói "Tôi đã từng ở đây rồi, đừng làm lại." `onPath` nói "Tôi đang ở
đây **ngay bây giờ** trên nhánh này — đừng vòng trở lại tôi." Sự khác biệt là
việc bỏ đánh dấu ở post-order.

---

## 7. Dùng CẢ `visited` và `onPath`: Phát hiện Chu trình

Khi bạn muốn phát hiện một chu trình trong đồ thị **có hướng**, bạn kết hợp cả
hai mảng.

* `visited[u]`  -> nút `u` đã được khám phá xong trước đó.
* `onPath[u]`   -> nút `u` đang nằm trên ngăn xếp đệ quy hiện tại.

Nếu trong DFS bạn chạm tới một nút `v` đã nằm trên đường đi hiện tại, bạn đã
tìm thấy một **cạnh quay lui** (back edge), nghĩa là có một chu trình.

```text
  directed cycle:                directed graph, no cycle:

       0                           0 -> 1 -> 2
      / \                          ^         |
     1<--2                         +---------+  (2 cannot reach 0)

  at node 2, neighbor 0 is
  onPath -> cycle detected!        at node 2, neighbor 0 is
                                   visited but NOT onPath -> no cycle
```

```python
def has_cycle(g):
    visited = [False] * g.size()
    on_path = [False] * g.size()
    cyc = [False]
    def dfs(u):
        visited[u] = True
        on_path[u] = True
        for v in g.neighbors(u):
            if on_path[v]:
                cyc[0] = True
            if not visited[v]:
                dfs(v)
        on_path[u] = False
    for s in range(g.size()):
        if not visited[s]:
            dfs(s)
    return cyc[0]
```

Hai mảng trả lời những câu hỏi khác nhau:

```text
  visited[u]  -> "was u ever processed?"
  onPath[u]   -> "is u on the path I am currently walking?"

  both True   -> a back edge exists -> a cycle exists.
```

---

## 8. BFS: Duyệt Theo Tầng của một Đồ thị

BFS thăm các nút theo **tầng khoảng cách** dùng một hàng đợi — giống hệt duyệt
theo tầng của một cây N-ary.

```text
        0
       / \
      1   2
     /     \
    3       4

  BFS layers:  [0], [1, 2], [3, 4]
  (a node is reached from its neighbors at the same "depth")
```

```python
def bfs_levels(g, start=0):
    n = g.size()
    visited = [False] * n
    dist = [-1] * n
    q = deque([start])
    visited[start] = True
    dist[start] = 0
    while q:
        u = q.popleft()
        for v in g.neighbors(u):
            if not visited[v]:
                visited[v] = True
                dist[v] = dist[u] + 1
                q.append(v)
    return [[i for i in range(n) if dist[i] == d]
            for d in range(max(dist) + 1)]
```

BFS quan trọng vì, trong một đồ thị **không trọng số**, lần đầu tiên BFS chạm
tới một nút, nó đã tìm ra **đường đi ngắn nhất** tới nút đó. Đó là hạt giống
của các thuật toán đường đi ngắn nhất trong một bài viết sau.

---

## 9. BFS Đường đi Ngắn nhất trong Đồ thị Không trọng số

Ghi lại tiền nhiệm của mỗi nút. Khi bạn chạm tới đích, đi ngược chuỗi tiền
nhiệm để dựng lại đường đi.

```text
  search from 0 to 3:

        0 -> 1 -> 3
        |         ^
        2 --------+

  first time BFS reaches 3, it came via 1 (prev[3] = 1)
  first time BFS reaches 1, it came via 0 (prev[1] = 0)
  reconstruct:  3 -> 1 -> 0, reversed -> [0, 1, 3]
```

```python
def bfs_shortest_path(g, src, dst):
    if src == dst:
        return [src]
    prev = {}
    visited = [False] * g.size()
    q = deque([src])
    visited[src] = True
    while q:
        u = q.popleft()
        for v in g.neighbors(u):
            if not visited[v]:
                visited[v] = True
                prev[v] = u
                if v == dst:
                    q.clear()
                    break
                q.append(v)
    if dst not in prev:
        return None
    path = []
    cur = dst
    while cur != src:
        path.append(cur)
        cur = prev[cur]
    path.append(src)
    path.reverse()
    return path
```

Đảm bảo này chỉ đúng với đồ thị **không trọng số** (mọi cạnh có cùng chi phí,
thường là `1`). Đồ thị có trọng số cần thuật toán Dijkstra (một bài viết sau).

---

## 10. DFS so với BFS: Dùng khi nào?

```text
                   DFS                    BFS
  data structure   stack (recursion)      queue
  path style       goes deep first        goes wide first
  use for          all paths, cycles,     shortest path (unweighted),
                   connectivity,          level/distance layers,
                   topological order      finding nearest target
  memory           O(depth)               O(width of frontier)
```

```text
  directed graph:         DFS:  0, 1, 3, 2     BFS:  0, 1, 2, 3
        0 --> 1 --> 3
        |           ^
        v           |
        2 ----------+

  DFS dives 0 -> 1 -> 3 before looking at 2.
  BFS fans out 0 -> {1, 2} before descending to 3.
```

---

## 11. Ba Hương vị trong nháy mắt

| Mục tiêu | Mảng | Đánh dấu tại | Bỏ đánh dấu | Ví dụ dùng |
|:---|:---|:---|:---|:---|
| Thăm mỗi nút một lần | `visited` 1D | pre-order | không | khả năng chạm tới, liên thông |
| Dùng mỗi cạnh một lần | `visited` 2D | trong vòng lặp | không | đường Euler |
| Liệt kê mọi đường đi | `onPath` | pre-order | post-order | liệt kê đường |
| Phát hiện chu trình có hướng | `visited` + `onPath` | pre-order | post-order | kiểm tra phụ thuộc |

```text
  summary of the three markers:

  1D visited[u]       -> this node, never again
  2D visited[u][v]    -> this edge, never again
  onPath[u]           -> this node, on the current branch only
```

---

## 12. Độ phức tạp

| Duyệt | Thời gian | Không gian | Ghi chú |
|:---|:---:|:---:|:---|
| Nút (DFS/BFS) | `O(V + E)` | `O(V)` | mỗi nút thăm một lần |
| Cạnh (visited 2D) | `O(E + V^2)` | `O(V^2)` | cấp phát mảng 2D |
| Mọi đường đi | `O(2^V)` worst | `O(V)` | kích thước đầu ra mũ |
| Phát hiện chu trình | `O(V + E)` | `O(V)` | visited + onPath |

Duyệt mọi đường đi có thể là hàm mũ vì chính số lượng đường đi tăng theo hàm
mũ — đó là bản chất của đầu ra, không phải lỗi của thuật toán.

---

## 13. Những Sai lầm Thường gặp

### Sai lầm 1: Quên `visited` trong đồ thị có chu trình

Không có nó, DFS đệ quy vô hạn quanh mọi chu trình. Luôn rào chắn bằng mảng
nút khi duyệt nút.

### Sai lầm 2: Đánh dấu cạnh bên ngoài vòng lặp

Với duyệt cạnh, việc đánh dấu pre-order phải nằm bên trong vòng `for` (một cạnh
được chọn theo từng lân cận), không phải trước vòng lặp.

### Sai lầm 3: Dùng `visited` nơi cần `onPath`

Để liệt kê các đường đi riêng biệt, `visited` sai lầm khi cấm thăm lại những
nút xuất hiện trên các nhánh khác nhau. Dùng `onPath` để một nút có thể xuất
hiện trên nhiều đường miễn là nó không nằm trên đường hiện tại.

### Sai lầm 4: Quên bỏ đánh dấu ở post-order

`onPath[u] = False` ở vị trí post-order là thứ cho phép quay lui. Quên nó, và
tìm kiếm sẽ chặn những nhánh hợp lệ.

### Sai lầm 5: Coi BFS là đường ngắn nhất trên đồ thị có trọng số

BFS chỉ cho đường ngắn nhất khi mọi cạnh có cùng chi phí. Đồ thị có trọng số
cần Dijkstra / Bellman-Ford (các bài viết sau).

---

## 14. Chạy Ví dụ

Chạy:

```text
python GraphTraversal.py
```

Đầu ra ổn định mong đợi:

```text
=== 1. DFS over all nodes (visited array) ===
cyclic graph, from 0: [0, 1, 2, 3]
cyclic graph, all components: [0, 1, 2, 3]

=== 2. DFS over all edges (2D visited array) ===
cyclic graph edges: [(0, 1), (1, 2), (2, 0), (1, 3)]

=== 3. Traverse all paths (onPath array) ===
DAG paths 0 -> 3: [[0, 1, 3], [0, 2, 3]]

=== 4. visited + onPath => cycle detection ===
cyclic graph has cycle: True
DAG has cycle: False

=== 5. BFS styles ===
BFS levels from 0 (cyclic): [[0], [1], [2, 3]]
BFS shortest path 0 -> 3 (DAG): [0, 1, 3]
visit order BFS: [0, 1, 2, 3] | DFS: [0, 1, 3, 2]
```

---

## 15. Bảng Tóm tắt Cuối cùng

```text
    1. Graph traversal = tree traversal + a guard against cycles.
    2. NODES: 1D visited[] marks each node once.
    3. EDGES: 2D visited[u][v] marks each directed edge once (inside loop).
    4. PATHS: onPath[] marks pre-order and unmarks post-order.
    5. visited  = "was processed before".
    6. onPath   = "is on the current branch".
    7. visited + onPath detect directed cycles (back edge).
    8. BFS = level-order with a queue; shortest path on unweighted graphs.
    9. DFS = deep-first with a stack; paths, cycles, connectivity.
    10. Node/edge traversal is O(V+E); all-paths can be exponential.
```

**Bước tiếp theo:** Dùng ý tưởng duyệt cạnh từ bài viết này để tìm đường Euler
— chủ đề của bài viết tiếp theo.
