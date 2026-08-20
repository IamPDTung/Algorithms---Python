from __future__ import annotations

from typing import Generic, Iterator, List, Optional, TypeVar, cast


T = TypeVar("T")


class CircularArray(Generic[T]):
    """A resizable array that keeps its logical front at ``_head``.

    Appending at either end is O(1) amortized.  Indexing remains O(1), while
    the physical storage can wrap from the last slot back to the first slot.
    """

    def __init__(self, capacity: int = 4):
        if capacity < 1:
            raise ValueError("capacity must be at least 1")

        self._minimum_capacity = capacity
        self._data: List[Optional[T]] = [None] * capacity
        self._head = 0
        self._size = 0

    @property
    def capacity(self) -> int:
        return len(self._data)

    @property
    def size(self) -> int:
        return self._size

    @property
    def head_index(self) -> int:
        """Return the physical slot used by logical index zero."""

        return self._head

    def _resize(self, new_capacity: int) -> None:
        if new_capacity < self._size:
            raise ValueError("new capacity cannot be smaller than size")

        new_data: List[Optional[T]] = [None] * new_capacity
        for logical_index, value in enumerate(self):
            new_data[logical_index] = value

        self._data = new_data
        self._head = 0

    def _ensure_capacity(self, required_size: int) -> None:
        if required_size <= self.capacity:
            return

        self._resize(max(required_size, self.capacity * 2))

    def _maybe_shrink(self) -> None:
        if self.capacity <= self._minimum_capacity:
            return

        if self._size <= self.capacity // 4:
            self._resize(max(self._minimum_capacity, self.capacity // 2))

    def _normalize_index(self, index: int) -> int:
        if not isinstance(index, int):
            raise TypeError("index must be an integer")

        if index < 0:
            index += self._size

        if not 0 <= index < self._size:
            raise IndexError("circular array index out of range")

        return index

    def _physical_index(self, logical_index: int) -> int:
        return (self._head + logical_index) % self.capacity

    def append(self, value: T) -> None:
        """Add ``value`` after the current logical tail."""

        self._ensure_capacity(self._size + 1)
        tail_index = self._physical_index(self._size)
        self._data[tail_index] = value
        self._size += 1

    def appendleft(self, value: T) -> None:
        """Add ``value`` before the current logical head."""

        self._ensure_capacity(self._size + 1)
        self._head = (self._head - 1) % self.capacity
        self._data[self._head] = value
        self._size += 1

    def pop(self) -> T:
        """Remove and return the logical tail."""

        if self._size == 0:
            raise IndexError("pop from empty circular array")

        tail_index = self._physical_index(self._size - 1)
        value = cast(T, self._data[tail_index])
        self._data[tail_index] = None
        self._size -= 1
        self._maybe_shrink()
        return value

    def popleft(self) -> T:
        """Remove and return the logical head."""

        if self._size == 0:
            raise IndexError("popleft from empty circular array")

        value = cast(T, self._data[self._head])
        self._data[self._head] = None
        self._head = (self._head + 1) % self.capacity
        self._size -= 1
        self._maybe_shrink()
        return value

    def clear(self) -> None:
        """Remove all values and return storage to its minimum capacity."""

        self._data = [None] * self._minimum_capacity
        self._head = 0
        self._size = 0

    def to_list(self) -> List[T]:
        return list(self)

    def debug_slots(self) -> List[Optional[T]]:
        """Return the physical storage, useful when learning the technique."""

        return self._data.copy()

    def __getitem__(self, index: int) -> T:
        logical_index = self._normalize_index(index)
        return cast(T, self._data[self._physical_index(logical_index)])

    def __setitem__(self, index: int, value: T) -> None:
        logical_index = self._normalize_index(index)
        self._data[self._physical_index(logical_index)] = value

    def __iter__(self) -> Iterator[T]:
        for logical_index in range(self._size):
            physical_index = self._physical_index(logical_index)
            yield cast(T, self._data[physical_index])

    def __len__(self) -> int:
        return self._size

    def __repr__(self) -> str:
        return f"CircularArray({self.to_list()!r}, capacity={self.capacity})"


if __name__ == "__main__":
    numbers = CircularArray[int](4)
    numbers.append(10)
    numbers.append(20)
    numbers.append(30)
    numbers.popleft()
    numbers.append(40)
    numbers.append(50)

    # The logical sequence is now split across the physical end of the array.
    print("Logical values:", numbers.to_list())
    print("Physical slots:", numbers.debug_slots())
    print("Head index:", numbers.head_index)

    numbers.appendleft(5)
    assert numbers.to_list() == [5, 20, 30, 40, 50]
    assert numbers[-1] == 50
    assert numbers.pop() == 50
    assert numbers.popleft() == 5
    assert numbers.to_list() == [20, 30, 40]

    print("After both-end operations:", numbers.to_list())
    print("Capacity:", numbers.capacity)
