"""TreeMap structure and visualization.

A TreeMap is a Map whose keys live in a binary search tree, so the keys
stay sorted at all times. This module implements a plain BST-backed map with
ordered queries: first/last key, floor/ceiling key, select/rank via subtree
sizes, range search, and a search-steps + draw helper that visualize why a
balanced BST beats a degenerate one.
"""

from __future__ import annotations

from typing import Dict, Generic, List, Optional, Tuple, TypeVar

K = TypeVar("K")
V = TypeVar("V")


class BSTNode(Generic[K, V]):
    """A single node of the binary search tree backing a TreeMap.

    Besides the key/value pair it keeps `size`, the number of nodes in the
    subtree rooted here. Subtree sizes power the O(logN) select/rank and the
    height visualization.
    """

    def __init__(self, key: K, value: V):
        self.key: K = key
        self.value: V = value
        self.left: Optional[BSTNode[K, V]] = None
        self.right: Optional[BSTNode[K, V]] = None
        self.size: int = 1

    def __repr__(self) -> str:
        return f"BSTNode(key={self.key!r})"


class TreeMap(Generic[K, V]):
    """A Map whose keys live in a binary search tree.

    Keys stay sorted at all times, so the TreeMap can answer ordered
    questions that a HashMap cannot: the smallest key, the largest key, the
    keys between two bounds, the k-th smallest key, and the rank of a key.
    Keys must be mutually comparable.
    """

    def __init__(self) -> None:
        self._root: Optional[BSTNode[K, V]] = None

    def size(self) -> int:
        """Return the number of key-value pairs in the map."""
        return self._size_of(self._root)

    def __len__(self) -> int:
        return self.size()

    def is_empty(self) -> bool:
        """Return True when the map holds no key-value pairs."""
        return self._root is None

    def height(self) -> int:
        """Return the height of the BST, i.e. the number of levels."""
        return self._height(self._root)

    def __contains__(self, key: object) -> bool:
        return self.contains_key(key)

    def __iter__(self):
        """Iterate the keys in ascending sorted order."""
        return iter(self.keys())

    def put(self, key: K, value: V) -> Optional[V]:
        """Insert the key with the given value, or update it if it exists.

        Return the old value when the key was already present, otherwise
        None. Recompute subtree sizes along the search path.
        """
        old = self.get(key)
        self._root = self._put(self._root, key, value)
        return old

    def get(self, key: K) -> Optional[V]:
        """Return the value stored under the key, or None if absent."""
        node = self._get(self._root, key)
        return node.value if node is not None else None

    def contains_key(self, key: K) -> bool:
        """Return True when the key exists in the map."""
        return self._get(self._root, key) is not None

    def remove(self, key: K) -> Optional[V]:
        """Delete the key and return its old value, or None if absent.

        A node with two children is replaced by its in-order successor, the
        smallest key of the right subtree. Subtree sizes are recomputed.
        """
        if not self.contains_key(key):
            return None
        old = self.get(key)
        self._root = self._remove(self._root, key)
        return old

    def keys(self) -> List[K]:
        """Return all keys in ascending order via in-order traversal."""
        result: List[K] = []
        self._inorder(self._root, result)
        return result

    def first_key(self) -> Optional[K]:
        """Return the smallest key, or None when the map is empty."""
        if self._root is None:
            return None
        return self._min_node(self._root).key

    def last_key(self) -> Optional[K]:
        """Return the largest key, or None when the map is empty."""
        if self._root is None:
            return None
        node = self._root
        while node.right is not None:
            node = node.right
        return node.key

    def floor_key(self, key: K) -> Optional[K]:
        """Return the largest key that is <= the given key, or None."""
        return self._floor(self._root, key)

    def ceiling_key(self, key: K) -> Optional[K]:
        """Return the smallest key that is >= the given key, or None."""
        return self._ceiling(self._root, key)

    def select(self, k: int) -> Optional[K]:
        """Return the k-th smallest key, 1-based (select(1) = smallest)."""
        if k < 1:
            return None
        return self._select(self._root, k)

    def rank(self, key: K) -> int:
        """Return the 1-based rank of the key.

        The rank is (number of keys strictly less than key) + 1. When the
        key is absent, its would-be insertion position is returned.
        """
        return self._rank(self._root, key)

    def range_keys(self, low: K, high: K) -> List[K]:
        """Return all keys with low <= key <= high, in ascending order.

        Subtrees that cannot contain an in-range key are pruned.
        """
        result: List[K] = []
        self._range(self._root, low, high, result)
        return result

    def search_steps(self, key: K) -> List[K]:
        """Record the path of keys visited while searching for the key.

        This powers the efficiency visualization: the path length on a
        balanced tree is far shorter than on a degenerate tree. Returns an
        empty list when the root is None.
        """
        path: List[K] = []
        node = self._root
        while node is not None:
            path.append(node.key)
            if key == node.key:
                break
            if key < node.key:
                node = node.left
            else:
                node = node.right
        return path

    def draw(self) -> str:
        """Render an ASCII diagram of the tree.

        `` +-- `` marks a left child and `` `-- `` marks a right child,
        following the classic tree printer.
        """
        if self._root is None:
            return "(empty)"
        lines: List[str] = []
        self._draw_lines(self._root, "", True, lines)
        return "\n".join(lines)

    def _put(self, node: Optional[BSTNode[K, V]], key: K, value: V) -> BSTNode[K, V]:
        if node is None:
            return BSTNode(key, value)
        if key < node.key:
            node.left = self._put(node.left, key, value)
        elif key > node.key:
            node.right = self._put(node.right, key, value)
        else:
            node.value = value
            return node
        node.size = self._size_of(node.left) + self._size_of(node.right) + 1
        return node

    def _get(self, node: Optional[BSTNode[K, V]], key: K) -> Optional[BSTNode[K, V]]:
        if node is None:
            return None
        if key < node.key:
            return self._get(node.left, key)
        if key > node.key:
            return self._get(node.right, key)
        return node

    def _remove(self, node: Optional[BSTNode[K, V]], key: K) -> Optional[BSTNode[K, V]]:
        if node is None:
            return None
        if key < node.key:
            node.left = self._remove(node.left, key)
        elif key > node.key:
            node.right = self._remove(node.right, key)
        else:
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            successor = self._min_node(node.right)
            node.key = successor.key
            node.value = successor.value
            node.right = self._delete_min(node.right)
        node.size = self._size_of(node.left) + self._size_of(node.right) + 1
        return node

    def _min_node(self, node: BSTNode[K, V]) -> BSTNode[K, V]:
        while node.left is not None:
            node = node.left
        return node

    def _delete_min(self, node: BSTNode[K, V]) -> Optional[BSTNode[K, V]]:
        if node.left is None:
            return node.right
        node.left = self._delete_min(node.left)
        node.size = self._size_of(node.left) + self._size_of(node.right) + 1
        return node

    def _size_of(self, node: Optional[BSTNode[K, V]]) -> int:
        return node.size if node is not None else 0

    def _height(self, node: Optional[BSTNode[K, V]]) -> int:
        if node is None:
            return 0
        return 1 + max(self._height(node.left), self._height(node.right))

    def _inorder(self, node: Optional[BSTNode[K, V]], out: List[K]) -> None:
        if node is None:
            return
        self._inorder(node.left, out)
        out.append(node.key)
        self._inorder(node.right, out)

    def _floor(self, node: Optional[BSTNode[K, V]], key: K) -> Optional[K]:
        if node is None:
            return None
        if key == node.key:
            return node.key
        if key < node.key:
            return self._floor(node.left, key)
        candidate = self._floor(node.right, key)
        return candidate if candidate is not None else node.key

    def _ceiling(self, node: Optional[BSTNode[K, V]], key: K) -> Optional[K]:
        if node is None:
            return None
        if key == node.key:
            return node.key
        if key > node.key:
            return self._ceiling(node.right, key)
        candidate = self._ceiling(node.left, key)
        return candidate if candidate is not None else node.key

    def _select(self, node: Optional[BSTNode[K, V]], k: int) -> Optional[K]:
        if node is None:
            return None
        left_size = self._size_of(node.left)
        if k == left_size + 1:
            return node.key
        if k <= left_size:
            return self._select(node.left, k)
        return self._select(node.right, k - left_size - 1)

    def _rank(self, node: Optional[BSTNode[K, V]], key: K) -> int:
        if node is None:
            return 1
        if key < node.key:
            return self._rank(node.left, key)
        if key > node.key:
            return self._size_of(node.left) + 1 + self._rank(node.right, key)
        return self._size_of(node.left) + 1

    def _range(self, node: Optional[BSTNode[K, V]], low: K, high: K, out: List[K]) -> None:
        if node is None:
            return
        if low < node.key:
            self._range(node.left, low, high, out)
        if low <= node.key <= high:
            out.append(node.key)
        if node.key < high:
            self._range(node.right, low, high, out)

    def _draw_lines(
        self,
        node: Optional[BSTNode[K, V]],
        prefix: str,
        is_tail: bool,
        lines: List[str],
    ) -> None:
        if node is None:
            lines.append(prefix + ("`-- None" if is_tail else "+-- None"))
            return
        lines.append(prefix + ("`-- " if is_tail else "+-- ") + str(node.key))
        child_prefix = prefix + ("    " if is_tail else "|   ")
        self._draw_lines(node.left, child_prefix, False, lines)
        self._draw_lines(node.right, child_prefix, True, lines)


if __name__ == "__main__":
    tm: TreeMap[int, int] = TreeMap()
    for key in (5, 3, 8, 2, 4, 7, 9):
        tm.put(key, key * 10)

    assert len(tm) == 7
    assert tm.contains_key(4) is True
    assert tm.contains_key(6) is False
    assert tm.keys() == [2, 3, 4, 5, 7, 8, 9]
    assert tm.first_key() == 2
    assert tm.last_key() == 9
    assert tm.floor_key(6) == 5
    assert tm.ceiling_key(6) == 7
    assert tm.floor_key(1) is None
    assert tm.ceiling_key(10) is None
    assert tm.select(1) == 2
    assert tm.select(4) == 5
    assert tm.rank(5) == 4
    assert tm.rank(2) == 1
    assert tm.range_keys(3, 8) == [3, 4, 5, 7, 8]
    assert list(tm) == [2, 3, 4, 5, 7, 8, 9]
    assert 4 in tm and 6 not in tm
    assert tm.height() == 3

    print("TreeMap demo: insert 5,3,8,2,4,7,9 with value = key * 10")
    print("Initial tree shape:")
    print(tm.draw())
    print("len =", len(tm), "| height =", tm.height())
    print("keys() =", tm.keys())
    print("first_key =", tm.first_key(), "| last_key =", tm.last_key())
    print("floor_key(6) =", tm.floor_key(6), "| ceiling_key(6) =", tm.ceiling_key(6))
    print("select(1) =", tm.select(1), "| select(4) =", tm.select(4))
    print("rank(5) =", tm.rank(5), "| rank(2) =", tm.rank(2))
    print("range_keys(3, 8) =", tm.range_keys(3, 8))
    print("search_steps(9) =", tm.search_steps(9))

    old = tm.put(5, 999)
    assert old == 50
    assert tm.get(5) == 999
    assert len(tm) == 7
    print("\nput(5, 999) updated an existing key; old value =", old, "| len =", len(tm))

    removed = tm.remove(5)
    assert removed == 999
    assert tm.keys() == [2, 3, 4, 7, 8, 9]
    assert len(tm) == 6
    assert tm.get(5) is None
    print("remove(5) returned", removed, "| keys() =", tm.keys(), "| len =", len(tm))

    tm.put(5, 50)
    assert tm.remove(2) == 20
    assert tm.remove(7) == 70
    assert tm.keys() == [3, 4, 5, 8, 9]
    assert len(tm) == 5
    assert tm.keys() == sorted(tm.keys())
    print("re-insert 5, then remove(2) and remove(7): keys() =", tm.keys(), "| len =", len(tm))

    degenerate: TreeMap[int, int] = TreeMap()
    for key in range(1, 9):
        degenerate.put(key, key * 10)

    balanced: TreeMap[int, int] = TreeMap()
    for key in (4, 2, 1, 3, 6, 5, 7, 8):
        balanced.put(key, key * 10)

    deg_h = degenerate.height()
    bal_h = balanced.height()
    deg_steps = degenerate.search_steps(8)
    bal_steps = balanced.search_steps(8)

    assert deg_h == 8
    assert bal_h == 4
    assert bal_h < deg_h
    assert deg_steps == [1, 2, 3, 4, 5, 6, 7, 8]
    assert bal_steps == [4, 6, 7, 8]
    assert len(bal_steps) < len(deg_steps)

    print("\nEfficiency comparison (8 keys)")
    print("Degenerate BST (insert 1..8 in order): height =", deg_h,
          "| search_steps(8) =", len(deg_steps), deg_steps)
    print("Balanced-ish BST (insert mid-first):    height =", bal_h,
          "| search_steps(8) =", len(bal_steps), bal_steps)
    print("\nBalanced-ish tree diagram:")
    print(balanced.draw())

    print("\nFinal sorted keys dump:", tm.keys())
    print("All assertions passed.")
