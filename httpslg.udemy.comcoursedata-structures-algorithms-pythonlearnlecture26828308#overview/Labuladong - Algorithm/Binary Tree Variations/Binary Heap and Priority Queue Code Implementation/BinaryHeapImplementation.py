"""Binary heap / priority queue code implementation.

This module implements a generic priority queue on top of a binary heap,
plus an indexed priority queue (IndexMinPQ) used by graph algorithms such
as Dijkstra's shortest path.

The heap is stored in a 0-indexed array:
    parent(i)  = (i-1)//2
    left(i)    = 2*i+1
    right(i)   = 2*i+2

`less(a, b)` decides the ordering.  The default comparator makes a MAX-heap
(the largest element pops first).  Pass `less=lambda a, b: a > b` to get a
MIN-heap.
"""

from __future__ import annotations

from typing import Callable, Generic, List, Optional, Tuple, TypeVar


T = TypeVar("T")


class PriorityQueue(Generic[T]):
    """A binary-heap priority queue with a pluggable comparator.

    The default comparator `less(a, b) = (a < b)` yields a max-heap: the
    largest item pops first.  For a min-heap pass `less=lambda a, b: a > b`.
    """

    def __init__(self, less: Optional[Callable[[T, T], bool]] = None) -> None:
        self._data: List[T] = []
        self._less = less if less is not None else (lambda a, b: a < b)

    def __len__(self) -> int:
        return len(self._data)

    def is_empty(self) -> bool:
        return len(self._data) == 0

    def contains(self, item: T) -> bool:
        return item in self._data

    def _less_at(self, i: int, j: int) -> bool:
        return self._less(self._data[i], self._data[j])

    def _swap(self, i: int, j: int) -> None:
        self._data[i], self._data[j] = self._data[j], self._data[i]

    def _swim(self, k: int) -> None:
        while k > 0:
            parent = (k - 1) // 2
            if not self._less_at(parent, k):
                break
            self._swap(parent, k)
            k = parent

    def _sink(self, k: int) -> None:
        n = len(self._data)
        while 2 * k + 1 < n:
            j = 2 * k + 1
            if j + 1 < n and self._less_at(j, j + 1):
                j += 1
            if not self._less_at(k, j):
                break
            self._swap(k, j)
            k = j

    def push(self, item: T) -> None:
        """Insert an item and restore the heap order (swim)."""

        self._data.append(item)
        self._swim(len(self._data) - 1)

    def pop(self) -> T:
        """Remove and return the top-priority item (swap root + sink)."""

        if self.is_empty():
            raise IndexError("pop from empty priority queue")
        top = self._data[0]
        last = self._data.pop()
        if self._data:
            self._data[0] = last
            self._sink(0)
        return top

    def peek(self) -> T:
        """Return the top-priority item without removing it."""

        if self.is_empty():
            raise IndexError("peek from empty priority queue")
        return self._data[0]

    def update(self, old_item: T, new_item: T) -> bool:
        """Replace ``old_item`` with ``new_item`` and restore the heap.

        Returns True if ``old_item`` was found, False otherwise.
        """

        try:
            index = self._data.index(old_item)
        except ValueError:
            return False
        self._data[index] = new_item
        self._swim(index)
        self._sink(index)
        return True

    def remove(self, item: T) -> bool:
        """Remove the first occurrence of ``item``; return whether found."""

        try:
            index = self._data.index(item)
        except ValueError:
            return False
        last = self._data.pop()
        if index < len(self._data):
            self._data[index] = last
            self._swim(index)
            self._sink(index)
        return True

    def is_valid(self) -> bool:
        """Verify the heap order property using the comparator."""

        n = len(self._data)
        for i in range(n):
            left = 2 * i + 1
            right = 2 * i + 2
            if left < n and self._less_at(i, left):
                return False
            if right < n and self._less_at(i, right):
                return False
        return True

    def draw(self) -> List[str]:
        """Return ASCII lines rendering the heap as a tree."""

        if not self._data:
            return ["<empty>"]

        def levels() -> List[List[T]]:
            result: List[List[T]] = []
            start = 0
            size = 1
            n = len(self._data)
            while start < n:
                result.append(self._data[start : min(start + size, n)])
                start += size
                size *= 2
            return result

        rows = levels()
        width = 2 ** (len(rows) - 1)
        lines: List[str] = []
        for depth, row in enumerate(rows):
            slot = " " * (width // (2 ** depth) - 1)
            gap = " " * (width // (2 ** max(depth, 1)) + 1)
            lines.append(slot + gap.join(str(v) for v in row))
        return lines


class IndexMinPQ:
    """An indexed priority queue over integer indices 0..capacity-1.

    It is a min-heap of indices: ``del_min`` returns the index with the
    smallest priority.  Three arrays cooperate:

        pq : heap of indices (the heap itself)
        qp : index -> its position in pq  (-1 if absent)
        priority : index -> current priority
    """

    def __init__(self, capacity: int) -> None:
        self._capacity = capacity
        self._pq: List[int] = []
        self._qp: List[int] = [-1] * capacity
        self._priority: List[Optional[float]] = [None] * capacity

    def is_empty(self) -> bool:
        return not self._pq

    def size(self) -> int:
        return len(self._pq)

    def contains(self, i: int) -> bool:
        return self._qp[i] != -1

    def _less(self, a_pos: int, b_pos: int) -> bool:
        return self._priority[self._pq[a_pos]] < self._priority[self._pq[b_pos]]

    def _swap(self, a_pos: int, b_pos: int) -> None:
        ia = self._pq[a_pos]
        ib = self._pq[b_pos]
        self._pq[a_pos], self._pq[b_pos] = ib, ia
        self._qp[ia] = b_pos
        self._qp[ib] = a_pos

    def _swim(self, k: int) -> None:
        while k > 0 and self._less(k, (k - 1) // 2):
            self._swap(k, (k - 1) // 2)
            k = (k - 1) // 2

    def _sink(self, k: int) -> None:
        n = len(self._pq)
        while 2 * k + 1 < n:
            j = 2 * k + 1
            if j + 1 < n and self._less(j + 1, j):
                j += 1
            if not self._less(j, k):
                break
            self._swap(k, j)
            k = j

    def insert(self, i: int, priority: float) -> None:
        """Insert index ``i`` with the given priority."""

        if self.contains(i):
            raise ValueError(f"index {i} already in the queue")
        self._priority[i] = priority
        self._qp[i] = len(self._pq)
        self._pq.append(i)
        self._swim(len(self._pq) - 1)

    def decrease_key(self, i: int, priority: float) -> None:
        """Lower the priority of index ``i``; new value must be smaller."""

        if priority >= self._priority[i]:
            raise ValueError("decrease_key requires a strictly smaller value")
        self._priority[i] = priority
        self._swim(self._qp[i])

    def increase_key(self, i: int, priority: float) -> None:
        """Raise the priority of index ``i``; new value must be larger."""

        if priority <= self._priority[i]:
            raise ValueError("increase_key requires a strictly larger value")
        self._priority[i] = priority
        self._sink(self._qp[i])

    def min_index(self) -> int:
        return self._pq[0]

    def min_priority(self) -> float:
        return self._priority[self._pq[0]]

    def del_min(self) -> int:
        """Remove and return the index with the smallest priority."""

        if self.is_empty():
            raise IndexError("del_min from empty IndexMinPQ")
        top = self._pq[0]
        self._swap(0, len(self._pq) - 1)
        self._pq.pop()
        self._qp[top] = -1
        if self._pq:
            self._sink(0)
        return top


def dijkstra(adj: List[List[Tuple[int, float]]], source: int) -> List[float]:
    """Shortest distances from ``source`` using an IndexMinPQ.

    ``adj[u]`` holds ``(v, weight)`` edges.
    """

    n = len(adj)
    dist = [float("inf")] * n
    dist[source] = 0.0
    pq = IndexMinPQ(n)
    pq.insert(source, 0.0)
    while not pq.is_empty():
        u = pq.del_min()
        for v, w in adj[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                if pq.contains(v):
                    pq.decrease_key(v, dist[v])
                else:
                    pq.insert(v, dist[v])
    return dist


if __name__ == "__main__":
    print("=== Priority queue demo ===")

    pq = PriorityQueue[int]()
    for value in [3, 1, 4, 1, 5, 9, 2, 6]:
        pq.push(value)
        assert pq.is_valid()
    assert pq.peek() == 9
    max_order = []
    while not pq.is_empty():
        max_order.append(pq.pop())
    assert max_order == [9, 6, 5, 4, 3, 2, 1, 1]
    print("max-heap pop order:", max_order)

    min_pq = PriorityQueue[int](less=lambda a, b: a > b)
    for value in [3, 1, 4, 1, 5, 9, 2, 6]:
        min_pq.push(value)
    min_order = []
    while not min_pq.is_empty():
        min_order.append(min_pq.pop())
    assert min_order == [1, 1, 2, 3, 4, 5, 6, 9]
    print("min-heap pop order:", min_order)

    upd = PriorityQueue[int]()
    for value in [5, 10, 3]:
        upd.push(value)
    assert upd.update(5, 100) is True
    assert upd.peek() == 100
    assert upd.update(999, 1) is False
    assert upd.remove(10) is True
    rest = []
    while not upd.is_empty():
        rest.append(upd.pop())
    assert rest == [100, 3]
    print("after update(5,100) and remove(10):", rest)

    print("\nIndexMinPQ basic ops...")
    imq = IndexMinPQ(5)
    imq.insert(0, 0.0)
    imq.insert(1, 2.0)
    imq.insert(2, 1.0)
    assert imq.min_index() == 0
    imq.decrease_key(1, -1.0)
    assert imq.min_index() == 1
    assert imq.size() == 3 and imq.contains(1)
    assert imq.del_min() == 1
    assert imq.del_min() == 0
    assert imq.del_min() == 2
    assert imq.is_empty()
    imq.insert(3, 4.0)
    imq.insert(4, 3.0)
    imq.increase_key(3, 5.0)
    assert imq.min_index() == 4
    assert imq.del_min() == 4
    assert imq.del_min() == 3
    print("IndexMinPQ basic ops passed.")

    print("\nDijkstra with IndexMinPQ...")
    graph = [
        [(1, 1.0), (2, 4.0)],
        [(0, 1.0), (2, 2.0), (3, 5.0)],
        [(0, 4.0), (1, 2.0), (3, 1.0)],
        [(1, 5.0), (2, 1.0)],
    ]
    dists = dijkstra(graph, 0)
    assert dists == [0.0, 1.0, 3.0, 4.0], dists
    print("shortest distances from node 0:", dists)

    print("\nAll assertions passed.")
