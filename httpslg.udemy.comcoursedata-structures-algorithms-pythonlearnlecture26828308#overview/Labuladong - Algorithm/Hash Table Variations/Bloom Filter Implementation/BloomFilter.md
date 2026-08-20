
---

# Bloom Filter Implementation

## 1. What Is a Bloom Filter?

A **Bloom filter** is a compact probabilistic data structure for membership
testing. It does not store the original values. Instead, it stores several bit
positions derived from each value's hash fingerprints.

Its answers have an intentional asymmetry:

- `False` means the value is definitely absent.
- `True` means the value might be present.

The implementation in `BloomFilter.py` uses a `bytearray` as the bit array and
double hashing to generate multiple positions. It is an add-only filter with a
`clear` operation; it does not expose an unsafe per-value delete operation.

Source references:

- [Hash Set Basic and Implementation](https://labuladong.online/en/algo/data-structure-basic/hash-set/)
- [Bloom Filter Core Principles and Implementation](https://labuladong.online/en/algo/data-structure-basic/bloom-filter/)
- [Bitmap Principles and Implementation](https://labuladong.online/en/algo/data-structure-basic/bitmap/)

## 2. Why a Hash Set Is Not Always Enough

A hash set gives exact membership testing and expected `O(1)` insertion and
lookup. However, it stores the real values, entry objects, references, and hash
table metadata. For a very large data set, that memory cost can be too high.

A Bloom filter is useful as a small preliminary test:

```text
query
  |
  v
Bloom filter says False? ---- yes ---> definitely absent
  |
  no
  v
Check the expensive hash set, database, or disk file
```

It can avoid expensive work when an item is definitely not in a large data
source. It cannot replace an exact set when a false positive would be harmful.

## 3. The Bit Array

The filter owns `m` bits, initially all zero:

```text
bits: 0 0 0 0 0 0 0 0 0 0 0 0 ...
       ^       ^       ^
       positions set by one inserted value
```

The Python implementation packs eight logical bits into each `bytearray` byte:

```python
byte_index = bit_position >> 3
bit_mask = 1 << (bit_position & 7)
bits[byte_index] |= bit_mask       # set
bool(bits[byte_index] & bit_mask)  # test
```

The filter stores no list of inserted values. Its memory for fingerprints is
`ceil(m / 8)` bytes, plus small object metadata.

## 4. Multiple Hash Positions

One hash position creates too many collisions. Bloom filters therefore use `k`
positions for every value:

```text
value -> h1, h2
          |
          +--> (h1 + 0 * h2) % m
          +--> (h1 + 1 * h2) % m
          +--> (h1 + 2 * h2) % m
          +--> ...
```

This is double hashing. It derives several positions from two hash values rather
than allocating `k` unrelated hash-function implementations. The positions are
set when a value is added and checked again during a query.

`BloomFilter` requires hashable values, just like a hash set. Python's `hash`
result can be negative; modulo by the positive bit count maps it to a valid bit.

## 5. Adding a Value

To add `x`, calculate all `k` positions and set every corresponding bit:

```text
before: all selected bits may be 0
add x:  set position 4, position 19, position 37, ... to 1
after:  those bits remain 1
```

Adding the same value again is harmless. It sets the same bits and does not
change the filter's logical answer. The implementation's `insertions` property
counts calls to `add`, not unique values, because a standard Bloom filter cannot
recover a unique cardinality from its bits.

The configured `expected_items` is a sizing target, not a hard insertion limit.
Adding more items is allowed, but the false-positive rate will increase beyond
the target estimate.

## 6. Membership Testing

To test `x`, calculate the same positions:

```text
if any required bit is 0:
    x is definitely absent
else:
    x might be present
```

The Python API makes the uncertainty explicit:

```python
if not bloom.might_contain(url):
    skip_expensive_lookup(url)
else:
    perform_exact_check(url)
```

The `in` operator is also supported, so `url in bloom` means “the filter says
this value might be present,” not “the value is proven to be present.”

## 7. Why False Positives Happen

Different values can set overlapping bits. Suppose `x` sets positions `2`, `5`,
and `9`. A value `y` that was never added can still find all three positions
already set by other values:

```text
query y -> bits 2, 5, 9 are all 1 -> possible presence
```

This is a false positive. It is a normal tradeoff, not an implementation bug.
The filter must never report `False` for an added value as long as the bits have
not been cleared or corrupted.

## 8. Sizing Formulas

Let:

- `n` be the expected number of inserted items.
- `p` be the target false-positive rate.
- `m` be the number of bits.
- `k` be the number of hash positions per item.

The standard sizing formulas are:

```text
m = -n * ln(p) / (ln(2) ^ 2)
k = (m / n) * ln(2)
```

The implementation rounds `m` up to a whole bit and rounds `k` to at least one
hash position. For `n = 1000` and `p = 0.01`, this gives roughly `9586` bits
and `7` hash positions.

The approximate false-positive rate after inserting `n` items is:

```text
p_actual ~= (1 - exp(-k * n / m)) ^ k
```

`estimated_false_positive_rate()` applies this formula to the number of add
calls so that the effect of exceeding the sizing target is visible.

## 9. `BloomFilter` Configuration

The constructor is:

```python
bloom = BloomFilter[str](
    expected_items=100_000,
    false_positive_rate=0.01,
)
```

It validates that the expected item count is positive and the target rate is
strictly between zero and one. It computes and stores:

- `bit_count`: total logical bits.
- `hash_count`: positions set per value.
- `byte_count`: packed byte storage size.

These properties make the memory/accuracy tradeoff inspectable instead of
hiding it behind magic constants.

## 10. No Safe Per-Value Deletion

A standard Bloom filter cannot safely implement `remove(value)`. If two values
share a bit, clearing that bit for one value may make the other value appear
absent, creating a false negative:

```text
x sets bit 4
y also sets bit 4
remove x -> clearing bit 4 breaks y
```

The implementation intentionally provides `clear()` for resetting the entire
filter, but no per-value removal. If deletion is required, use a counting Bloom
filter with counters per position or rebuild the standard filter from the
remaining source data. A counting filter uses more memory and still requires
careful handling of collisions.

## 11. Complexity and Memory

Let `k` be the configured hash count:

| Operation | Time | Extra stored data |
|:---|:---:|:---|
| `add` | `O(k)` | Only the configured bit array |
| `might_contain` | `O(k)` | No value storage |
| `clear` | `O(m / 8)` | Reuses the same dimensions |
| `estimated_false_positive_rate` | `O(1)` | No scan of values |

For a fixed target accuracy, `k` is a small constant. The main memory cost is
the bit array, not the number or size of the original values.

## 12. Public Python API

```python
bloom = BloomFilter[str](expected_items=1000, false_positive_rate=0.01)
bloom.add("/blocked")
bloom.add_many(["/admin", "/private"])

bloom.might_contain("/blocked")
"/private" in bloom

bloom.bit_count
bloom.hash_count
bloom.byte_count
bloom.insertions
bloom.estimated_false_positive_rate()
bloom.to_bytes()
bloom.clear()
```

`contains` and `__contains__` deliberately retain the “might be present”
meaning. An exact result requires a second data source such as a hash set.

## 13. Example

The executable example stores a few URL fingerprints, tests a known URL and an
unknown URL, and prints the configured bit count and estimated rate. It also
searches for a possible false positive to make the probabilistic behavior
visible when one occurs.

Run it with:

```text
python BloomFilter.py
```

The exact output can vary because Python hash randomization varies between
processes and because false positives are probabilistic.

## 14. Practical Uses and Privacy Limits

Useful applications include:

- Checking whether a URL may be in a very large blacklist.
- Avoiding disk reads for files that definitely cannot contain a key.
- Filtering duplicate or previously seen identifiers before an expensive step.

The filter does not retain the original values, which reduces direct exposure
and memory usage. It is not a complete privacy or security boundary: an
attacker may still infer information by sending queries, and the hash inputs
exist while operations are running. Sensitive systems should combine the filter
with appropriate access controls and exact verification.

## 15. Bloom Filter Versus Hash Set

| Property | Bloom filter | Hash set |
|:---|:---|:---|
| Stores original values | No | Yes |
| False positives | Possible | No |
| False negatives after normal adds | No | No |
| Safe per-value delete | No, not standard | Yes |
| Memory | Compact bit array | Entry/object and table storage |
| Best role | Fast pre-check | Exact membership source |

A common production design uses both: ask the Bloom filter first, then consult
the exact set or database only when the answer is positive.

## 16. References

- [Bloom Filter Implementation](https://labuladong.online/en/algo/data-structure-basic/bloom-filter/)
- [Hash Set Basic and Implementation](https://labuladong.online/en/algo/data-structure-basic/hash-set/)
- [Bitmap Principles and Implementation](https://labuladong.online/en/algo/data-structure-basic/bitmap/)
