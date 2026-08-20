
---

# Hash Set: Basics and Implementation

## 1. What Is a Hash Set?

A **set** stores values without associated values. A dictionary or hash map
stores pairs:

```text
    key -> value
```

A hash set stores only the keys:

```text
    value A
    value B
    value C
```

The central rule is **uniqueness**. Adding an existing value does not create a
second copy. The implementation in `HashSet.py` uses the same hash-table idea as
separate chaining, but each node contains only one value and one `next` pointer.

Source references:

- [Core Principles of HashMap](https://labuladong.online/en/algo/data-structure-basic/hashmap-basic/)
- [Hash Set Basic and Implementation](https://labuladong.online/en/algo/data-structure-basic/hash-set/)

---

## 2. A Set Is a Key-Only Hash Map

The simplest mental model is a hash map whose values are ignored:

```text
    HashMap                         HashSet

    "alice" -> 100                  "alice"
    "bob"   -> 200                  "bob"
    "carol" -> 300                  "carol"
```

To implement a set with a map, one possible design is to store every value as a
key and use one shared placeholder value. `HashSet.py` stores only the key
nodes directly, which avoids allocating and updating an unnecessary placeholder
value while keeping the same bucket and collision logic.

---

## 3. Bucket Layout

The set hashes each value to a bucket index:

```text
    value                 hash(value)                bucket

    12              --->  hash(12)             --->    2
    17              --->  hash(17)             --->    2   collision
    20              --->  hash(20)             --->    0
```

Each bucket stores a chain of values:

```text
    index       bucket

      0         [20] ---> None
      1         None
      2         [17] ---> [12] ---> None
      3         None
```

The implementation inserts new values at the head of a chain. Bucket order and
iteration order are not sorted-order or insertion-order guarantees.

---

## 4. Hashing and Key Requirements

The bucket index is computed with:

```python
index = hash(value) % capacity
```

Python requires set values to be hashable. A value must also remain stable while
it is stored. Mutable objects whose hash or equality behavior changes can become
unreachable inside the table.

Good values include:

```python
HashSet([1, 2, 3])
HashSet(["red", "green", "blue"])
HashSet([(1, 2), (3, 4)])
```

Lists and dictionaries are not hashable and cannot be inserted directly. Convert
them to an immutable representation when that matches the problem's semantics,
such as a tuple or a frozen set.

---

## 5. `add`: Enforce Uniqueness

`add(value)` performs these steps:

```text
    1. Compute the value's bucket index.
    2. Scan that bucket's chain.
    3. Return False if an equal value is already present.
    4. Otherwise, add a node at the chain head.
    5. Increase size and resize if required.
```

The duplicate check is the defining difference between a set and a bag:

```text
    add("A") -> True
    add("A") -> False

    final contents: {"A"}
```

The method returns whether the set changed. This makes duplicate behavior easy
to test even though Python's built-in `set.add` returns `None`.

---

## 6. Membership Testing

Membership follows exactly one bucket chain:

```text
    contains value B:

    hash(B) -> bucket 2
                      |
                      v
    [A] ---> [B] ---> [C] ---> None
              ^
              +-- equality match -> True
```

The class supports both explicit and idiomatic forms:

```python
members.contains("B")
"B" in members
```

If the value is absent from its chain, the result is `False`. The operation does
not need to inspect unrelated buckets.

---

## 7. `discard` and `remove`

Removing a node from a chain uses the same predecessor link repair as a chained
hash map:

```text
    before:

    previous ------> target ------> next

    after:

    previous ---------------------> next
```

The implementation provides both common semantics:

```python
members.discard("missing")  # False, no exception
members.remove("present")   # removes it
members.remove("missing")   # raises KeyError
```

Use `discard` when absence is expected and should be harmless. Use `remove` when
missing data indicates a logic error that should be visible.

---

## 8. Resizing and Load Factor

The load factor is:

```text
    load factor = number of stored values / number of buckets
```

Separate chaining can technically support a load factor above `1`, because a
bucket can hold a long chain. Long chains still make membership slower, so this
implementation grows the table when the load factor exceeds `0.75`.

```text
    capacity = 4, size = 3
    load factor = 0.75

    add another value:
    size = 4, load factor = 1.0
    resize to capacity 8
```

Every value must be rehashed after resizing because the capacity is part of the
bucket-index calculation:

```text
    old index = hash(value) % old_capacity
    new index = hash(value) % new_capacity
```

The set's logical contents and size do not change during a resize.

---

## 9. Set Algebra

Given sets `A` and `B`:

```text
    A = {1, 2, 3}
    B = {3, 4, 5}

    union:        A U B = {1, 2, 3, 4, 5}
    intersection: A n B = {3}
    difference:   A - B = {1, 2}
```

`HashSet.py` implements these operations without relying on Python's built-in
set for the stored data:

```python
left = HashSet([1, 2, 3])
right = HashSet([3, 4, 5])

left.union(right)
left.intersection(right)
left.difference(right)
left.is_subset(right)

left | right
left & right
left - right
```

For a general iterable, the implementation first builds a temporary `HashSet`
when membership checks against the other collection are needed. This keeps the
operation expected `O(n + m)` rather than scanning the other iterable for every
value.

---

## 10. Public Interface

```python
members = HashSet(["red", "blue"], capacity=5)

members.add("green")
members.update(["blue", "yellow"])

"red" in members
members.contains("green")
members.discard("yellow")
members.remove("blue")

len(members)
list(members)
members.bucket_snapshot()
members.clear()
```

The constructor accepts an optional iterable. Values are yielded in physical
bucket order, so callers should sort the result when a deterministic display is
needed:

```python
sorted(members)
```

The set does not promise insertion order.

---

## 11. Complexity

Let `n` be the number of values and `k` the length of the selected chain.

| Operation | Expected time | Worst-case time | Extra space | Reason |
|:---|:---:|:---:|:---:|:---|
| `add` | `O(1)` | `O(n)` | `O(1)` | Hash plus one chain scan |
| `contains` | `O(1)` | `O(n)` | `O(1)` | Scan one bucket chain |
| `discard` / `remove` | `O(1)` | `O(n)` | `O(1)` | Find and unlink one node |
| `union` | `O(n + m)` expected | `O(nm)` | `O(n + m)` | Add values from both sets |
| `intersection` | `O(n + m)` expected | `O(nm)` | `O(n + m)` | Membership checks in other set |
| `difference` | `O(n + m)` expected | `O(nm)` | `O(n + m)` | Exclude values in other set |
| Iteration | `O(capacity + n)` | `O(capacity + n)` | `O(1)` | Visit buckets and nodes |
| Resize | `O(n)` | `O(n)` | `O(n)` temporarily | Rehash every stored value |
| Stored set | - | - | `O(n + capacity)` | Nodes plus bucket heads |

The expected bounds require a reasonably distributed hash function and stable
hashable values.

---

## 12. Set Use Cases

Hash sets are useful whenever the question is “have I seen this value?” rather
than “what value belongs to this key?”

```text
    +-------------------------------------------------------------+
    | COMMON HASH SET USE CASES                                   |
    +-------------------------------------------------------------+
    | Remove duplicates from a sequence                           |
    | Track visited graph vertices                                |
    | Test whether two collections share an item                  |
    | Check membership in a large collection                      |
    | Count distinct values                                       |
    | Build union, intersection, and difference results           |
    +-------------------------------------------------------------+
```

For example, a visited set prevents graph traversal from processing the same
vertex repeatedly. A duplicate detector adds each item and checks the boolean
return from `add`.

---

## 13. Important Invariants

```text
    1. Every stored value is reachable from exactly one bucket head.
    2. A value appears at most once.
    3. A value's bucket is hash(value) % capacity.
    4. The size counter equals the number of stored values.
    5. Removing a chain head updates the bucket head.
    6. Resizing rehashes every value using the new capacity.
    7. The set never exposes bucket order as sorted or insertion order.
```

These invariants explain every main method. If one is broken, membership may
fail, duplicates may appear, or a resize may make values disappear.

---

## 14. Run the Example

Run:

```text
python HashSet.py
```

The demo shows duplicate rejection, membership, removal, and the three main set
operations. It sorts display values only for readable output; the set itself
does not maintain sorted order.

---

## 15. Hash Set Compared with HashMap

| Feature | HashSet | HashMap |
|:---|:---|:---|
| Stored data | Unique values | Unique keys with values |
| Main query | Is this value present? | What value belongs to this key? |
| Duplicate rule | Duplicate values rejected | Duplicate keys update values |
| Collision handling | Bucket chains | Bucket chains or probes |
| Typical use | Membership and distinctness | Association and lookup |

The set is not a sorted collection. If ordered traversal is required, use a
different structure or sort a result after iteration.

---

## 16. Final Checklist

```text
    1. A set stores keys/values without a separate mapped value.
    2. Every stored value must be unique.
    3. Hash the value to choose one bucket.
    4. Compare equal values inside that bucket.
    5. Add returns False for a duplicate.
    6. Discard is quiet; remove raises for a missing value.
    7. Resize rehashes all values because capacity changes indices.
    8. Average membership is O(1); worst case is O(n).
    9. Set algebra is built from membership and insertion.
```

**Next step:** Use a `HashSet` to detect the first duplicate in a list, then
rewrite the solution using a map and compare which data each structure stores.
