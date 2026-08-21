"""Red-Black Tree basics.

A left-leaning red-black tree (LLRB) is a self-balancing binary search
tree.  It guarantees that every path from the root to a leaf has the same
number of black links, so the height stays bounded by ~2*log2(N+1) and all
core operations (insert / delete / find / update) run in O(log N).

This module implements the classic Sedgewick left-leaning variant, which
corresponds to a 2-3-4 tree: a black node with a single red left child is
a "3-node", and a black node with two red children is a "4-node".
"""

from __future__ import annotations

import random
from typing import Generic, List, Optional, TypeVar


K = TypeVar("K")
V = TypeVar("V")

RED = True
BLACK = False


class RBNode(Generic[K, V]):
    """A node of the red-black tree.

    The ``color`` field stores the color of the link coming from the
    parent: RED means the parent treats this node as part of a 3/4-node.
    """

    def __init__(self, key: K, value: V, color: bool = RED) -> None:
        self.key = key
        self.value = value
        self.color = color
        self.size = 1
        self.left: Optional[RBNode[K, V]] = None
        self.right: Optional[RBNode[K, V]] = None

    def __repr__(self) -> str:
        return f"RBNode({self.key}, {'R' if self.color else 'B'})"


def _is_red(node: Optional[RBNode]) -> bool:
    return node is not None and node.color is RED


def _size(node: Optional[RBNode]) -> int:
    return node.size if node is not None else 0


class RedBlackTree(Generic[K, V]):
    """A left-leaning red-black tree mapping comparable keys to values.

    Public operations: ``put``, ``get``, ``delete``, ``delete_min``,
    ``delete_max``, ``min``, ``max``, ``keys``, ``height``, ``is_valid``.
    """

    def __init__(self) -> None:
        self._root: Optional[RBNode[K, V]] = None

    # ------------------------------------------------------------- helpers

    def _size_of(self, node: Optional[RBNode[K, V]]) -> int:
        return node.size if node is not None else 0

    @staticmethod
    def _rotate_left(h: RBNode[K, V]) -> RBNode[K, V]:
        x = h.right
        h.right = x.left
        x.left = h
        x.color = h.color
        h.color = RED
        x.size = h.size
        h.size = 1 + _size(h.left) + _size(h.right)
        return x

    @staticmethod
    def _rotate_right(h: RBNode[K, V]) -> RBNode[K, V]:
        x = h.left
        h.left = x.right
        x.right = h
        x.color = h.color
        h.color = RED
        x.size = h.size
        h.size = 1 + _size(h.left) + _size(h.right)
        return x

    @staticmethod
    def _flip_colors(h: RBNode[K, V]) -> None:
        h.color = not h.color
        h.left.color = not h.left.color
        h.right.color = not h.right.color

    def _fix_up(self, h: RBNode[K, V]) -> RBNode[K, V]:
        if _is_red(h.right) and not _is_red(h.left):
            h = self._rotate_left(h)
        if _is_red(h.left) and _is_red(h.left.left):
            h = self._rotate_right(h)
        if _is_red(h.left) and _is_red(h.right):
            self._flip_colors(h)
        h.size = 1 + self._size_of(h.left) + self._size_of(h.right)
        return h

    def _move_red_left(self, h: RBNode[K, V]) -> RBNode[K, V]:
        self._flip_colors(h)
        if _is_red(h.right.left):
            h.right = self._rotate_right(h.right)
            h = self._rotate_left(h)
            self._flip_colors(h)
        return h

    def _move_red_right(self, h: RBNode[K, V]) -> RBNode[K, V]:
        self._flip_colors(h)
        if _is_red(h.left.left):
            h = self._rotate_right(h)
            self._flip_colors(h)
        return h

    # ------------------------------------------------------------- insert

    def put(self, key: K, value: V) -> None:
        """Insert ``key -> value``, replacing any existing value."""

        self._root = self._put(self._root, key, value)
        self._root.color = BLACK

    def _put(
        self, h: Optional[RBNode[K, V]], key: K, value: V
    ) -> RBNode[K, V]:
        if h is None:
            return RBNode(key, value, RED)
        if key < h.key:
            h.left = self._put(h.left, key, value)
        elif key > h.key:
            h.right = self._put(h.right, key, value)
        else:
            h.value = value
        return self._fix_up(h)

    # ------------------------------------------------------------- lookup

    def get(self, key: K) -> Optional[V]:
        """Return the value for ``key``, or ``None`` if absent."""

        node = self._root
        while node is not None:
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                return node.value
        return None

    def contains_key(self, key: K) -> bool:
        return self.get(key) is not None

    def __contains__(self, key: K) -> bool:
        return self.contains_key(key)

    def min(self) -> Optional[K]:
        """Return the smallest key, or ``None`` if empty."""

        node = self._root
        if node is None:
            return None
        while node.left is not None:
            node = node.left
        return node.key

    def max(self) -> Optional[K]:
        """Return the largest key, or ``None`` if empty."""

        node = self._root
        if node is None:
            return None
        while node.right is not None:
            node = node.right
        return node.key

    def keys(self) -> List[K]:
        """Return all keys in ascending order."""

        result: List[K] = []
        self._inorder(self._root, result)
        return result

    def _inorder(self, node: Optional[RBNode[K, V]], result: List[K]) -> None:
        if node is None:
            return
        self._inorder(node.left, result)
        result.append(node.key)
        self._inorder(node.right, result)

    # ------------------------------------------------------------- delete

    def delete_min(self) -> Optional[V]:
        """Remove and return the value of the smallest key."""

        if self._root is None:
            return None
        value = self.get(self.min())
        if not _is_red(self._root.left) and not _is_red(self._root.right):
            self._root.color = RED
        self._root = self._delete_min(self._root)
        if self._root is not None:
            self._root.color = BLACK
        return value

    def _delete_min(self, h: RBNode[K, V]) -> Optional[RBNode[K, V]]:
        if h.left is None:
            return None
        if not _is_red(h.left) and not _is_red(h.left.left):
            h = self._move_red_left(h)
        h.left = self._delete_min(h.left)
        return self._fix_up(h)

    def delete_max(self) -> Optional[V]:
        """Remove and return the value of the largest key."""

        if self._root is None:
            return None
        value = self.get(self.max())
        if not _is_red(self._root.left) and not _is_red(self._root.right):
            self._root.color = RED
        self._root = self._delete_max(self._root)
        if self._root is not None:
            self._root.color = BLACK
        return value

    def _delete_max(self, h: RBNode[K, V]) -> Optional[RBNode[K, V]]:
        if _is_red(h.left):
            h = self._rotate_right(h)
        if h.right is None:
            return None
        if not _is_red(h.right) and not _is_red(h.right.left):
            h = self._move_red_right(h)
        h.right = self._delete_max(h.right)
        return self._fix_up(h)

    def delete(self, key: K) -> Optional[V]:
        """Remove ``key`` and return its old value, or ``None`` if absent."""

        if self._root is None or not self.contains_key(key):
            return None
        value = self.get(key)
        if not _is_red(self._root.left) and not _is_red(self._root.right):
            self._root.color = RED
        self._root = self._delete(self._root, key)
        if self._root is not None:
            self._root.color = BLACK
        return value

    def _delete(
        self, h: RBNode[K, V], key: K
    ) -> Optional[RBNode[K, V]]:
        if key < h.key:
            if not _is_red(h.left) and not _is_red(h.left.left):
                h = self._move_red_left(h)
            h.left = self._delete(h.left, key)
        else:
            if _is_red(h.left):
                h = self._rotate_right(h)
            if key == h.key and h.right is None:
                return None
            if not _is_red(h.right) and not _is_red(h.right.left):
                h = self._move_red_right(h)
            if key == h.key:
                successor = h.right
                while successor.left is not None:
                    successor = successor.left
                h.key = successor.key
                h.value = successor.value
                h.right = self._delete_min(h.right)
            else:
                h.right = self._delete(h.right, key)
        return self._fix_up(h)

    # ------------------------------------------------------------- metrics

    def height(self) -> int:
        """Return the height in edges (0 for a single node, -1 if empty)."""

        return self._height(self._root)

    def _height(self, node: Optional[RBNode[K, V]]) -> int:
        if node is None:
            return -1
        return 1 + max(self._height(node.left), self._height(node.right))

    def __len__(self) -> int:
        return self._size_of(self._root)

    def is_empty(self) -> bool:
        return self._root is None

    # ------------------------------------------------------------- checks

    def is_valid(self) -> bool:
        """Check every red-black invariant on the current tree."""

        if self._root is None:
            return True
        if _is_red(self._root):
            return False
        if self.keys() != sorted(self.keys()):
            return False
        return self._black_height(self._root) >= 0

    def _black_height(self, node: Optional[RBNode[K, V]]) -> int:
        """Return black-height on success, -1 if any invariant is broken."""

        if node is None:
            return 0
        if _is_red(node):
            if _is_red(node.left) or _is_red(node.right):
                return -1
        if _is_red(node.right):
            return -1
        left_black = self._black_height(node.left)
        right_black = self._black_height(node.right)
        if left_black < 0 or right_black < 0 or left_black != right_black:
            return -1
        return left_black + (0 if _is_red(node) else 1)

    # ------------------------------------------------------------- draw

    def draw(self) -> List[str]:
        """Return ASCII lines rendering the tree, red links marked (R)."""

        if self._root is None:
            return ["<empty tree>"]
        levels: List[List[Optional[RBNode[K, V]]]] = []
        frontier = [self._root]
        while any(node is not None for node in frontier):
            levels.append(frontier)
            nxt: List[Optional[RBNode[K, V]]] = []
            for node in frontier:
                if node is None:
                    nxt.extend([None, None])
                else:
                    nxt.append(node.left)
                    nxt.append(node.right)
            frontier = nxt
        lines: List[str] = []
        for depth, level in enumerate(levels):
            indent = " " * (max(0, len(levels) - depth))
            tokens: List[str] = []
            for node in level:
                if node is None:
                    tokens.append(" . ")
                else:
                    mark = "R" if node.color else "B"
                    tokens.append(f"{node.key}({mark})")
            lines.append(indent + "  ".join(tokens))
        return lines


class PlainBST(Generic[K, V]):
    """A deliberately naive, non-balancing BST used to show degeneration."""

    def __init__(self) -> None:
        self._root: Optional[RBNode[K, V]] = None

    def put(self, key: K, value: V) -> None:
        self._root = self._put(self._root, key, value)

    def _put(
        self, node: Optional[RBNode[K, V]], key: K, value: V
    ) -> RBNode[K, V]:
        if node is None:
            return RBNode(key, value, BLACK)
        if key < node.key:
            node.left = self._put(node.left, key, value)
        elif key > node.key:
            node.right = self._put(node.right, key, value)
        else:
            node.value = value
        return node

    def height(self) -> int:
        return self._height(self._root)

    def _height(self, node: Optional[RBNode[K, V]]) -> int:
        if node is None:
            return -1
        return 1 + max(self._height(node.left), self._height(node.right))

    def get(self, key: K) -> Optional[V]:
        node = self._root
        while node is not None:
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                return node.value
        return None


if __name__ == "__main__":
    print("=== Red-Black Tree demo ===")

    rbt = RedBlackTree[int, int]()
    plain = PlainBST[int, int]()

    for k in range(1, 16):
        rbt.put(k, k * 10)
        plain.put(k, k * 10)

    print("Inserted 1..15 in increasing order.")
    print(f"Plain BST height : {plain.height()}  (degenerated into a linked list)")
    print(f"Red-black height : {rbt.height()}  (stays logarithmic)")
    assert plain.height() == 14
    assert rbt.height() <= 7
    assert rbt.is_valid()
    assert len(rbt) == 15
    assert rbt.keys() == list(range(1, 16))
    for k in range(1, 16):
        assert rbt.get(k) == k * 10

    print("\nRed-black tree drawn with colors:")
    for line in rbt.draw():
        print("   " + line)

    print("\nRandom insert / delete stress test...")
    reference = {}
    rbt2 = RedBlackTree[int, int]()
    random.seed(2026)
    for _ in range(80):
        key = random.randint(0, 199)
        value = random.randint(0, 1000)
        rbt2.put(key, value)
        reference[key] = value
        assert rbt2.is_valid(), f"invalid after put {key}"
    assert len(rbt2) == len(reference)
    for key in reference:
        assert rbt2.get(key) == reference[key]
    while reference:
        key = random.choice(list(reference))
        old = rbt2.delete(key)
        assert old == reference[key]
        del reference[key]
        assert rbt2.is_valid(), f"invalid after delete {key}"
    assert len(rbt2) == len(reference)
    for key in reference:
        assert rbt2.get(key) == reference[key]

    print("Stress test passed: invariants held after every put/delete.")
    print(f"Final size: {len(rbt2)}")

    while len(rbt2) > 0:
        key = rbt2.min()
        rbt2.delete(key)
    assert rbt2.is_empty() and rbt2.is_valid()

    print("\nAll assertions passed.")
