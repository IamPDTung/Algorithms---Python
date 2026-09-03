
---

# Graph Structure DFS/BFS Traversal

## 1. Goal

Graph traversal is an extension of N-ary tree traversal. The two main methods
are still **depth-first search (DFS)** and **breadth-first search (BFS)**.

The only new wrinkle is cycles: a tree has none, but a graph may. So we need a
`visited` array to stop the traversal from looping forever.

Graphs are richer than trees, so traversal comes in three flavors:

```text
  traverse NODES  -> 1D visited[]   (visit each node once)
  traverse EDGES  -> 2D visited[]   (visit each edge once)
  traverse PATHS  -> onPath[]       (record full node sequences)
```

Source references:
- https://labuladong.online/en/algo/data-structure-basic/graph-traverse-basic/

---

## 2. Why Cycles Force a `visited` Array

A tree has no cycles, so a simple recursion visits every node and stops.

```text
  tree:
       1
      / \
     2   3

  traverse(1) -> traverse(2), traverse(3)
  no node is ever reached twice.
```

A graph can loop back. Consider the smallest cycle, an edge both ways:

```text
  1 <=> 2
```

Without a `visited` guard, starting at `1` you go to `2`, back to `1`, to `2`,
to `1`, ... forever:

```text
  1 -> 2 -> 1 -> 2 -> 1 -> 2 -> ...  (infinite recursion)
```

The `visited` array fixes this. Mark `1` the first time you see it. When the
search comes back to `1` through the cycle, it sees `visited[1] == True` and
returns immediately, stopping the loop.

```text
  with visited:
    1 (mark) -> 2 (mark) -> 1? already visited -> return
                              -> no infinite loop
```

---

## 3. Tree Traversal vs Graph Traversal Side by Side

The N-ary tree and the graph share almost the same recursive shape. The graph
adds one line: the `visited` check.

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

In the code (`GraphTraversal.py`) this becomes `dfs_nodes`:

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

Because the `visited` array prunes revisits, every node is visited once and
every edge is attempted once, so the complexity is `O(V + E)`.

### Why `O(V + E)` and not just `O(V)`?

A tree's edge count is roughly equal to its node count, so tree traversal is
`O(N + N) = O(N)`. In a graph, any two nodes can be connected, so the edge
count is independent of the node count — hence `O(V + E)`.

---

## 4. Traversing All NODES (`visited`)

A 1D `visited` array is enough when you only care about visiting every node
once, no matter the order.

```text
  directed graph:

        0 --> 1 --> 3
        |           ^
        v           |
        2 ----------+

  DFS from 0:  0, 1, 3, 2   (go deep, then backtrack)
  BFS from 0:  0, 1, 2, 3   (visit by distance layer)
```

The version `dfs_nodes_all` additionally restarts the search from every
unvisited node, which lets you cover **all connected components** of a
disconnected graph:

```text
  disconnected graph:           DFS all components:
    0 --- 1       3 --- 4         component {0,1}: 0, 1
        |                         component {3,4}: 3, 4
        2                          result: [0, 1, 3, 4]
```

---

## 5. Traversing All EDGES (2D `visited`)

Sometimes the goal is to use each **edge** exactly once (this is the basis of
Euler paths, the next article). For that, a 1D node array is not enough — you
must record which edge `u -> v` has been used.

A 2D array `visited[u][v]` tracks each directed edge:

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

Notice the marking happens **inside the for loop**, not before it. An edge is
made of two nodes, so the pre-order position must be where an edge is chosen.

```text
  0 -> 1 -> 2 -> 0   (a triangle cycle)

  edge traversal:  (0,1), (1,2), (2,0)
```

The cost is higher: `O(E + V^2)` time and `O(V^2)` space because of the 2D
array. The next article (Euler paths) shows a smarter way that avoids the 2D
array.

---

## 6. Traversing All PATHS (`onPath`)

To list every full path from a source to a destination, we need to know not
just "was this node visited" but "is this node on the **current** path".

That is the job of `onPath`:

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

`visited` says "I have been here before, do not redo it." `onPath` says "I am
here **right now** on this branch — do not loop back onto me." The difference
is the post-order unmark.

---

## 7. Using BOTH `visited` and `onPath`: Cycle Detection

When you want to detect a cycle in a **directed** graph, you combine both
arrays.

* `visited[u]`  -> the node `u` was fully explored earlier.
* `onPath[u]`   -> the node `u` is on the current recursion stack.

If during DFS you reach a node `v` that is already on the current path, you
found a **back edge**, which means there is a cycle.

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

The two arrays answer different questions:

```text
  visited[u]  -> "was u ever processed?"
  onPath[u]   -> "is u on the path I am currently walking?"

  both True   -> a back edge exists -> a cycle exists.
```

---

## 8. BFS: Level-Order Traversal of a Graph

BFS visits nodes by **distance layer** using a queue — exactly like the
level-order traversal of an N-ary tree.

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

BFS is important because, in an **unweighted** graph, the first time BFS
reaches a node, it has found the **shortest path** to it. That is the seed of
the shortest-path algorithms in a later article.

---

## 9. BFS Shortest Path in an Unweighted Graph

Record the predecessor of each node. When you reach the destination, walk the
predecessor chain backward to reconstruct the path.

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

The guarantee holds only for **unweighted** graphs (every edge costs the same,
typically `1`). Weighted graphs need Dijkstra's algorithm (a later article).

---

## 10. DFS vs BFS: Which to Use?

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

## 11. The Three Flavors at a Glance

| Goal | Array | Mark at | Unmark | Example use |
|:---|:---|:---|:---|:---|
| Visit every node once | 1D `visited` | pre-order | no | reachability, connectivity |
| Use every edge once | 2D `visited` | inside loop | no | Euler paths |
| Enumerate all paths | `onPath` | pre-order | post-order | path listing |
| Detect directed cycles | `visited` + `onPath` | pre-order | post-order | dependency validation |

```text
  summary of the three markers:

  1D visited[u]       -> this node, never again
  2D visited[u][v]    -> this edge, never again
  onPath[u]           -> this node, on the current branch only
```

---

## 12. Complexity

| Traversal | Time | Space | Notes |
|:---|:---:|:---:|:---|
| Nodes (DFS/BFS) | `O(V + E)` | `O(V)` | one visit per node |
| Edges (2D visited) | `O(E + V^2)` | `O(V^2)` | 2D array allocation |
| All paths | `O(2^V)` worst | `O(V)` | exponential output size |
| Cycle detection | `O(V + E)` | `O(V)` | visited + onPath |

The all-paths traversal can be exponential because the number of paths itself
grows exponentially — that is inherent to the output, not a bug in the
algorithm.

---

## 13. Common Mistakes

### Mistake 1: Forgetting `visited` in a cyclic graph

Without it, DFS recurses forever around any cycle. Always guard with the node
array for node traversal.

### Mistake 2: Marking edges outside the loop

For edge traversal the pre-order marking must be inside the `for` loop (an
edge is chosen per neighbor), not before the loop.

### Mistake 3: Using `visited` where you need `onPath`

To enumerate distinct paths, `visited` wrongly forbids revisiting nodes that
appear on different branches. Use `onPath` so a node can appear on many paths
as long as it is not on the current one.

### Mistake 4: Forgetting the post-order unmark

`onPath[u] = False` at the post-order position is what allows backtracking.
Forget it and the search blocks legitimate branches.

### Mistake 5: Treating BFS as shortest-path on weighted graphs

BFS gives the shortest path only when every edge costs the same. Weighted
graphs need Dijkstra / Bellman-Ford (later articles).

---

## 14. Running the Example

Run:

```text
python GraphTraversal.py
```

Expected stable output:

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

## 15. Final Cheat Sheet

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

**Next Step:** Use the edge-traversal idea from this article to find Euler
paths — the subject of the next article.
