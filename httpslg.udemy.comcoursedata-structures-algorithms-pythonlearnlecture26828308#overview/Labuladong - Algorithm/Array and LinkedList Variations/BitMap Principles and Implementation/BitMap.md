
---

# BitMap Principles and Implementation

## 1. What Is a Bitmap?

A **bitmap** represents a collection of boolean states with individual bits.
For a set of integers, bit position `x` answers the question:

```text
    Is x present?
```

The implementation in `BitMap.py` stores a fixed universe of values from `0`
through `size - 1` inside a `bytearray`.

```text
    value 0 -> bit 0
    value 1 -> bit 1
    value 2 -> bit 2
    ...
    value 7 -> bit 7
    value 8 -> bit 0 of the next byte
```

One bit stores one yes/no answer. This is much more compact than storing one
Python boolean object or one Python integer object per possible value.

---

## 2. The Problem It Solves

Suppose a problem asks whether IDs from `0` to `15` have appeared:

```text
    Python set representation:

    {1, 3, 8, 13}
```

The set is flexible and offers fast average membership checks, but it stores
hash-table metadata and object references. If the universe is dense and known,
a bitmap can represent the same answers in two bytes:

```text
    values present: 1, 3, 8, 13

    value:     15 14 13 12 11 10  9  8 |  7  6  5  4  3  2  1  0
    bit:        0  0  1  0  0  0  0  1 |  0  0  0  0  1  0  1  0
    byte:                          32 + 1 = 33 |     8 + 2 = 10
```

The bitmap uses exactly `ceil(size / 8)` bytes for the bit storage, not counting
the small Python object and metadata.

---

## 3. Bits, Bytes, and Masks

Eight bits make one byte:

```text
    bit offset:   7   6   5   4   3   2   1   0
                 +---+---+---+---+---+---+---+---+
    byte value:  |   |   |   |   |   |   |   |   |
                 +---+---+---+---+---+---+---+---+
```

For an integer value `x`, calculate:

```text
    byte_index = x >> 3       # same as x // 8
    bit_offset = x & 7        # same as x % 8
    bit_mask   = 1 << bit_offset
```

Example for `x = 13`:

```text
    byte_index = 13 >> 3 = 1
    bit_offset = 13 & 7  = 5
    bit_mask   = 1 << 5  = 00100000
```

The mask selects only the desired bit:

```text
    current byte:  00001011
    mask for 13:   00100000
                    -------- OR
    add 13:        00101011
```

---

## 4. Setting a Bit

Use bitwise OR to turn a bit on:

```python
bits[byte_index] |= bit_mask
```

OR preserves all existing bits and guarantees that the selected bit becomes
`1`:

```text
    current:  01000001
    mask:     00000100
              -------- OR
    result:   01000101
```

Adding an already-present value changes nothing. `BitMap.add()` returns `False`
in that case and keeps its cardinality unchanged.

---

## 5. Clearing a Bit

Use the inverted mask with bitwise AND:

```python
bits[byte_index] &= ~bit_mask
```

The selected bit is forced to `0`, while all other bits remain unchanged:

```text
    current:  01000101
    ~mask:     11111011
               -------- AND
    result:    01000001
```

Python integers use unlimited precision, but assigning the result back to a
`bytearray` element keeps the stored value within one byte.

---

## 6. Testing a Bit

Use bitwise AND and convert the result to a boolean:

```python
present = bool(bits[byte_index] & bit_mask)
```

The result is nonzero exactly when the selected bit is set:

```text
    byte:       01000101
    mask:       00000100
                -------- AND
    result:     00000100  -> present
```

`value in bitmap` is implemented as a safe membership check. Invalid or
out-of-range values return `False` through the membership operator, while the
explicit `add`, `remove`, `toggle`, and `contains` methods reject invalid
values with an exception.

---

## 7. Toggling a Bit

Exclusive OR flips exactly one bit:

```python
bits[byte_index] ^= bit_mask
```

```text
    current:  01000101
    mask:     00000100
              -------- XOR
    result:    01000001

    apply the same XOR again:

    current:  01000001
    mask:     00000100
              -------- XOR
    result:    01000101
```

`BitMap.toggle()` returns the new boolean state after flipping the bit.

---

## 8. Mapping Values to Bytes

For a bitmap of size `20`, three bytes are required because:

```text
    ceil(20 / 8) = 3 bytes
```

The exact calculation is `(size + 7) // 8`, so `20` needs `3` bytes. The valid
values occupy the first four bits of the last byte:

```text
    byte 0: values  0 -  7
    byte 1: values  8 - 15
    byte 2: values 16 - 19, remaining bits unused

    values:       0  1  2  3  4  5  6  7 |  8 ... 15 | 16 17 18 19
    byte index:   0  0  0  0  0  0  0  0 |  1 ...  1 |  2  2  2  2
```

Bits outside the declared universe are rejected when loading raw bytes, so a
`BitMap(20)` cannot accidentally contain value `23`.

---

## 9. Bitmap vs Boolean Array vs Set

| Representation | Membership | Storage idea | Best when |
|:---|:---:|:---|:---|
| Python `set` | Average `O(1)` | Hash table and objects | Values are sparse or arbitrary |
| Boolean list | `O(1)` | One Python object/reference per slot | Simplicity matters |
| `BitMap` | `O(1)` | One bit per possible value | Dense bounded integer universe |
| Sorted list | `O(log n)` with binary search | One object per stored value | Values need ordered storage |

The bitmap is not automatically better. If the universe is enormous but only a
few values are present, a set can use less memory because it does not represent
every missing value.

---

## 10. Implementation Interface

The complete implementation is in `BitMap.py`:

```python
bitmap = BitMap(16)

bitmap.add(13)              # set value 13; returns True if new
bitmap.remove(13)           # clear value 13; returns True if present
bitmap.toggle(13)           # flip value 13; returns its new state
bitmap.contains(13)         # explicit checked membership
13 in bitmap                # safe membership syntax
list(bitmap)                # set values in ascending order
len(bitmap)                 # number of set values
bitmap.to_bytes()           # packed bytes
```

The class also provides `union()` and `intersection()` for bitwise set
operations between bitmaps with the same universe size.

---

## 11. Union and Intersection

Two bitmaps with the same universe can be combined byte by byte.

```text
    A:       01001100
    B:       00010110

    A union B:
             01011110       bitwise OR

    A intersect B:
             00000100       bitwise AND
```

The result has the same `size` as both inputs. The implementation recalculates
the number of set bits after the operation.

---

## 12. Enumerating Set Values

To iterate efficiently, the implementation scans each byte and repeatedly
removes its lowest set bit:

```text
    remaining = byte
    while remaining != 0:
        lowest_bit = remaining & -remaining
        process lowest_bit
        remaining ^= lowest_bit
```

Example:

```text
    remaining:       10110100
    lowest bit:      00000100
    after removing:  10110000

    lowest bit:      00010000
    after removing:  10100000
```

This visits set bits rather than testing every possible value inside a byte.
The yielded values are still in ascending order because bytes and bit offsets
are scanned from low to high.

---

## 13. Serialization

`to_bytes()` returns the packed representation. The size is stored separately
because the final byte may contain unused bits:

```python
payload = bitmap.to_bytes()
restored = BitMap.from_bytes(bitmap.size, payload)
```

The serialized bytes do not contain Python object metadata. They are useful for
compact storage or transfer when the receiver also knows the universe size.

---

## 14. Complexity

| Operation | Time | Extra space | Reason |
|:---|:---:|:---:|:---|
| `add` | `O(1)` | `O(1)` | Locate one byte and set one bit |
| `remove` | `O(1)` | `O(1)` | Locate one byte and clear one bit |
| `toggle` | `O(1)` | `O(1)` | One XOR-like update |
| `contains` | `O(1)` | `O(1)` | One byte lookup |
| `len` | `O(1)` | `O(1)` | Maintained counter |
| Iteration | `O(number of set bits + bytes)` | `O(1)` | Scan packed storage |
| `union` | `O(size / 8)` | `O(size / 8)` | Combine every byte |
| `intersection` | `O(size / 8)` | `O(size / 8)` | Combine every byte |
| Storage | - | `O(size / 8)` bytes | One bit per possible value |

The input universe size controls bitmap memory, even if only one value is set.

---

## 15. Where Is It Useful?

```text
    +---------------------------------------------------------------+
    | BITMAP USE CASES                                              |
    +---------------------------------------------------------------+
    | Presence flags       -> seen IDs, visited states              |
    | Sieve of Eratosthenes-> mark composite integers               |
    | Permission masks     -> compact feature flags                 |
    | Deduplication        -> bounded integer values                |
    | Bloom-filter bits    -> compact probabilistic membership       |
    | Calendar occupancy   -> one bit per day or time slot           |
    +---------------------------------------------------------------+
```

A bitmap is especially valuable in contest problems with constraints such as
`0 <= value <= 10^7` and a need for fast presence checks. Always compare its
`size / 8` memory cost with the problem's memory limit.

---

## 16. Edge Cases

### Empty Universe

`BitMap(0)` is valid but has no valid values. Adding any value raises an error.

### Duplicate Add

Adding a value twice does not increase `len(bitmap)` twice.

### Invalid Values

The explicit mutation and query methods reject negative values, values greater
than or equal to `size`, non-integers, and booleans.

### Unused Final Bits

If `size` is not divisible by `8`, the final byte has unused high bits. The
serialization loader rejects those bits instead of silently inventing values
outside the declared universe.

### Sparse Universe

If `size` is `10^9` and only three values exist, a bitmap requires about
`125,000,000` bytes before Python object overhead. A set is likely more suitable.

---

## 17. Running the Example

Run:

```text
python BitMap.py
```

Expected output:

```text
Members: [1, 3, 8, 13]
Count: 4
Contains 13: True
After remove/toggle: [1, 5, 8, 13]
Union: [1, 5, 8, 12, 13]
Intersection: [5]
```

---

## 18. Final Cheat Sheet

```text
    1. A bitmap stores one boolean state per bit.
    2. byte_index = value >> 3.
    3. bit_mask = 1 << (value & 7).
    4. OR sets a bit.
    5. AND with an inverted mask clears a bit.
    6. AND tests a bit.
    7. XOR toggles a bit.
    8. Membership is O(1).
    9. Storage is one bit per value in the universe.
   10. Use a set instead when the universe is large and sparse.
```

**Next Step:** Write the byte and mask for values `0`, `7`, `8`, and `15` by
hand, then compare them with `BitMap.debug`-style reasoning in `BitMap.py`.
