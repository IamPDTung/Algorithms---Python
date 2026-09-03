
---

# Graph Structure Code Implementation

## 1. Goal

A graph is an extension of the N-ary tree. A tree has strict rules: a parent
may point to its children, but children never point back at their parents and
siblings never point at each other. A graph removes all of those rules, so any
node may point at any other node, forming rich networks.

This article builds the two classic ways to store a graph in code — the
**adjacency list** and the **adjacency matrix** — and shows all four combinations
of directed/undirected and weighted/unweighted graphs.

Source references:
- https://labuladong.online/en/algo/data-structure-basic/graph-basic/

---

## 2. Why Graphs Were Born

A tree forces a strict one-way parent-to-child relationship. Many real-world
problems do not fit that shape:

```text
tree:                          graph:

      A                               A
     / \                            /   \
    B   C       B cannot           B <---> C
   /     \      point back,        | \   / |
  D       E     siblings           D---E---F
                cannot connect

  A social network, a road map, an electric circuit,
  or a web of dependencies is NOT a tree.
```

Graphs were born to model things that link together in arbitrary ways:

* social networks (friends follow friends)
* road / flight networks (any city connects to any other)
* circuit boards and plumbing (components touch many neighbors)
* dependency graphs (a task may depend on many others)

A graph is simply a collection of **nodes** (vertices) and the **edges**
(links) that join them.

---

## 3. The Building Blocks: Vertices and Edges

A vertex is just a labelled point. An edge joins two vertices and may carry a
**weight** (a cost, distance, or capacity).

```text
  a labelled vertex:              an edge with a weight:

        ( 0 )                     0 ------w=3------> 1
        (   )
```

Graphs are described with four properties:

| Property | Options | Meaning |
|:---|:---|:---|
| Direction | directed / undirected | Does the edge have an arrow? |
| Weight | weighted / unweighted | Does the edge carry a cost? |
| Cycles | cyclic / acyclic | Can you loop back to a node? |
| Connectivity | connected / disconnected | Can every node reach every other? |

The code in `GraphStructure.py` focuses on the first two properties, since
they change how the graph is physically stored.

---

## 4. The Two Storage Strategies

There are two dominant ways to store a graph, and every graph library is built
on one of them (or both).

### 4.1 Adjacency List

Each node keeps a list of the nodes it can reach.

```text
      1
     / \
    2   3
     \
      4

  adjacency list:
  1 -> [2, 3]
  2 -> [4]
  3 -> []
  4 -> []
```

### 4.2 Adjacency Matrix

A `V x V` table where cell `[u][v]` says whether (and at what cost) `u` can
reach `v`.

```text
      1
     / \
    2   3
     \
      4

  adjacency matrix (1 = edge exists, 0 = no edge):

          1   2   3   4
    1  [  0   1   1   0 ]
    2  [  0   0   0   1 ]
    3  [  0   0   0   0 ]
    4  [  0   0   0   0 ]
```

### 4.3 Choosing Between Them

```text
              adjacency list          adjacency matrix
  memory       O(V + E)               O(V^2) always
  edge (u,v)?  walk u's list O(deg)   O(1) direct lookup
  iterate out  O(deg)                 O(V)
  best for     sparse (E << V^2)      dense (E ~ V^2)
  simple?      yes                    very simple
```

Rule of thumb: use an **adjacency list** unless the graph is small and dense.
Real-world graphs are almost always sparse, so the adjacency list wins in
practice.

---

## 5. The Four Combinations

The `GraphStructure.py` module exposes a uniform node-labelled API
(`0 .. n-1`). Every representation supports the same three operations:

```python
graph.size()              # number of nodes
graph.neighbors(u)        # outgoing edges from node u
graph.add_edge(u, v, w)   # add an edge with weight w
```

The four storage combinations are:

| Storage | Directed | Undirected |
|:---|:---|:---|
| Adjacency list | `Graph` | `UndirectedGraph` |
| Adjacency matrix | `MatrixGraph` | `UndirectedMatrixGraph` |

---

## 6. Directed Weighted Graph (Adjacency List)

`Graph` stores each directed edge once, in the source node's list.

```text
  edges:
    0 -> 1 (1)
    0 -> 2 (4)
    1 -> 2 (2)
    2 -> 3 (3)

  adjacency list:
    0: [1(w=1), 2(w=4)]
    1: [2(w=2)]
    2: [3(w=3)]
    3: []
```

```python
g = Graph(4, [(0, 1, 1.0), (0, 2, 4.0), (1, 2, 2.0), (2, 3, 3.0)])
g.neighbors(0)   # [Edge(0->1, w=1.0), Edge(0->2, w=4.0)]
```

Because the edge is directed, `0 -> 1` appears in node `0`'s list but NOT in
node `1`'s list.

---

## 7. Directed Weighted Graph (Adjacency Matrix)

`MatrixGraph` stores the same graph in a `V x V` table. `None` means "no edge".

```text
          0    1    2    3
    0  [  .    1    4    . ]
    1  [  .    .    2    . ]
    2  [  .    .    .    3 ]
    3  [  .    .    .    . ]

  lookup weight(0,2) = 4    (direct O(1) read)
  lookup weight(0,3) = None (no edge)
```

```python
mg = MatrixGraph(4, [(0, 1, 1.0), (0, 2, 4.0), (1, 2, 2.0), (2, 3, 3.0)])
mg.weight(0, 2)   # 4.0
mg.weight(0, 3)   # None
```

---

## 8. Undirected Weighted Graph (Adjacency List)

`UndirectedGraph` treats every edge as a two-way link. An edge `u-v` is stored
**twice**: once in `u`'s list and once in `v`'s list.

```text
  edges:
    0 - 1 (1)
    0 - 2 (4)
    1 - 2 (2)
    2 - 3 (3)

  adjacency list (each edge appears twice):
    0: [1(w=1), 2(w=4)]
    1: [0(w=1), 2(w=2)]
    2: [0(w=4), 1(w=2), 3(w=3)]
    3: [2(w=3)]
```

```python
ug = UndirectedGraph(4, [(0, 1, 1.0), (0, 2, 4.0), (1, 2, 2.0), (2, 3, 3.0)])
ug.neighbors(1)   # [Edge(1->0, w=1.0), Edge(1->2, w=2.0)]
```

Doubling the storage is the price of being able to walk the edge in either
direction.

---

## 9. Undirected Weighted Graph (Adjacency Matrix)

`UndirectedMatrixGraph` writes each undirected edge to **both** cells
`[u][v]` and `[v][u]`, so the matrix is always symmetric.

```text
          0    1    2    3
    0  [  .    1    4    . ]
    1  [  1    .    2    . ]
    2  [  4    2    .    3 ]
    3  [  .    .    3    . ]

  the matrix is symmetric: weight(u,v) == weight(v,u)
```

```python
umg = UndirectedMatrixGraph(4, [(0, 1, 1.0), (0, 2, 4.0), (1, 2, 2.0), (2, 3, 3.0)])
umg.weight(1, 2)   # 2.0
umg.weight(2, 1)   # 2.0   (symmetric)
```

---

## 10. Unweighted Graphs as a Special Case

An unweighted graph is just a weighted graph where every edge has weight `1`.
The reference implementation defaults `weight` to `1.0`, so you can omit it:

```python
# unweighted directed graph, every edge has weight 1
g = Graph(3)
g.add_edge(0, 1)
g.add_edge(1, 2)
g.add_edge(2, 0)
```

For unweighted graphs a plain boolean matrix or a plain list of neighbor
ids is enough — the weight column is simply dropped.

```text
  unweighted adjacency list:      unweighted matrix:
    0: [1, 2]                          0   1   2
    1: [2]                       0  [  0   1   1 ]
    2: [0]                       1  [  0   0   1 ]
                                 2  [  1   0   0 ]
```

---

## 11. The Unified API Is What Matters

Notice that every representation exposes the exact same methods:

```python
graph.size()               # -> int
graph.neighbors(u)         # -> list of Edge
graph.add_edge(u, v, w)    # -> None
```

This is the most important design decision in the module. Because the API is
uniform, **graph algorithms written once against this interface work unchanged
on every representation**. Traversal, shortest path, and MST algorithms (the
later articles in this series) never care whether the backing store is a list
or a matrix — they only call `neighbors(u)`.

```text
                 uniform API
  algorithms <----------------- Graph / UndirectedGraph
      |                        MatrixGraph / UndirectedMatrixGraph
      |
      +--- call only: size(), neighbors(), add_edge()
```

---

## 12. Complexity Summary

| Storage | Memory | Edge lookup `(u,v)` | List all neighbors of `u` |
|:---|:---:|:---:|:---:|
| Adjacency list | `O(V + E)` | `O(deg(u))` | `O(deg(u))` |
| Adjacency matrix | `O(V^2)` | `O(1)` | `O(V)` |

where `V` is the number of nodes and `E` is the number of edges.

* The adjacency matrix shines for **dense** graphs where `E ~ V^2`, because
  edge lookup is `O(1)` and the matrix is small relative to its size.
* The adjacency list shines for **sparse** graphs where `E << V^2`, because it
  only stores what actually exists.

---

## 13. Common Mistakes

### Mistake 1: Forgetting to store an undirected edge twice

In an undirected adjacency list, `add_edge(u, v)` must append to BOTH
`adj[u]` and `adj[v]`. Storing it once makes the graph directed by accident.

### Mistake 2: Using the wrong representation for the graph density

Using a `V^2` matrix for a graph with a million nodes and a thousand edges
wastes gigabytes. Use an adjacency list for sparse graphs.

### Mistake 3: Confusing directed and undirected

In a directed graph, `0 -> 1` does not imply `1 -> 0`. In an undirected
graph it does. The two have different adjacency structures (one copy vs two).

### Mistake 4: Not normalising node labels

The API expects labels `0 .. n-1`. If your input uses arbitrary labels
(strings, or 1-based ids), you must map them to this range first, or the
array/table indexing breaks.

---

## 14. Running the Example

Run:

```text
python GraphStructure.py
```

Expected stable output (shown for the 4-node graph above):

```text
=== Directed weighted graph, adjacency list ===
0: [1(w=1), 2(w=4)]
1: [2(w=2)]
2: [3(w=3)]
3: []

=== Same graph as adjacency matrix ===
      0     1     2     3
 0    .     1     4     .
 1    .     .     2     .
 2    .     .     .     3
 3    .     .     .     .

=== Undirected graph, adjacency list (edge stored twice) ===
0: [1(w=1), 2(w=4)]
1: [0(w=1), 2(w=2)]
2: [0(w=4), 1(w=2), 3(w=3)]
3: [2(w=3)]

=== Undirected graph, adjacency matrix (symmetric) ===
      0     1     2     3
 0    .     1     4     .
 1    1     .     2     .
 2    4     2     .     3
 3    .     .     3     .
```

A `.` in the matrix means "no edge".

---

## 15. Final Cheat Sheet

```text
    1. A graph = vertices + edges, with no parent/child restriction.
    2. Adjacency list: each node owns a list of its outgoing edges.
    3. Adjacency matrix: a V x V table; cell [u][v] is the edge weight.
    4. Directed edge is stored once; undirected edge is stored twice.
    5. Unweighted is just weighted with every weight = 1.
    6. List -> O(V+E) space, good for sparse graphs.
    7. Matrix -> O(V^2) space, O(1) edge lookup, good for dense graphs.
    8. Expose a unified size()/neighbors()/add_edge() API.
    9. Algorithms written against the API work on any representation.
```

**Next Step:** Try the DFS/BFS traversal article next, which walks this exact
`neighbors(u)` interface to visit every node.
