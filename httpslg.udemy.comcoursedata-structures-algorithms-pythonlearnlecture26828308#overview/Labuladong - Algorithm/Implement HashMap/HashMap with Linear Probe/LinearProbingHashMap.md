
---

# HashMap with Linear Probing

## 1. Core Idea

**Linear probing** is an open-addressing strategy for resolving hash collisions.
The table itself stores entries directly. When the home slot is occupied, the
map checks the next slot, then the next one, until it finds the key or an empty
slot.

```text
    home index for key A = 3
    home index for key B = 3

    index:      0       1       2       3       4       5
             +-------+-------+-------+-------+-------+-------+
    values:  |       |       |       |   A   |   B   |       |
             +-------+-------+-------+-------+-------+-------+
                                     home    probe + 1
```

The implementation in `LinearProbingHashMap.py` includes both deletion
strategies covered by the reference material:

- `LinearProbingHashMap`: marks removed slots with a tombstone.
- `RehashingLinearProbingHashMap`: clears a slot and repairs the following cluster.

Both classes expose the same map interface, so their deletion behavior can be
compared directly.

Source references:

- [Core Principles of HashMap](https://labuladong.online/en/algo/data-structure-basic/hashmap-basic/)
- [Key Points to Implement Linear Probing](https://labuladong.online/en/algo/data-structure-basic/linear-probing-key-point/)
- [Two Implementations of Linear Probing](https://labuladong.online/en/algo/data-structure-basic/linear-probing-code/)

---

## 2. Home Index and Probing Sequence

The first position is computed from the key:

```python
home = hash(key) % capacity
```

If that slot is unavailable, linear probing checks consecutive positions:

```text
    probe 0: home
    probe 1: (home + 1) % capacity
    probe 2: (home + 2) % capacity
    probe 3: (home + 3) % capacity
    ...
```

The modulo is essential. It makes the array circular instead of stopping at the
last physical index:

```text
    capacity = 7, home = 5

    5 -> 6 -> 0 -> 1 -> 2 -> 3 -> 4
```

Without the modulo, a key whose probe sequence reaches the end could fail even
when an empty slot exists at the beginning of the array.

---

## 3. Collision Clusters

Keys that occupy consecutive slots form a **cluster**:

```text
    index:      0       1       2       3       4       5       6
             +-------+-------+-------+-------+-------+-------+-------+
    values:  |       |   A   |   B   |   C   |       |       |       |
             +-------+-------+-------+-------+-------+-------+-------+
                         <----------- cluster ----------->
```

If `B` and `C` both started at index `1`, their stored positions do not change
their home index. Search for `C` must start at `1`, pass over `A` and `B`, and
continue until it finds `C` or a slot that proves `C` cannot be present.

This is why linear probing has a strong locality of reference: entries live in
one array. It is also why deletion is subtle: an ordinary empty slot can be a
signal that search should stop.

---

## 4. `put`: Find or Update a Slot

Insertion follows this procedure:

```text
    1. Compute the key's home index.
    2. Probe forward, wrapping around the array.
    3. If the key is found, replace its value.
    4. Otherwise, insert at the first usable slot.
    5. Resize before the table becomes too full.
```

Updating must preserve one entry per key:

```text
    before put("A", 99):

    index:      0       1       2       3
             +-------+-------+-------+-------+
             |       | "A":10|       |       |
             +-------+-------+-------+-------+

    after put("A", 99):

             |       | "A":99|       |       |
```

The `put` methods return the previous value if the key existed and `None` for a
new key. The familiar syntax is also available:

```python
table["A"] = 10
table["A"] = 99
```

---

## 5. Search Must Follow the Probe Sequence

Search starts at the same home index used during insertion:

```text
    search for C, home = 1

    index:      0       1       2       3       4
             +-------+-------+-------+-------+-------+
    values:  |       |   A   |   B   |   C   |       |
             +-------+-------+-------+-------+-------+
                         ^       ^       ^
                         |       |       found C
                       probe   probe
```

The search rules are:

```text
    occupied slot with another key -> continue
    tombstone                      -> continue
    empty slot                     -> key is absent
    matching key                   -> return its value
```

The empty-slot rule is valid only when deletion preserves the probe invariant.
That is the reason a linear-probing implementation cannot simply set every
deleted slot to `None`.

---

## 6. Why a Simple `None` Deletion Breaks Search

Consider three colliding keys:

```text
    before deleting B:

    index:      0       1       2       3
             +-------+-------+-------+-------+
    values:  |       |   A   |   B   |   C   |
             +-------+-------+-------+-------+

    after setting B's slot to None:

    index:      0       1       2       3
             +-------+-------+-------+-------+
    values:  |       |   A   | None  |   C   |
             +-------+-------+-------+-------+
```

A search for `C` starts at index `1`, sees `A`, then sees `None` at index `2` and
incorrectly concludes that `C` was never inserted. The empty slot is a hole in
the cluster.

The two standard repairs are:

```text
    Method 1: move/reinsert the entries after the hole.
    Method 2: leave a special deleted marker in the hole.
```

---

## 7. Method 1: Rehash the Following Cluster

`RehashingLinearProbingHashMap` uses the first method. After removing `B`, it
temporarily removes and reinserts the entries after the hole until the cluster
ends:

```text
    before:
    index:      0       1       2       3       4
             +-------+-------+-------+-------+-------+
    values:  |       |   A   |   B   |   C   |   D   |
             +-------+-------+-------+-------+-------+

    remove B, then repair C and D:

    index:      0       1       2       3       4
             +-------+-------+-------+-------+-------+
    values:  |       |   A   |   C   |   D   |       |
             +-------+-------+-------+-------+-------+
```

The algorithm is:

```text
    1. Set the removed slot to None.
    2. Move to the next circular slot.
    3. While the slot is occupied:
       a. Save the entry.
       b. Clear its old slot.
       c. Insert it again using its original hash.
       d. Move to the next slot.
    4. Stop at the first empty slot.
```

Reinsertion may move an entry closer to its home index. Search can then stop at
the first ordinary empty slot without needing any marker.

The cost of one deletion is expected `O(1)` when clusters are short, but it can
be `O(n)` when a large cluster must be rebuilt.

---

## 8. Method 2: Tombstone Marker

`LinearProbingHashMap` uses a unique internal `_DELETED` object. A removed slot
is neither an ordinary empty slot nor a live entry:

```text
    before:

    index:      0       1       2       3
             +-------+-------+-------+-------+
    values:  |       |   A   |   B   |   C   |
             +-------+-------+-------+-------+

    after remove(B):

    values:  |       |   A   | DELETED |  C   |
             +-------+-------+-------+-------+
```

Search skips the tombstone and reaches `C`. Insertion remembers the first
tombstone encountered, but continues probing until it either finds the key or
finds an ordinary empty slot. This prevents a duplicate key from being created
later in the same probe sequence.

```text
    insert D:

    first usable reuse slot = the tombstone
    continue search to verify D does not already exist
    store D in the tombstone slot
```

Tombstones make individual deletion simple, but too many markers lengthen probe
sequences. This implementation periodically rebuilds the table at the same
capacity when tombstones become more numerous than live entries and occupy a
large part of the table.

---

## 9. Circular Probing Is Required for Every Operation

The table is logically circular for `put`, `get`, and `remove`:

```text
    physical array:  [0] [1] [2] [3] [4]
                              ^       |
                              |       v
                              +-------+

    probe order from 3: 3 -> 4 -> 0 -> 1 -> 2
```

The implementation limits each search to at most `capacity` probes. This bound
prevents an infinite loop if a table is full or if an invariant is broken.

Linear probing must also keep the table below a load factor of `1`. The default
threshold is `0.7`, which leaves empty space for searches to terminate and helps
control primary clustering.

---

## 10. Resizing and Rehashing

When the next insertion would exceed the load-factor threshold, the table grows
and every live entry is inserted again:

```text
    old index = hash(key) % old_capacity
    new index = hash(key) % new_capacity
```

Entries cannot simply be copied to the same physical positions because their
probe sequences depend on the new capacity. Resizing also removes all tombstone
markers.

```text
    table before resize:  [A] [DELETED] [B] [ ] [C]
    table after resize:   [ ] [ ] [A] [ ] [B] [ ] [C] [ ] [ ]
```

Rehashing takes `O(n)` time and is occasional. Its cost is amortized across the
insertions that caused the table to grow.

---

## 11. Public Interface

Both classes provide the same operations:

```python
table = LinearProbingHashMap[str, int]()
# Or:
table = RehashingLinearProbingHashMap[str, int]()

table.put("red", 1)
table["blue"] = 2

table.get("red")             # 1
table.get("missing", -1)    # -1
table["blue"]                # 2
"red" in table               # True
table.contains_key("blue")   # True
table.remove("red")
len(table)
list(table.items())
table.keys()
table.values()
table.slot_snapshot()         # inspect empty, live, and deleted slots
```

The map accepts hashable keys and arbitrary values. The physical slot order is
not a sorted-order or insertion-order guarantee.

---

## 12. Complexity

Let `n` be the number of entries and let `alpha` be the load factor.

| Operation | Expected time | Worst-case time | Extra space | Notes |
|:---|:---:|:---:|:---:|:---|
| `put` | `O(1)` | `O(n)` | `O(1)` | Probe until key or usable slot |
| `get` | `O(1)` | `O(n)` | `O(1)` | Probe one cluster |
| `remove`, tombstone | `O(1)` | `O(n)` | `O(1)` | Marker write plus possible cleanup |
| `remove`, cluster repair | `O(1)` | `O(n)` | `O(1)` | Reinsert following cluster |
| `keys` / `items` | `O(capacity)` | `O(capacity)` | `O(n)` for result | Scan physical slots |
| Resize | `O(n)` | `O(n)` | `O(n)` temporarily | Reinsert live entries |
| Stored map | - | - | `O(capacity)` | One array slot per position |

Expected performance depends on a good hash distribution and a load factor that
stays comfortably below `1`. Linear probing can suffer from primary clustering:
nearby occupied slots cause longer nearby probe sequences.

---

## 13. Invariants and Edge Cases

```text
    1. Every live key is stored at or after its home slot in probe order.
    2. Search never skips a live entry or tombstone.
    3. An ordinary empty slot terminates a search.
    4. Probing wraps from capacity - 1 back to 0.
    5. A key appears at most once.
    6. Linear probing resizes before the table is full.
    7. Tombstones are not returned as live entries.
```

Important edge cases include:

- A collision cluster crosses the physical end of the array.
- A deleted key sits between its home slot and another live key.
- Updating an existing key must not increase `len(table)`.
- A table with tombstones may have low live size but still require cleanup.
- Unhashable or mutable keys should not be used as map keys.

---

## 14. Run the Example

Run:

```text
python LinearProbingHashMap.py
```

The demo creates three custom keys with the same hash value, removes the middle
key, verifies that the last key remains searchable, and inserts a replacement.
It runs the same scenario against both deletion strategies and prints the final
items and physical slot layout.

The tombstone implementation may show `"<DELETED>"` briefly after deletion;
the cluster-repair implementation does not need that marker.

---

## 15. Chaining Compared with Linear Probing

| Feature | Separate chaining | Linear probing |
|:---|:---|:---|
| Collision direction | Vertical linked chain | Horizontal array probe |
| Load factor | Can exceed `1` | Must remain below `1` |
| Deletion complexity | Unlink one node | Tombstone or cluster repair |
| Storage locality | Nodes may be separate objects | Entries remain in one array |
| Empty slot meaning | Only that bucket has no head | Can prove a key is absent |

The deletion difference is the central implementation lesson. In a chained map,
removing one node does not hide later nodes. In an open-addressed map, the probe
path itself must remain discoverable after removal.

---

## 16. Final Checklist

```text
    1. Start every operation at hash(key) % capacity.
    2. Probe with (index + 1) % capacity.
    3. Never stop at a tombstone while searching.
    4. Never use None as a deleted marker.
    5. Repair the cluster or keep a tombstone after deletion.
    6. Update existing keys instead of adding duplicates.
    7. Resize before load factor reaches 1.
    8. Rehash after capacity changes.
    9. Expect average O(1), not an unconditional guarantee.
```

**Next step:** Draw a wrapped cluster that occupies the last two slots and the
first two slots, then delete one entry and trace both deletion strategies.
