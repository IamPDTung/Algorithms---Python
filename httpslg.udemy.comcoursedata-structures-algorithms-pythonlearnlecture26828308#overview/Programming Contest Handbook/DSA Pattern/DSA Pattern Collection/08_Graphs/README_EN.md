# GRAPHS

## What is it?

A Graph is a set of **nodes (vertices)** connected by **edges**. Edges can be:
- **Directed** (one-way) or **undirected** (two-way).
- **Weighted** (cost per edge) or **unweighted**.
- Stored as **adjacency list** `{node: [neighbors]}` (most common) or **matrix**.

Core traversal algorithms:
- **DFS** — depth-first (stack / recursion).
- **BFS** — breadth-first (queue); gives **shortest path in unweighted graphs**.
- **Dijkstra** — shortest path in weighted graphs (heap-based).
- **Topological Sort** — ordering for DAGs (Kahn / DFS).
- **Union Find** — connectivity (see pattern 12).

## Why use it?

- Real-world data is relational: friends, roads, web links, prerequisites, networks.
- Many problems reduce to *"can we reach X?"*, *"shortest route"*, *"is there a cycle?"*,
  *"in what order can tasks run?"* — all graph questions.
- Learning these 5 tools covers the vast majority of contest graph problems.

## When to use?

| Signal in the problem | Tool |
|---|---|
| "Connected / reachable / number of islands" | DFS or BFS |
| "Shortest path, unweighted" | BFS |
| "Shortest path, weighted" | Dijkstra |
| "Order of courses / tasks (DAG)" | Topological Sort |
| "Cycle detection" | DFS (coloring) / Kahn / Union Find |
| "Provinces / connected components" | Union Find or DFS |

## Visualization — undirected graph, adjacency list

```
    A ─── B
    │     │
    C ─── D

 adjacency list:
   A: [B, C]
   B: [A, D]
   C: [A, D]
   D: [B, C]

 BFS from A:  A -> B, C -> D    order: A, B, C, D
 DFS from A:  A -> B -> D -> C  order: A, B, D, C
```

## Visualization — Dijkstra on weighted graph

```
       1
   A ───── B
   | \     |
  4|  \2   |2
   |   \   |
   C ──3── D

 dist:  A=0, B=1, C=4, D=3
 path to D: A -> B -> D  (1 + 2 = 3)
 (direct A->D = 5, via C = 4 + 3 = 7, so via B is best)

 Algorithm: greedy - repeatedly relax the smallest dist node (priority queue)
```

## Complexity

- **DFS / BFS:** O(V + E) time, O(V) space
- **Dijkstra:** O((V + E) log V)
- **Topological sort (Kahn):** O(V + E)

## Template (BFS)

```python
from collections import deque

def bfs(graph, start):
    visited = {start}
    q = deque([start])
    while q:
        node = q.popleft()
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                q.append(neighbor)
```

## Example problems solved in this folder

| Problem | File | Idea |
|---|---|---|
| Number of Islands | `number_of_islands.py` | DFS flood fill |
| Course Schedule | `course_schedule.py` | topological sort / cycle check |
| Clone Graph | `clone_graph.py` | DFS + hash map |

## Practice

Try: Network Delay Time (Dijkstra), Word Ladder (BFS), Alien Dictionary (topo sort),
Number of Provinces (Union Find), Rotting Oranges (multi-source BFS).
