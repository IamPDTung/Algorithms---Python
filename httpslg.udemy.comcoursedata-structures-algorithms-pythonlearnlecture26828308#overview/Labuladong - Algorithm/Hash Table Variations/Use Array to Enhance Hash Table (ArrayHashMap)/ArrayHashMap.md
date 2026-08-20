
---

# Use Array to Enhance Hash Table (ArrayHashMap)

## 1. Goal

A hash table gives expected `O(1)` key lookup, but its bucket array contains
empty slots and collision chains. Choosing a random physical bucket does not
therefore choose a random key uniformly.

The implementation in `ArrayHashMap.py` adds a compact dense entry array. It
supports:

- Expected `O(1)` `put`, `get`, `remove`, and `contains_key`.
- Uniform `random_key()` in `O(1)` time.
- Hash buckets for lookup and collision handling.
- Swap-with-last deletion so the dense array never contains holes.

Source references:

- [Hash Table Core Principles](https://labuladong.online/en/algo/data-structure-basic/hashmap-basic/)
- [Use Array to Enhance Hash Table](https://labuladong.online/en/algo/data-structure-basic/hashtable-with-array/)

## 2. The New `random_key` API

The usual map API looks like this:

```python
map.get(key)
map.put(key, value)
map.remove(key)
map.contains_key(key)
map.keys()
```

The enhancement adds:

```python
key = map.random_key()
```

The requirement is uniform randomness: if the map contains `N` keys, each key
must be selected with probability `1 / N`. The method should also be `O(1)`.

## 3. Why Picking a Hash-Table Slot Is Wrong

Consider an open-addressed table with empty slots:

```text
table: [A, None, C, None, None, D]
```

Picking a random physical index gives empty results. If the algorithm scans to
the right after hitting a gap, keys near the right side of gaps become more
likely. If it repeatedly retries random indices, the result can be uniform,
but the running time depends on luck and is not guaranteed `O(1)`.

With chaining, a random bucket index has another problem. Buckets may contain
different numbers of nodes, so choosing a bucket uniformly and then a node
uniformly weights keys in short chains more heavily than keys in long chains.

The solution is to maintain a separate compact array containing exactly one
entry for every live key.

## 4. Two Structures, One Entry Set

`ArrayHashMap` maintains:

```text
bucket array                         dense entry array
---------------                     -------------------------
0 -> None                            index 0: [A, value A]
1 -> [C] -> [A]                      index 1: [B, value B]
2 -> [B]                             index 2: [C, value C]
```

The bucket array answers key lookup. The dense array answers enumeration and
random selection. Each `_ArrayEntry` stores its own `array_index`, so deletion
can update the moved entry in constant time.

The map does not use a second dictionary to track array positions. The entry
object carries the position needed by the swap operation.

## 5. Entry and Bucket Layout

Each entry contains:

```text
key, value
    The user-visible mapping.

array_index
    The current position in the compact `_entries` list.

next_bucket
    The next entry in the collision chain for this key's bucket.
```

The key invariant is:

```text
0 <= entry.array_index < len(_entries)
_entries[entry.array_index] is entry
```

Every live entry appears exactly once in a bucket chain and exactly once in the
dense array.

## 6. `put`: Insert or Update

`put(key, value)` first searches the appropriate bucket:

```text
1. Compute hash(key) % capacity.
2. Walk that bucket's chain.
3. If the key exists, replace only its value.
4. Otherwise, create an entry at the end of `_entries`.
5. Link it into the bucket chain.
6. Resize if the load factor is too high.
```

Updating an existing key does not add another array entry:

```python
array_map.put("a", 1)
array_map.put("b", 2)
array_map.put("a", 10)

assert array_map.keys() == ["a", "b"]
assert array_map["a"] == 10
```

The method returns the previous value for an update and `None` for a new key.

## 7. `remove`: Swap with the Last Entry

Removing from the middle of a Python list by shifting every later element would
cost `O(N)`. The dense-array trick avoids shifting:

```text
before: [A, B, C, D]
remove B
move D into B's slot
after:  [A, D, C]
```

The steps are:

```text
1. Unlink the target from its bucket chain.
2. Read the last dense-array entry.
3. If target is not last, place last in target's array slot.
4. Update last.array_index.
5. Pop the final list position.
```

The order of `keys()` is therefore not an insertion-order guarantee. It is the
current compact-array order, and a deletion can move one key. This change is
necessary to keep `remove` and future `random_key` calls `O(1)`.

## 8. Uniform Random Selection

After every insertion or deletion, `_entries` contains no holes:

```python
index = rng.randrange(len(_entries))
return _entries[index].key
```

Every valid index is equally likely, and every valid index holds one live key.
Therefore every key has probability `1 / len(_entries)`. The algorithm does not
inspect empty hash buckets, retry, or scan for a neighbor.

The constructor accepts an optional `random.Random` instance. This is useful for
reproducible demonstrations and tests; the data-structure invariant does not
depend on the random generator.

Calling `random_key()` on an empty map raises `KeyError` because there is no key
that can satisfy the requested result.

## 9. Resizing the Hash Table

The dense array and the bucket array have different jobs during resize. The
entry array is already compact and can stay in the same order. Only the bucket
links need to be rebuilt:

```text
old index = hash(key) % old capacity
new index = hash(key) % new capacity
```

The implementation walks `_entries`, computes each new index, and inserts the
entry into the new bucket list. No entry is copied and no array index changes.

## 10. Lookup, Enumeration, and Complexity

| Operation | Expected time | Reason |
|:---|:---:|:---|
| `put` | `O(1)` | Search one expected-short chain and append |
| `get` | `O(1)` | Search one expected-short chain |
| `contains_key` | `O(1)` | Same bucket search |
| `remove` | `O(1)` | Unlink and swap with the final entry |
| `random_key` | `O(1)` | One random index and one array access |
| `keys` / `items` | `O(N)` | Visit the dense entry array |
| Resize | `O(N)` | Rebuild all bucket links |

As with every hash table, poor hash distribution can make a collision chain
long. The `O(1)` claims are expected or amortized bounds under normal hashing.

## 11. Public Python API

```python
array_map = ArrayHashMap[str, int]()
array_map.put("language", 1)
array_map["version"] = 3

array_map.get("language")
array_map.contains_key("version")
array_map.random_key()
array_map.remove("language")
array_map.keys()
array_map.values()
array_map.items()
array_map.dense_array_snapshot()
array_map.bucket_snapshot()
array_map.clear()
```

The class also supports `len(array_map)`, `key in array_map`, iteration, and
`del array_map[key]`.

## 12. Example and Deletion Demonstration

The executable example creates a seeded random generator, inserts four keys,
removes one key from the middle of the dense array, and prints both the dense
array and bucket chains. The output makes the swap-with-last operation visible.

Run it with:

```text
python ArrayHashMap.py
```

The random key may differ when a different random generator is supplied, but
each live key remains equally likely.

## 13. Design Limits

The dense array is an auxiliary index, not a sorted array and not an insertion
order list. If an application needs stable insertion order, use the
`LinkedHashMap` implementation instead.

`random_key` returns keys, not values. A random value can be obtained by using
the selected key with `get`, but the key/value selection remains a single
uniform selection from the live entries.

Keys must be hashable and stable while stored. The array optimization cannot
repair a key whose hash or equality behavior changes.

## 14. References

- [Use Array to Enhance Hash Table (ArrayHashMap)](https://labuladong.online/en/algo/data-structure-basic/hashtable-with-array/)
- [Basic Concept of HashMap](https://labuladong.online/en/algo/data-structure-basic/hashmap-basic/)
- [Use Linked List to Enhance Hash Table (LinkedHashMap)](https://labuladong.online/en/algo/data-structure-basic/hashtable-with-linked-list/)
