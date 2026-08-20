from __future__ import annotations

from typing import Generic, Iterator, List, Optional, Tuple, TypeVar


K = TypeVar("K")
V = TypeVar("V")


class _Entry(Generic[K, V]):
    def __init__(
        self,
        key: K,
        value: V,
        next_entry: Optional[_Entry[K, V]] = None,
    ):
        self.key = key
        self.value = value
        self.next = next_entry


class SeparateChainingHashMap(Generic[K, V]):
    """A resizable hash map whose buckets use linked-list chaining."""

    def __init__(self, capacity: int = 7, max_load_factor: float = 0.75):
        if not isinstance(capacity, int) or isinstance(capacity, bool):
            raise TypeError("capacity must be an integer")
        if capacity < 1:
            raise ValueError("capacity must be at least 1")
        if not 0 < max_load_factor <= 1:
            raise ValueError("max_load_factor must be in the interval (0, 1]")

        self._capacity = capacity
        self._max_load_factor = max_load_factor
        self._buckets: List[Optional[_Entry[K, V]]] = [None] * capacity
        self._size = 0

    @property
    def capacity(self) -> int:
        return self._capacity

    @property
    def load_factor(self) -> float:
        return self._size / self._capacity

    def _bucket_index(self, key: K, capacity: Optional[int] = None) -> int:
        bucket_count = self._capacity if capacity is None else capacity
        return hash(key) % bucket_count

    def _find_entry(
        self, key: K
    ) -> Tuple[int, Optional[_Entry[K, V]], Optional[_Entry[K, V]]]:
        index = self._bucket_index(key)
        previous: Optional[_Entry[K, V]] = None
        current = self._buckets[index]

        while current is not None:
            if current.key == key:
                return index, previous, current
            previous = current
            current = current.next

        return index, previous, None

    def _resize(self, new_capacity: int) -> None:
        old_buckets = self._buckets
        self._capacity = new_capacity
        self._buckets = [None] * new_capacity

        for head in old_buckets:
            current = head
            while current is not None:
                next_entry = current.next
                index = self._bucket_index(current.key)
                current.next = self._buckets[index]
                self._buckets[index] = current
                current = next_entry

    def put(self, key: K, value: V) -> Optional[V]:
        """Insert or update a key and return its previous value, if any."""

        index, _, entry = self._find_entry(key)
        if entry is not None:
            previous_value = entry.value
            entry.value = value
            return previous_value

        self._buckets[index] = _Entry(key, value, self._buckets[index])
        self._size += 1

        if self.load_factor > self._max_load_factor:
            self._resize(self._capacity * 2)
        return None

    def get(self, key: K, default: Optional[V] = None) -> Optional[V]:
        """Return a value or ``default`` when the key is absent."""

        _, _, entry = self._find_entry(key)
        return default if entry is None else entry.value

    def remove(self, key: K) -> V:
        """Remove a key and return its value.

        Raises:
            KeyError: If ``key`` is not present.
        """

        index, previous, entry = self._find_entry(key)
        if entry is None:
            raise KeyError(key)

        if previous is None:
            self._buckets[index] = entry.next
        else:
            previous.next = entry.next
        self._size -= 1
        return entry.value

    def contains_key(self, key: K) -> bool:
        return self._find_entry(key)[2] is not None

    def items(self) -> Iterator[Tuple[K, V]]:
        for head in self._buckets:
            current = head
            while current is not None:
                yield current.key, current.value
                current = current.next

    def keys(self) -> List[K]:
        return [key for key, _ in self.items()]

    def values(self) -> List[V]:
        return [value for _, value in self.items()]

    def bucket_snapshot(self) -> List[List[Tuple[K, V]]]:
        """Return every chain for visualizing collisions."""

        return [list(self._chain_items(head)) for head in self._buckets]

    @staticmethod
    def _chain_items(head: Optional[_Entry[K, V]]) -> Iterator[Tuple[K, V]]:
        current = head
        while current is not None:
            yield current.key, current.value
            current = current.next

    def clear(self) -> None:
        self._buckets = [None] * self._capacity
        self._size = 0

    def __getitem__(self, key: K) -> V:
        _, _, entry = self._find_entry(key)
        if entry is None:
            raise KeyError(key)
        return entry.value

    def __setitem__(self, key: K, value: V) -> None:
        self.put(key, value)

    def __delitem__(self, key: K) -> None:
        self.remove(key)

    def __contains__(self, key: object) -> bool:
        return self.contains_key(key)  # type: ignore[arg-type]

    def __iter__(self) -> Iterator[K]:
        for key, _ in self.items():
            yield key

    def __len__(self) -> int:
        return self._size

    def __repr__(self) -> str:
        return f"{type(self).__name__}({dict(self.items())!r})"


if __name__ == "__main__":
    class CollisionKey:
        def __init__(self, name: str, hash_value: int):
            self.name = name
            self.hash_value = hash_value

        def __hash__(self) -> int:
            return self.hash_value

        def __eq__(self, other: object) -> bool:
            return (
                isinstance(other, CollisionKey)
                and self.name == other.name
                and self.hash_value == other.hash_value
            )

        def __repr__(self) -> str:
            return self.name

    hash_map = SeparateChainingHashMap[CollisionKey, int](capacity=5)
    alpha = CollisionKey("alpha", 1)
    beta = CollisionKey("beta", 1)
    gamma = CollisionKey("gamma", 3)

    assert hash_map.put(alpha, 10) is None
    assert hash_map.put(beta, 20) is None
    assert hash_map.put(gamma, 30) is None
    assert hash_map[alpha] == 10
    assert hash_map[beta] == 20
    assert hash_map.put(alpha, 15) == 10
    assert hash_map.remove(beta) == 20
    assert beta not in hash_map

    print("Items:", list(hash_map.items()))
    print("Chains:", hash_map.bucket_snapshot())
    print("Size:", len(hash_map))
