
---

# Các Thuật toán Đường đi Ngắn nhất trong Đồ thị (Graph Shortest Path Algorithms)

## 1. Mục tiêu

Tìm đường đi ngắn nhất (rẻ nhất, nhanh nhất) giữa các điểm trong một mạng là
một trong những bài toán hữu ích nhất trong tính toán. Nó hỗ trợ định vị GPS,
định tuyến mạng và lập lịch tác vụ.

Bài viết này bao quát bốn thuật toán đường đi ngắn nhất kinh điển và, quan
trọng hơn, **từng thuật toán thuộc về đâu** — vì chọn sai thuật toán sẽ phá hỏng
câu trả lời của bạn.

Nguồn tham khảo:
- https://labuladong.online/en/algo/data-structure-basic/graph-shortest-path/

---

## 2. Vì sao Đường đi Ngắn nhất ra đời

Các cạnh của một đồ thị có thể mang một **trọng số** — một chi phí, khoảng
cách, hoặc thời gian. Bài toán đường đi ngắn nhất hỏi: tổng trọng số tối thiểu
cần thiết để đi từ một nút này tới một nút khác là bao nhiêu?

```text
         2
  A ----------- B
  | \          /|
  |  \ 1      / |
  |   \      /  |
  |    1    1   |
  |      \  /   |
  |       C     1
  |             |
  D ----------- E
        1

  shortest A -> E?
  direct:  A-B-E = 2+1 = 3
  via C:   A-C-E = 1+1 = 2   <-- shortest
```

Nếu không có thuật toán có hệ thống, bạn sẽ phải liệt kê mọi đường đi — và có
vô số đường (theo hàm mũ). Các thuật toán đường đi ngắn nhất ra đời để tìm giá
trị tối thiểu mà không cần liệt kê hết chúng.

---

## 3. Hai Loại Bài toán Đường đi Ngắn nhất

| Loại | Hỏi | Đầu ra |
|:---|:---|:---|
| **Một nguồn** | đường ngắn nhất từ một điểm bắt đầu tới mọi nút khác | mảng 1D `distTo` |
| **Mọi cặp** | đường ngắn nhất giữa mọi cặp nút | mảng 2D `dist` |

Ngoài ra còn có biến thể **điểm-tới-điểm**: chỉ từ `src` tới một `dst`. Nó
thường được giải bằng cách dừng sớm một thuật toán một nguồn, hoặc bằng A*.

```text
  single-source:   distTo[i] = shortest from src to i
                   distTo = [0, 1, 3, 4]

  all-pairs:       dist[i][j] = shortest from i to j (a V x V matrix)
```

Đầu ra một nguồn `distTo` cùng ý tưởng với các tầng `visited` trong BFS — nhưng
giờ các "tầng" có trọng số, nên một hàng đợi đơn thuần là không đủ.

---

## 4. Bốn Thuật toán trong nháy mắt

| Thuật toán | Loại | Trọng số âm? | Ý tưởng |
|:---|:---|:---:|:---|
| Dijkstra | một nguồn | không | BFS + tham lam + hàng đợi ưu tiên |
| A* | điểm-tới-điểm | không | Dijkstra + hàm heuristic |
| Bellman-Ford / SPFA | một nguồn | có | nới lỏng mọi cạnh lặp lại |
| Floyd-Warshall | mọi cặp | có | quy hoạch động |

```text
  the family tree:

  BFS (unweighted)      --->  Dijkstra (weighted, greedy)
                              |--> A* (adds a heuristic)
  BFS / relaxation      --->  Bellman-Ford / SPFA (negative ok)
  dynamic programming   --->  Floyd-Warshall (all pairs)
```

Mỗi thuật toán là một mở rộng nhỏ của một ý tưởng bạn đã biết (BFS hoặc DP).
Không cái nào là phép màu cả.

---

## 5. Vấn đề Trọng số Âm (Vì sao một số Thuật toán Từ chối)

Dijkstra (và A*) giả định một tính chất then chốt: **khi bạn thêm nhiều cạnh
hơn, tổng trọng số không bao giờ giảm** — tức là không có cạnh âm.

Vì sao? Xét một nguồn `s` có hai lân cận `a` và `b`:

```text
  s -> a : 3
  s -> b : 4

  if all weights are non-negative, the shortest path to a is s -> a (cost 3).
  any route s -> b ... -> a costs at least 4 > 3, so it cannot beat 3.
```

Nhưng nếu có một cạnh âm, suy luận đó sụp đổ:

```text
  s -> a : 3
  s -> b : 4
  b -> a : -10

  path s -> b -> a = 4 + (-10) = -6  <  3   (beats the direct edge!)
```

Tham lam "cam kết khoảng cách nhỏ nhất đã chốt" của Dijkstra hỏng: nó đã khóa
`s -> a = 3` trước khi phát hiện lộ trình rẻ hơn `-6`.

Và nếu có một **chu trình âm** (các trọng số cộng lại thành giá trị âm trong
một vòng lặp), đường đi ngắn nhất không xác định — bạn có thể lặp mãi và tổng
cứ giảm:

```text
  0 -> 1 : 1
  1 -> 0 : -3        cycle total = 1 + (-3) = -2 < 0

  loop 0->1->0->1->0...  total -> -infinity
  -> the shortest path is meaningless
```

Vậy nên: Dijkstra và A* không xử lý được cạnh âm. Bellman-Ford/SPFA và Floyd
xử lý được, và Bellman-Ford được dùng cụ thể để **phát hiện chu trình âm**.

---

## 6. Dijkstra: BFS + Tham lam + Hàng đợi Ưu tiên

Dijkstra là BFS với hai nâng cấp:

1. Một **hàng đợi ưu tiên** (min-heap) thay vì hàng đợi đơn thuần, sắp theo
   khoảng cách hiện tại, để nút gần nhất chưa chốt luôn được xử lý trước.
2. **Nới lỏng (relaxation)**: khi ta tìm ra lộ trình ngắn hơn tới một nút, ta
   cập nhật khoảng cách của nó và đẩy lại vào hàng đợi.

```text
  Dijkstra on:

         2
   0 ---------> 2
   |          / |
   | 1      1/  |
   |        /   |
   1 ------>3    4
        1

  dist = [0, inf, inf, inf, inf]
  pop 0: relax 1 (1), 2 (2)     -> dist [0, 1, 2, inf, inf]
  pop 1: relax 3 (2)            -> dist [0, 1, 2, 2, inf]
  pop 2: relax 3 (2+1=3, no)    -> unchanged
  pop 3: relax 4 (3)            -> dist [0, 1, 2, 2, 3]
```

```python
def dijkstra(g, src):
    n = g.size()
    dist = [float("inf")] * n
    prev = [-1] * n
    dist[src] = 0.0
    pq = [(0.0, src)]
    visited = [False] * n
    while pq:
        d, u = heapq.heappop(pq)
        if visited[u]:
            continue
        visited[u] = True
        for v, w in g.neighbors(u):
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(pq, (nd, v))
    return dist, prev
```

Vì sao nó đúng: lựa chọn tham lam an toàn **chỉ vì** không có cạnh âm. Một khi
một nút được pop (đã chốt), khoảng cách của nó là cuối cùng. Đó chính xác là
tính chất mà trọng số âm phá hủy.

Độ phức tạp: `O(E log V)` với binary heap.

---

## 7. A*: Dijkstra Chỉ về một Đích

A* giải bài toán **điểm-tới-điểm** (một `src`, một `dst`). Nó là Dijkstra cộng
một **heuristic** — một ước lượng `h(node)` về việc `node` cách đích bao xa.

```text
  Dijkstra explores in all directions:

         o  o  o  o  o
         o  o  o  o  o
         o  o  S  o  o      expands a full circle
         o  o  o  o  o
         o  o  o  o  o

  A* biases the search toward the target:

         o  o  o  o  o
         o  o  o  o  o
         o  o  S  .  .      . = preferred direction (small h)
         o  o  o  o  .
         o  o  o  o  T
```

Ưu tiên của một nút trở thành `g(node) + h(node)`:

* `g(node)` = khoảng cách thực đã tìm thấy tới giờ (từ Dijkstra).
* `h(node)` = ước lượng heuristic của khoảng cách còn lại tới đích.

```python
def a_star(g, src, dst, heuristic):
    dist = [float("inf")] * g.size()
    prev = [-1] * g.size()
    dist[src] = 0.0
    pq = [(0.0 + heuristic[src], 0.0, src)]   # (g + h, g, node)
    while pq:
        _, d, u = heapq.heappop(pq)
        if u == dst:
            return dist[dst], reconstruct(prev, dst)
        for v, w in g.neighbors(u):
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(pq, (nd + heuristic[v], nd, v))
    return None, []
```

Để đúng, heuristic phải **chấp nhận được** (admissible — không bao giờ ước
lượng quá khoảng cách thực; ví dụ khoảng cách đường thẳng). Khi đó A* được đảm
bảo tìm ra đường ngắn nhất thực sự, và một `h` chọn khéo khiến nó chạm đích
nhanh hơn Dijkstra.

Nhưng heuristic là một phỏng đoán. Nếu nó tệ, A* có thể đi vòng và chậm hơn
Dijkstra thường. Đó là sự đánh đổi của tìm kiếm heuristic.

---

## 8. Bellman-Ford: Nới lỏng Mọi thứ, `V-1` Lần

Bellman-Ford xử lý **cạnh âm**. Ý tưởng đẹp đến giản dị: lặp lại việc nới lỏng
**mọi cạnh**; mỗi lượt đầy đủ đảm bảo ít nhất một khoảng cách ngắn nhất nữa trở
thành cuối cùng, và sau `V-1` lượt thì tất cả đều cuối cùng.

```text
  a shortest path uses at most V-1 edges
  (a path with V edges would repeat a node -> could remove the loop)

  so relaxing every edge V-1 times is enough
```

```python
def bellman_ford(g, src):
    n = g.size()
    dist = [float("inf")] * n
    prev = [-1] * n
    dist[src] = 0.0
    edges = [(u, v, w) for u in range(n) for v, w in g.neighbors(u)]
    for _ in range(n - 1):
        updated = False
        for u, v, w in edges:
            if dist[u] != inf and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                prev[v] = u
                updated = True
        if not updated:
            break
    # one more pass detects negative cycles
    for u, v, w in edges:
        if dist[u] != inf and dist[u] + w < dist[v]:
            return None, []          # negative cycle reachable
    return dist, prev
```

**SPFA** là phiên bản dùng hàng đợi: thay vì quét mọi cạnh mỗi lượt, nó chỉ
xử lý lại một nút khi khoảng cách của nó thực sự được cải thiện, đẩy nó vào một
hàng đợi. Nó là "BFS + nới lỏng".

```text
  Bellman-Ford:       for each pass: relax ALL edges     O(V*E)
  SPFA:               only relax nodes whose distance changed   often faster
```

Cả hai phát hiện chu trình âm bằng cách nhận thấy một khoảng cách cứ cải thiện
mãi dù đã qua `V-1` lượt.

Độ phức tạp: Bellman-Ford `O(V * E)`; SPFA là `O(V*E)` trong trường hợp xấu
nhất nhưng thường nhanh hơn nhiều trong thực tế.

---

## 9. Floyd-Warshall: Mọi Cặp qua Quy hoạch Động

Floyd-Warshall tính đường đi ngắn nhất giữa **mọi cặp** nút. Nó là một thuật
toán quy hoạch động.

Ý tưởng then chốt: `dist[k][i][j]` = đường đi ngắn nhất từ `i` tới `j` chỉ dùng
các nút trung gian `0..k`. Ta tăng `k` từ `0` tới `n-1`:

```text
  the DP recurrence:

  dist[i][j] = min( dist[i][j],            # not going through k
                    dist[i][k] + dist[k][j] )   # going through k
```

```python
def floyd_warshall(g):
    n = g.size()
    dist = [[float("inf")] * n for _ in range(n)]
    for u in range(n):
        dist[u][u] = 0.0
    for u in range(n):
        for v, w in g.neighbors(u):
            dist[u][v] = min(dist[u][v], w)
    for k in range(n):          # allow node k as an intermediate
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist
```

```text
  before allowing k:                after allowing k:

     i -----> j  (cost 8)              i --k--> j  (cost 3+4 = 7)
                                        ^
                                        |  better, so dist[i][j] = 7
```

Ba vòng lặp lồng nhau khiến nó là `O(V^3)`. Nó là lựa chọn đúng khi đồ thị dày
đặc hoặc bạn thực sự cần mọi cặp. Với một nguồn duy nhất trên đồ thị thưa lớn,
chạy Dijkstra từ mọi nút thường nhanh hơn.

---

## 10. Chọn Thuật toán Đúng

```text
  need only one source?
    yes -> negative edges?
             no  -> Dijkstra          (fastest, O(E log V))
             yes -> Bellman-Ford/SPFA (O(V*E))
  need point-to-point (src -> dst)?
    yes -> Dijkstra (early stop) or A* (with a good heuristic)
  need all pairs?
    yes -> Floyd-Warshall (O(V^3)) or
           run Dijkstra from every node on sparse graphs
  need to detect negative cycles?
    yes -> Bellman-Ford / SPFA
```

```text
  algorithm     negative ok?   single/all/p2p      time
  ----------    ------------   -----------------   ----------
  Dijkstra      no             single / p2p        O(E log V)
  A*            no             p2p                 depends on heuristic
  Bellman-Ford  yes            single              O(V*E)
  SPFA          yes            single              O(V*E) worst
  Floyd         yes            all                 O(V^3)
```

---

## 11. Tóm tắt Độ phức tạp

| Thuật toán | Thời gian | Không gian | Trọng số âm | Loại |
|:---|:---:|:---:|:---:|:---|
| Dijkstra | `O(E log V)` | `O(V + E)` | không | một nguồn |
| A* | biến thiên (heuristic) | `O(V + E)` | không | điểm-tới-điểm |
| Bellman-Ford | `O(V * E)` | `O(V)` | có | một nguồn |
| SPFA | `O(V * E)` worst | `O(V)` | có | một nguồn |
| Floyd-Warshall | `O(V^3)` | `O(V^2)` | có | mọi cặp |

Trong đó `V` = nút, `E` = cạnh.

---

## 12. Những Sai lầm Thường gặp

### Sai lầm 1: Dùng Dijkstra với trọng số âm

Dijkstra khóa khoảng cách một cách tham lam; một cạnh âm xuất hiện sau có thể
khiến một nút đã chốt trở nên sai. Dùng Bellman-Ford/SPFA khi có cạnh âm.

### Sai lầm 2: Quên chu trình âm

Với một chu trình âm, đường đi ngắn nhất không xác định (tiến tới âm vô cùng).
Luôn kiểm tra nó khi đồ thị có thể chứa cạnh âm.

### Sai lầm 3: Dùng A* với heuristic không chấp nhận được

Nếu `h` ước lượng quá khoảng cách thực, A* có thể trả về một đường không tối
ưu. Heuristic phải không bao giờ ước lượng quá (chấp nhận được) để đảm bảo
đúng.

### Sai lầm 4: Dùng BFS/hàng đợi thường cho đồ thị có trọng số

BFS chỉ cho đường ngắn nhất khi mọi cạnh có cùng chi phí. Với trọng số, bạn
cần một hàng đợi ưu tiên (Dijkstra) — một hàng đợi thường xử lý theo thứ tự
đến, không theo thứ tự chi phí.

### Sai lầm 5: Chạy Floyd trên đồ thị thưa khổng lồ

`O(V^3)` rất nặng với đồ thị lớn. Nếu bạn chỉ cần một nguồn, hoặc đồ thị thưa,
hãy ưu tiên Dijkstra (hoặc Dijkstra cho từng nguồn) hơn Floyd.

---

## 13. Chạy Ví dụ

Chạy:

```text
python ShortestPath.py
```

Đầu ra ổn định mong đợi:

```text
=== Graph for shortest paths (directed, weighted) ===
edges:
  0 -> 1  (w=1)
  0 -> 2  (w=4)
  1 -> 2  (w=2)
  2 -> 3  (w=1)

=== Dijkstra (single-source, no negative weights) ===
dist to 0..3: [0.0, 1.0, 3.0, 4.0]
path to 3: [0, 1, 2, 3]

=== A* (point-to-point, with a heuristic) ===
A* dist to 3: 4.0 | path: [0, 1, 2, 3]

=== Bellman-Ford & SPFA (negative weights OK) ===
Bellman-Ford dist: [0.0, 1.0, -1.0, 0.0] | path to 3: [0, 1, 2, 3]
SPFA dist: [0.0, 1.0, -1.0, 0.0] | path to 3: [0, 1, 2, 3]

=== Negative cycle detection ===
Bellman-Ford detects negative cycle: True
SPFA detects negative cycle: True

=== Floyd-Warshall (all-pairs) ===
dist matrix:
      0     1     2     3
  0    0.0    1.0    3.0    4.0
  1    inf    0.0    2.0    3.0
  2    inf    inf    0.0    1.0
  3    inf    inf    inf    0.0
```

Chú ý `dist = [0.0, 1.0, 3.0, 4.0]` của Dijkstra — nút 2 được chạm tới qua 1
(1+2=3) thay vì trực tiếp (4).

---

## 14. Bảng Tóm tắt Cuối cùng

```text
    1. Edge weight = cost; shortest path = min total weight.
    2. Single-source -> distTo[]; all-pairs -> dist[][] matrix.
    3. Dijkstra = BFS + greedy + priority queue. No negative edges.
    4. A* = Dijkstra + heuristic, for point-to-point. h must be admissible.
    5. Bellman-Ford relaxes all edges V-1 times. Handles negatives.
    6. SPFA = queue-based Bellman-Ford, usually faster in practice.
    7. Floyd = DP over intermediate nodes k. All-pairs, O(V^3).
    8. Negative cycle -> shortest path undefined -> detect & reject.
    9. Dijkstra cannot handle negatives; Bellman-Ford/SPFA/Floyd can.
    10. Choose by: source count, negative edges, graph density.
```

**Bước tiếp theo:** Đường đi ngắn nhất nối các nút; bài viết tiếp theo nối **tất
cả các nút với chi phí rẻ nhất có thể** — Cây khung Nhỏ nhất (Minimum Spanning
Tree).
