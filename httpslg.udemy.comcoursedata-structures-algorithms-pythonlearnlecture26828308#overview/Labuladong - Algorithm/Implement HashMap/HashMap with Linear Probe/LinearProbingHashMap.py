from __future__ import annotations

from typing import Generic, Iterator, List, Optional, Tuple, TypeVar


K = TypeVar("K")
V = TypeVar("V")


class _Entry(Generic[K, V]):
    def __init__(self, key: K, value: V):
        self.key = key
        self.value = value


_DELETED = object()


class _LinearProbingMapBase(Generic[K, V]):
    """Shared mapping interface for the two linear-probing strategies."""

    def __init__(self, capacity: int, max_load_factor: float):
        if not isinstance(capacity, int) or isinstance(capacity, bool):
            raise TypeError("capacity must be an integer")
        if capacity < 1:
            raise ValueError("capacity must be at least 1")
        if not 0 < max_load_factor < 1:
            raise ValueError("max_load_factor must be in the interval (0, 1)")

        self._capacity = capacity
        self._max_load_factor = max_load_factor
        self._table: List[object] = [None] * capacity
        self._size = 0

    @property
    def capacity(self) -> int:
        return self._capacity

    @property
    def load_factor(self) -> float:
        return self._size / self._capacity

    def _start_index(self, key: K) -> int:
        return hash(key) % self._capacity

    def _find_index(self, key: K) -> Optional[int]:
        raise NotImplementedError

    def _resize(self, new_capacity: int) -> None:
        raise NotImplementedError

    def get(self, key: K, default: Optional[V] = None) -> Optional[V]:
        index = self._find_index(key)
        if index is None:
            return default
        entry = self._table[index]
        return entry.value  # type: ignore[union-attr]

    def contains_key(self, key: K) -> bool:
        return self._find_index(key) is not None

    def items(self) -> Iterator[Tuple[K, V]]:
        for slot in self._table:
            if isinstance(slot, _Entry):
                yield slot.key, slot.value

    def keys(self) -> List[K]:
        return [key for key, _ in self.items()]

    def values(self) -> List[V]:
        return [value for _, value in self.items()]

    def slot_snapshot(self) -> List[object]:
        """Return slots as ``None``, ``"<DELETED>"``, or key/value tuples."""

        snapshot: List[object] = []
        for slot in self._table:
            if slot is None:
                snapshot.append(None)
            elif slot is _DELETED:
                snapshot.append("<DELETED>")
            else:
                entry = slot  # type: ignore[assignment]
                snapshot.append((entry.key, entry.value))
        return snapshot

    def clear(self) -> None:
        self._table = [None] * self._capacity
        self._size = 0
        self._clear_deleted_count()

    def _clear_deleted_count(self) -> None:
        pass

    def __getitem__(self, key: K) -> V:
        index = self._find_index(key)
        if index is None:
            raise KeyError(key)
        entry = self._table[index]
        return entry.value  # type: ignore[union-attr]

    def __setitem__(self, key: K, value: V) -> None:
        self.put(key, value)  # type: ignore[attr-defined]

    def __delitem__(self, key: K) -> None:
        self.remove(key)  # type: ignore[attr-defined]

    def __contains__(self, key: object) -> bool:
        return self.contains_key(key)  # type: ignore[arg-type]

    def __iter__(self) -> Iterator[K]:
        for key, _ in self.items():
            yield key

    def __len__(self) -> int:
        return self._size

    def __repr__(self) -> str:
        return f"{type(self).__name__}({dict(self.items())!r})"


class LinearProbingHashMap(_LinearProbingMapBase[K, V]):
    """A linear-probing map that uses a tombstone for deleted slots."""

    def __init__(self, capacity: int = 8, max_load_factor: float = 0.7):
        super().__init__(capacity, max_load_factor)
        self._deleted_count = 0

    def _find_slot(
        self, key: K, for_insert: bool = False
    ) -> Tuple[Optional[int], bool]:
        index = self._start_index(key)
        first_deleted: Optional[int] = None

        for _ in range(self._capacity):
            slot = self._table[index]
            if slot is None:
                if for_insert and first_deleted is not None:
                    return first_deleted, False
                return index, False
            if slot is _DELETED:
                if first_deleted is None:
                    first_deleted = index
            else:
                entry = slot  # type: ignore[assignment]
                if entry.key == key:
                    return index, True
            index = (index + 1) % self._capacity

        if for_insert and first_deleted is not None:
            return first_deleted, False
        return None, False

    def _find_index(self, key: K) -> Optional[int]:
        index, found = self._find_slot(key)
        return index if found else None

    def _insert_without_resize(self, key: K, value: V) -> None:
        index, found = self._find_slot(key, for_insert=True)
        if index is None or found:
            raise RuntimeError("linear-probing table has no insertion slot")

        if self._table[index] is _DELETED:
            self._deleted_count -= 1
        self._table[index] = _Entry(key, value)
        self._size += 1

    def _resize(self, new_capacity: int) -> None:
        entries = [slot for slot in self._table if isinstance(slot, _Entry)]
        self._capacity = max(1, new_capacity)
        self._table = [None] * self._capacity
        self._size = 0
        self._deleted_count = 0
        for entry in entries:
            self._insert_without_resize(entry.key, entry.value)

    def put(self, key: K, value: V) -> Optional[V]:
        """Insert or update a key and return its previous value, if any."""

        index, found = self._find_slot(key)
        if found and index is not None:
            entry = self._table[index]
            previous_value = entry.value  # type: ignore[union-attr]
            entry.value = value  # type: ignore[union-attr]
            return previous_value

        if self._size + 1 > self._capacity * self._max_load_factor:
            self._resize(self._capacity * 2)
        self._insert_without_resize(key, value)
        return None

    def remove(self, key: K) -> V:
        """Remove a key by marking its slot as deleted."""

        index = self._find_index(key)
        if index is None:
            raise KeyError(key)

        entry = self._table[index]
        self._table[index] = _DELETED
        self._size -= 1
        self._deleted_count += 1

        if (
            self._deleted_count > self._capacity // 2
            and self._deleted_count > self._size
        ):
            self._resize(self._capacity)
        return entry.value  # type: ignore[union-attr]

    def _clear_deleted_count(self) -> None:
        self._deleted_count = 0


class RehashingLinearProbingHashMap(_LinearProbingMapBase[K, V]):
    """A linear-probing map that repairs the cluster after deletion."""

    def __init__(self, capacity: int = 8, max_load_factor: float = 0.7):
        super().__init__(capacity, max_load_factor)

    def _find_index(self, key: K) -> Optional[int]:
        index = self._start_index(key)
        for _ in range(self._capacity):
            slot = self._table[index]
            if slot is None:
                return None
            entry = slot  # type: ignore[assignment]
            if entry.key == key:
                return index
            index = (index + 1) % self._capacity
        return None

    def _empty_slot(self, key: K) -> int:
        index = self._start_index(key)
        for _ in range(self._capacity):
            if self._table[index] is None:
                return index
            index = (index + 1) % self._capacity
        raise RuntimeError("linear-probing table has no empty slot")

    def _insert_without_resize(self, key: K, value: V) -> None:
        index = self._empty_slot(key)
        self._table[index] = _Entry(key, value)
        self._size += 1

    def _resize(self, new_capacity: int) -> None:
        entries = [slot for slot in self._table if isinstance(slot, _Entry)]
        self._capacity = max(1, new_capacity)
        self._table = [None] * self._capacity
        self._size = 0
        for entry in entries:
            self._insert_without_resize(entry.key, entry.value)

    def put(self, key: K, value: V) -> Optional[V]:
        """Insert or update a key and return its previous value, if any."""

        index = self._find_index(key)
        if index is not None:
            entry = self._table[index]
            previous_value = entry.value  # type: ignore[union-attr]
            entry.value = value  # type: ignore[union-attr]
            return previous_value

        if self._size + 1 > self._capacity * self._max_load_factor:
            self._resize(self._capacity * 2)
        self._insert_without_resize(key, value)
        return None

    def remove(self, key: K) -> V:
        """Remove a key and reinsert the cluster that follows its slot."""

        index = self._find_index(key)
        if index is None:
            raise KeyError(key)

        entry = self._table[index]
        self._table[index] = None
        self._size -= 1

        next_index = (index + 1) % self._capacity
        while self._table[next_index] is not None:
            displaced = self._table[next_index]
            self._table[next_index] = None
            self._size -= 1
            self._insert_without_resize(displaced.key, displaced.value)  # type: ignore[union-attr]
            next_index = (next_index + 1) % self._capacity

        return entry.value  # type: ignore[union-attr]


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

    for map_type in (
        LinearProbingHashMap,
        RehashingLinearProbingHashMap,
    ):
        hash_map = map_type[CollisionKey, int](capacity=5)
        first = CollisionKey("first", 1)
        second = CollisionKey("second", 1)
        third = CollisionKey("third", 1)
        replacement = CollisionKey("replacement", 1)

        for key, value in ((first, 10), (second, 20), (third, 30)):
            assert hash_map.put(key, value) is None
        assert hash_map[third] == 30
        assert hash_map.remove(second) == 20
        assert hash_map[third] == 30
        assert hash_map.put(replacement, 40) is None

        print(type(hash_map).__name__)
        print("Items:", list(hash_map.items()))
        print("Slots:", hash_map.slot_snapshot())
