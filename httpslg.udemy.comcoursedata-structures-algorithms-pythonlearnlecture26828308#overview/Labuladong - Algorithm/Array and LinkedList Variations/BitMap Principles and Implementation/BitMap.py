from __future__ import annotations

from typing import Iterator, List


class BitMap:
    """A fixed-universe set of non-negative integers backed by bits."""

    def __init__(self, size: int):
        if not isinstance(size, int) or isinstance(size, bool):
            raise TypeError("size must be an integer")
        if size < 0:
            raise ValueError("size cannot be negative")

        self._size = size
        self._bits = bytearray((size + 7) // 8)
        self._count = 0

    @property
    def size(self) -> int:
        """Return the exclusive upper bound of valid values."""

        return self._size

    def _validate(self, value: int) -> None:
        if not isinstance(value, int) or isinstance(value, bool):
            raise TypeError("bitmap values must be integers")
        if not 0 <= value < self._size:
            raise ValueError(f"value must be between 0 and {self._size - 1}")

    @staticmethod
    def _location(value: int) -> tuple[int, int]:
        byte_index = value >> 3
        bit_mask = 1 << (value & 7)
        return byte_index, bit_mask

    def add(self, value: int) -> bool:
        """Set a bit; return True only when the set changed."""

        self._validate(value)
        byte_index, bit_mask = self._location(value)
        if self._bits[byte_index] & bit_mask:
            return False

        self._bits[byte_index] |= bit_mask
        self._count += 1
        return True

    def remove(self, value: int) -> bool:
        """Clear a bit; return True only when the value was present."""

        self._validate(value)
        byte_index, bit_mask = self._location(value)
        if not self._bits[byte_index] & bit_mask:
            return False

        self._bits[byte_index] &= ~bit_mask
        self._count -= 1
        return True

    def toggle(self, value: int) -> bool:
        """Flip a bit and return its new state."""

        self._validate(value)
        byte_index, bit_mask = self._location(value)
        was_set = bool(self._bits[byte_index] & bit_mask)

        if was_set:
            self._bits[byte_index] &= ~bit_mask
            self._count -= 1
        else:
            self._bits[byte_index] |= bit_mask
            self._count += 1

        return not was_set

    def contains(self, value: int) -> bool:
        self._validate(value)
        byte_index, bit_mask = self._location(value)
        return bool(self._bits[byte_index] & bit_mask)

    def clear(self) -> None:
        """Clear every bit while keeping the universe size."""

        self._bits = bytearray(len(self._bits))
        self._count = 0

    def to_bytes(self) -> bytes:
        """Return the packed byte representation."""

        return bytes(self._bits)

    @classmethod
    def from_bytes(cls, size: int, raw: bytes) -> "BitMap":
        """Rebuild a bitmap from bytes produced by ``to_bytes``."""

        if not isinstance(raw, (bytes, bytearray)):
            raise TypeError("raw must be bytes or bytearray")

        bitmap = cls(size)
        expected_length = len(bitmap._bits)
        if len(raw) != expected_length:
            raise ValueError(
                f"raw must contain exactly {expected_length} bytes"
            )

        bitmap._bits = bytearray(raw)
        if size % 8:
            valid_mask = (1 << (size % 8)) - 1
            if bitmap._bits and bitmap._bits[-1] & ~valid_mask:
                raise ValueError("raw contains bits outside the bitmap universe")

        bitmap._count = sum(bin(byte).count("1") for byte in bitmap._bits)
        return bitmap

    def _check_compatible(self, other: "BitMap") -> None:
        if not isinstance(other, BitMap):
            raise TypeError("other must be a BitMap")
        if self._size != other._size:
            raise ValueError("bitmaps must have the same size")

    def union(self, other: "BitMap") -> "BitMap":
        self._check_compatible(other)
        result = BitMap(self._size)
        result._bits = bytearray(
            left | right for left, right in zip(self._bits, other._bits)
        )
        result._count = sum(bin(byte).count("1") for byte in result._bits)
        return result

    def intersection(self, other: "BitMap") -> "BitMap":
        self._check_compatible(other)
        result = BitMap(self._size)
        result._bits = bytearray(
            left & right for left, right in zip(self._bits, other._bits)
        )
        result._count = sum(bin(byte).count("1") for byte in result._bits)
        return result

    def __contains__(self, value: object) -> bool:
        if not isinstance(value, int) or isinstance(value, bool):
            return False
        if not 0 <= value < self._size:
            return False

        byte_index, bit_mask = self._location(value)
        return bool(self._bits[byte_index] & bit_mask)

    def __iter__(self) -> Iterator[int]:
        """Yield set values in ascending order."""

        for byte_index, byte in enumerate(self._bits):
            remaining = byte
            while remaining:
                lowest_bit = remaining & -remaining
                bit_offset = lowest_bit.bit_length() - 1
                value = byte_index * 8 + bit_offset
                if value < self._size:
                    yield value
                remaining ^= lowest_bit

    def __len__(self) -> int:
        return self._count

    def __repr__(self) -> str:
        return f"BitMap(size={self._size}, values={list(self)!r})"


if __name__ == "__main__":
    bitmap = BitMap(16)
    for value in (1, 3, 8, 13):
        bitmap.add(value)

    print("Members:", list(bitmap))
    print("Count:", len(bitmap))
    print("Contains 13:", 13 in bitmap)

    bitmap.remove(3)
    bitmap.toggle(5)
    print("After remove/toggle:", list(bitmap))

    other = BitMap(16)
    other.add(5)
    other.add(12)
    print("Union:", list(bitmap.union(other)))
    print("Intersection:", list(bitmap.intersection(other)))

    restored = BitMap.from_bytes(bitmap.size, bitmap.to_bytes())
    assert list(restored) == list(bitmap)
