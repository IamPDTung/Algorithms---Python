from __future__ import annotations

from collections import deque
from typing import Deque, Dict, List, Optional, Sequence, Tuple


class UndirectedGraph:
    """Undirected graph on nodes ``0 .. n-1`` (adjacency list)."""

    def __init__(self, n: int, edges: Optional[Sequence[Tuple[int, int]]] = None) -> None:
        self._n = n
        self._adj: List[List[int]] = [[] for _ in range(n)]
        self._edge_count = 0
        if edges is not None:
            for u, v in edges:
                self.add_edge(u, v)

    def size(self) -> int:
        return self._n

    def add_edge(self, u: int, v: int) -> None:
        self._adj[u].append(v)
        self._adj[v].append(u)
        self._edge_count += 1

    def neighbors(self, u: int) -> List[int]:
        return self._adj[u]

    def degree(self, u: int) -> int:
        return len(self._adj[u])

    def degrees(self) -> List[int]:
        return [len(self._adj[u]) for u in range(self._n)]

    def edge_count(self) -> int:
        return self._edge_count


def is_connected(g: UndirectedGraph) -> bool:
    """True if every non-isolated node is reachable from any other."""
    n = g.size()
    if n == 0:
        return True
    start = next((i for i in range(n) if g.degree(i) > 0), 0)
    visited = [False] * n
    q: Deque[int] = deque([start])
    visited[start] = True
    while q:
        u = q.popleft()
        for v in g.neighbors(u):
            if not visited[v]:
                visited[v] = True
                q.append(v)
    for i in range(n):
        if g.degree(i) > 0 and not visited[i]:
            return False
    return True


def has_eulerian_circuit(g: UndirectedGraph) -> bool:
    """All edges can be used once, returning to the start node."""
    if not is_connected(g):
        return False
    return all(d % 2 == 0 for d in g.degrees())


def has_eulerian_path(g: UndirectedGraph) -> Tuple[bool, List[int]]:
    """Whether an Eulerian path exists; if so, the two odd-degree starts.

    Returns ``(exists, start_nodes)`` where ``start_nodes`` lists the 0, 1, or
    2 nodes with odd degree (a valid starting point must be one of them).
    """
    if not is_connected(g):
        return False, []
    odd = [i for i, d in enumerate(g.degrees()) if d % 2 == 1]
    if len(odd) == 0:
        return True, []
    if len(odd) == 2:
        return True, odd
    return False, odd


def hierholzer_undirected(g: UndirectedGraph, start: Optional[int] = None) -> List[int]:
    """Find an Eulerian circuit (or path) via Hierholzer's algorithm.

    Uses a stack-based DFS and removes edges as they are used, so no 2D
    visited array is needed. Returns the node sequence.
    """
    n = g.size()
    adj: List[Deque[int]] = [deque(sorted(g.neighbors(u))) for u in range(n)]

    if start is None:
        if any(d % 2 == 1 for d in g.degrees()):
            start = next(i for i, d in enumerate(g.degrees()) if d % 2 == 1)
        else:
            start = next((i for i in range(n) if g.degree(i) > 0), 0)

    stack: List[int] = [start]
    path: List[int] = []
    while stack:
        u = stack[-1]
        if adj[u]:
            v = adj[u].popleft()
            # remove the reverse half-edge in an undirected graph
            rev = adj[v]
            for idx, x in enumerate(rev):
                if x == u:
                    del rev[idx]
                    break
            stack.append(v)
        else:
            path.append(stack.pop())
    path.reverse()
    return path


class DirectedGraph:
    """Directed graph on nodes ``0 .. n-1`` (adjacency list)."""

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

    def indegree(self, u: int) -> int:
        return sum(1 for v in range(self._n) if u in self._adj[v])

    def outdegree(self, u: int) -> int:
        return len(self._adj[u])

    def degrees(self) -> Tuple[List[int], List[int]]:
        outd = [len(self._adj[u]) for u in range(self._n)]
        ind = [0] * self._n
        for u in range(self._n):
            for v in self._adj[u]:
                ind[v] += 1
        return ind, outd


def has_eulerian_path_directed(g: DirectedGraph) -> Tuple[bool, Optional[int]]:
    """Eulerian path in a directed graph.

    A path exists if (connectivity of non-zero-degree nodes) holds and at most
    one node has ``out - in == 1`` (start), at most one has ``in - out == 1``
    (end), and all others have ``in == out``. Returns ``(exists, start)``.
    """
    n = g.size()
    ind, outd = g.degrees()

    start_diff = [i for i in range(n) if outd[i] - ind[i] == 1]
    end_diff = [i for i in range(n) if ind[i] - outd[i] == 1]
    others_ok = all(
        ind[i] == outd[i]
        for i in range(n)
        if (i not in start_diff and i not in end_diff)
    )
    if not (len(start_diff) <= 1 and len(end_diff) <= 1 and others_ok):
        return False, None

    start = start_diff[0] if start_diff else next(
        (i for i in range(n) if outd[i] > 0), 0
    )

    # connectivity: every node with edges reachable from start
    visited = [False] * n
    q: Deque[int] = deque([start])
    visited[start] = True
    while q:
        u = q.popleft()
        for v in g.neighbors(u):
            if not visited[v]:
                visited[v] = True
                q.append(v)
    for i in range(n):
        if (outd[i] > 0 or ind[i] > 0) and not visited[i]:
            return False, None
    return True, start


def hierholzer_directed(g: DirectedGraph, start: Optional[int] = None) -> List[int]:
    """Find an Eulerian path/circuit in a directed graph via Hierholzer."""
    n = g.size()
    adj: List[Deque[int]] = [deque(sorted(g.neighbors(u))) for u in range(n)]
    if start is None:
        ind, outd = g.degrees()
        start = next((i for i in range(n) if outd[i] - ind[i] == 1),
                     next((i for i in range(n) if outd[i] > 0), 0))
    stack: List[int] = [start]
    path: List[int] = []
    while stack:
        u = stack[-1]
        if adj[u]:
            v = adj[u].popleft()
            stack.append(v)
        else:
            path.append(stack.pop())
    path.reverse()
    return path


def _demo() -> None:
    print("=== The Seven Bridges of Konigsberg (undirected) ===")
    # 4 regions, 7 bridges. Every region has odd degree -> no Euler circuit/path.
    koenigsberg = UndirectedGraph(4, [
        (0, 1), (0, 1), (0, 2), (0, 2),
        (0, 3), (1, 3), (2, 3),
    ])
    print("degrees:", koenigsberg.degrees())
    print("connected:", is_connected(koenigsberg))
    ok, starts = has_eulerian_path(koenigsberg)
    print("Eulerian path exists:", ok, "| odd-degree starts:", starts)
    print("Eulerian circuit exists:", has_eulerian_circuit(koenigsberg))
    print()

    print("=== A solvable one-stroke puzzle (exactly 2 odd nodes) ===")
    # square with a diagonal: nodes 0..3, diagonal 1-3 -> odd nodes 0 and 2
    puzzle = UndirectedGraph(4, [(0, 1), (1, 2), (2, 3), (3, 0), (1, 3)])
    print("degrees:", puzzle.degrees())
    ok, starts = has_eulerian_path(puzzle)
    print("Eulerian path exists:", ok, "| must start at one of:", starts)
    if ok:
        sp = starts[0] if starts else 0
        route = hierholzer_undirected(puzzle, sp)
        print("one-stroke route:", route)
    print()

    print("=== A graph with an Eulerian CIRCUIT (all even) ===")
    even = UndirectedGraph(4, [(0, 1), (1, 2), (2, 3), (3, 0)])
    print("degrees:", even.degrees())
    print("Eulerian circuit exists:", has_eulerian_circuit(even))
    print("circuit route:", hierholzer_undirected(even, 0))
    print()

    print("=== Directed Eulerian path (word chains / routes) ===")
    dg = DirectedGraph(4, [(0, 1), (1, 2), (2, 0), (0, 3), (3, 2)])
    ok, start = has_eulerian_path_directed(dg)
    print("directed Eulerian path exists:", ok, "| start:", start)
    if ok:
        print("directed route:", hierholzer_directed(dg, start))
    print()

    # --- assertions ---
    assert koenigsberg.degrees() == [5, 3, 3, 3]
    assert has_eulerian_path(koenigsberg)[0] is False
    assert has_eulerian_circuit(koenigsberg) is False

    ok2, starts2 = has_eulerian_path(puzzle)
    assert ok2 is True and sorted(starts2) == [1, 3]
    route2 = hierholzer_undirected(puzzle, starts2[0])
    assert route2[0] in starts2 and route2[-1] == route2[-1]
    # verify every undirected edge is used exactly once
    used = set()
    for a, b in zip(route2, route2[1:]):
        used.add(frozenset((a, b)))
    assert len(used) == 5, used

    assert has_eulerian_circuit(even) is True
    route3 = hierholzer_undirected(even, 0)
    used3 = set()
    for a, b in zip(route3, route3[1:]):
        used3.add(frozenset((a, b)))
    assert len(used3) == 4 and route3[0] == route3[-1]

    ok4, start4 = has_eulerian_path_directed(dg)
    assert ok4 is True
    route4 = hierholzer_directed(dg, start4)
    used4 = set()
    for a, b in zip(route4, route4[1:]):
        used4.add((a, b))
    assert len(used4) == 5, used4
    print("All assertions passed.")


if __name__ == "__main__":
    _demo()
