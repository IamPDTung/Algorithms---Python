from __future__ import annotations

from collections import deque
from typing import Deque, Dict, List, Optional, Sequence, Tuple


class Graph:
    """A directed unweighted graph on nodes ``0 .. n-1`` (adjacency list)."""

    def __init__(self, n: int, edges: Optional[Sequence[Tuple[int, int]]] = None) -> None:
        self._n = n
        self._adj: List[List[int]] = [[] for _ in range(n)]
        if edges is not None:
            for u, v in edges:
                self._adj[u].append(v)

    def size(self) -> int:
        return self._n

    def add_edge(self, u: int, v: int) -> None:
        self._adj[u].append(v)

    def neighbors(self, u: int) -> List[int]:
        return self._adj[u]


# ---------------------------------------------------------------------------
# 1. Traversing all NODES: a 1D `visited` array.
#    Guard against revisiting a node so cycles do not cause infinite loops.
# ---------------------------------------------------------------------------

def dfs_nodes(g: Graph, start: int = 0) -> List[int]:
    order: List[int] = []
    visited = [False] * g.size()

    def dfs(u: int) -> None:
        if visited[u]:
            return
        visited[u] = True
        order.append(u)  # pre-order position
        for v in g.neighbors(u):
            dfs(v)

    dfs(start)
    return order


def dfs_nodes_all(g: Graph) -> List[int]:
    """DFS over every connected component (reachable from any node)."""
    order: List[int] = []
    visited = [False] * g.size()

    def dfs(u: int) -> None:
        if visited[u]:
            return
        visited[u] = True
        order.append(u)
        for v in g.neighbors(u):
            dfs(v)

    for s in range(g.size()):
        if not visited[s]:
            dfs(s)
    return order


# ---------------------------------------------------------------------------
# 2. Traversing all EDGES: a 2D `visited[u][v]` array.
#    Mark the edge at the pre-order position (inside the for loop).
# ---------------------------------------------------------------------------

def dfs_edges(g: Graph, start: int = 0) -> List[Tuple[int, int]]:
    order: List[Tuple[int, int]] = []
    n = g.size()
    visited = [[False] * n for _ in range(n)]

    def dfs(u: int) -> None:
        for v in g.neighbors(u):
            if visited[u][v]:
                continue
            visited[u][v] = True
            order.append((u, v))  # mark + visit the edge
            dfs(v)

    dfs(start)
    return order


# ---------------------------------------------------------------------------
# 3. Traversing all PATHS: an `onPath` array.
#    Mark at pre-order and UNmark at post-order so the search backtracks.
# ---------------------------------------------------------------------------

def all_paths(g: Graph, src: int, dst: int) -> List[List[int]]:
    result: List[List[int]] = []
    path: List[int] = []
    on_path = [False] * g.size()

    def dfs(u: int) -> None:
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


# ---------------------------------------------------------------------------
# 4. Using BOTH `visited` and `onPath`: topological cycle detection.
#    visited  -> node was fully explored before.
#    onPath   -> node is on the CURRENT recursion stack (a back edge).
# ---------------------------------------------------------------------------

def has_cycle(g: Graph) -> bool:
    n = g.size()
    visited = [False] * n
    on_path = [False] * n
    has_cyc = [False]

    def dfs(u: int) -> None:
        visited[u] = True
        on_path[u] = True
        for v in g.neighbors(u):
            if on_path[v]:
                has_cyc[0] = True  # back edge: cycle found
            if not visited[v]:
                dfs(v)
        on_path[u] = False

    for s in range(n):
        if not visited[s]:
            dfs(s)
    return has_cyc[0]


# ---------------------------------------------------------------------------
# 5. BFS: level-order traversal using a queue. Several "styles".
# ---------------------------------------------------------------------------

def bfs_levels(g: Graph, start: int = 0) -> List[List[int]]:
    """Style 1: record the level of every node (the distance layer)."""
    n = g.size()
    visited = [False] * n
    dist = [-1] * n
    q: Deque[int] = deque([start])
    visited[start] = True
    dist[start] = 0
    while q:
        u = q.popleft()
        for v in g.neighbors(u):
            if not visited[v]:
                visited[v] = True
                dist[v] = dist[u] + 1
                q.append(v)

    layers: List[List[int]] = []
    for d in range(max(dist) + 1):
        layers.append([i for i in range(n) if dist[i] == d])
    return layers


def bfs_shortest_path(g: Graph, src: int, dst: int) -> Optional[List[int]]:
    """Style 2: BFS gives the shortest path in an UNweighted graph."""
    n = g.size()
    if src == dst:
        return [src]
    prev: Dict[int, int] = {}
    visited = [False] * n
    q: Deque[int] = deque([src])
    visited[src] = True
    found = False
    while q and not found:
        u = q.popleft()
        for v in g.neighbors(u):
            if not visited[v]:
                visited[v] = True
                prev[v] = u
                if v == dst:
                    found = True
                    break
                q.append(v)
    if not found:
        return None
    path: List[int] = []
    cur = dst
    while cur != src:
        path.append(cur)
        cur = prev[cur]
    path.append(src)
    path.reverse()
    return path


def bfs_dfs_comparison(g: Graph, start: int = 0) -> Dict[str, List[int]]:
    """Style 3: plain BFS visit order (contrast with DFS visit order)."""
    n = g.size()
    bfs_order: List[int] = []
    visited = [False] * n
    q: Deque[int] = deque([start])
    visited[start] = True
    while q:
        u = q.popleft()
        bfs_order.append(u)
        for v in g.neighbors(u):
            if not visited[v]:
                visited[v] = True
                q.append(v)
    return {"bfs": bfs_order, "dfs": dfs_nodes(g, start)}


def _demo() -> None:
    # A directed graph with a cycle: 0 -> 1 -> 2 -> 0
    cyclic = Graph(4, [(0, 1), (1, 2), (2, 0), (1, 3)])

    # A directed acyclic graph (DAG) for paths: 0 -> 1, 0 -> 2, 1 -> 3, 2 -> 3
    dag = Graph(4, [(0, 1), (0, 2), (1, 3), (2, 3)])

    print("=== 1. DFS over all nodes (visited array) ===")
    print("cyclic graph, from 0:", dfs_nodes(cyclic, 0))
    print("cyclic graph, all components:", dfs_nodes_all(cyclic))
    print()

    print("=== 2. DFS over all edges (2D visited array) ===")
    print("cyclic graph edges:", dfs_edges(cyclic, 0))
    print()

    print("=== 3. Traverse all paths (onPath array) ===")
    print("DAG paths 0 -> 3:", all_paths(dag, 0, 3))
    print()

    print("=== 4. visited + onPath => cycle detection ===")
    print("cyclic graph has cycle:", has_cycle(cyclic))
    print("DAG has cycle:", has_cycle(dag))
    print()

    print("=== 5. BFS styles ===")
    print("BFS levels from 0 (cyclic):", bfs_levels(cyclic, 0))
    print("BFS shortest path 0 -> 3 (DAG):", bfs_shortest_path(dag, 0, 3))
    comp = bfs_dfs_comparison(dag, 0)
    print("visit order BFS:", comp["bfs"], "| DFS:", comp["dfs"])
    print()

    assert dfs_nodes(cyclic, 0) == [0, 1, 2, 3]
    assert len(dfs_edges(cyclic, 0)) == 4
    assert sorted(map(tuple, all_paths(dag, 0, 3))) == [(0, 1, 3), (0, 2, 3)]
    assert has_cycle(cyclic) is True
    assert has_cycle(dag) is False
    assert bfs_shortest_path(dag, 0, 3) == [0, 1, 3] or bfs_shortest_path(
        dag, 0, 3
    ) == [0, 2, 3]
    assert comp["bfs"] == [0, 1, 2, 3]
    print("All assertions passed.")


if __name__ == "__main__":
    _demo()
