from __future__ import annotations

from typing import Dict, Generic, List, Optional, TypeVar

V = TypeVar("V")


class TrieNode(Generic[V]):
    """One node of a trie: a dict of children plus an optional value.

    Every edge is one character, so `children[c]` is the node reached by
    consuming the character `c`. The `val` field is None unless this node
    is the end of a stored key; the path from the root to such a node
    spells the key itself.
    """

    def __init__(self) -> None:
        self.children: Dict[str, TrieNode[V]] = {}
        self.val: Optional[V] = None

    def __repr__(self) -> str:
        return f"TrieNode(val={self.val!r}, children={sorted(self.children)})"


class TrieMap(Generic[V]):
    """A map from strings to values, backed by a trie.

    Inserting, deleting, and looking up a key of length L each walk L
    edges, so every operation costs O(L). Keys that share a prefix share
    the nodes of that prefix, which is exactly what saves memory compared
    with a HashMap and what makes prefix and wildcard queries possible.
    """

    def __init__(self) -> None:
        """Create an empty trie map."""
        self.root = TrieNode[V]()
        self._size = 0

    def put(self, key: str, value: V) -> Optional[V]:
        """Map `key` to `value`, creating nodes as needed.

        Returns the previous value stored under `key`, or None if `key`
        was not present before.
        """
        node = self.root
        for char in key:
            node = node.children.setdefault(char, TrieNode[V]())
        old = node.val
        node.val = value
        if old is None:
            self._size += 1
        return old

    def get(self, key: str) -> Optional[V]:
        """Return the value stored under `key`, or None if it is absent."""
        node = self._find_node(key)
        return node.val if node is not None else None

    def contains_key(self, key: str) -> bool:
        """Return True if `key` is stored in the map."""
        node = self._find_node(key)
        return node is not None and node.val is not None

    def __contains__(self, key: str) -> bool:
        """Support the `key in map` syntax."""
        return self.contains_key(key)

    def __len__(self) -> int:
        """Return the number of stored keys."""
        return self._size

    def is_empty(self) -> bool:
        """Return True if no key is stored."""
        return self._size == 0

    def keys(self) -> List[str]:
        """Return every stored key in lexicographic order."""
        result: List[str] = []
        self._collect(self.root, "", result)
        return result

    def remove(self, key: str) -> Optional[V]:
        """Delete `key`, pruning nodes that become useless.

        A node is pruned when it no longer ends a key and has no children.
        Nodes on a shared prefix survive because other keys still need
        them. Returns the value that was stored, or None if `key` was not
        present.
        """

        def do_remove(node: TrieNode[V], depth: int) -> Optional[V]:
            if depth == len(key):
                old = node.val
                node.val = None
                return old
            char = key[depth]
            child = node.children.get(char)
            if child is None:
                return None
            old = do_remove(child, depth + 1)
            if child.val is None and not child.children:
                del node.children[char]
            return old

        old = do_remove(self.root, 0)
        if old is not None:
            self._size -= 1
        return old

    def shortest_prefix_of(self, s: str) -> Optional[str]:
        """Return the shortest stored key that is a prefix of `s`.

        Walks `s` down the trie and stops at the first node whose value is
        not None; returns None if no stored key is a prefix of `s`.
        """
        node = self.root
        for i, char in enumerate(s):
            node = node.children.get(char)
            if node is None:
                break
            if node.val is not None:
                return s[: i + 1]
        return None

    def longest_prefix_of(self, s: str) -> Optional[str]:
        """Return the longest stored key that is a prefix of `s`."""
        node = self.root
        longest: Optional[str] = None
        for i, char in enumerate(s):
            node = node.children.get(char)
            if node is None:
                break
            if node.val is not None:
                longest = s[: i + 1]
        return longest

    def has_key_with_prefix(self, prefix: str) -> bool:
        """Return True if at least one stored key starts with `prefix`."""
        return self._find_node(prefix) is not None

    def keys_with_prefix(self, prefix: str) -> List[str]:
        """Return every stored key that starts with `prefix`, in sorted order."""
        node = self._find_node(prefix)
        if node is None:
            return []
        result: List[str] = []
        self._collect(node, prefix, result)
        return result

    def has_key_with_pattern(self, pattern: str) -> bool:
        """Return True if some stored key matches `pattern`.

        In the pattern, '.' matches any single character and every other
        character must match exactly.
        """

        def match(node: TrieNode[V], index: int) -> bool:
            if index == len(pattern):
                return node.val is not None
            char = pattern[index]
            if char == ".":
                return any(match(child, index + 1) for child in node.children.values())
            child = node.children.get(char)
            return child is not None and match(child, index + 1)

        return match(self.root, 0)

    def keys_with_pattern(self, pattern: str) -> List[str]:
        """Return every stored key matching `pattern`, in sorted order."""
        result: List[str] = []
        self._collect_pattern(self.root, pattern, 0, "", result)
        return result

    def node_count(self) -> int:
        """Return the total number of nodes, including the root.

        Useful for memory illustrations: each node is one distinct prefix
        of some stored key.
        """
        count = 0
        stack = [self.root]
        while stack:
            node = stack.pop()
            count += 1
            stack.extend(node.children.values())
        return count

    def _find_node(self, prefix: str) -> Optional[TrieNode[V]]:
        """Return the node reached by walking `prefix`, or None."""
        node = self.root
        for char in prefix:
            node = node.children.get(char)
            if node is None:
                return None
        return node

    def _collect(self, node: TrieNode[V], prefix: str, result: List[str]) -> None:
        """DFS that appends every key under `node` to `result`.

        Children are visited in sorted character order so the output is
        lexicographic, and shorter keys appear before their extensions.
        """
        if node.val is not None:
            result.append(prefix)
        for char in sorted(node.children):
            self._collect(node.children[char], prefix + char, result)

    def _collect_pattern(
        self,
        node: TrieNode[V],
        pattern: str,
        index: int,
        prefix: str,
        result: List[str],
    ) -> None:
        """DFS matching `pattern` from `index`, appending matches to `result`."""
        if index == len(pattern):
            if node.val is not None:
                result.append(prefix)
            return
        char = pattern[index]
        if char == ".":
            for c in sorted(node.children):
                self._collect_pattern(
                    node.children[c], pattern, index + 1, prefix + c, result
                )
        else:
            child = node.children.get(char)
            if child is not None:
                self._collect_pattern(child, pattern, index + 1, prefix + char, result)


class TrieSet:
    """A set of strings implemented as a TrieMap.

    None already means "not the end of a key" inside a trie node, so the
    set stores a non-None sentinel (True) as the value of every key. All
    the prefix and wildcard APIs come for free from the underlying map.
    """

    def __init__(self) -> None:
        """Create an empty trie set."""
        self._map: TrieMap[bool] = TrieMap()

    def add(self, key: str) -> None:
        """Insert `key` into the set."""
        self._map.put(key, True)

    def remove(self, key: str) -> None:
        """Remove `key` from the set, pruning unused nodes."""
        self._map.remove(key)

    def contains(self, key: str) -> bool:
        """Return True if `key` is in the set."""
        return self._map.contains_key(key)

    def keys(self) -> List[str]:
        """Return every key in the set, in lexicographic order."""
        return self._map.keys()

    def keys_with_prefix(self, prefix: str) -> List[str]:
        """Return every key starting with `prefix`, in sorted order."""
        return self._map.keys_with_prefix(prefix)

    def shortest_prefix_of(self, s: str) -> Optional[str]:
        """Return the shortest key in the set that is a prefix of `s`."""
        return self._map.shortest_prefix_of(s)

    def longest_prefix_of(self, s: str) -> Optional[str]:
        """Return the longest key in the set that is a prefix of `s`."""
        return self._map.longest_prefix_of(s)

    def has_key_with_prefix(self, prefix: str) -> bool:
        """Return True if any key in the set starts with `prefix`."""
        return self._map.has_key_with_prefix(prefix)

    def has_key_with_pattern(self, pattern: str) -> bool:
        """Return True if some key matches `pattern` ('.' = any char)."""
        return self._map.has_key_with_pattern(pattern)

    def keys_with_pattern(self, pattern: str) -> List[str]:
        """Return every key matching `pattern`, in sorted order."""
        return self._map.keys_with_pattern(pattern)

    def __len__(self) -> int:
        """Return the number of keys in the set."""
        return len(self._map)


def trie_to_lines(trie: TrieMap[V]) -> List[str]:
    """Render a small trie as one line per depth, for ASCII visualization.

    Nodes that end a key are printed with a `#` marker after their
    character, e.g. `p#` for the key "app". Only suitable for shallow
    tries; deep trees produce long lines.
    """
    lines: List[str] = ["depth 0: (root)"]
    level: List[TrieNode[V]] = [trie.root]
    depth = 1
    while level:
        next_level: List[TrieNode[V]] = []
        entries: List[str] = []
        for node in level:
            for char in sorted(node.children):
                child = node.children[char]
                next_level.append(child)
                entries.append(char + ("#" if child.val is not None else ""))
        if not entries:
            break
        lines.append(f"depth {depth}: " + "  ".join(entries))
        level = next_level
        depth += 1
    return lines


if __name__ == "__main__":
    print("=== TrieMap / TrieSet demo ===")

    print("\nPart A: shared prefixes save memory")
    tm: TrieMap[int] = TrieMap()
    assert tm.put("apple", 1) is None
    assert tm.put("app", 2) is None
    assert tm.put("appl", 3) is None
    assert len(tm) == 3
    assert tm.contains_key("apple") and tm.contains_key("app") and tm.contains_key("appl")
    assert tm.keys() == ["app", "appl", "apple"]
    assert tm.node_count() == 6
    print("  keys:", tm.keys())
    print("  chars a HashMap stores: 12 (apple + app + appl)")
    print(f"  trie node_count (incl. root): {tm.node_count()} -> 5 shared char nodes")

    print("\nPart B: prefix operations")
    for key, value in [("that", 1), ("the", 2), ("them", 3), ("apple", 4)]:
        tm.put(key, value)
    assert tm.shortest_prefix_of("themxyz") == "the"
    assert tm.longest_prefix_of("themxyz") == "them"
    assert tm.has_key_with_prefix("tha") is True
    assert tm.has_key_with_prefix("thz") is False
    assert tm.keys_with_prefix("th") == ["that", "the", "them"]
    print('  shortest_prefix_of("themxyz") =', tm.shortest_prefix_of("themxyz"))
    print('  longest_prefix_of("themxyz")  =', tm.longest_prefix_of("themxyz"))
    print('  has_key_with_prefix("tha")    =', tm.has_key_with_prefix("tha"))
    print('  has_key_with_prefix("thz")    =', tm.has_key_with_prefix("thz"))
    print('  keys_with_prefix("th")        =', tm.keys_with_prefix("th"))

    print("\nPart C: wildcard patterns")
    assert tm.has_key_with_pattern("t.e") is True
    assert tm.has_key_with_pattern("t.x") is False
    assert tm.keys_with_pattern("t..t") == ["that"]
    assert tm.keys_with_pattern(".pp.") == ["appl"]
    print('  has_key_with_pattern("t.e")  =', tm.has_key_with_pattern("t.e"))
    print('  has_key_with_pattern("t.x")  =', tm.has_key_with_pattern("t.x"))
    print('  keys_with_pattern("t..t")    =', tm.keys_with_pattern("t..t"))
    print('  keys_with_pattern(".pp.")    =', tm.keys_with_pattern(".pp."))

    print("\nPart D: delete with pruning")
    size_before = len(tm)
    keys_before = tm.keys()
    app_value = tm.remove("app")
    assert app_value == 2
    assert len(tm) == size_before - 1
    assert tm.contains_key("app") is False
    assert "apple" in tm.keys() and "appl" in tm.keys()
    assert tm.keys() == sorted(tm.keys())
    apple_value = tm.remove("apple")
    assert apple_value == 4
    assert tm.contains_key("apple") is False
    assert tm.contains_key("appl") is True
    assert tm.keys() == sorted(tm.keys())
    missing_value = tm.remove("missing")
    assert missing_value is None
    assert len(tm) == size_before - 2
    print(f"  keys before: {keys_before}")
    print(f"  remove('app') -> {app_value}, keys now: {tm.keys()}")
    print("  pruning kept 'appl' because its own node still carries a value")
    print(f"  remove('apple') -> {apple_value}, 'appl' still present: {tm.contains_key('appl')}")
    print(f"  remove('missing') -> {missing_value}, len unchanged = {len(tm)}")

    print("\nPart E: TrieSet wrapper")
    s = TrieSet()
    s.add("cat")
    s.add("car")
    s.add("dog")
    assert s.contains("cat") is True
    assert s.contains("cow") is False
    assert s.keys() == ["car", "cat", "dog"]
    assert s.keys_with_prefix("ca") == ["car", "cat"]
    assert len(s) == 3
    print('  contains("cat") =', s.contains("cat"))
    print('  contains("cow") =', s.contains("cow"))
    print("  keys() =", s.keys())
    print('  keys_with_prefix("ca") =', s.keys_with_prefix("ca"))

    print("\nASCII trie drawing for 'app', 'appl', 'apple' (# marks end of a key)")
    small = TrieMap[int]()
    small.put("app", 2)
    small.put("appl", 3)
    small.put("apple", 1)
    for line in trie_to_lines(small):
        print("  " + line)
    print("  lexicographic keys:", small.keys())

    print("\nAll asserts passed.")