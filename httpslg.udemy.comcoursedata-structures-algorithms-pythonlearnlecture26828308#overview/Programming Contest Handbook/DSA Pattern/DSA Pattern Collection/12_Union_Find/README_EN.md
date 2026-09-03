# UNION FIND (DSU)

## What is it?

Union-Find (Disjoint Set Union, DSU) is a data structure that manages a partition of
elements into **disjoint sets**. It supports two operations:
1. **Find(x)** — which set does x belong to? (with **path compression**)
2. **Union(x, y)** — merge the sets of x and y. (by **rank / size**)

Each set is represented as a tree; the **root** is the set representative. With both
optimizations, operations run in nearly **O(1)** amortized — **O(α(n))**, the inverse
Ackermann function.

## Why use it?

- Extremely fast **connectivity queries**: "are A and B connected?"
- **Dynamic connectivity** — edges added over time; union as they arrive.
- **Cycle detection in undirected graphs**: if two nodes already share a root, the new
  edge closes a cycle.
- Count **connected components** by counting distinct roots.

## When to use?

| Signal in the problem | Why |
|---|---|
| "Connected components / provinces / groups" | union members, count roots |
| "Are A and B connected?" | find(A) == find(B) |
| "Redundant connection / cycle in undirected" | union edge endpoints, detect cycle |
| "Accounts / people merging" | union overlapping identities |
| "Dynamic / online connectivity" | process unions incrementally |

## Visualization — union by rank

```
 Initial:  0  1  2  3  4  5        (each its own set)

 union(0,1):  parent[0] = 1        rank[1] = 1
 union(2,3):  parent[2] = 3        rank[3] = 1
 union(0,3):  0 -> 1,  2 -> 3
              rank equal -> attach root of one under the other
              parent[1] = 3        rank[3] = 2

 Set trees:
   before union(0,3):    1         3
                       /          /
                      0          2
   after union(0,3):      3
                        / \
                       1   2
                      /
                     0
   find(0): 0 -> 1 -> 3   (path compression: 0 now points directly to 3)

 Roots: {3} for {0,1,2,3}, {4}, {5}  -> 3 connected components
```

## Complexity

- **Time:** O(α(n)) ~ O(1) amortized per operation
- **Space:** O(n)

## Template

```python
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):                    # path compression
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, x, y):                # union by rank
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False                  # already connected (cycle!)
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1
        return True
```

## Example problems solved in this folder

| Problem | File | Idea |
|---|---|---|
| DSU class | `union_find.py` | reusable implementation |
| Redundant Connection | `redundant_connection.py` | union edges, first cycle edge |
| Number of Provinces | `number_of_provinces.py` | union cities, count roots |

## Practice

Try: Accounts Merge, Number of Connected Components in an Undirected Graph,
Smallest String With Swaps, Satisfiability of Equality Equations, Regions Cut By Slashes.
