
---

# Basic Concept of Union Find Algorithm

## 1. Goal

The **Union-Find** data structure (also called **Disjoint Set**) answers
connectivity questions in an undirected graph in near-constant time:

```text
  union(p, q)      -> connect p and q into one group
  connected(p, q)  -> are p and q in the same group?
  count()          -> how many separate groups are there?
```

It is the engine behind Kruskal's MST (previous article), friend-circle
problems, and dynamic connectivity. This article explains the concept, why it
beats naive graph traversal, and the two optimizations that make it fast.

Source references:
- https://labuladong.online/en/algo/data-structure-basic/union-find-basic/

---

## 2. The Dynamic Connectivity Problem

Consider 10 nodes labelled `0..9` with no edges. Each node is its own group —
there are 10 **connected components**.

```text
  0  1  2  3  4  5  6  7  8  9     (10 isolated nodes, 10 components)
```

Now perform some **union operations**: connect `0-1` and `1-2`.

```text
  after union(0,1) and union(1,2):

  0 -- 1 -- 2    3  4  5  6  7  8  9

  nodes 0,1,2 are now one component.
  components went from 10 down to 8.
```

The **dynamic connectivity problem** asks: given a sequence of unions and
queries, can you answer `connected(p, q)` and `count()` quickly as the graph
changes over time?

Connectivity has three useful properties:

```text
  reflexivity:  p is connected to itself
  symmetry:     if p ~ q then q ~ p
  transitivity: if p ~ q and q ~ r then p ~ r
```

The transitivity property is the crucial one — it is what makes a simple
"is there a direct edge?" check fail, as we see next.

---

## 3. Why Naive Graph Traversal Is Too Slow

A natural first attempt is to store the graph with an adjacency list and run
BFS/DFS to answer `connected(p, q)`:

```python
# naive idea: BFS from p to see if q is reachable
def connected_via_dfs(adj, p, q):
    visited = [False] * len(adj)
    stack = [p]
    while stack:
        u = stack.pop()
        if u == q:
            return True
        if not visited[u]:
            visited[u] = True
            stack.extend(adj[u])
    return False
```

But this is `O(V + E)` **per query**. And it fails to exploit transitivity:

```text
  0 -- 1 -- 2

  connected(0, 2)?
  there is no direct edge 0-2,
  but 0 connects to 1, and 1 connects to 2
  -> 0 and 2 ARE connected (transitively)

  a simple adjacency-matrix lookup "is there edge (0,2)?" would wrongly say no.
```

So to handle transitivity you must traverse the whole reachable set — slow, and
repeated for every query.

---

## 4. The Union-Find API

Union-Find solves this with just one array. It provides:

```text
  class UF:
      init(n)        # O(n): n nodes, each its own component
      union(p,q)     # ~O(1): connect p and q
      connected(p,q) # ~O(1): are they in the same component?
      count()        # ~O(1): number of components
```

The clever part: it keeps track of connectivity using a **tree per component**,
so `connected` only needs to compare the roots of the two trees — no traversal.

---

## 5. Core Idea: A Tree per Component

Represent each component as a tree. `parent[x]` points to `x`'s parent; the
**root** of a tree is a node whose parent is itself.

```text
  array representation:

  index:   0  1  2  3  4  5
  parent: [0, 0, 0, 3, 3, 5]

  trees:
     0           3      5
    /|\         / \
   1 2 ...     4   ...

  connected(1,2)?  find(1)=0, find(2)=0 -> same root -> True
  connected(2,4)?  find(2)=0, find(4)=3 -> different roots -> False
```

The `find(x)` operation walks up the parent pointers to the root:

```python
def find(self, x):
    while self._parent[x] != x:
        x = self._parent[x]
    return x
```

Then:

```python
def connected(self, p, q):
    return self.find(p) == self.find(q)

def union(self, p, q):
    rp, rq = self.find(p), self.find(q)
    if rp == rq:
        return False          # already connected
    self._parent[rp] = rq     # hang p's tree under q's tree
    self._count -= 1
    return True
```

`union` just points one root at the other — a single array write. `connected`
just compares two roots. Both are cheap. The **only** thing that can go wrong
is the trees growing tall.

---

## 6. The Problem: Trees Can Degrade Into Linked Lists

With no optimization, a sequence of unions can make a tree become a long chain.
Consider `union(0,1), union(1,2), union(2,3), ...`:

```text
  0 -> 1 -> 2 -> 3 -> 4 -> 5

  find(5) must walk 5 steps up the chain
  -> O(V) per find, so O(V) per union/connected
  -> the whole thing is as slow as a linked list
```

```text
  naive parent array after 0..5 chained:
  [1, 2, 3, 4, 5, 5]

  0 -> 1 -> 2 -> 3 -> 4 -> 5   (a degenerate tree / linked list)
```

This is why the reference shows an **unoptimized** Union-Find first: it reveals
the problem that the two optimizations fix.

---

## 7. Optimization 1: Union by Size (Weight Array)

The first fix: when merging two trees, always hang the **smaller** tree under
the **larger** one. Keep a `size[]` array recording how many nodes each root
owns.

```python
def union(self, p, q):
    rp, rq = self.find(p), self.find(q)
    if rp == rq:
        return False
    if self._size[rp] < self._size[rq]:
        rp, rq = rq, rp            # rp is now the larger tree
    self._parent[rq] = rp          # hang the smaller under the larger
    self._size[rp] += self._size[rq]
    self._count -= 1
    return True
```

```text
  without size:               with union by size:
  0->1->2->3->4->5            every node points to one tall root
                              (the tree stays shallow)
  height ~ V                  height ~ log V
```

Because the smaller tree (at most half the nodes) is always hung under the
larger, a node's depth can grow by at most `log V` times. So the height is
`O(log V)` — no more linked-list degradation.

---

## 8. Optimization 2: Path Compression

The second fix flattens the trees even further. During `find`, every node on
the walked path gets repointed directly at the root.

```python
def find(self, x):
    root = x
    while self._parent[root] != root:
        root = self._parent[root]
    while self._parent[x] != x:     # second pass: flatten the path
        nxt = self._parent[x]
        self._parent[x] = root
        x = nxt
    return root
```

```text
  before find(5):            after find(5):

  0 -> 1 -> 2 -> 3 -> 4 -> 5      0
                                 /|\
                                1 2 3 4 5
  (long path)                  (all now point straight at the root)
```

The next time you call `find` on any of those nodes, it is one step. This makes
the amortized cost essentially constant.

```text
  naive chain:  [1, 2, 3, 4, 5, 5]        (linked list)
  compressed:   [0, 0, 0, 0, 0, 0]        (all point at root 0)
```

---

## 9. The Combined Result

With both **union by size** and **path compression**:

```text
  amortized time per operation:  O(alpha(V))

  alpha = the inverse Ackermann function
  for any practical V, alpha(V) <= 4   -> "basically O(1)"
```

```text
  version            union      connected      space
  naive              O(V)       O(V)           O(V)
  union by size      O(log V)   O(log V)       O(V)
  + path compress    ~O(1)      ~O(1)          O(V)
```

That is why Union-Find is the tool of choice for dynamic connectivity: it turns
`O(V + E)` per query into `~O(1)`.

---

## 10. Application: Counting Friend Circles

A classic use: given an adjacency matrix where `M[i][j] == 1` means people `i`
and `j` are friends, count how many **friend circles** exist (people connected
through a chain of friendship).

```text
  people: A B C D
  friends: A-B are friends; C and D have no friends

  matrix:
     A B C D
  A [1 1 0 0]
  B [1 1 0 0]
  C [0 0 1 0]
  D [0 0 0 1]

  union every friendship, then count()
  -> 3 circles: {A,B}, {C}, {D}
```

```python
def friend_circles(m):
    n = len(m)
    uf = UnionFind(n)
    for i in range(n):
        for j in range(n):
            if m[i][j] == 1:
                uf.union(i, j)
    return uf.count()
```

The `count()` result is exactly the number of connected components after all
unions — a single `O(1)` read.

---

## 11. Complexity Summary

| Operation | Naive | Union by size | + path compression |
|:---|:---:|:---:|:---:|
| `union` | `O(V)` | `O(log V)` | `O(alpha(V))` ~ `O(1)` |
| `connected` | `O(V)` | `O(log V)` | `O(alpha(V))` ~ `O(1)` |
| `count` | `O(1)` | `O(1)` | `O(1)` |
| space | `O(V)` | `O(V)` | `O(V)` |

---

## 12. Common Mistakes

### Mistake 1: Forgetting transitivity

`connected(p, q)` must find the **root** of each tree and compare roots, not
check for a direct edge. A direct-edge lookup misses transitive connections.

### Mistake 2: Not flattening during find

Without path compression, repeated `find` calls keep walking long chains.
Always repoint the path to the root as you go.

### Mistake 3: Hanging trees arbitrarily

Unioning without union-by-size can build `O(V)`-tall trees. Always attach the
smaller tree to the larger root to keep height at `O(log V)`.

### Mistake 4: Confusing root with the node itself

Two nodes are connected only if their **roots** match. Comparing `parent[p]`
and `parent[q]` directly is wrong — they may be non-root nodes with different
immediate parents but the same root.

### Mistake 5: Off-by-one on component count

Every successful `union` (one that actually merges two different roots) must
decrement `count`. Failing to track this gives the wrong `count()`.

---

## 13. Running the Example

Run:

```text
python UnionFindBasics.py
```

Expected stable output:

```text
=== Dynamic connectivity: 10 isolated nodes ===
initial components: 10 (each node is its own)

=== Union operations ===
  union(0,1) -> components now: 9
  union(1,2) -> components now: 8
  union(5,6) -> components now: 7

=== connected() queries ===
connected(0,2): True (0-1, 1-2 transitive)
connected(0,5): False (different circles)
connected(5,6): True

=== Why transitive connectivity matters ===
  0-1, 1-2  =>  0 and 2 are connected through 1
  connected(0,2) = True

=== Friend circles (LeetCode-style) ===
adjacency matrix:
   [1, 1, 0, 0]
   [1, 1, 0, 0]
   [0, 0, 1, 0]
   [0, 0, 0, 1]
number of friend circles: 3

=== Naive vs optimized tree shape ===
naive parent chain (0..5): [1, 2, 3, 4, 5, 5] (0->1->2->...->5 list)
opt   parent chain (0..5): [0, 0, 0, 0, 0, 0] (all point at one root)
```

Note the contrast: the naive array is a linked list (`[1,2,3,4,5,5]`), while
the optimized array is flat (`[0,0,0,0,0,0]`).

---

## 14. Final Cheat Sheet

```text
    1. Union-Find tracks connected components of an undirected graph.
    2. Each component is a tree; parent[] stores one pointer per node.
    3. find(x) walks to the root of x's tree.
    4. connected(p,q) = (find(p) == find(q)).
    5. union(p,q) points one root at the other, count() decreases.
    6. Without care, trees degrade into O(V)-tall linked lists.
    7. Union by size keeps height at O(log V).
    8. Path compression flattens trees to ~O(1) amortized.
    9. Combined: O(alpha(V)) ~ constant per operation.
    10. Ideal for dynamic connectivity, Kruskal MST, friend circles.
```

**Next Step:** You now have the full graph toolbox — storage, traversal, Euler
paths, shortest paths, MST, and connectivity. Try applying them to real
problems to lock in the intuition.
