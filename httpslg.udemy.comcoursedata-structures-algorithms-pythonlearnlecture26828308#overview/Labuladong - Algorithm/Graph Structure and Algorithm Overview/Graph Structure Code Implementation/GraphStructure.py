from __future__ import annotations

from typing import Iterable, List, Optional, Sequence, Tuple


class Edge:
    """A directed edge from ``from_`` to ``to`` with an optional weight."""

    __slots__ = ("from_", "to", "weight")

    def __init__(self, from_: int, to: int, weight: float = 1.0) -> None:
        self.from_ = from_
        self.to = to
        self.weight = weight

    def __repr__(self) -> str:
        return f"Edge({self.from_}->{self.to}, w={self.weight})"


class Graph:
    """A weighted directed graph stored with an adjacency list.

    Nodes are labelled ``0 .. n-1``. Each node owns a list of outgoing edges.
    This is the natural representation for sparse graphs (``E << V^2``).
    """

    def __init__(self, n: int, edges: Optional[Iterable[Tuple[int, int, float]]] = None) -> None:
        self._n = n
        self._adj: List[List[Edge]] = [[] for _ in range(n)]
        if edges is not None:
            for e in edges:
                self.add_edge(e[0], e[1], e[2])

    def size(self) -> int:
        return self._n

    def add_edge(self, u: int, v: int, weight: float = 1.0) -> None:
        self._adj[u].append(Edge(u, v, weight))

    def neighbors(self, u: int) -> List[Edge]:
        return self._adj[u]

    def to_adjacency_matrix(self) -> List[List[Optional[float]]]:
        n = self._n
        m: List[List[Optional[float]]] = [[None] * n for _ in range(n)]
        for u in range(n):
            for e in self._adj[u]:
                m[u][e.to] = e.weight
        return m


class UndirectedGraph(Graph):
    """An undirected weighted graph stored with an adjacency list.

    Every undirected edge ``u-v`` is stored twice: once in ``adj[u]`` and once
    in ``adj[v]``.
    """

    def add_edge(self, u: int, v: int, weight: float = 1.0) -> None:
        self._adj[u].append(Edge(u, v, weight))
        self._adj[v].append(Edge(v, u, weight))


class MatrixGraph:
    """A weighted directed graph stored with an adjacency matrix.

    ``matrix[u][v]`` is the weight of edge ``u -> v``, or ``None`` when there is
    no such edge. This is the natural representation for dense graphs
    (``E ~ V^2``).
    """

    def __init__(self, n: int, edges: Optional[Iterable[Tuple[int, int, float]]] = None) -> None:
        self._n = n
        self._m: List[List[Optional[float]]] = [[None] * n for _ in range(n)]
        if edges is not None:
            for e in edges:
                self.add_edge(e[0], e[1], e[2])

    def size(self) -> int:
        return self._n

    def add_edge(self, u: int, v: int, weight: float = 1.0) -> None:
        self._m[u][v] = weight

    def weight(self, u: int, v: int) -> Optional[float]:
        return self._m[u][v]

    def neighbors(self, u: int) -> List[Edge]:
        out: List[Edge] = []
        for v in range(self._n):
            w = self._m[u][v]
            if w is not None:
                out.append(Edge(u, v, w))
        return out

    def to_adjacency_matrix(self) -> List[List[Optional[float]]]:
        return [row[:] for row in self._m]


class UndirectedMatrixGraph(MatrixGraph):
    """An undirected weighted graph stored with an adjacency matrix.

    Adding an edge writes to both ``matrix[u][v]`` and ``matrix[v][u]``.
    """

    def add_edge(self, u: int, v: int, weight: float = 1.0) -> None:
        self._m[u][v] = weight
        self._m[v][u] = weight


def draw_adjacency_list(g: Graph) -> str:
    lines: List[str] = []
    for u in range(g.size()):
        parts = []
        for e in g.neighbors(u):
            parts.append(f"{e.to}(w={e.weight:g})")
        lines.append(f"{u}: [{', '.join(parts)}]")
    return "\n".join(lines)


def draw_matrix(m: List[List[Optional[float]]]) -> str:
    n = len(m)
    header = "   " + "  ".join(f"{i:>4}" for i in range(n))
    lines = [header]
    for i in range(n):
        row = []
        for j in range(n):
            w = m[i][j]
            row.append("   ." if w is None else f"{w:4g}")
        lines.append(f"{i:>2} " + "  ".join(row))
    return "\n".join(lines)


def _demo() -> None:
    edges: Sequence[Tuple[int, int, float]] = [
        (0, 1, 1.0),
        (0, 2, 4.0),
        (1, 2, 2.0),
        (2, 3, 3.0),
    ]

    print("=== Directed weighted graph, adjacency list ===")
    g = Graph(4, edges)
    print(draw_adjacency_list(g))
    print()
    print("size =", g.size())
    print("neighbors(0) =", g.neighbors(0))
    print()

    print("=== Same graph as adjacency matrix ===")
    mg = MatrixGraph(4, edges)
    print(draw_matrix(mg.to_adjacency_matrix()))
    print()

    print("=== Undirected graph, adjacency list (edge stored twice) ===")
    ug = UndirectedGraph(4, edges)
    print(draw_adjacency_list(ug))
    print()

    print("=== Undirected graph, adjacency matrix (symmetric) ===")
    umg = UndirectedMatrixGraph(4, edges)
    print(draw_matrix(umg.to_adjacency_matrix()))
    print()

    assert g.size() == 4
    assert mg.weight(0, 2) == 4.0
    assert mg.weight(0, 3) is None
    assert [e.to for e in g.neighbors(0)] == [1, 2]
    assert [e.to for e in ug.neighbors(1)] == [0, 2]
    assert umg.weight(1, 2) == 2.0 and umg.weight(2, 1) == 2.0
    print("All assertions passed.")


if __name__ == "__main__":
    _demo()
