
---

# Graph Shortest Path Algorithms

## 1. Goal

Finding the shortest (cheapest, fastest) path between points in a network is
one of the most useful problems in computing. It powers GPS navigation, network
routing, and task scheduling.

This article covers the four classic shortest-path algorithms and, more
importantly, **where each one belongs** — because choosing the wrong one
breaks your answer.

Source references:
- https://labuladong.online/en/algo/data-structure-basic/graph-shortest-path/

---

## 2. Why Shortest Paths Were Born

A graph's edges can carry a **weight** — a cost, distance, or time. The
shortest-path problem asks: what is the minimum total weight needed to go from
one node to another?

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

Without a systematic algorithm, you would have to enumerate every path — and
there are exponentially many. Shortest-path algorithms were born to find the
minimum without enumerating them all.

---

## 3. Two Kinds of Shortest-Path Problems

| Kind | Asks | Output |
|:---|:---|:---|
| **Single-source** | shortest path from one start to every other node | 1D array `distTo` |
| **All-pairs** | shortest path between every pair of nodes | 2D array `dist` |

There is also a **point-to-point** variant: from `src` to one `dst` only. It
is usually solved by stopping a single-source algorithm early, or by A*.

```text
  single-source:   distTo[i] = shortest from src to i
                   distTo = [0, 1, 3, 4]

  all-pairs:       dist[i][j] = shortest from i to j (a V x V matrix)
```

The single-source output `distTo` is the same idea as the `visited` layers in
BFS — but now the "layers" have weights, so a plain queue is not enough.

---

## 4. The Four Algorithms at a Glance

| Algorithm | Type | Negative weights? | Idea |
|:---|:---|:---:|:---|
| Dijkstra | single-source | no | BFS + greedy + priority queue |
| A* | point-to-point | no | Dijkstra + heuristic |
| Bellman-Ford / SPFA | single-source | yes | relax all edges repeatedly |
| Floyd-Warshall | all-pairs | yes | dynamic programming |

```text
  the family tree:

  BFS (unweighted)      --->  Dijkstra (weighted, greedy)
                              |--> A* (adds a heuristic)
  BFS / relaxation      --->  Bellman-Ford / SPFA (negative ok)
  dynamic programming   --->  Floyd-Warshall (all pairs)
```

Each one is a small extension of an idea you already know (BFS or DP). None of
them are magic.

---

## 5. The Negative-Weight Problem (Why Some Algorithms Refuse)

Dijkstra (and A*) assume a critical property: **as you add more edges, the
total weight never decreases** — i.e. there are no negative edges.

Why? Consider a source `s` with two neighbors `a` and `b`:

```text
  s -> a : 3
  s -> b : 4

  if all weights are non-negative, the shortest path to a is s -> a (cost 3).
  any route s -> b ... -> a costs at least 4 > 3, so it cannot beat 3.
```

But if there is a negative edge, that reasoning collapses:

```text
  s -> a : 3
  s -> b : 4
  b -> a : -10

  path s -> b -> a = 4 + (-10) = -6  <  3   (beats the direct edge!)
```

Dijkstra's greedy "commit to the smallest settled distance" breaks: it would
have already locked in `a = 3` before discovering the cheaper `-6` route.

And if a **negative cycle** exists (weights that sum to a negative value in a
loop), the shortest path is undefined — you can loop forever and the total
keeps dropping:

```text
  0 -> 1 : 1
  1 -> 0 : -3        cycle total = 1 + (-3) = -2 < 0

  loop 0->1->0->1->0...  total -> -infinity
  -> the shortest path is meaningless
```

So: Dijkstra and A* cannot handle negative edges. Bellman-Ford/SPFA and Floyd
can, and Bellman-Ford is specifically used to **detect negative cycles**.

---

## 6. Dijkstra: BFS + Greedy + Priority Queue

Dijkstra is BFS with two upgrades:

1. A **priority queue** (min-heap) instead of a plain queue, ordered by the
   current distance, so the closest unsettled node is always processed first.
2. **Relaxation**: when we find a shorter route to a node, we update its
   distance and re-push it.

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

Why it works: the greedy choice is safe **only because** there are no negative
edges. Once a node is popped (settled), its distance is final. That is exactly
the property negative weights destroy.

Complexity: `O(E log V)` with a binary heap.

---

## 7. A*: Dijkstra Pointing at a Target

A* solves the **point-to-point** problem (one `src`, one `dst`). It is Dijkstra
plus a **heuristic** — an estimate `h(node)` of how far `node` is from the
target.

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

The priority of a node becomes `g(node) + h(node)`:

* `g(node)` = the real distance found so far (from Dijkstra).
* `h(node)` = the heuristic guess of remaining distance to the target.

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

For correctness the heuristic must be **admissible** (never overestimate the
true distance — e.g. straight-line distance). Then A* is guaranteed to find
the true shortest path, and a well-chosen `h` makes it reach the target faster
than Dijkstra.

But a heuristic is a guess. If it is bad, A* can detour and be slower than
plain Dijkstra. That is the trade-off of heuristic search.

---

## 8. Bellman-Ford: Relax Everything, `V-1` Times

Bellman-Ford handles **negative edges**. The idea is beautifully simple:
repeatedly relax **every edge**; each full pass guarantees at least one more
shortest distance becomes final, and after `V-1` passes all of them are.

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

**SPFA** is the queue-based version: instead of scanning every edge every pass,
it only re-processes a node when its distance actually improved, pushing it
onto a queue. It is "BFS + relaxation".

```text
  Bellman-Ford:       for each pass: relax ALL edges     O(V*E)
  SPFA:               only relax nodes whose distance changed   often faster
```

Both detect a negative cycle by noticing that a distance keeps improving even
after `V-1` passes.

Complexity: Bellman-Ford `O(V * E)`; SPFA is `O(V*E)` worst case but usually
much faster in practice.

---

## 9. Floyd-Warshall: All-Pairs via Dynamic Programming

Floyd-Warshall computes the shortest path between **every pair** of nodes. It
is a dynamic programming algorithm.

The key idea: `dist[k][i][j]` = the shortest path from `i` to `j` using only
intermediate nodes `0..k`. We grow `k` from `0` to `n-1`:

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

The three nested loops make it `O(V^3)`. It is the right choice when the graph
is dense or you truly need all pairs. For a single source on a large sparse
graph, running Dijkstra from every node is often faster.

---

## 10. Choosing the Right Algorithm

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

## 11. Complexity Summary

| Algorithm | Time | Space | Negative weights | Type |
|:---|:---:|:---:|:---:|:---|
| Dijkstra | `O(E log V)` | `O(V + E)` | no | single-source |
| A* | varies (heuristic) | `O(V + E)` | no | point-to-point |
| Bellman-Ford | `O(V * E)` | `O(V)` | yes | single-source |
| SPFA | `O(V * E)` worst | `O(V)` | yes | single-source |
| Floyd-Warshall | `O(V^3)` | `O(V^2)` | yes | all-pairs |

Where `V` = nodes, `E` = edges.

---

## 12. Common Mistakes

### Mistake 1: Using Dijkstra with negative weights

Dijkstra locks in distances greedily; a later negative edge can make an
already-settled node wrong. Use Bellman-Ford/SPFA when negative edges exist.

### Mistake 2: Forgetting negative cycles

With a negative cycle, the shortest path is undefined (approaches negative
infinity). Always check for it when the graph may contain negative edges.

### Mistake 3: Using A* with a non-admissible heuristic

If `h` overestimates the true distance, A* may return a sub-optimal path. The
heuristic must never overestimate (admissible) to guarantee correctness.

### Mistake 4: Using a plain BFS/queue for weighted graphs

BFS gives shortest paths only when every edge costs the same. With weights,
you need a priority queue (Dijkstra) — a plain queue processes in arrival
order, not cost order.

### Mistake 5: Running Floyd on a huge sparse graph

`O(V^3)` is brutal on big graphs. If you only need one source, or the graph is
sparse, prefer Dijkstra (or Dijkstra per source) over Floyd.

---

## 13. Running the Example

Run:

```text
python ShortestPath.py
```

Expected stable output:

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

Notice Dijkstra's `dist = [0.0, 1.0, 3.0, 4.0]` — node 2 is reached via 1
(1+2=3) rather than directly (4).

---

## 14. Final Cheat Sheet

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

**Next Step:** Shortest paths connect nodes; the next article connects **all
nodes as cheaply as possible** — the Minimum Spanning Tree.
