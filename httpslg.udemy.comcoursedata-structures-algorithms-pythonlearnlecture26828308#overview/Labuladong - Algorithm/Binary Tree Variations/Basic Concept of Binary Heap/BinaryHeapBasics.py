"""Basic concept of a binary heap.

A binary heap is a complete binary tree that satisfies the heap order
property.  For a max-heap, every parent is greater than or equal to its
children, so the largest element always sits at the root.  Because the tree
is complete, it can live inside a flat array with pure index arithmetic
(index 1 is the root, parent of i is i//2, children of i are 2i and 2i+1).

This module demonstrates the two core operations (swim and sink), the
O(N) build-heap via bottom-up sinking, and heap sort.
"""

from __future__ import annotations

import random
from typing import List, Optional, Sequence, TypeVar


T = TypeVar("T")


class MaxHeap:
    """A binary max-heap stored in a 1-indexed array (index 0 unused)."""

    def __init__(self) -> None:
        self._data: List[Optional[T]] = [None]

    # ------------------------------------------------------------- basics

    def __len__(self) -> int:
        return len(self._data) - 1

    def is_empty(self) -> bool:
        return len(self) == 0

    def peek(self) -> T:
        """Return the largest element without removing it."""

        if self.is_empty():
            raise IndexError("peek from empty heap")
        return self._data[1]

    def _swap(self, i: int, j: int) -> None:
        self._data[i], self._data[j] = self._data[j], self._data[i]

    # ------------------------------------------------------------- helpers

    def _swim(self, k: int) -> None:
        """Bubble a large value at position k up toward the root."""

        while k > 1 and self._data[k // 2] < self._data[k]:
            self._swap(k // 2, k)
            k //= 2

    def _sink(self, k: int) -> None:
        """Push a small value at position k down toward a leaf."""

        n = len(self)
        while 2 * k <= n:
            j = 2 * k
            if j < n and self._data[j] < self._data[j + 1]:
                j += 1
            if self._data[k] >= self._data[j]:
                break
            self._swap(k, j)
            k = j

    # ------------------------------------------------------------- operations

    def insert(self, value: T) -> None:
        """Add a value: append at the end, then swim it up."""

        self._data.append(value)
        self._swim(len(self))

    def del_max(self) -> T:
        """Remove and return the largest element."""

        if self.is_empty():
            raise IndexError("del_max from empty heap")
        maximum = self._data[1]
        last = self._data.pop()
        if not self.is_empty():
            self._data[1] = last
            self._sink(1)
        return maximum

    # ------------------------------------------------------------- integrity

    def is_valid(self) -> bool:
        """Return True if the heap order property holds everywhere."""

        n = len(self)
        for i in range(1, n + 1):
            if 2 * i <= n and self._data[i] < self._data[2 * i]:
                return False
            if 2 * i + 1 <= n and self._data[i] < self._data[2 * i + 1]:
                return False
        return True

    # ------------------------------------------------------------- building

    @classmethod
    def heapify(cls, values: Sequence[T]) -> MaxHeap:
        """Build a heap in O(N) by sinking from the bottom up."""

        heap = cls()
        heap._data = [None] + list(values)
        n = len(heap)
        for k in range(n // 2, 0, -1):
            heap._sink(k)
        return heap

    # ------------------------------------------------------------- sorting

    @staticmethod
    def heap_sort(values: List[T]) -> List[T]:
        """Return a new list sorted in ascending order using a max-heap."""

        heap = MaxHeap.heapify(values)
        result: List[T] = []
        while not heap.is_empty():
            result.append(heap.del_max())
        result.reverse()
        return result

    # ------------------------------------------------------------- drawing

    def to_levels(self) -> List[List[T]]:
        """Return values grouped by tree level, left to right."""

        if self.is_empty():
            return []
        n = len(self)
        levels: List[List[T]] = []
        start = 1
        while start <= n:
            end = min(2 * start, n + 1)
            levels.append([self._data[i] for i in range(start, end)])
            start = end
        return levels

    def draw(self) -> List[str]:
        """Return ASCII lines rendering the heap as a tree."""

        levels = self.to_levels()
        if not levels:
            return ["<empty heap>"]
        width = 2 ** (len(levels) - 1)
        lines: List[str] = []
        for depth, level in enumerate(levels):
            slot = " " * (width // (2 ** depth) - 1)
            gap = " " * (width // (2 ** max(depth, 1)) + 1)
            line = slot + gap.join(str(v) for v in level)
            lines.append(line)
        return lines


if __name__ == "__main__":
    print("=== Binary heap basics demo ===")

    heap = MaxHeap()
    for value in [3, 1, 4, 1, 5, 9, 2, 6]:
        heap.insert(value)
        assert heap.is_valid()

    assert len(heap) == 8
    assert heap.peek() == 9

    popped = [heap.del_max()]
    for _ in range(len(heap)):
        assert heap.is_valid()
        popped.append(heap.del_max())
    assert popped == [9, 6, 5, 4, 3, 2, 1, 1]
    assert heap.is_empty()

    print("insert/pop order (max first):", popped)

    built = MaxHeap.heapify([5, 3, 8, 1, 9, 2, 7, 4, 6])
    assert built.is_valid()
    assert built.peek() == 9
    order = [built.del_max() for _ in range(len(built))]
    assert order == [9, 8, 7, 6, 5, 4, 3, 2, 1]

    print("\nheapify([5,3,8,1,9,2,7,4,6]) tree:")
    built2 = MaxHeap.heapify([5, 3, 8, 1, 9, 2, 7, 4, 6])
    for line in built2.draw():
        print("   " + line)

    assert MaxHeap.heap_sort([5, 3, 8, 1, 9, 2, 7, 4, 6]) == [
        1, 2, 3, 4, 5, 6, 7, 8, 9,
    ]
    assert MaxHeap.heap_sort([]) == []
    assert MaxHeap.heap_sort([7]) == [7]

    random.seed(7)
    for _ in range(50):
        data = [random.randint(-50, 50) for _ in range(random.randint(0, 60))]
        assert MaxHeap.heap_sort(data) == sorted(data)

    print("\nheap_sort randomized check passed for 50 arrays.")
    print("All assertions passed.")
