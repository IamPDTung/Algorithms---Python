from __future__ import annotations

import random
from typing import Generic, Iterator, List, Optional, Tuple, TypeVar


K = TypeVar("K")
V = TypeVar("V")


class _ArrayEntry(Generic[K, V]):
    def __init__(self, key: K, value: V, array_index: int):
        self.key = key
        self.value = value
        self.array_index = array_index
        self.next_bucket: Optional[_ArrayEntry[K, V]] = None


class ArrayHashMap(Generic[K, V]):
    """A hash map with a dense entry array and O(1) ``random_key``."""

    def __init__(
        self,
        capacity: int = 7,
        max_load_factor: float = 0.75,
        rng: Optional[random.Random] = None,
    ):
        if not isinstance(capacity, int) or isinstance(capacity, bool):
            raise TypeError("capacity must be an integer")
        if capacity < 1:
            raise ValueError("capacity must be at least 1")
        if not 0 < max_load_factor <= 1:
            raise ValueError("max_load_factor must be in the interval (0, 1]")

        self._capacity = capacity
        self._max_load_factor = max_load_factor
        self._buckets: List[Optional[_ArrayEntry[K, V]]] = [None] * capacity
        self._entries: List[_ArrayEntry[K, V]] = []
        self._rng = rng if rng is not None else random.Random()

    @property
    def capacity(self) -> int:
        return self._capacity

    @property
    def load_factor(self) -> float:
        return len(self._entries) / self._capacity

    def _bucket_index(self, key: K, capacity: Optional[int] = None) -> int:
        bucket_count = self._capacity if capacity is None else capacity
        return hash(key) % bucket_count

    def _find_entry(
        self, key: K
    ) -> Tuple[int, Optional[_ArrayEntry[K, V]], Optional[_ArrayEntry[K, V]]]:
        index = self._bucket_index(key)
        previous: Optional[_ArrayEntry[K, V]] = None
        current = self._buckets[index]

        while current is not None:
            if current.key == key:
                return index, previous, current
            previous = current
            current = current.next_bucket

        return index, previous, None

    def _resize(self, new_capacity: int) -> None:
        new_buckets: List[Optional[_ArrayEntry[K, V]]] = [None] * new_capacity
        for entry in self._entries:
            index = self._bucket_index(entry.key, new_capacity)
            entry.next_bucket = new_buckets[index]
            new_buckets[index] = entry

        self._capacity = new_capacity
        self._buckets = new_buckets

    def put(self, key: K, value: V) -> Optional[V]:
        """Insert or update a key and return its previous value, if any."""

        index, _, entry = self._find_entry(key)
        if entry is not None:
            previous_value = entry.value
            entry.value = value
            return previous_value

        entry = _ArrayEntry(key, value, len(self._entries))
        entry.next_bucket = self._buckets[index]
        self._buckets[index] = entry
        self._entries.append(entry)

        if self.load_factor > self._max_load_factor:
            self._resize(self._capacity * 2)
        return None

    def get(self, key: K, default: Optional[V] = None) -> Optional[V]:
        """Return a value or ``default`` when the key is absent."""

        _, _, entry = self._find_entry(key)
        return default if entry is None else entry.value

    def remove(self, key: K) -> V:
        """Remove a key and keep the dense array compact."""

        index, previous, entry = self._find_entry(key)
        if entry is None:
            raise KeyError(key)

        if previous is None:
            self._buckets[index] = entry.next_bucket
        else:
            previous.next_bucket = entry.next_bucket

        last_entry = self._entries[-1]
        if entry is not last_entry:
            self._entries[entry.array_index] = last_entry
            last_entry.array_index = entry.array_index
        self._entries.pop()
        entry.next_bucket = None
        return entry.value

    def contains_key(self, key: K) -> bool:
        return self._find_entry(key)[2] is not None

    def random_key(self) -> K:
        """Return a uniformly selected key in O(1) expected time."""

        if not self._entries:
            raise KeyError("random_key from empty ArrayHashMap")
        return self._entries[self._rng.randrange(len(self._entries))].key

    def items(self) -> Iterator[Tuple[K, V]]:
        for entry in self._entries:
            yield entry.key, entry.value

    def keys(self) -> List[K]:
        return [entry.key for entry in self._entries]

    def values(self) -> List[V]:
        return [entry.value for entry in self._entries]

    def dense_array_snapshot(self) -> List[Tuple[K, V]]:
        """Return the compact array used by ``random_key``."""

        return list(self.items())

    def bucket_snapshot(self) -> List[List[Tuple[K, V]]]:
        """Return every bucket chain for visualizing collisions."""

        result: List[List[Tuple[K, V]]] = []
        for head in self._buckets:
            chain: List[Tuple[K, V]] = []
            current = head
            while current is not None:
                chain.append((current.key, current.value))
                current = current.next_bucket
            result.append(chain)
        return result

    def clear(self) -> None:
        self._buckets = [None] * self._capacity
        self._entries.clear()

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
        return len(self._entries)

    def __repr__(self) -> str:
        return f"{type(self).__name__}({dict(self.items())!r})"


if __name__ == "__main__":
    array_map = ArrayHashMap[str, int](capacity=3, rng=random.Random(7))
    array_map.put("alpha", 10)
    array_map.put("beta", 20)
    array_map.put("gamma", 30)
    array_map.put("delta", 40)

    assert array_map["beta"] == 20
    assert array_map.remove("beta") == 20
    assert "beta" not in array_map
    assert len(array_map.dense_array_snapshot()) == len(array_map)
    assert array_map.random_key() in {"alpha", "gamma", "delta"}

    print("Dense array:", array_map.dense_array_snapshot())
    print("Random key:", array_map.random_key())
    print("Buckets:", array_map.bucket_snapshot())
