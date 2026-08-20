from __future__ import annotations

from typing import Generic, Iterator, List, Optional, Tuple, TypeVar


K = TypeVar("K")
V = TypeVar("V")


class _LinkedEntry(Generic[K, V]):
    def __init__(self, key: K, value: V):
        self.key = key
        self.value = value

        # Link used by the hash bucket.
        self.next_bucket: Optional[_LinkedEntry[K, V]] = None

        # Links used by the global insertion-order list.
        self.previous_order: Optional[_LinkedEntry[K, V]] = None
        self.next_order: Optional[_LinkedEntry[K, V]] = None


class LinkedHashMap(Generic[K, V]):
    """A resizable hash map that iterates keys in insertion order."""

    def __init__(self, capacity: int = 7, max_load_factor: float = 0.75):
        if not isinstance(capacity, int) or isinstance(capacity, bool):
            raise TypeError("capacity must be an integer")
        if capacity < 1:
            raise ValueError("capacity must be at least 1")
        if not 0 < max_load_factor <= 1:
            raise ValueError("max_load_factor must be in the interval (0, 1]")

        self._capacity = capacity
        self._max_load_factor = max_load_factor
        self._buckets: List[Optional[_LinkedEntry[K, V]]] = [None] * capacity
        self._head: Optional[_LinkedEntry[K, V]] = None
        self._tail: Optional[_LinkedEntry[K, V]] = None
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
    ) -> Tuple[int, Optional[_LinkedEntry[K, V]], Optional[_LinkedEntry[K, V]]]:
        index = self._bucket_index(key)
        previous: Optional[_LinkedEntry[K, V]] = None
        current = self._buckets[index]

        while current is not None:
            if current.key == key:
                return index, previous, current
            previous = current
            current = current.next_bucket

        return index, previous, None

    def _append_to_order(self, entry: _LinkedEntry[K, V]) -> None:
        if self._tail is None:
            self._head = entry
            self._tail = entry
            return

        entry.previous_order = self._tail
        self._tail.next_order = entry
        self._tail = entry

    def _remove_from_order(self, entry: _LinkedEntry[K, V]) -> None:
        if entry.previous_order is None:
            self._head = entry.next_order
        else:
            entry.previous_order.next_order = entry.next_order

        if entry.next_order is None:
            self._tail = entry.previous_order
        else:
            entry.next_order.previous_order = entry.previous_order

        entry.previous_order = None
        entry.next_order = None

    def _resize(self, new_capacity: int) -> None:
        new_buckets: List[Optional[_LinkedEntry[K, V]]] = [None] * new_capacity
        current = self._head

        # Rehash in list order. The order links are intentionally untouched.
        while current is not None:
            next_in_order = current.next_order
            index = self._bucket_index(current.key, new_capacity)
            current.next_bucket = new_buckets[index]
            new_buckets[index] = current
            current = next_in_order

        self._capacity = new_capacity
        self._buckets = new_buckets

    def put(self, key: K, value: V) -> Optional[V]:
        """Insert or update a key and return its previous value, if any."""

        index, _, entry = self._find_entry(key)
        if entry is not None:
            previous_value = entry.value
            entry.value = value
            return previous_value

        entry = _LinkedEntry(key, value)
        entry.next_bucket = self._buckets[index]
        self._buckets[index] = entry
        self._append_to_order(entry)
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
            self._buckets[index] = entry.next_bucket
        else:
            previous.next_bucket = entry.next_bucket

        self._remove_from_order(entry)
        entry.next_bucket = None
        self._size -= 1
        return entry.value

    def contains_key(self, key: K) -> bool:
        return self._find_entry(key)[2] is not None

    def items(self) -> Iterator[Tuple[K, V]]:
        """Yield entries from oldest insertion to newest insertion."""

        current = self._head
        while current is not None:
            yield current.key, current.value
            current = current.next_order

    def keys(self) -> List[K]:
        return [key for key, _ in self.items()]

    def values(self) -> List[V]:
        return [value for _, value in self.items()]

    def clear(self) -> None:
        self._buckets = [None] * self._capacity
        self._head = None
        self._tail = None
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

    linked_map = LinkedHashMap[CollisionKey, int](capacity=3)
    alpha = CollisionKey("alpha", 1)
    beta = CollisionKey("beta", 1)
    gamma = CollisionKey("gamma", 2)
    delta = CollisionKey("delta", 0)

    linked_map.put(alpha, 10)
    linked_map.put(beta, 20)
    linked_map.put(gamma, 30)
    assert linked_map.keys() == [alpha, beta, gamma]
    assert linked_map.put(beta, 25) == 20
    assert linked_map.keys() == [alpha, beta, gamma]
    assert linked_map.remove(alpha) == 10
    linked_map.put(delta, 40)
    assert linked_map.keys() == [beta, gamma, delta]

    print("Insertion order:", linked_map.keys())
    print("Items:", list(linked_map.items()))
    print("Size:", len(linked_map))
