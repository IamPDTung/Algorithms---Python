from __future__ import annotations

import random
from typing import List, Optional, Sequence, Tuple


class SegmentTree:
    """A sum-aggregate segment tree with point update and range query.

    Leaves store the array elements; every internal node stores the sum of
    its interval [start, end]. The tree lives in a flat array of size 4*N
    with the classic 1-indexed heap layout (children of node are 2*node and
    2*node+1).
    """

    def __init__(self, values: Sequence[int]):
        """Build the segment tree from the given values."""
        self.values: List[int] = list(values)
        self.n: int = len(self.values)
        self.tree: List[int] = [0] * (4 * self.n)
        if self.n > 0:
            self._build(1, 0, self.n - 1)

    def _build(self, node: int, start: int, end: int) -> None:
        """Recursively build the tree; leaves hold values, parents hold sums."""
        if start == end:
            self.tree[node] = self.values[start]
            return
        mid = (start + end) // 2
        self._build(2 * node, start, mid)
        self._build(2 * node + 1, mid + 1, end)
        self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]

    def query(self, left: int, right: int) -> int:
        """Return the inclusive sum over the range [left, right]."""
        return self._query(1, 0, self.n - 1, left, right)

    def _query(self, node: int, start: int, end: int, left: int, right: int) -> int:
        """Recursive range query with full-overlap, partial and no-overlap cases."""
        if right < start or end < left:
            return 0
        if left <= start and end <= right:
            return self.tree[node]
        mid = (start + end) // 2
        return self._query(2 * node, start, mid, left, right) + self._query(
            2 * node + 1, mid + 1, end, left, right
        )

    def update(self, index: int, value: int) -> None:
        """Set values[index] = value and refresh every ancestor on the path."""
        self.values[index] = value
        self._update(1, 0, self.n - 1, index, value)

    def _update(self, node: int, start: int, end: int, index: int, value: int) -> None:
        """Recursive point update; recompute sums on the way back up."""
        if start == end:
            self.tree[node] = value
            return
        mid = (start + end) // 2
        if index <= mid:
            self._update(2 * node, start, mid, index, value)
        else:
            self._update(2 * node + 1, mid + 1, end, index, value)
        self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]

    def to_list(self) -> List[int]:
        """Return a copy of the underlying values array."""
        return list(self.values)

    def size(self) -> int:
        """Return the number of elements stored."""
        return self.n

    def draw(self) -> List[str]:
        """Render the tree as ASCII lines, each node showing [l,r]=sum."""
        lines: List[str] = []
        self._draw(1, 0, self.n - 1, 0, lines)
        return lines

    def _draw(self, node: int, start: int, end: int, depth: int, lines: List[str]) -> None:
        """Recursively collect one text line per tree node, indented by depth."""
        if start > end:
            return
        label = f"[{start},{end}]={self.tree[node]}"
        if start == end:
            label += " (leaf)"
        lines.append("  " * depth + label)
        if start != end:
            mid = (start + end) // 2
            self._draw(2 * node, start, mid, depth + 1, lines)
            self._draw(2 * node + 1, mid + 1, end, depth + 1, lines)


class LazySegmentTree:
    """A sum segment tree with lazy range-add and range-sum queries.

    Besides the sum tree, a parallel `lazy` array records pending additions
    that still apply to a whole interval. A pending tag is pushed down to
    the children only when a later operation must visit them.
    """

    def __init__(self, values: Sequence[int]):
        """Build the tree and the lazy array from the given values."""
        self.values: List[int] = list(values)
        self.n: int = len(self.values)
        self.tree: List[int] = [0] * (4 * self.n)
        self.lazy: List[int] = [0] * (4 * self.n)
        if self.n > 0:
            self._build(1, 0, self.n - 1)

    def _build(self, node: int, start: int, end: int) -> None:
        """Recursively build the sum tree (same shape as SegmentTree)."""
        if start == end:
            self.tree[node] = self.values[start]
            return
        mid = (start + end) // 2
        self._build(2 * node, start, mid)
        self._build(2 * node + 1, mid + 1, end)
        self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]

    def _push(self, node: int, start: int, end: int) -> None:
        """Propagate the lazy tag of `node` to its children and clear it."""
        if self.lazy[node] == 0 or start == end:
            return
        delta = self.lazy[node]
        mid = (start + end) // 2
        self.tree[2 * node] += delta * (mid - start + 1)
        self.tree[2 * node + 1] += delta * (end - mid)
        self.lazy[2 * node] += delta
        self.lazy[2 * node + 1] += delta
        self.lazy[node] = 0

    def range_add(self, left: int, right: int, delta: int) -> None:
        """Add `delta` to every element in the inclusive range [left, right]."""
        self._update_range(1, 0, self.n - 1, left, right, delta)

    def _update_range(
        self, node: int, start: int, end: int, left: int, right: int, delta: int
    ) -> None:
        """Recursive range add; a fully covered node only gets a lazy tag."""
        if right < start or end < left:
            return
        if left <= start and end <= right:
            self.tree[node] += delta * (end - start + 1)
            self.lazy[node] += delta
            return
        self._push(node, start, end)
        mid = (start + end) // 2
        self._update_range(2 * node, start, mid, left, right, delta)
        self._update_range(2 * node + 1, mid + 1, end, left, right, delta)
        self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]

    def range_sum(self, left: int, right: int) -> int:
        """Return the inclusive sum over the range [left, right]."""
        return self._query(1, 0, self.n - 1, left, right)

    def _query(self, node: int, start: int, end: int, left: int, right: int) -> int:
        """Recursive range sum; push lazy tags down before descending."""
        if right < start or end < left:
            return 0
        if left <= start and end <= right:
            return self.tree[node]
        self._push(node, start, end)
        mid = (start + end) // 2
        return self._query(2 * node, start, mid, left, right) + self._query(
            2 * node + 1, mid + 1, end, left, right
        )

    def point_get(self, index: int) -> int:
        """Return the current value stored at the given index."""
        return self.range_sum(index, index)

    def to_list(self) -> List[int]:
        """Return the current values by reading every index through the tree."""
        return [self.point_get(i) for i in range(self.n)]


def _verify_segment_tree(rng: random.Random, rounds: int = 200) -> None:
    """Cross-check SegmentTree against a plain reference list."""
    values = [rng.randint(0, 100) for _ in range(30)]
    reference = list(values)
    tree = SegmentTree(values)

    for _ in range(rounds):
        if rng.random() < 0.5:
            index = rng.randrange(len(values))
            value = rng.randint(0, 100)
            tree.update(index, value)
            reference[index] = value
        else:
            left = rng.randrange(len(values))
            right = rng.randrange(left, len(values))
            expected = sum(reference[left : right + 1])
            assert tree.query(left, right) == expected, (
                f"query({left},{right}): got {tree.query(left, right)}, "
                f"expected {expected}"
            )

    assert tree.to_list() == reference


def _verify_lazy_tree(rng: random.Random, rounds: int = 200) -> None:
    """Cross-check LazySegmentTree against a plain reference list."""
    values = [rng.randint(0, 100) for _ in range(30)]
    reference = list(values)
    tree = LazySegmentTree(values)

    for _ in range(rounds):
        if rng.random() < 0.5:
            left = rng.randrange(len(values))
            right = rng.randrange(left, len(values))
            delta = rng.randint(-20, 20)
            tree.range_add(left, right, delta)
            for i in range(left, right + 1):
                reference[i] += delta
        else:
            left = rng.randrange(len(values))
            right = rng.randrange(left, len(values))
            expected = sum(reference[left : right + 1])
            assert tree.range_sum(left, right) == expected, (
                f"range_sum({left},{right}): got {tree.range_sum(left, right)}, "
                f"expected {expected}"
            )

    assert tree.to_list() == reference


if __name__ == "__main__":
    values = [1, 3, 5, 7, 9, 11]

    basic = SegmentTree(values)
    assert basic.query(0, 5) == 36
    assert basic.query(2, 4) == 21
    assert basic.query(0, 0) == 1
    assert basic.query(3, 3) == 7
    assert basic.query(1, 3) == 15

    basic.update(3, 8)
    assert basic.to_list() == [1, 3, 5, 8, 9, 11]
    assert basic.query(2, 4) == 22
    assert basic.query(0, 5) == 37

    print("Basic SegmentTree on [1, 3, 5, 7, 9, 11]")
    print("  query(0,5) =", 36, " query(2,4) =", 21, " query(0,0) =", 1)
    print("  query(3,3) =", 7, " query(1,3) =", 15)
    print("  update(3, 8) ->", basic.to_list())
    print("  query(2,4) =", 22, " query(0,5) =", 37)
    print("  size() =", basic.size())

    print("\nSegment tree drawing (each node is [interval]=sum):")
    for line in basic.draw():
        print(" " + line)

    rng = random.Random(42)
    _verify_segment_tree(rng)
    print("\nSegmentTree randomized cross-check passed: 200 operations")

    lazy = LazySegmentTree(values)
    lazy.range_add(1, 4, 10)
    assert lazy.to_list() == [1, 13, 15, 17, 19, 11]
    assert lazy.range_sum(0, 5) == 76
    assert lazy.range_sum(2, 3) == 32
    assert lazy.range_sum(0, 0) == 1

    print("\nLazySegmentTree on [1, 3, 5, 7, 9, 11]")
    print("  range_add(1, 4, 10) ->", [1, 13, 15, 17, 19, 11])
    print("  range_sum(0,5) =", 76, " range_sum(2,3) =", 32, " range_sum(0,0) =", 1)

    lazy.range_add(0, 0, 5)
    assert lazy.to_list() == [6, 13, 15, 17, 19, 11]
    assert lazy.range_sum(0, 2) == 34
    print("  range_add(0, 0, 5) ->", [6, 13, 15, 17, 19, 11])
    print("  range_sum(0,2) =", 34)

    _verify_lazy_tree(rng)
    print("\nLazySegmentTree randomized cross-check passed: 200 operations")
    print("\nAll assertions passed.")