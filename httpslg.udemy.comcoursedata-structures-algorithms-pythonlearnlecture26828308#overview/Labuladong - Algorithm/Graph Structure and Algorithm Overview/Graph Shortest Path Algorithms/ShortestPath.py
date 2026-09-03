from __future__ import annotations

import heapq
from collections import deque
from typing import Dict, Deque, List, Optional, Sequence, Tuple


class WeightedGraph:
    """Directed weighted graph on nodes ``0 .. n-1`` (adjacency list)."""

    def __init__(
        self,
        n: int,
        edges: Optional[Sequence[Tuple[int, int, float]]] = None,
    ) -> None:
        self._n = n
        self._adj: List[List[Tuple[int, float]]] = [[] for _ in range(n)]
        if edges is not None:
            for u, v, w in edges:
                self.add_edge(u, v, w)

    def size(self) -> int:
        return self._n

    def add_edge(self, u: int, v: int, weight: float) -> None:
        self._adj[u].append((v, weight))

    def neighbors(self, u: int) -> List[Tuple[int, float]]:
        return self._adj[u]


# ---------------------------------------------------------------------------
# Dijkstra: BFS + greedy + priority queue. No negative weights allowed.
# ---------------------------------------------------------------------------

def dijkstra(g: WeightedGraph, src: int) -> Tuple[List[float], List[int]]:
    n = g.size()
    dist = [float("inf")] * n
    prev: List[int] = [-1] * n
    dist[src] = 0.0
    pq: List[Tuple[float, int]] = [(0.0, src)]
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


def reconstruct(prev: List[int], dst: int) -> List[int]:
    path: List[int] = []
    cur = dst
    while cur != -1:
        path.append(cur)
        cur = prev[cur]
    path.reverse()
    return path


# ---------------------------------------------------------------------------
# A*: Dijkstra + a heuristic for point-to-point searches.
# ---------------------------------------------------------------------------

def a_star(
    g: WeightedGraph,
    src: int,
    dst: int,
    heuristic: Optional[Sequence[float]] = None,
) -> Tuple[Optional[float], List[int]]:
    """A* point-to-point search.

    ``heuristic`` is an estimate of the distance from each node to ``dst``.
    A good heuristic (e.g. straight-line distance) makes the search reach the
    target faster. The heuristic must be admissible (never overestimate) for
    correctness.
    """
    n = g.size()
    if heuristic is None:
        heuristic = [0.0] * n
    dist = [float("inf")] * n
    prev: List[int] = [-1] * n
    dist[src] = 0.0
    # priority = g-score (dist) + h-score (heuristic)
    pq: List[Tuple[float, float, int]] = [
        (0.0 + heuristic[src], 0.0, src)
    ]

    while pq:
        _, d, u = heapq.heappop(pq)
        if u == dst:
            return dist[dst], reconstruct(prev, dst)
        if d > dist[u]:
            continue
        for v, w in g.neighbors(u):
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(pq, (nd + heuristic[v], nd, v))
    return None, []


# ---------------------------------------------------------------------------
# Bellman-Ford / SPFA: BFS-like, handles negative weights and detects
# negative cycles.
# ---------------------------------------------------------------------------

def bellman_ford(
    g: WeightedGraph, src: int
) -> Tuple[Optional[List[float]], List[int]]:
    """Bellman-Ford: returns (dist, prev) or (None, []) on a negative cycle."""
    n = g.size()
    dist = [float("inf")] * n
    prev: List[int] = [-1] * n
    dist[src] = 0.0

    edges: List[Tuple[int, int, float]] = []
    for u in range(n):
        for v, w in g.neighbors(u):
            edges.append((u, v, w))

    for _ in range(n - 1):
        updated = False
        for u, v, w in edges:
            if dist[u] != float("inf") and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                prev[v] = u
                updated = True
        if not updated:
            break

    # one more pass to detect negative cycles
    for u, v, w in edges:
        if dist[u] != float("inf") and dist[u] + w < dist[v]:
            return None, []  # negative cycle reachable from src
    return dist, prev


def spfa(g: WeightedGraph, src: int) -> Tuple[Optional[List[float]], List[int]]:
    """Queue-based Bellman-Ford (SPFA). Returns (dist, prev) or (None, [])."""
    n = g.size()
    dist = [float("inf")] * n
    prev: List[int] = [-1] * n
    in_queue = [False] * n
    relax_count = [0] * n
    dist[src] = 0.0
    q: Deque[int] = deque([src])
    in_queue[src] = True

    while q:
        u = q.popleft()
        in_queue[u] = False
        for v, w in g.neighbors(u):
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                prev[v] = u
                if not in_queue[v]:
                    q.append(v)
                    in_queue[v] = True
                    relax_count[v] += 1
                    if relax_count[v] >= n:
                        return None, []  # negative cycle
    return dist, prev


# ---------------------------------------------------------------------------
# Floyd-Warshall: dynamic programming, all-pairs shortest path.
# ---------------------------------------------------------------------------

def floyd_warshall(g: WeightedGraph) -> List[List[float]]:
    n = g.size()
    dist = [[float("inf")] * n for _ in range(n)]
    for u in range(n):
        dist[u][u] = 0.0
    for u in range(n):
        for v, w in g.neighbors(u):
            dist[u][v] = min(dist[u][v], w)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist


def _demo() -> None:
    print("=== Graph for shortest paths (directed, weighted) ===")
    #   0 ->1(1) ->2(2) ->3(1)
    #   |         ^
    #   +-------> 2(4)  (alternative route)
    g = WeightedGraph(4, [
        (0, 1, 1.0),
        (1, 2, 2.0),
        (2, 3, 1.0),
        (0, 2, 4.0),
    ])

    print("edges:")
    for u in range(g.size()):
        for v, w in g.neighbors(u):
            print(f"  {u} -> {v}  (w={w:g})")
    print()

    dist, prev = dijkstra(g, 0)
    print("=== Dijkstra (single-source, no negative weights) ===")
    print("dist to 0..3:", dist)
    print("path to 3:", reconstruct(prev, 3))
    print()

    print("=== A* (point-to-point, with a heuristic) ===")
    # heuristic: pretend node 3 is reachable, others estimate 0 except 2->3
    h = [3.0, 2.0, 1.0, 0.0]
    adist, apath = a_star(g, 0, 3, h)
    print("A* dist to 3:", adist, "| path:", apath)
    print()

    print("=== Bellman-Ford & SPFA (negative weights OK) ===")
    gn = WeightedGraph(4, [
        (0, 1, 1.0),
        (1, 2, -2.0),   # negative edge
        (2, 3, 1.0),
        (0, 2, 4.0),
    ])
    bd, bp = bellman_ford(gn, 0)
    sd, sp = spfa(gn, 0)
    print("Bellman-Ford dist:", bd, "| path to 3:", reconstruct(bp, 3))
    print("SPFA dist:", sd, "| path to 3:", reconstruct(sp, 3))
    print()

    print("=== Negative cycle detection ===")
    gc = WeightedGraph(2, [(0, 1, 1.0), (1, 0, -3.0)])  # 1 + (-3) < 0
    print("Bellman-Ford detects negative cycle:", bellman_ford(gc, 0)[0] is None)
    print("SPFA detects negative cycle:", spfa(gc, 0)[0] is None)
    print()

    print("=== Floyd-Warshall (all-pairs) ===")
    mat = floyd_warshall(g)
    print("dist matrix:")
    print("      0     1     2     3")
    for i in range(4):
        print(f"  {i}  " + "  ".join(f"{mat[i][j]:5.1f}" for j in range(4)))
    print()

    # ---- assertions ----
    assert dist == [0.0, 1.0, 3.0, 4.0]
    assert reconstruct(prev, 3) == [0, 1, 2, 3]
    assert adist == 4.0 and apath == [0, 1, 2, 3]
    assert bd == [0.0, 1.0, -1.0, 0.0]
    assert sd == [0.0, 1.0, -1.0, 0.0]
    assert bellman_ford(gc, 0)[0] is None
    assert spfa(gc, 0)[0] is None
    assert mat[0][3] == 4.0 and mat[1][3] == 3.0
    print("All assertions passed.")


if __name__ == "__main__":
    _demo()
