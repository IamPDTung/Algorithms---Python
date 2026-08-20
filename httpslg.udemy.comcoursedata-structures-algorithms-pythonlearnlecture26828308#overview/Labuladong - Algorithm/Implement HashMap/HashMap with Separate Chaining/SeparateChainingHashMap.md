
---

# HashMap with Separate Chaining

## 1. Core Idea

A **hash map** stores unique keys and their associated values. It uses a hash
function to turn a key into an array index:

```text
    key                 hash function              bucket index

    "alpha"       --->  hash("alpha")       --->       1
    "beta"        --->  hash("beta")        --->       1   collision
    "gamma"       --->  hash("gamma")       --->       3
```

An array gives `O(1)` access when the index is known. A hash map uses the key to
compute that index, then stores or finds the key/value pair there. The main
operations are expected `O(1)` when the hash function distributes keys well.

The implementation in `SeparateChainingHashMap.py` uses **separate chaining**:
each array position stores the head of a linked list. Every pair whose key maps
to that position is stored in the same chain.

Source references:

- [Core Principles of HashMap](https://labuladong.online/en/algo/data-structure-basic/hashmap-basic/)
- [Implement HashMap with Separate Chaining](https://labuladong.online/en/algo/data-structure-basic/hashtable-chaining/)

---

## 2. Why Collisions Are Unavoidable

The set of possible keys is usually much larger than the number of array
positions. Therefore, two different keys can produce the same index:

```text
    many possible keys
             |
             v
        hash(key)
             |
             v
    only a fixed number of buckets

    key A ---> bucket 1
    key B ---> bucket 1
```

This is a **hash collision**. A collision is not necessarily a bug. The data
structure must preserve both pairs and still distinguish them by comparing
their keys.

Separate chaining resolves the collision by extending the bucket vertically:

```text
    bucket 1
       |
       v
    +---------+      +---------+
    | key A   | ---> | key B   | ---> None
    | value A |      | value B |
    +---------+      +---------+
```

The linked list is the chain. Search first chooses the bucket, then scans only
that chain instead of scanning the whole table.

---

## 3. Entry and Bucket Layout

Each `_Entry` stores three pieces of information:

```text
    +-------------------+
    | key               |
    | value             |
    | next entry ------ |----> another entry or None
    +-------------------+
```

The table is a list of bucket heads:

```text
    index       bucket head

      0         None
      1         [beta] ---> [alpha] ---> None
      2         None
      3         [gamma] ---> None
      4         None
```

`SeparateChainingHashMap` inserts new entries at the head of a chain. This is
constant time once the bucket index is known. Consequently, chain order and
overall iteration order are implementation details, not insertion-order
guarantees.

---

## 4. Hashing a Key

The implementation delegates hashing to Python's `hash(key)` and maps the
result into the current capacity with modulo:

```python
def _bucket_index(self, key, capacity=None):
    bucket_count = self._capacity if capacity is None else capacity
    return hash(key) % bucket_count
```

Python's modulo result is non-negative when the divisor is positive, so negative
hash values still produce valid indices.

A key must be hashable and stable while it is stored:

```text
    same key value + same table capacity -> same bucket index
```

Mutable keys are dangerous. If a key changes the data used by its `__hash__` or
`__eq__`, the pair can remain in a chain but become impossible to find using the
changed key. Use immutable keys such as strings, numbers, or tuples containing
immutable values.

---

## 5. `put`: Insert or Update

`put(key, value)` follows these steps:

```text
    1. Compute the bucket index.
    2. Walk that bucket's chain.
    3. If the key exists, replace its value.
    4. Otherwise, create an entry at the chain head.
    5. Increase size and resize if the load factor is too high.
```

Updating must not create a duplicate key:

```text
    before put("A", 99):

    bucket 2: ["A", 10] ---> ["B", 20] ---> None

    after put("A", 99):

    bucket 2: ["A", 99] ---> ["B", 20] ---> None
```

The method returns the previous value when the key existed, otherwise `None`.
This return convention is useful for observing updates, while `__setitem__`
provides normal map syntax:

```python
hash_map["language"] = "Python"
hash_map["language"] = "Python 3"
```

---

## 6. `get`: Search a Chain

`get(key, default)` computes one bucket and compares keys along its chain:

```text
    search for key B:

    hash(B) -> bucket 1
                     |
                     v
    [key A] -> [key B] -> [key C] -> None
                ^
                | equality match -> return value B
```

If the bucket is empty, or the key is not present in the chain, the supplied
default is returned. The default is `None` when it is omitted:

```python
value = hash_map.get("missing")
value = hash_map.get("missing", 0)
```

`hash_map[key]` uses the same search but raises `KeyError` when the key is
absent, just like a built-in Python dictionary.

---

## 7. `remove`: Unlink One Entry

To remove an entry from a singly linked chain, keep both the current entry and
its predecessor:

```text
    before:

    previous ------> target ------> next

    after:

    previous ---------------------> next
```

If the target is the head, the bucket head moves to `target.next`. Otherwise,
the predecessor's `next` pointer skips over the target.

```python
removed_value = hash_map.remove("language")
del hash_map["other-key"]
```

`remove` raises `KeyError` if the key is absent. This makes accidental deletion
of a missing key visible instead of silently changing nothing.

---

## 8. Load Factor and Resizing

The load factor measures how many entries share the available buckets:

```text
    load factor = number of entries / number of buckets
```

For separate chaining, a load factor can exceed `1` because chains can grow.
Nevertheless, long chains make search slower, so this implementation resizes
when the load factor exceeds `0.75` by default.

```text
    capacity = 4, size = 3
    load factor = 3 / 4 = 0.75

    inserting one more item:
    size = 4, load factor = 1.0
    grow table to capacity 8
```

Resizing is not just copying the old bucket positions. The index depends on the
capacity, so every entry must be rehashed:

```text
    old index = hash(key) % old_capacity
    new index = hash(key) % new_capacity
```

The `_resize` method moves every existing entry into a new bucket array. The
map's logical size does not change during this operation.

---

## 9. Public Interface

The class exposes both descriptive methods and familiar mapping syntax:

```python
table = SeparateChainingHashMap[str, int]()

table.put("red", 1)
table["blue"] = 2

table.get("red")             # 1
table.get("missing", -1)    # -1
table["blue"]                # 2
"red" in table               # True
table.contains_key("blue")   # True
table.remove("red")
len(table)                    # 1
list(table.items())
table.keys()
table.values()
table.bucket_snapshot()       # useful for visualizing chains
```

The map accepts any hashable key type and does not require keys to be strings.
Values may repeat and may have any type.

---

## 10. Complexity

Let `n` be the number of entries and `k` be the length of the selected chain.

| Operation | Expected time | Worst-case time | Extra space | Reason |
|:---|:---:|:---:|:---:|:---|
| `put` new key | `O(1)` | `O(n)` | `O(1)` | Hash plus chain scan and possible resize |
| `put` existing key | `O(1)` | `O(n)` | `O(1)` | Find the key inside its chain |
| `get` | `O(1)` | `O(n)` | `O(1)` | Scan at most one chain |
| `remove` | `O(1)` | `O(n)` | `O(1)` | Find and unlink one entry |
| `keys` / `values` | `O(n)` | `O(n)` | `O(n)` for result | Visit every entry |
| Resize | `O(n)` | `O(n)` | `O(n)` | Rehash every entry |
| Stored map | - | - | `O(n + capacity)` | Entries plus bucket heads |

Expected `O(1)` assumes a good hash distribution and a controlled load factor.
If every key hashes to the same bucket, the structure behaves like one linked
list and operations degrade to `O(n)`.

---

## 11. Important Invariants

The implementation remains correct when these statements are always true:

```text
    1. Every entry is reachable from exactly one bucket head.
    2. Every chain contains unique keys.
    3. An entry's bucket is hash(entry.key) % capacity.
    4. The size counter equals the number of stored entries.
    5. Updating a key changes its value, not the number of entries.
    6. Removing the chain head updates the bucket head.
    7. Resizing rehashes every entry using the new capacity.
```

These invariants are more important than the choice of linked-node syntax. They
are the checklist to use when debugging a collision or resize bug.

---

## 12. Run the Example

Run the file from this directory:

```text
python SeparateChainingHashMap.py
```

The demo uses custom keys with the same hash value so a collision is guaranteed
without depending on Python's randomized string hash seed. It demonstrates:

```text
    insert alpha and beta into one chain
    insert gamma into another bucket
    update alpha without duplicating it
    remove beta from the middle/head of a chain
```

The printed bucket snapshot is not required to have a stable global order after
resizing. Hash table traversal order should never be used as a sorted or
insertion-order contract.

---

## 13. Chaining Compared with Linear Probing

| Feature | Separate chaining | Linear probing |
|:---|:---|:---|
| Collision direction | Extend a bucket into a chain | Search forward in the array |
| Storage | Entries plus linked pointers | One entry per array slot |
| Load factor | Can exceed `1` | Must stay below `1` |
| Deletion | Unlink an entry | Needs tombstones or cluster repair |
| Main locality | Pointer-based chain traversal | Array-friendly probing |

Both approaches use the same first step: hash the key to an initial index. They
differ in how they preserve all entries when that index is already occupied.

---

## 14. Final Checklist

```text
    1. A key is unique; values may repeat.
    2. Different keys may map to one bucket.
    3. A chain stores every pair that collides at that bucket.
    4. Search compares keys, not only hash indices.
    5. Updating an existing key must not increase size.
    6. Resizing requires rehashing because capacity changes indices.
    7. Immutable, hashable keys are safest.
    8. Average operations are O(1); worst-case operations are O(n).
```

**Next step:** Create two custom keys with the same `__hash__` value and trace
their `put`, `get`, update, and `remove` operations through one chain.
