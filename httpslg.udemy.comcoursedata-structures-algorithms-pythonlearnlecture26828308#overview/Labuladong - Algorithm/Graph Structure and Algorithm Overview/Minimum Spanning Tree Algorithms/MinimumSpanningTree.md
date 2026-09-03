
---

# Minimum Spanning Tree Algorithms

## 1. Goal

A **minimum spanning tree (MST)** connects every node of an undirected
weighted graph using the smallest total edge weight possible — with no cycles.

This is a workhorse problem: designing the cheapest road/network layout, wiring
circuits, and laying pipelines all reduce to it. This article covers the
definition, why it exists, and the two classic algorithms: **Kruskal's** and
**Prim's**.

Source references:
- https://labuladong.online/en/algo/data-structure-basic/graph-minimum-spanning-tree/

---

## 2. Why MST Was Born

Suppose you must connect several cities with roads, and each possible road has
a construction cost. You want to connect all cities with the **lowest total
cost**.

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

The naive approach would try every subset of roads — exponential. MST
algorithms were born to find the cheapest connected layout **efficiently** and
**provably optimally**.

Real uses:

```text
  telecommunication  - lay cable to connect all offices at minimum cost
  road / rail        - link all towns with the cheapest network
  circuit wiring     - connect all pins with minimal copper
  pipeline layout    - connect sources to sinks with least pipe
  maze generation    - carve a random connected maze (see below)
```

---

## 3. What Is a Spanning Tree?

Given a connected undirected graph `G`, a **spanning tree** is a subgraph that:

* includes **all** the vertices of `G`
* is a **tree** — connected and acyclic
* therefore uses exactly `V - 1` edges

```text
  graph G (4 nodes, 5 edges):        one spanning tree (3 edges):

        A---B                              A---B
        |\ /|                              |   |
        | X |                              |   |
        |/ \|                              |   |
        C---D                              C   D
```

A connected graph generally has **many** different spanning trees. Here are a
few of the spanning trees of the same graph:

```text
  spanning tree #1:                spanning tree #2:
        A---B                           A---B
            |                           |
            |                           |
        C---D                           C---D

  both include all 4 nodes, both use 3 edges, both are acyclic
```

---

## 4. What Is a Minimum Spanning Tree?

If the graph is **weighted**, the **minimum spanning tree** is the spanning
tree with the **smallest total edge weight**.

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

The MST picks edges to connect everything while **minimizing the sum**.

```text
  cities + road costs:           MST (cheapest connected network):

     A --5-- B                     A --5-- B
     |      /|                     |
     7    3/ |                     7
     |    /  |                     |
     C --1-- D                     C --1-- D
                                    (A-B=5, A-C=7, C-D=1 => 13)
```

There is exactly one answer for the **total weight**, though different sets of
edges can tie for it.

---

## 5. Two Classic Algorithms

Both are greedy, but they grow the tree differently:

| Algorithm | Grows by | Core tool |
|:---|:---|:---|
| **Kruskal** | choosing the cheapest edge that does not create a cycle | sort edges + Union-Find |
| **Prim** | growing one component by its cheapest boundary edge | priority queue (Dijkstra-like) |

```text
  Kruskal: pick edges globally, cheapest first.
  Prim:    grow a single blob outward, cheapest boundary first.

  both end with the same MST total weight.
```

---

## 6. Kruskal's Algorithm: Sort + Union-Find

Kruskal's idea is beautifully simple:

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

To test "does this edge connect two different components?" cheaply, Kruskal
uses the **Union-Find** data structure (the next article's subject):

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

Why skipping cycles is correct: adding an edge between two nodes already in the
same component would create a cycle, which a tree cannot contain.

Complexity: sorting is `O(E log E)`; the Union-Find adds nearly `O(1)` per
edge, so overall `O(E log E)`.

---

## 7. Prim's Algorithm: Grow One Component

Prim works like Dijkstra (the previous article), but instead of minimizing
distance to a source, it minimizes the cost to **grow a single tree**:

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

The priority queue always picks the cheapest edge that connects the tree to a
node outside it — exactly the greedy step that keeps the tree minimal.

Complexity: `O(E log V)` with a binary heap (same as Dijkstra).

---

## 8. Kruskal vs Prim

| | Kruskal | Prim |
|:---|:---|:---|
| Growth | global: cheapest edges first | local: grow one blob |
| Key tool | Union-Find | priority queue |
| Sparse graph | good (`E log E`) | good (`E log V`) |
| Dense graph | okay | often better |
| Feels like | sorting + connectivity | Dijkstra |

Both produce a valid MST. The choice is mostly about which fits the tools and
data you already have. Kruskal is often easiest to reason about; Prim feels
natural when you already have Dijkstra.

---

## 9. Random Maze Generation (Fun Application)

With a twist, MST algorithms generate random mazes and cave maps. The key
property: an MST connects all points **without forming cycles** — exactly what
a maze needs (one connected path, no loops).

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

That is why the two algorithms produce mazes with different visual character:
Kruskal carves many separate starts, while Prim spreads from one origin.

---

## 10. Complexity Summary

| Algorithm | Time | Space | Tool |
|:---|:---:|:---:|:---|
| Kruskal | `O(E log E)` | `O(V + E)` | sort + Union-Find |
| Prim | `O(E log V)` | `O(V + E)` | priority queue |

Where `V` = nodes, `E` = edges. Both are efficient and scale to real networks.

---

## 11. Common Mistakes

### Mistake 1: Forgetting the `V-1` stopping rule

A spanning tree must have exactly `V - 1` edges. If the graph is disconnected,
you cannot reach `V - 1` — detect that (fewer edges means no spanning tree).

### Mistake 2: Adding an edge that creates a cycle

In Kruskal, always check that `u` and `v` are in different components before
adding. Adding within the same component creates a cycle and breaks the tree.

### Mistake 3: Using Prim without skipping in-tree nodes

When popping from the priority queue, skip an edge whose far end is already in
the tree. Forgetting this duplicates work and can corrupt the result.

### Mistake 4: Using MST for shortest-path problems

An MST connects everything cheaply but does **not** give shortest paths between
two specific nodes. Those are different problems (MST vs shortest path). Don't
confuse them.

### Mistake 5: Treating MST as unique

The total weight of an MST is unique, but the set of edges may not be. Two
different edge sets can both be valid MSTs with the same weight.

---

## 12. Running the Example

Run:

```text
python MinimumSpanningTree.py
```

Expected stable output:

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

Both algorithms select 5 edges (a tree on 6 nodes) with the same total weight
`9`, and the set of chosen edges is identical in this example.

---

## 13. Final Cheat Sheet

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

**Next Step:** Kruskal relies on Union-Find — the very next topic. Understanding
it completes the MST story.
