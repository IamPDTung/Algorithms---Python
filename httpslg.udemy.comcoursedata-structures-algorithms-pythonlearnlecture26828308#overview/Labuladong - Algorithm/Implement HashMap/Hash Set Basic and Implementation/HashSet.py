from __future__ import annotations

from typing import Generic, Iterable, Iterator, List, Optional, Tuple, TypeVar


T = TypeVar("T")


class _SetNode(Generic[T]):
    def __init__(self, value: T, next_node: Optional[_SetNode[T]] = None):
        self.value = value
        self.next = next_node


class HashSet(Generic[T]):
    """A resizable hash set implemented with separate-chained buckets."""

    def __init__(
        self,
        values: Optional[Iterable[T]] = None,
        capacity: int = 7,
        max_load_factor: float = 0.75,
    ):
        if not isinstance(capacity, int) or isinstance(capacity, bool):
            raise TypeError("capacity must be an integer")
        if capacity < 1:
            raise ValueError("capacity must be at least 1")
        if not 0 < max_load_factor <= 1:
            raise ValueError("max_load_factor must be in the interval (0, 1]")

        self._capacity = capacity
        self._max_load_factor = max_load_factor
        self._buckets: List[Optional[_SetNode[T]]] = [None] * capacity
        self._size = 0

        if values is not None:
            self.update(values)

    @property
    def capacity(self) -> int:
        return self._capacity

    @property
    def load_factor(self) -> float:
        return self._size / self._capacity

    def _bucket_index(self, value: T, capacity: Optional[int] = None) -> int:
        bucket_count = self._capacity if capacity is None else capacity
        return hash(value) % bucket_count

    def _find_node(
        self, value: T
    ) -> Tuple[int, Optional[_SetNode[T]], Optional[_SetNode[T]]]:
        index = self._bucket_index(value)
        previous: Optional[_SetNode[T]] = None
        current = self._buckets[index]

        while current is not None:
            if current.value == value:
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
                next_node = current.next
                index = self._bucket_index(current.value)
                current.next = self._buckets[index]
                self._buckets[index] = current
                current = next_node

    def add(self, value: T) -> bool:
        """Add a value and return whether the set changed."""

        index, _, node = self._find_node(value)
        if node is not None:
            return False

        self._buckets[index] = _SetNode(value, self._buckets[index])
        self._size += 1
        if self.load_factor > self._max_load_factor:
            self._resize(self._capacity * 2)
        return True

    def discard(self, value: T) -> bool:
        """Remove a value if present and return whether it was found."""

        index, previous, node = self._find_node(value)
        if node is None:
            return False

        if previous is None:
            self._buckets[index] = node.next
        else:
            previous.next = node.next
        self._size -= 1
        return True

    def remove(self, value: T) -> None:
        """Remove a value, raising ``KeyError`` when it is absent."""

        if not self.discard(value):
            raise KeyError(value)

    def contains(self, value: T) -> bool:
        return self._find_node(value)[2] is not None

    def update(self, values: Iterable[T]) -> None:
        for value in values:
            self.add(value)

    def union(self, other: Iterable[T]) -> HashSet[T]:
        result = HashSet(self, capacity=self._capacity)
        result.update(other)
        return result

    def intersection(self, other: Iterable[T]) -> HashSet[T]:
        other_set = other if isinstance(other, HashSet) else HashSet(other)
        return HashSet(
            (value for value in self if value in other_set),
            capacity=self._capacity,
        )

    def difference(self, other: Iterable[T]) -> HashSet[T]:
        other_set = other if isinstance(other, HashSet) else HashSet(other)
        return HashSet(
            (value for value in self if value not in other_set),
            capacity=self._capacity,
        )

    def is_subset(self, other: Iterable[T]) -> bool:
        other_set = other if isinstance(other, HashSet) else HashSet(other)
        return all(value in other_set for value in self)

    def bucket_snapshot(self) -> List[List[T]]:
        """Return every chain for visualizing collisions."""

        result: List[List[T]] = []
        for head in self._buckets:
            chain: List[T] = []
            current = head
            while current is not None:
                chain.append(current.value)
                current = current.next
            result.append(chain)
        return result

    def clear(self) -> None:
        self._buckets = [None] * self._capacity
        self._size = 0

    def __contains__(self, value: object) -> bool:
        return self.contains(value)  # type: ignore[arg-type]

    def __iter__(self) -> Iterator[T]:
        for head in self._buckets:
            current = head
            while current is not None:
                yield current.value
                current = current.next

    def __len__(self) -> int:
        return self._size

    def __or__(self, other: Iterable[T]) -> HashSet[T]:
        return self.union(other)

    def __and__(self, other: Iterable[T]) -> HashSet[T]:
        return self.intersection(other)

    def __sub__(self, other: Iterable[T]) -> HashSet[T]:
        return self.difference(other)

    def __repr__(self) -> str:
        return f"{type(self).__name__}({list(self)!r})"


if __name__ == "__main__":
    numbers = HashSet([1, 3, 5, 7], capacity=5)
    other = HashSet([3, 5, 8], capacity=5)

    assert numbers.add(1) is False
    assert numbers.add(9) is True
    assert 9 in numbers
    assert numbers.discard(7)
    assert not numbers.discard(7)

    print("Members:", sorted(numbers))
    print("Count:", len(numbers))
    print("Union:", sorted(numbers | other))
    print("Intersection:", sorted(numbers & other))
    print("Difference:", sorted(numbers - other))
    print("Chains:", numbers.bucket_snapshot())
