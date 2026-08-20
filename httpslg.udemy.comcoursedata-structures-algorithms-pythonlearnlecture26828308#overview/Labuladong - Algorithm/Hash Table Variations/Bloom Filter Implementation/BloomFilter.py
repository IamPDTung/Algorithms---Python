from __future__ import annotations

from math import exp, ceil, log
from typing import Generic, Iterable, Optional, TypeVar


T = TypeVar("T")


class BloomFilter(Generic[T]):
    """A compact probabilistic membership filter for hashable values.

    A positive result means the value *might* have been added. A negative
    result means the value has definitely not been added.
    """

    _SECONDARY_SALT = 0x9E3779B97F4A7C15

    def __init__(
        self,
        expected_items: int,
        false_positive_rate: float = 0.01,
    ):
        if (
            not isinstance(expected_items, int)
            or isinstance(expected_items, bool)
        ):
            raise TypeError("expected_items must be an integer")
        if expected_items < 1:
            raise ValueError("expected_items must be at least 1")
        if not 0 < false_positive_rate < 1:
            raise ValueError("false_positive_rate must be in the interval (0, 1)")

        self._expected_items = expected_items
        self._target_false_positive_rate = false_positive_rate
        self._bit_count = max(
            1,
            ceil(
                -expected_items
                * log(false_positive_rate)
                / (log(2) ** 2)
            ),
        )
        self._hash_count = max(
            1,
            round(self._bit_count / expected_items * log(2)),
        )
        self._bits = bytearray((self._bit_count + 7) // 8)
        self._insertions = 0

    @property
    def expected_items(self) -> int:
        return self._expected_items

    @property
    def false_positive_rate(self) -> float:
        return self._target_false_positive_rate

    @property
    def bit_count(self) -> int:
        return self._bit_count

    @property
    def hash_count(self) -> int:
        return self._hash_count

    @property
    def byte_count(self) -> int:
        return len(self._bits)

    @property
    def insertions(self) -> int:
        """Return add calls, not the number of unique values."""

        return self._insertions

    def _hash_pair(self, value: T) -> tuple[int, int]:
        first_hash = hash(value)
        second_hash = hash((value, self._SECONDARY_SALT)) % self._bit_count
        if second_hash == 0:
            second_hash = 1
        return first_hash, second_hash

    def _positions(self, value: T):
        first_hash, second_hash = self._hash_pair(value)
        for offset in range(self._hash_count):
            yield (first_hash + offset * second_hash) % self._bit_count

    @staticmethod
    def _location(bit_position: int) -> tuple[int, int]:
        byte_index = bit_position >> 3
        bit_mask = 1 << (bit_position & 7)
        return byte_index, bit_mask

    def add(self, value: T) -> None:
        """Add a value's fingerprints without storing the value itself."""

        for bit_position in self._positions(value):
            byte_index, bit_mask = self._location(bit_position)
            self._bits[byte_index] |= bit_mask
        self._insertions += 1

    def add_many(self, values: Iterable[T]) -> None:
        for value in values:
            self.add(value)

    def might_contain(self, value: T) -> bool:
        """Return False for definite absence and True for possible presence."""

        for bit_position in self._positions(value):
            byte_index, bit_mask = self._location(bit_position)
            if not self._bits[byte_index] & bit_mask:
                return False
        return True

    def contains(self, value: T) -> bool:
        """Alias for ``might_contain`` that emphasizes membership testing."""

        return self.might_contain(value)

    def estimated_false_positive_rate(
        self, item_count: Optional[int] = None
    ) -> float:
        """Estimate the false-positive rate after ``item_count`` additions."""

        count = self._insertions if item_count is None else item_count
        if not isinstance(count, int) or isinstance(count, bool):
            raise TypeError("item_count must be an integer")
        if count < 0:
            raise ValueError("item_count cannot be negative")

        occupied_probability = 1 - exp(-self._hash_count * count / self._bit_count)
        return occupied_probability**self._hash_count

    def clear(self) -> None:
        """Clear every fingerprint while keeping the configured dimensions."""

        self._bits = bytearray(len(self._bits))
        self._insertions = 0

    def to_bytes(self) -> bytes:
        """Return the packed bit array for inspection or storage."""

        return bytes(self._bits)

    def __contains__(self, value: object) -> bool:
        return self.might_contain(value)  # type: ignore[arg-type]

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}(bits={self._bit_count}, "
            f"hashes={self._hash_count}, insertions={self._insertions})"
        )


if __name__ == "__main__":
    bloom = BloomFilter[str](expected_items=20, false_positive_rate=0.01)
    bloom.add_many(["/admin", "/login", "/private/report"])

    assert "/admin" in bloom
    missing_result = "maybe present" if "/missing" in bloom else "definitely absent"

    possible_false_positive = next(
        (
            f"/candidate/{index}"
            for index in range(1000)
            if f"/candidate/{index}" in bloom
        ),
        None,
    )
    print("Filter:", bloom)
    print("Bits:", bloom.bit_count)
    print("Missing URL:", missing_result)
    print("Possible false positive:", possible_false_positive)
    print("Estimated rate:", bloom.estimated_false_positive_rate())
