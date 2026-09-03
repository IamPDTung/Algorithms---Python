from __future__ import annotations

import heapq
from typing import List, Optional, Sequence, Tuple


class UnionFind:
    """Disjoint-set with path compression + union by size."""

    def __init__(self, n: int) -> None:
        self._parent = list(range(n))
        self._size = [1] * n
        self._count = n

    def find(self, x: int) -> int:
        root = x
        while self._parent[root] != root:
            root = self._parent[root]
        while self._parent[x] != x:  # path compression
            nxt = self._parent[x]
            self._parent[x] = root
            x = nxt
        return root

    def union(self, a: int, b: int) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self._size[ra] < self._size[rb]:
            ra, rb = rb, ra
        self._parent[rb] = ra
        self._size[ra] += self._size[rb]
        self._count -= 1
        return True

    def connected(self, a: int, b: int) -> bool:
        return self.find(a) == self.find(b)

    def count(self) -> int:
        return self._count


class UndirectedWeightedGraph:
    """Undirected weighted graph on nodes ``0 .. n-1`` (adjacency list)."""

    def __init__(
        self,
        n: int,
        edges: Optional[Sequence[Tuple[int, int, float]]] = None,
    ) -> None:
        self._n = n
        self._adj: List[List[Tuple[int, float]]] = [[] for _ in range(n)]
        self._edges: List[Tuple[int, int, float]] = []
        if edges is not None:
            for u, v, w in edges:
                self.add_edge(u, v, w)

    def size(self) -> int:
        return self._n

    def add_edge(self, u: int, v: int, weight: float) -> None:
        self._adj[u].append((v, weight))
        self._adj[v].append((u, weight))
        self._edges.append((u, v, weight))

    def neighbors(self, u: int) -> List[Tuple[int, float]]:
        return self._adj[u]

    def all_edges(self) -> List[Tuple[int, int, float]]:
        return list(self._edges)


# ---------------------------------------------------------------------------
# Kruskal: sort edges by weight, add the cheapest that does not create a cycle.
# Uses Union-Find to test connectivity in O(alpha).
# ---------------------------------------------------------------------------

def kruskal(g: UndirectedWeightedGraph) -> Tuple[float, List[Tuple[int, int, float]]]:
    edges = sorted(g.all_edges(), key=lambda e: e[2])
    uf = UnionFind(g.size())
    mst: List[Tuple[int, int, float]] = []
    total = 0.0
    for u, v, w in edges:
        if uf.union(u, v):          # add only if it connects two components
            mst.append((u, v, w))
            total += w
    return total, mst


# ---------------------------------------------------------------------------
# Prim: grow one component from a start node, always adding the cheapest edge
# that connects the component to the outside. Priority queue = Dijkstra-like.
# ---------------------------------------------------------------------------

def prim(g: UndirectedWeightedGraph, start: int = 0) -> Tuple[float, List[Tuple[int, int, float]]]:
    n = g.size()
    in_mst = [False] * n
    pq: List[Tuple[float, int, int]] = []   # (weight, from, to)
    in_mst[start] = True
    for v, w in g.neighbors(start):
        heapq.heappush(pq, (w, start, v))

    mst: List[Tuple[int, int, float]] = []
    total = 0.0
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


def _demo() -> None:
    # A weighted connected graph on 6 nodes.
    #   0 --1-- 1 --3-- 2
    #   |       |       |
    #   4       2       1
    #   |       |       |
    #   3 --2-- 4 --5-- 5
    edges: Sequence[Tuple[int, int, float]] = [
        (0, 1, 1.0), (1, 2, 3.0), (0, 3, 4.0),
        (1, 4, 2.0), (2, 5, 1.0), (3, 4, 2.0),
        (4, 5, 5.0),
    ]
    g = UndirectedWeightedGraph(6, edges)

    print("=== The graph (undirected, weighted) ===")
    for u, v, w in g.all_edges():
        print(f"  {u} - {v}  (w={w:g})")
    print()

    print("=== Kruskal's algorithm ===")
    k_total, k_mst = kruskal(g)
    print("MST edges:", [(u, v, w) for u, v, w in k_mst])
    print("total weight:", k_total)
    print()

    print("=== Prim's algorithm ===")
    p_total, p_mst = prim(g, 0)
    print("MST edges:", [(u, v, w) for u, v, w in p_mst])
    print("total weight:", p_total)
    print()

    print("=== Which edges were chosen? (1 + 1 + 2 + 2 + 3 = 9) ===")
    chosen = {frozenset((u, v)) for u, v, _ in k_mst}
    print("chosen edge set (Kruskal):",
          sorted(tuple(sorted(e)) for e in chosen))
    print()

    # A spanning tree on 6 nodes uses exactly 5 edges.
    assert len(k_mst) == 5 and len(p_mst) == 5
    assert abs(k_total - 9.0) < 1e-9
    assert abs(p_total - 9.0) < 1e-9
    assert {frozenset((u, v)) for u, v, _ in k_mst} == \
           {frozenset((u, v)) for u, v, _ in p_mst}
    print("All assertions passed.")


if __name__ == "__main__":
    _demo()
