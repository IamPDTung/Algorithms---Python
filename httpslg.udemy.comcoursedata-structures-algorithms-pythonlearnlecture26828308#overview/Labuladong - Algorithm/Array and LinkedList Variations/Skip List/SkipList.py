from __future__ import annotations

import random
from typing import Generic, Iterator, List, Optional, TypeVar


T = TypeVar("T")


class SkipListNode(Generic[T]):
    def __init__(self, value: Optional[T], level: int):
        self.value = value
        self.forward: List[Optional[SkipListNode[T]]] = [None] * level


class SkipList(Generic[T]):
    """An ordered set implemented with probabilistic forward pointers."""

    def __init__(
        self,
        max_level: int = 16,
        probability: float = 0.5,
        seed: Optional[int] = None,
    ):
        if max_level < 1:
            raise ValueError("max_level must be at least 1")
        if not 0 < probability < 1:
            raise ValueError("probability must be between 0 and 1")

        self.max_level = max_level
        self.probability = probability
        self._level = 1
        self._size = 0
        self._random = random.Random(seed)
        self._head: SkipListNode[T] = SkipListNode(None, max_level)

    def _random_level(self) -> int:
        level = 1
        while level < self.max_level and self._random.random() < self.probability:
            level += 1
        return level

    @staticmethod
    def _validate_value(value: T) -> None:
        if value is None:
            raise ValueError("SkipList values must be comparable and not None")

    def _find_predecessors(
        self, value: T
    ) -> tuple[List[SkipListNode[T]], Optional[SkipListNode[T]]]:
        update: List[SkipListNode[T]] = [self._head] * self.max_level
        current = self._head

        for level in range(self._level - 1, -1, -1):
            next_node = current.forward[level]
            while next_node is not None and next_node.value < value:
                current = next_node
                next_node = current.forward[level]
            update[level] = current

        return update, current.forward[0]

    def search(self, value: T) -> Optional[T]:
        """Return the stored value equal to ``value``, or ``None``."""

        self._validate_value(value)
        _, candidate = self._find_predecessors(value)
        if candidate is not None and candidate.value == value:
            return candidate.value
        return None

    def contains(self, value: T) -> bool:
        return self.search(value) is not None

    def insert(self, value: T) -> bool:
        """Insert a unique value and return whether the list changed."""

        self._validate_value(value)

        update, candidate = self._find_predecessors(value)
        if candidate is not None and candidate.value == value:
            return False

        node_level = self._random_level()
        if node_level > self._level:
            for level in range(self._level, node_level):
                update[level] = self._head
            self._level = node_level

        new_node = SkipListNode(value, node_level)
        for level in range(node_level):
            new_node.forward[level] = update[level].forward[level]
            update[level].forward[level] = new_node

        self._size += 1
        return True

    def delete(self, value: T) -> bool:
        """Delete a value and return whether it was present."""

        self._validate_value(value)
        update, candidate = self._find_predecessors(value)
        if candidate is None or candidate.value != value:
            return False

        for level in range(self._level):
            if update[level].forward[level] is not candidate:
                continue
            update[level].forward[level] = candidate.forward[level]

        while self._level > 1 and self._head.forward[self._level - 1] is None:
            self._level -= 1

        self._size -= 1
        return True

    def levels(self) -> List[List[T]]:
        """Return values in each active level, highest level first."""

        result: List[List[T]] = []
        for level in range(self._level - 1, -1, -1):
            values: List[T] = []
            current = self._head.forward[level]
            while current is not None:
                values.append(current.value)  # type: ignore[arg-type]
                current = current.forward[level]
            result.append(values)
        return result

    def clear(self) -> None:
        self._head.forward = [None] * self.max_level
        self._level = 1
        self._size = 0

    def to_list(self) -> List[T]:
        return list(self)

    def __iter__(self) -> Iterator[T]:
        current = self._head.forward[0]
        while current is not None:
            yield current.value  # type: ignore[misc]
            current = current.forward[0]

    def __contains__(self, value: T) -> bool:
        return self.contains(value)

    def __len__(self) -> int:
        return self._size

    def __repr__(self) -> str:
        return f"SkipList({self.to_list()!r})"


if __name__ == "__main__":
    skip_list = SkipList[int](max_level=5, seed=7)
    for value in (30, 10, 50, 20, 40):
        assert skip_list.insert(value)

    assert skip_list.to_list() == [10, 20, 30, 40, 50]
    assert skip_list.insert(30) is False
    assert skip_list.search(40) == 40
    assert 25 not in skip_list
    assert skip_list.delete(20)
    assert not skip_list.delete(20)

    print("Ordered values:", skip_list.to_list())
    print("Contains 40:", 40 in skip_list)
    print("Contains 25:", 25 in skip_list)
    print("Levels:", skip_list.levels())
