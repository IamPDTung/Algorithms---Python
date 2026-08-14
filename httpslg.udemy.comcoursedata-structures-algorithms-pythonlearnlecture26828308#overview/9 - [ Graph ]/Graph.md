
---

# Graph

## 1. What is a Graph?

A **Graph** is a data structure made of a set of **Vertices** (also called **nodes**) connected by **Edges**. It is the most **general** of all the data structures we have studied — a **Linked List is a restricted Tree**, and a **Tree is a restricted Graph**.

A tree is a graph with strict rules: one root, no cycles, exactly one path between any two nodes. A graph removes all those rules — **any vertex can connect to any other vertex**, cycles are allowed, and there is no "root".

### Key Terminology:

* **Vertex** — a node in the graph (plural: vertices).
* **Edge** — a connection between two vertices.
* **Adjacent / Neighbor** — two vertices connected by an edge are adjacent to each other.

### Types of Graphs:

* **Directed vs Undirected** — do the edges have a direction (one-way street) or not (two-way street)?
* **Weighted vs Unweighted** — do the edges carry a cost/distance/value, or are they all equal?

> **This course builds an UNDIRECTED, unweighted graph stored as an Adjacency List** — a Python dictionary that maps each vertex to a list of its neighbors.

### Visualization — Tree vs Graph:

```
        TREE (restricted graph):              GRAPH (general):

               A  <- one root                     A ------- B
              / \                                / \       /
             B   C                              /   \     /
            / \   \                            D ----- C
           D   E   F                            \     /
            ^   ^   ^                            \   /
            |   |   |                             E
        no cycles allowed                    cycles ARE allowed
        one path between nodes               many paths between nodes
```

### Types of Graphs — Visualized:

```
        UNDIRECTED (two-way edges):          DIRECTED (one-way edges):

            A --------- B                        A --------> B
            |           |                        |           |
            |           |                        v           v
            C --------- D                        C --------> D

            "A and B are friends"                "A follows B"
            (Facebook)                           (Twitter/X)


        UNWEIGHTED:                            WEIGHTED:

            A --------- B                        A ---- 5 ---- B
            |           |                        |             |
            |           |                        2             7
            C --------- D                        |             |
                                                 C ---- 1 ---- D

            edges are equal                      edges have a COST
                                                 (distance, time, $)
```

---

## 2. Why Were Graphs Created?

All the structures we studied so far are **hierarchies or lines**: a linked list is a straight line, a tree branches downward from a single root, and each node has only **one parent**.

But the real world is full of **networks**, not hierarchies:

* **Cities and flights** — you can fly City A -> City B -> City C -> back to City A (a **cycle**!). A tree cannot represent that.
* **Social networks** — Alice is friends with Bob, Bob is friends with Carol, and Carol is friends with Alice. **Many-to-many** relationships.
* **The World Wide Web** — pages link to each other in every direction.

### The Limitation of Trees:

```
    WHAT A TREE CAN MODEL:                WHAT ONLY A GRAPH CAN MODEL:

        Company org chart                     Flight routes
            CEO                                  NYC --------> LA
           /   \                                ^  \          ^
          VP   VP                               |    \        |
         /  \  /  \                             |     v       |
       ... ... ... ...                         CHI <--- DAL <---
           |                                       ^          |
       no cycles, one boss each                    |          |
                                                   SEA <------+
                                              (fly in circles —
                                               trees FORBID this!)
```

### The Graph Insight:

> When the problem is about **relationships between things** — and those relationships can loop, cross, and connect in any pattern — you need a **Graph**. It is the structure underneath maps, networks, and the internet itself.

---

## 3. Problems Graphs Solve

Graphs power some of the most important software in the world:

```
    +---------------------------+----------------------------------------+
    |      APPLICATION          |      VERTICES / EDGES                  |
    +---------------------------+----------------------------------------+
    | Social networks           | People / friendships (undirected)      |
    | (Facebook, LinkedIn)      | follows (directed)                     |
    +---------------------------+----------------------------------------+
    | Google Maps routing       | Intersections / roads (weighted by     |
    |                           | distance or time)                      |
    +---------------------------+----------------------------------------+
    | Web crawling & PageRank   | Pages / hyperlinks (directed)          |
    +---------------------------+----------------------------------------+
    | Network topology          | Routers, computers / cables            |
    +---------------------------+----------------------------------------+
    | Dependency resolution     | Packages, tasks / "depends on" edges   |
    | (pip, npm, build systems) | (directed — install order matters)     |
    +---------------------------+----------------------------------------+
```

* **Social networks** — "friend suggestions" are just vertices 2 edges away from you.
* **Google Maps** — the shortest-path problem: which route of edges minimizes total weight?
* **Web crawling (PageRank)** — Google's original algorithm ranks pages by analyzing the link graph.
* **Network topology** — find the cheapest way to connect all computers (spanning tree).
* **Dependency resolution** — a package can only be installed after everything it points to.

### What Comes Next:

The **BFS and DFS traversals** from folder 13 were written for trees, but they extend **directly** to graphs (you just track "visited" vertices so cycles don't loop forever). After that come the famous graph algorithms:

```
    BFS / DFS on graphs   -->   Shortest Path (Dijkstra, Bellman-Ford)
                            -->   Minimum Spanning Tree (Prim, Kruskal)
                            -->   Topological Sort (dependency order)
```

---

## 4. Storing a Graph: Adjacency List vs Adjacency Matrix

There are two classic ways to store a graph in memory. We will use the same example graph for both:

```
            A --------- B
            |           |
            |           |
            C --------- D

        Edges: A-B, A-C, B-D, C-D
```

### Option 1 — Adjacency Matrix (2D grid):

A `V x V` grid of 0s and 1s. `matrix[A][B] = 1` means "edge A-B exists".

```
              A   B   C   D
           +---+---+---+---+
        A  | 0 | 1 | 1 | 0 |
           +---+---+---+---+
        B  | 1 | 0 | 0 | 1 |
           +---+---+---+---+
        C  | 1 | 0 | 0 | 1 |
           +---+---+---+---+
        D  | 0 | 1 | 1 | 0 |
           +---+---+---+---+

        Row A says: "A touches B and C"
```

### Option 2 — Adjacency List (dictionary of lists) — **what this course uses**:

Each vertex maps to a **list of its neighbors** only:

```
        {
            'A' : ['B', 'C'],
            'B' : ['A', 'D'],
            'C' : ['A', 'D'],
            'D' : ['B', 'C']
        }

        Key 'A' says: "A touches B and C"
```

### Why the Adjacency List Wins (for most real graphs):

```
    +----------------------+--------------------+--------------------+
    |                      |  ADJACENCY LIST    |  ADJACENCY MATRIX  |
    +----------------------+--------------------+--------------------+
    | Space                | O(V + E)           | O(V^2)             |
    |                      | (only real edges)  | (every cell, even  |
    |                      |                    |  the empty ones)   |
    +----------------------+--------------------+--------------------+
    | Check "is A-B an     | O(degree)          | O(1)               |
    | edge?"               | scan neighbor list | one grid lookup    |
    +----------------------+--------------------+--------------------+
    | Best for             | SPARSE graphs      | DENSE graphs       |
    |                      | (few edges — most  | (almost every pair |
    |                      |  real networks)    |  is connected)     |
    +----------------------+--------------------+--------------------+

    Facebook: ~3 billion users, ~300 friends each.
        Matrix: 3B x 3B cells  = 9 QUINTILLION cells  <- impossible!
        List:   3B x 300 entries                      <- totally fine
```

---

## 5. How the Graph Works — Step by Step

The class stores everything in `self.adj_list`, a dictionary where:

```
        key   = a vertex
        value = a LIST of that vertex's neighbors
```

### 5.1 `add_vertex` — Add a Key with an Empty List

A brand-new vertex has **no edges yet**, so it gets an empty neighbor list:

```
    BEFORE:  adj_list = {}

    add_vertex('A'):

    AFTER:   adj_list = { 'A' : [] }

                 A      <- exists, but connected to nothing
```

If the vertex **already exists**, the method returns `False` and changes nothing.

### 5.2 `add_edge` — Append Each Vertex to the Other's List

Because the graph is **undirected**, every edge is stored **twice** — once on each side:

```
    BEFORE:  { 1: [], 2: [] }

        1       2          <- no edge

    add_edge(1, 2):
        append 2 to adj_list[1]     -->  1: [2]
        append 1 to adj_list[2]     -->  2: [1]   <- BOTH directions!

    AFTER:   { 1: [2], 2: [1] }

        1 ------- 2        <- one undirected edge
```

**Edge case from the code:** if either vertex is **missing** from the dictionary, return `False` — you cannot connect vertices that don't exist.

### 5.3 `remove_edge` — Remove Both Directions

The mirror image of `add_edge` — delete each vertex from the **other's** list:

```
    BEFORE:  A : ['B', 'C']
             B : ['A', 'C']
             C : ['B', 'A']

            A ----- B
             \     /
              \   /
                C

    remove_edge('A', 'C'):
        remove 'C' from adj_list['A']  -->  A : ['B']
        remove 'A' from adj_list['C']  -->  C : ['B']

    AFTER:   A : ['B']
             B : ['A', 'C']
             C : ['B']

            A ----- B
                   /
                  /
                C          <- the A-C edge is gone
```

The code wraps the removal in a `try/except ValueError` so that removing an edge that **isn't there** does nothing (still returns `True`). If either vertex is **missing entirely**, return `False`.

### 5.4 `remove_vertex` — Remove the Vertex AND Every Edge Pointing to It

This is the tricky one. You can't just delete the key — every neighbor still has a **dangling reference** to it. You must first loop over the vertex's neighbor list and erase it from **each neighbor's** list:

```
    BEFORE:  A : ['B', 'C', 'D']
             B : ['A', 'D']
             C : ['A', 'D']
             D : ['A', 'B', 'C']

                 A
               / | \
              B--D--C        <- D is connected to A, B, C

    remove_vertex('D'):

        Step 1: loop over adj_list['D'] = ['A', 'B', 'C']

            other_vertex = 'A':  remove 'D' from A's list
                                 A : ['B', 'C', 'D'] -> ['B', 'C']
            other_vertex = 'B':  remove 'D' from B's list
                                 B : ['A', 'D']      -> ['A']
            other_vertex = 'C':  remove 'D' from C's list
                                 C : ['A', 'D']      -> ['A']

        Step 2: NOW delete the key itself:
                del adj_list['D']

    AFTER:   A : ['B', 'C']
             B : ['A']
             C : ['A']

                 A
                / \
               B   C         <- D and ALL its edges are gone
```

**Edge case from the code:** if the vertex is **not in the dictionary**, return `False`.

---

## 6. The Full Code

This is the complete `Graph` class (from `SOLUTION-GR-Remove_Vertex.py`, which includes all methods):

```python
class Graph:
    def __init__(self):
        self.adj_list = {}

    def print_graph(self):
        for vertex in self.adj_list:
            print(vertex, ':', self.adj_list[vertex])

    def add_vertex(self, vertex):
        if vertex not in self.adj_list.keys():
            self.adj_list[vertex] = []
            return True
        return False

    def add_edge(self, v1, v2):
        if v1 in self.adj_list.keys() and v2 in self.adj_list.keys():
            self.adj_list[v1].append(v2)
            self.adj_list[v2].append(v1)
            return True
        return False

    def remove_edge(self, v1, v2):
        if v1 in self.adj_list.keys() and v2 in self.adj_list.keys(): 
            try:
                self.adj_list[v1].remove(v2)
                self.adj_list[v2].remove(v1)
            except ValueError:
                pass
            return True
        return False

    def remove_vertex(self, vertex):
        if vertex in self.adj_list.keys():
            for other_vertex in self.adj_list[vertex]:
                self.adj_list[other_vertex].remove(vertex)
            del self.adj_list[vertex]
            return True
        return False        
```

### Demo Run (from the SOLUTION file):

```python
my_graph = Graph()
my_graph.add_vertex('A')
my_graph.add_vertex('B')
my_graph.add_vertex('C')
my_graph.add_vertex('D')

my_graph.add_edge('A','B')
my_graph.add_edge('A','C')
my_graph.add_edge('A','D')
my_graph.add_edge('B','D')
my_graph.add_edge('C','D')

my_graph.remove_vertex('D')
```

### Output:

```
    Graph before remove_vertex():
    A : ['B', 'C', 'D']
    B : ['A', 'D']
    C : ['A', 'D']
    D : ['A', 'B', 'C']

    Graph after remove_vertex():
    A : ['B', 'C']
    B : ['A']
    C : ['A']
```

---

## 7. Big O Analysis

### Graph Operations (Adjacency List):

| Operation | Time Complexity | Why |
|:---|:---|:---|
| **Add Vertex** | `O(1)` | One dictionary insert |
| **Add Edge** | `O(1)` | Two list appends |
| **Remove Edge** | `O(V)` | Must scan one vertex's neighbor list to find the value (worst case a vertex connects to all `V-1` others) |
| **Remove Vertex** | `O(V + E)` | Loop over the vertex's neighbors (`O(V)` worst case) and remove it from each of their lists; every affected edge is touched once |
| **Space** | `O(V + E)` | One key per vertex + one list entry per edge endpoint (each edge stored twice) |

> `V` = number of vertices, `E` = number of edges. An edge between two vertices appears **twice** in an undirected adjacency list, which is why space is `O(V + E)` and not just `O(V)`.

### Adjacency List vs Adjacency Matrix — Final Comparison:

| | **Adjacency List** | **Adjacency Matrix** |
|:---|:---|:---|
| **Space** | `O(V + E)` | `O(V^2)` |
| **Add Vertex** | `O(1)` | `O(V^2)` (rebuild grid) or `O(V)` (add row/col) |
| **Add Edge** | `O(1)` | `O(1)` |
| **Check Edge Exists** | `O(degree)` — scan a neighbor list | `O(1)` — direct grid lookup |
| **Remove Vertex** | `O(V + E)` | `O(V^2)` |
| **Best For** | **Sparse** graphs (few edges per vertex — social networks, maps) | **Dense** graphs (almost all pairs connected) |

---

## 8. Summary

```
    +----------------------------------------------------------+
    |  GRAPH = Vertices + Edges                                |
    +----------------------------------------------------------+
    |  - Generalizes trees (trees forbid cycles & many paths)  |
    |  - Directed or undirected, weighted or unweighted        |
    |  - Stored as an ADJACENCY LIST: dict of neighbor lists   |
    |                                                          |
    |  add_vertex    ->  new key, empty list          O(1)     |
    |  add_edge      ->  append BOTH directions       O(1)     |
    |  remove_edge   ->  remove BOTH directions       O(V)     |
    |  remove_vertex ->  clean up neighbors FIRST,    O(V+E)   |
    |                    then delete the key                   |
    +----------------------------------------------------------+
```

---

**Next Step:** Now let's traverse this graph — take the BFS and DFS traversals from folder 13 and see how they walk a graph with cycles, then tackle the classic shortest-path problems!
