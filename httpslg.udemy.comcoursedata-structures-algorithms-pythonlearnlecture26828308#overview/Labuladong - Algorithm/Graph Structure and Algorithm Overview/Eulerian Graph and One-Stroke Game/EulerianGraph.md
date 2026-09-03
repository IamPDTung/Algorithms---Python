
---

# Eulerian Graph and One-Stroke Game

## 1. Goal

The "one-stroke drawing" puzzle is really a graph problem: can you trace every
edge of a figure exactly once, in a single continuous stroke, without lifting
your pen? You may pass through vertices many times, but each edge must be used
exactly once.

This article explains the theory behind that puzzle — **Eulerian paths and
Eulerian circuits** — the famous Seven Bridges of Königsberg problem, the
simple degree rule that tells you whether a solution exists, and Hierholzer's
algorithm that actually finds the route.

Source references:
- https://labuladong.online/en/algo/data-structure-basic/eulerian-graph/

---

## 2. Why Eulerian Graphs Were Born

The story starts in 18th-century Königsberg. A river divided the city into a
north bank, a south bank, and two islands. Seven bridges connected these four
regions.

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

The question that stumped the townspeople: **can you design a walk that
crosses each bridge exactly once and returns to your starting point?**

Euler turned this into a graph problem. Each region is a node; each bridge is
an edge.

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

Euler proved the walk is impossible. In doing so he invented an entire branch
of graph theory. That is why Eulerian graphs were born: to answer "can I
traverse every link exactly once?" — a question behind routing, circuit
design, and puzzles.

---

## 3. Terminology

| Term | Definition |
|:---|:---|
| **Degree** | Number of edges touching a node. In the picture below, node `A` has degree 3. |
| **Eulerian path** | A route that uses every edge exactly once (may start and end at different nodes). |
| **Eulerian circuit** | An Eulerian path that starts and ends at the **same** node. |
| **Eulerian graph** | A graph that has an Eulerian circuit. |

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

The one-stroke puzzle asks for an **Eulerian path** (it is fine if the pen
ends somewhere other than where it started). If you must also return to the
start, you need an **Eulerian circuit**.

---

## 4. The One-Stroke Drawing Puzzle

The rule of the game:

```text
  1. Draw every edge in one continuous stroke.
  2. You may pass through vertices multiple times.
  3. Each edge must be traversed exactly once.
  4. Never lift the pen.
```

There is a simple trick to know whether a figure is drawable — just look at
the **degrees** of its vertices:

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

## 5. The Seven Bridges Problem: Why It Has No Solution

Model Königsberg as a graph and count the degree of every node.

```text
  N (north):  3 bridges   -> degree 3  (odd)
  S (south):  3 bridges   -> degree 3  (odd)
  I1 (island1): 3 bridges -> degree 3  (odd)
  I2 (island2): 5 bridges -> degree 5  (odd)
```

Every node has odd degree. That means **four** odd nodes exist, which violates
both rules above (we need 0 or exactly 2). So:

```text
  all four degrees are odd
  -> not 0, not exactly 2
  -> no Eulerian circuit, no Eulerian path
  -> the puzzle is impossible
```

This is exactly what Euler proved in 1736. It was the first real result of
graph theory.

The Python demo reproduces it:

```python
koenigsberg = UndirectedGraph(4, [
    (0, 1), (0, 1), (0, 2), (0, 2),   # bridges touching region 0
    (0, 3), (1, 3), (2, 3),
])
koenigsberg.degrees()          # [5, 3, 3, 3]  -> four odd nodes
has_eulerian_path(koenigsberg) # (False, [0, 1, 2, 3]) -> impossible
```

---

## 6. The Degree Rules (Undirected Graphs)

An undirected graph is connected (all non-isolated nodes reachable) and:

| Condition | Result | Start node |
|:---|:---|:---|
| All degrees even | Eulerian circuit exists | anywhere |
| Exactly 2 degrees odd | Eulerian path exists | one of the two odd nodes |
| More than 2 odd | neither exists | impossible |

The code implements exactly this:

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

Why the rule works:

* Every time a route passes **through** a node it uses two edges (one in, one
  out). So in a closed route, every node's used edges pair up — all degrees
  must be even.
* An **open** path has two endpoints that each use one unpaired edge, so
  exactly two nodes may be odd.
* Three or more odd nodes cannot be paired into a single continuous route.

```text
  route through a node:  ------->  (node)  ------->
                          one in    one out    = 2 edges, an even contribution

  a circuit is a closed loop of these even contributions
  -> every node must have even degree
```

---

## 7. Finding the Route: Hierholzer's Algorithm

Knowing a route exists is only half the story. **Hierholzer's algorithm**
actually constructs it, and it is a clever extension of the edge-traversal DFS
from the previous article.

The key trick: instead of a 2D `visited` array, it **deletes each edge as it
is used**. That avoids the `O(V^2)` memory and keeps things simple.

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

It works in two phases even though they are interleaved in the loop:

```text
  Phase 1 (go deep):  follow unused edges, pushing nodes onto the stack.
  Phase 2 (backtrack): when a node runs out of edges, pop it into the path.
  Finally reverse the path.
```

A worked example on the 4-cycle `0-1-2-3-0`:

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

## 8. Why Deletion Replaces the 2D `visited` Array

Recall from the traversal article that edge traversal used a 2D array
`visited[u][v]`. Hierholzer avoids it entirely:

```text
  2D visited array:                  delete-on-use:

  visited[u][v] = True               adj[u].popleft()  removes the edge
  checks "have I used u->v?"         next time, the edge simply is not there

  memory O(V^2)                      memory O(E)
```

Deleting the edge from the adjacency list is equivalent to marking it visited,
but it costs no extra 2D array. This is why Hierholzer is the standard,
efficient way to find Euler paths.

---

## 9. Directed Graphs: Word Chains and Routes

Many real problems are directed — e.g. "arrange words so the last letter of
one equals the first letter of the next." Each word is an edge from its first
letter to its last letter. Finding the ordering is finding a directed Eulerian
path.

The directed degree rule uses **indegree** and **outdegree**:

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

The directed version uses the same Hierholzer loop, but only removes the one
outgoing edge (no reverse half-edge to delete).

---

## 10. Applications

Eulerian paths/circuits are not just a puzzle:

```text
  garbage collection   - sweep every street with a truck, don't repeat
  postal delivery      - a route covering every street exactly once
  circuit design       - layout a board to touch every trace
  route planning       - snowplows, buses, road painting
  word puzzles         - arrange words into a chain by matching letters
  DNA fragment assembly- reconstruct a genome from overlapping reads
```

Whenever a problem says "cover every edge exactly once," think Euler.

---

## 11. Complexity

| Operation | Time | Space |
|:---|:---:|:---:|
| Compute degrees | `O(V + E)` | `O(V)` |
| Connectivity check | `O(V + E)` | `O(V)` |
| Degree-rule existence test | `O(V + E)` | `O(V)` |
| Hierholzer's algorithm | `O(E)` | `O(E)` |

Hierholzer is very efficient — `O(E)` time and space — because it touches
each edge a constant number of times and never allocates a 2D array.

---

## 12. Common Mistakes

### Mistake 1: Forgetting the connectivity check

The degree rule alone is not enough. A disconnected graph can still have all
even degrees but no single continuous route. Always check connectivity of the
non-isolated nodes first.

### Mistake 2: Confusing path and circuit

A circuit must return to the start and requires **all even** degrees. A path
may end elsewhere and allows **exactly two odd** degrees. Do not use the
circuit rule when only a path is needed (or vice versa).

### Mistake 3: Not removing the reverse edge in undirected graphs

In an undirected graph an edge `u-v` is stored in both `adj[u]` and `adj[v]`.
When you use it from `u`, you must also remove it from `v`, or the algorithm
will think it is still available and try to use it twice.

### Mistake 4: Treating directed and undirected degree rules as the same

Directed graphs use `in == out` (not raw degree). A node with `out - in = 1`
is a potential start; a node with `in - out = 1` is a potential end.

### Mistake 5: Starting from the wrong node

For an open Eulerian path you must start at one of the odd-degree nodes. If
you start elsewhere, you may get stuck before using every edge.

---

## 13. Running the Example

Run:

```text
python EulerianGraph.py
```

Expected stable output:

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

## 14. Final Cheat Sheet

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

**Next Step:** Now that you can traverse graphs and understand edges, move on
to the shortest-path algorithms — Dijkstra, Bellman-Ford, and Floyd — in the
next article.
