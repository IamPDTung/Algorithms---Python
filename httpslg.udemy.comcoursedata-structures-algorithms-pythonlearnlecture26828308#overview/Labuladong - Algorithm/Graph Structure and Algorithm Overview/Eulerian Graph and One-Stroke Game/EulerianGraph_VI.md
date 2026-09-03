
---

# Đồ thị Euler và Trò chơi Vẽ một Nét (Eulerian Graph and One-Stroke Game)

## 1. Mục tiêu

Trò chơi "vẽ một nét" thực chất là một bài toán đồ thị: bạn có thể vẽ mọi cạnh
của một hình đúng một lần, trong một nét liên tục duy nhất, không nhấc bút
không? Bạn có thể đi qua các đỉnh nhiều lần, nhưng mỗi cạnh phải được dùng đúng
một lần.

Bài viết này giải thích lý thuyết đằng sau câu đố đó — **đường đi Euler và
chu trình Euler** — bài toán Bảy cây cầu Königsberg nổi tiếng, quy tắc bậc đơn
giản cho biết lời giải có tồn tại hay không, và thuật toán Hierholzer để thực
sự tìm ra hành trình.

Nguồn tham khảo:
- https://labuladong.online/en/algo/data-structure-basic/eulerian-graph/

---

## 2. Vì sao Đồ thị Euler ra đời

Câu chuyện bắt đầu từ Königsberg thế kỷ 18. Một con sông chia thành phố thành
bờ bắc, bờ nam và hai hòn đảo. Bảy cây cầu nối bốn vùng này.

```text
        north bank
          |  |  |
        +-+  |  +-+
        | island1   island2 |
        +-+  |  +-+
          |  |  |
        south bank

   four regions, seven bridges
```

Câu hỏi làm người dân bối rối: **bạn có thể thiết kế một lộ trình băng qua mỗi
cây cầu đúng một lần và quay về điểm xuất phát không?**

Euler biến nó thành một bài toán đồ thị. Mỗi vùng là một nút; mỗi cây cầu là
một cạnh.

```text
        N
       /|\
      / | \
     I1  |  I2
      \  |  /
       \ | /
        S

   N = north bank, S = south bank
   I1 = island 1, I2 = island 2
   edges = the seven bridges
```

Euler chứng minh lộ trình là không thể. Làm vậy, ông đã khai sinh ra cả một
nhánh của lý thuyết đồ thị. Đó là lý do đồ thị Euler ra đời: để trả lời "tôi có
thể đi qua mọi liên kết đúng một lần không?" — một câu hỏi nằm sau lập tuyến
đường, thiết kế mạch và các câu đố.

---

## 3. Thuật ngữ

| Thuật ngữ | Định nghĩa |
|:---|:---|
| **Bậc (degree)** | Số cạnh chạm vào một nút. Trong hình dưới, nút `A` có bậc 3. |
| **Đường đi Euler** | Một lộ trình dùng mọi cạnh đúng một lần (có thể bắt đầu và kết thúc ở các nút khác nhau). |
| **Chu trình Euler** | Một đường đi Euler bắt đầu và kết thúc ở **cùng** một nút. |
| **Đồ thị Euler** | Một đồ thị có chu trình Euler. |

```text
  degree of a node = number of edges at it

        B
        |
        |
  A ----+---- C        A has degree 3 (edges AB, AC, AD)
        |              B has degree 1
        |
        D
```

Trò chơi vẽ một nét yêu cầu một **đường đi Euler** (việc bút kết thúc ở một nơi
khác điểm bắt đầu là chấp nhận được). Nếu bạn phải quay về điểm bắt đầu, bạn cần
một **chu trình Euler**.

---

## 4. Trò chơi Vẽ một Nét

Quy tắc của trò chơi:

```text
  1. Draw every edge in one continuous stroke.
  2. You may pass through vertices multiple times.
  3. Each edge must be traversed exactly once.
  4. Never lift the pen.
```

Có một mẹo đơn giản để biết một hình có vẽ được hay không — chỉ cần nhìn vào
**bậc** của các đỉnh:

```text
  all nodes even degree  ->  Eulerian circuit exists.
                            Start anywhere, end where you started.

  exactly two odd nodes  ->  Eulerian path exists.
                            Start at one odd node, end at the other.

  otherwise              ->  impossible.
```

```text
  drawable (2 odd nodes)          not drawable (4 odd nodes)

        A                                  A
       / \                                /|\
      /   \                              / | \
     B-----C                            B  |  C
            \                            \ | /
             D                            \|/
              (B and D odd)                D
       start at B, end at D        all four degrees odd -> impossible
```

---

## 5. Bài toán Bảy cây cầu: Vì sao Không có Lời giải

Mô hình Königsberg thành một đồ thị và đếm bậc của mọi nút.

```text
  N (north):  3 bridges   -> degree 3  (odd)
  S (south):  3 bridges   -> degree 3  (odd)
  I1 (island1): 3 bridges -> degree 3  (odd)
  I2 (island2): 5 bridges -> degree 5  (odd)
```

Mọi nút đều có bậc lẻ. Nghĩa là có **bốn** nút lẻ, vi phạm cả hai quy tắc trên
(chúng ta cần 0 hoặc đúng 2). Vậy nên:

```text
  all four degrees are odd
  -> not 0, not exactly 2
  -> no Eulerian circuit, no Eulerian path
  -> the puzzle is impossible
```

Đây chính xác là điều Euler đã chứng minh năm 1736. Đây là kết quả thực sự đầu
tiên của lý thuyết đồ thị.

Bản demo Python tái hiện điều đó:

```python
koenigsberg = UndirectedGraph(4, [
    (0, 1), (0, 1), (0, 2), (0, 2),   # bridges touching region 0
    (0, 3), (1, 3), (2, 3),
])
koenigsberg.degrees()          # [5, 3, 3, 3]  -> four odd nodes
has_eulerian_path(koenigsberg) # (False, [0, 1, 2, 3]) -> impossible
```

---

## 6. Quy tắc Bậc (Đồ thị Không hướng)

Một đồ thị không hướng là liên thông (mọi nút không cô lập đều chạm tới được)
và:

| Điều kiện | Kết quả | Nút bắt đầu |
|:---|:---|:---|
| Mọi bậc đều chẵn | Chu trình Euler tồn tại | bất kỳ đâu |
| Đúng 2 bậc lẻ | Đường đi Euler tồn tại | một trong hai nút lẻ |
| Nhiều hơn 2 nút lẻ | không tồn tại cái nào | bất khả thi |

Code cài đặt chính xác quy tắc đó:

```python
def has_eulerian_circuit(g):
    if not is_connected(g):
        return False
    return all(d % 2 == 0 for d in g.degrees())


def has_eulerian_path(g):
    if not is_connected(g):
        return False, []
    odd = [i for i, d in enumerate(g.degrees()) if d % 2 == 1]
    if len(odd) == 0:
        return True, []          # circuit: start anywhere
    if len(odd) == 2:
        return True, odd         # path: start at one odd node
    return False, odd            # impossible
```

Vì sao quy tắc này đúng:

* Mỗi lần một lộ trình đi **qua** một nút, nó dùng hai cạnh (một vào, một ra).
  Nên trong một lộ trình khép kín, các cạnh đã dùng tại mỗi nút ghép thành cặp
  — mọi bậc phải là chẵn.
* Một đường đi **hở** có hai điểm đầu mút, mỗi đầu dùng một cạnh không ghép
  cặp, nên đúng hai nút có thể có bậc lẻ.
* Ba hoặc nhiều nút lẻ không thể ghép thành một lộ trình liên tục duy nhất.

```text
  route through a node:  ------->  (node)  ------->
                          one in    one out    = 2 edges, an even contribution

  a circuit is a closed loop of these even contributions
  -> every node must have even degree
```

---

## 7. Tìm Hành trình: Thuật toán Hierholzer

Biết một hành trình tồn tại mới là nửa câu chuyện. **Thuật toán Hierholzer**
thực sự dựng nó, và nó là một mở rộng thông minh của phép duyệt cạnh DFS ở bài
viết trước.

Mẹo then chốt: thay vì mảng `visited` 2D, nó **xóa mỗi cạnh khi dùng xong**.
Điều đó tránh bộ nhớ `O(V^2)` và giữ mọi thứ đơn giản.

```python
def hierholzer_undirected(g, start=None):
    adj = [deque(sorted(g.neighbors(u))) for u in range(g.size())]
    if start is None:
        start = next((i for i, d in enumerate(g.degrees()) if d % 2 == 1),
                     next((i for i in range(g.size()) if g.degree(i) > 0), 0))
    stack, path = [start], []
    while stack:
        u = stack[-1]
        if adj[u]:
            v = adj[u].popleft()          # use edge u->v
            # remove the reverse half-edge (undirected)
            rev = adj[v]
            for idx, x in enumerate(rev):
                if x == u:
                    del rev[idx]
                    break
            stack.append(v)
        else:
            path.append(stack.pop())      # no edges left -> emit node
    path.reverse()
    return path
```

Nó hoạt động theo hai pha dù chúng đan xen trong vòng lặp:

```text
  Phase 1 (go deep):  follow unused edges, pushing nodes onto the stack.
  Phase 2 (backtrack): when a node runs out of edges, pop it into the path.
  Finally reverse the path.
```

Một ví dụ chạy tay trên chu trình 4 cạnh `0-1-2-3-0`:

```text
  stack: [0] -> push 1 -> push 2 -> push 3 -> push 0 (back to start)
  0 now has no unused edges, pop 0 -> path [0]
  3 -> path [0,3]
  2 -> path [0,3,2]
  1 -> path [0,3,2,1]
  0 -> path [0,3,2,1,0]
  reverse -> [0, 1, 2, 3, 0]   (an Eulerian circuit!)
```

---

## 8. Vì sao Xóa Cạnh Thay thế Mảng `visited` 2D

Nhớ lại từ bài duyệt rằng duyệt cạnh dùng mảng 2D `visited[u][v]`. Hierholzer
tránh nó hoàn toàn:

```text
  2D visited array:                  delete-on-use:

  visited[u][v] = True               adj[u].popleft()  removes the edge
  checks "have I used u->v?"         next time, the edge simply is not there

  memory O(V^2)                      memory O(E)
```

Xóa cạnh khỏi danh sách kề tương đương với việc đánh dấu nó đã thăm, nhưng
không tốn mảng 2D phụ. Đây là lý do Hierholzer là cách chuẩn, hiệu quả để tìm
đường Euler.

---

## 9. Đồ thị Có hướng: Chuỗi Từ và Lộ trình

Nhiều bài toán thực tế có hướng — ví dụ "sắp xếp các từ sao cho chữ cuối của từ
này bằng chữ đầu của từ kế tiếp." Mỗi từ là một cạnh từ chữ đầu tới chữ cuối.
Tìm thứ tự chính là tìm một đường đi Euler có hướng.

Quy tắc bậc có hướng dùng **bậc vào (indegree)** và **bậc ra (outdegree)**:

```text
  condition for a directed Eulerian path:
    - at most one node with out - in = 1   (the start)
    - at most one node with in - out = 1   (the end)
    - all other nodes have in == out
    - the underlying graph is weakly connected
  if in == out for every node -> a directed Eulerian circuit
```

```python
def has_eulerian_path_directed(g):
    ind, outd = g.degrees()
    start_diff = [i for i in range(g.size()) if outd[i] - ind[i] == 1]
    end_diff   = [i for i in range(g.size()) if ind[i] - outd[i] == 1]
    others_ok = all(ind[i] == outd[i]
                    for i in range(g.size())
                    if i not in start_diff and i not in end_diff)
    if not (len(start_diff) <= 1 and len(end_diff) <= 1 and others_ok):
        return False, None
    start = start_diff[0] if start_diff else next(
        (i for i in range(g.size()) if outd[i] > 0), 0)
    return True, start
```

```text
  a directed Eulerian path:

        0 -> 1 -> 2
        ^         |
        |         v
        3 <- 0    0

  out-in per node:
    0: out 2, in 1 -> +1 (start)
    1: out 1, in 1 ->  0
    2: out 0, in 2 -> -1 (end)
    3: out 1, in 0 -> +1 (also a start? -> would be 2 starts -> invalid)
```

Phiên bản có hướng dùng cùng vòng lặp Hierholzer, nhưng chỉ xóa một cạnh ra
(không có nửa cạnh ngược để xóa).

---

## 10. Ứng dụng

Đường đi/chu trình Euler không chỉ là câu đố:

```text
  garbage collection   - sweep every street with a truck, don't repeat
  postal delivery      - a route covering every street exactly once
  circuit design       - layout a board to touch every trace
  route planning       - snowplows, buses, road painting
  word puzzles         - arrange words into a chain by matching letters
  DNA fragment assembly- reconstruct a genome from overlapping reads
```

Bất cứ khi nào một bài toán nói "bao phủ mọi cạnh đúng một lần", hãy nghĩ tới
Euler.

---

## 11. Độ phức tạp

| Thao tác | Thời gian | Không gian |
|:---|:---:|:---:|
| Tính bậc | `O(V + E)` | `O(V)` |
| Kiểm tra liên thông | `O(V + E)` | `O(V)` |
| Kiểm tra tồn tại theo quy tắc bậc | `O(V + E)` | `O(V)` |
| Thuật toán Hierholzer | `O(E)` | `O(E)` |

Hierholzer rất hiệu quả — `O(E)` thời gian và không gian — vì nó chạm mỗi cạnh
một số lần hằng số và không bao giờ cấp phát mảng 2D.

---

## 12. Những Sai lầm Thường gặp

### Sai lầm 1: Quên kiểm tra liên thông

Chỉ riêng quy tắc bậc là không đủ. Một đồ thị không liên thông vẫn có thể có
mọi bậc chẵn nhưng không có lộ trình liên tục duy nhất nào. Luôn kiểm tra tính
liên thông của các nút không cô lập trước.

### Sai lầm 2: Nhầm lẫn đường đi và chu trình

Chu trình phải quay về điểm bắt đầu và yêu cầu **mọi bậc chẵn**. Đường đi có
thể kết thúc ở chỗ khác và cho phép **đúng hai bậc lẻ**. Đừng dùng quy tắc chu
trình khi chỉ cần một đường đi (hoặc ngược lại).

### Sai lầm 3: Không xóa cạnh ngược trong đồ thị không hướng

Trong đồ thị không hướng, một cạnh `u-v` được lưu ở cả `adj[u]` và `adj[v]`.
Khi bạn dùng nó từ `u`, bạn cũng phải xóa nó khỏi `v`, nếu không thuật toán sẽ
tưởng nó vẫn còn và cố dùng nó hai lần.

### Sai lầm 4: Coi quy tắc bậc có hướng giống không hướng

Đồ thị có hướng dùng `in == out` (không phải bậc thô). Một nút có `out - in = 1`
là ứng viên bắt đầu; một nút có `in - out = 1` là ứng viên kết thúc.

### Sai lầm 5: Bắt đầu từ sai nút

Với một đường đi Euler hở bạn phải bắt đầu tại một trong các nút bậc lẻ. Nếu
bắt đầu ở chỗ khác, bạn có thể bị kẹt trước khi dùng hết mọi cạnh.

---

## 13. Chạy Ví dụ

Chạy:

```text
python EulerianGraph.py
```

Đầu ra ổn định mong đợi:

```text
=== The Seven Bridges of Konigsberg (undirected) ===
degrees: [5, 3, 3, 3]
connected: True
Eulerian path exists: False | odd-degree starts: [0, 1, 2, 3]
Eulerian circuit exists: False

=== A solvable one-stroke puzzle (exactly 2 odd nodes) ===
degrees: [2, 3, 2, 3]
Eulerian path exists: True | must start at one of: [1, 3]
one-stroke route: [1, 0, 3, 1, 2, 3]

=== A graph with an Eulerian CIRCUIT (all even) ===
degrees: [2, 2, 2, 2]
Eulerian circuit exists: True
circuit route: [0, 1, 2, 3, 0]

=== Directed Eulerian path (word chains / routes) ===
directed Eulerian path exists: True | start: 0
directed route: [0, 1, 2, 0, 3, 2]
```

---

## 14. Bảng Tóm tắt Cuối cùng

```text
    1. One-stroke = find an Eulerian path or circuit.
    2. Degree = number of edges touching a node.
    3. Circuit = every edge once AND return to start.
    4. Path   = every edge once, may end elsewhere.
    5. All even degrees      -> circuit exists, start anywhere.
    6. Exactly two odd nodes -> path exists, start at one of them.
    7. More than two odd     -> impossible.
    8. Must also check connectivity of non-isolated nodes.
    9. Hierholzer: delete edges as used -> find the route in O(E).
    10. Directed: use in==out rule instead of raw degree.
```

**Bước tiếp theo:** Giờ bạn đã duyệt được đồ thị và hiểu các cạnh, hãy chuyển
sang các thuật toán đường đi ngắn nhất — Dijkstra, Bellman-Ford và Floyd — ở
bài viết tiếp theo.
