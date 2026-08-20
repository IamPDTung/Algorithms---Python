
---

# Use Linked List to Enhance Hash Table (LinkedHashMap)

## 1. Goal

A normal hash table is optimized for lookup, insertion, update, and deletion.
Its bucket array does not provide a useful user-facing order for traversing
keys. This implementation adds a second structure so that the map can also
iterate keys in insertion order.

The implementation in `LinkedHashMap.py` supports:

- Expected `O(1)` `put`, `get`, `remove`, and `contains_key`.
- Insertion-order `keys`, `items`, and `values` traversal.
- Resizing while preserving the logical insertion order.
- Normal mapping syntax such as `map[key]` and `map[key] = value`.

Source references:

- [Hash Table Core Principles](https://labuladong.online/en/algo/data-structure-basic/hashmap-basic/)
- [Use Linked List to Enhance Hash Table](https://labuladong.online/en/algo/data-structure-basic/hashtable-with-linked-list/)

## 2. The Core Idea

The data structure combines two independent views of the same entries:

```text
                          insertion-order list
                         head                   tail
                          |                      |
                          v                      v
                       [A] <-> [B] <-> [C] <-> [D]
                        |             |          |
                        +-------------+----------+
                              entries also live in buckets
```

The bucket links answer hash-table questions. The global doubly linked list
answers ordering questions. One entry object participates in both structures;
the map does not store a second copy of the key/value pair.

## 3. Why a Normal Hash Map Has No Order Guarantee

A hash map first computes an array index:

```python
index = hash(key) % capacity
```

Iteration normally scans the bucket array from index `0` to the final index.
That order reflects hash values and collision chains, not insertion order.
When the map resizes, the modulus changes and entries are rehashed into new
positions. The traversal order can therefore change even when no item was
removed.

The important rule is that a hash table's bucket order is an implementation
detail. Code that needs a stable insertion order must store that order
explicitly.

## 4. Two Links, Two Responsibilities

`_LinkedEntry` has three groups of fields:

```text
key, value
    The user-visible mapping.

next_bucket
    The next entry in the bucket selected by hash(key).

previous_order, next_order
    The previous and next entries in insertion order.
```

The two link systems must not be confused. Removing an entry requires unlinking
it from both the bucket chain and the order list. Resizing only rebuilds bucket
links; it must leave order links untouched.

## 5. Bucket Lookup and Collisions

Each bucket stores the head of a singly linked collision chain:

```text
bucket 1 ---> [beta] ---> [alpha] ---> None
```

Lookup computes one bucket and compares keys along that chain. Different keys
can have the same hash index, so equality comparison is still required after
hashing. A key must remain hashable and must not change the data used by its
`__hash__` or `__eq__` methods while stored.

Python's positive modulo behavior makes `hash(key) % capacity` a valid index
even when `hash(key)` is negative.

## 6. `put`: Insert or Update

`put(key, value)` follows this sequence:

```text
1. Find the key in its bucket chain.
2. If it exists, replace only its value.
3. Otherwise, create one entry.
4. Link the entry into the bucket chain.
5. Append the same entry to the order-list tail.
6. Resize if the load factor is too high.
```

Updating an existing key does not move it to the end. This is insertion-order
behavior: the key's original insertion position remains stable. If a key is
removed and later inserted again, the new entry is appended at the tail.

```python
linked_map.put("a", 1)
linked_map.put("b", 2)
linked_map.put("a", 10)

assert linked_map.keys() == ["a", "b"]
assert linked_map["a"] == 10
```

The method returns the old value for an update and `None` for a new key.

## 7. `get` and `contains_key`

Both operations use the bucket chain, not the order list:

```python
value = linked_map.get("missing", 0)
exists = linked_map.contains_key("a")

assert value == 0
assert exists
```

`get` returns its `default` when no matching key is found. Bracket lookup,
`linked_map[key]`, raises `KeyError` for a missing key, matching the behavior
of a normal Python mapping.

## 8. `remove`: Repair Both Structures

For a bucket chain, removal bypasses the target entry:

```text
previous ---> target ---> next

previous ----------------> next
```

The same target must also be removed from the doubly linked order list:

```text
before:  A <-> target <-> B
after:   A <-----------> B
```

The implementation handles all order-list positions:

- Removing the head moves `_head` to the next entry.
- Removing the tail moves `_tail` to the previous entry.
- Removing the only entry clears both endpoints.
- Removing a middle entry joins its two neighbors.

`remove` returns the value and raises `KeyError` when the key is absent.

## 9. Resizing Without Losing Order

The load factor is:

```text
load factor = number of entries / number of buckets
```

When it exceeds the configured threshold, the table grows. Because the bucket
index depends on capacity, every entry must be rehashed:

```text
old index = hash(key) % old capacity
new index = hash(key) % new capacity
```

`_resize` walks the global order list and rebuilds only the bucket links. The
order links and the head/tail endpoints remain unchanged, so a resize cannot
change `keys()` order.

## 10. Traversal and Complexity

| Operation | Expected time | Reason |
|:---|:---:|:---|
| `put` | `O(1)` | Hash one bucket; append to list tail |
| `get` | `O(1)` | Search one expected-short chain |
| `contains_key` | `O(1)` | Same bucket search as `get` |
| `remove` | `O(1)` | Unlink from bucket and doubly linked list |
| `keys` / `items` | `O(N)` | Visit every order-list entry |
| Resize | `O(N)` | Rehash every entry |

The expected bounds assume a useful hash distribution. A deliberately bad hash
function can make one collision chain long and degrade bucket operations.

## 11. Public Python API

The class exposes these main methods:

```python
linked_map = LinkedHashMap[str, int]()
linked_map.put("language", 1)
linked_map["version"] = 3

linked_map.get("language")
linked_map.contains_key("version")
linked_map.remove("language")
linked_map.keys()
linked_map.values()
linked_map.items()
linked_map.clear()
```

`len(linked_map)`, `key in linked_map`, iteration, and `del linked_map[key]`
are also supported.

## 12. Example and Collision Demonstration

The executable example defines `CollisionKey`, whose instances can be given
the same hash value. It inserts colliding keys, updates one key, triggers a
resize, removes the head of the insertion list, and prints the final order.

Run it with:

```text
python LinkedHashMap.py
```

The printed order comes from the linked list, not from the physical bucket
array. This is the central enhancement over a basic hash map.

## 13. Design Limits

This class implements insertion-order traversal, not access-order traversal.
Calling `get` does not move a key to the tail. An access-order cache would need
to unlink and append an entry after successful access, usually with an optional
capacity-based eviction policy.

The map still requires hashable, stable keys. The linked list preserves order,
but it does not fix an invalid or mutable hash key.

## 14. References

- [Use Linked List to Enhance Hash Table (LinkedHashMap)](https://labuladong.online/en/algo/data-structure-basic/hashtable-with-linked-list/)
- [Basic Concept of HashMap](https://labuladong.online/en/algo/data-structure-basic/hashmap-basic/)
- [Implement HashMap with Separate Chaining](https://labuladong.online/en/algo/data-structure-basic/hashtable-chaining/)
