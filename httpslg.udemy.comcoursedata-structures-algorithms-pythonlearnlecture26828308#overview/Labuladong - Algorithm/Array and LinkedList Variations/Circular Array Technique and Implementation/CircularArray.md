
---

# Circular Array Technique and Implementation

## 1. What Is a Circular Array?

A **circular array** stores values in a normal fixed-size array, but treats the
last physical slot as connected to the first physical slot. The logical front
does not have to be at physical index `0`.

The structure tracks three pieces of state:

* `head` — the physical slot containing logical index `0`
* `size` — how many values are currently stored
* `capacity` — how many physical slots exist

The key mapping is:

```text
    physical_index = (head + logical_index) % capacity
```

The implementation in `CircularArray.py` uses this technique to support
`append`, `appendleft`, `pop`, and `popleft` without shifting every value.

---

## 2. What Problem Does It Solve?

A regular Python list is excellent for indexing, but inserting at the front
requires the existing values to move right.

```text
    REGULAR ARRAY: appendleft(5)

    before:     [ 10 ][ 20 ][ 30 ][ 40 ]
    after:      [  5 ][ 10 ][ 20 ][ 30 ][ 40 ]
                    <---- every old value shifts ---->
```

If the structure is used as a queue, repeatedly removing from index `0` can
also be expensive:

```text
    popleft() from a regular list:

    [ 10 ][ 20 ][ 30 ][ 40 ][ 50 ]
       X    [ 20 ][ 30 ][ 40 ][ 50 ]  <- values shift left
```

A circular array moves only the logical boundary:

```text
    popleft() from a circular array:

    before:  head -> [ 10 ][ 20 ][ 30 ][ 40 ][    ]
    after:          [    ][ 20 ][ 30 ][ 40 ][    ]
                             head ->
```

The values remain in their physical slots. Only `head` and `size` change.

---

## 3. Logical Order vs Physical Storage

The logical order is the order a caller sees. The physical order is the order
of slots inside the backing array. They can be different after the head wraps.

```text
    capacity = 8
    head = 6
    size = 5

    physical slots:
    index       0       1       2       3       4       5       6       7
             +-------+-------+-------+-------+-------+-------+-------+-------+
    storage  |  30   |  40   |  50   |       |       |       |  10   |  20   |
             +-------+-------+-------+-------+-------+-------+-------+-------+
                 ^       ^       ^                               ^       ^
                 |       |       |                               |       |
              logical  logical  logical                         logical logical
                2       3       4                                0       1

    logical values: [10, 20, 30, 40, 50]
```

The logical indices are mapped as follows:

```text
    logical 0 -> (6 + 0) % 8 = 6
    logical 1 -> (6 + 1) % 8 = 7
    logical 2 -> (6 + 2) % 8 = 0
    logical 3 -> (6 + 3) % 8 = 1
    logical 4 -> (6 + 4) % 8 = 2
```

This is why modulo is the central operation in a circular array.

---

## 4. The Three Invariants

The implementation is correct when these conditions always remain true:

1. `0 <= size <= capacity`
2. Logical index `i` is stored at `(head + i) % capacity` for
   `0 <= i < size`.
3. Every slot outside the logical range is empty or irrelevant to the public
   sequence.

```text
    valid logical range:

        head                                      tail
          |                                         |
          v                                         v
    [ value ][ value ][ value ][ empty ][ empty ]
       0         1         2
```

When the range crosses the physical boundary, it becomes two pieces:

```text
    [ value ][ value ][ empty ][ empty ][ value ][ value ]
       ^       ^                              ^       ^
      head    next                           ...     tail
```

The logical sequence is still one sequence even though the storage is split.

---

## 5. Adding at the Right End

For `append(value)`, the next physical slot is:

```text
    tail_slot = (head + size) % capacity
```

Example:

```text
    head = 6, size = 3, capacity = 8

    tail_slot = (6 + 3) % 8 = 1

    index:    0       1       2       3       4       5       6       7
            +-------+-------+-------+-------+-------+-------+-------+-------+
            |  30   | empty | empty |       |       |       |  10   |  20   |
            +-------+-------+-------+-------+-------+-------+-------+-------+
                              write the new value at slot 1
```

No values need to move. If the array is full, the implementation first
allocates a larger backing array and copies values in logical order.

---

## 6. Adding at the Left End

For `appendleft(value)`, move the head one slot backward:

```text
    new_head = (head - 1) % capacity
```

The modulo operation handles the wrap from slot `0` to the last slot:

```text
    head = 0, capacity = 8
    new_head = (0 - 1) % 8 = 7

    index:    0       1       2       3       4       5       6       7
            +-------+-------+-------+-------+-------+-------+-------+-------+
            |  10   |  20   |  30   |       |       |       |       |  new  |
            +-------+-------+-------+-------+-------+-------+-------+-------+
                                                                        ^
                                                                      head
```

This is the circular-array version of prepending to a deque.

---

## 7. Resizing Without Losing Logical Order

When a dynamic circular array becomes full, it doubles its capacity. The
values are copied from logical index `0` onward into the new storage:

```text
    old storage, wrapped:

        head -> [ 40 ][ 50 ][    ][    ][ 10 ][ 20 ][ 30 ]
                  3     4                 0     1     2

    new storage, normalized:

        head -> [ 10 ][ 20 ][ 30 ][ 40 ][ 50 ][    ][    ][    ]
                  0     1     2     3     4
```

After resizing, `head` becomes `0`. The values are not sorted or changed; only
their physical layout is normalized.

The implementation also shrinks storage when it becomes mostly empty, but it
never shrinks below the original capacity supplied to the constructor.

---

## 8. Core Implementation Ideas

### Constructor

```python
numbers = CircularArray[int](capacity=4)
```

The constructor creates four physical slots, sets `head = 0`, and starts with
`size = 0`.

### Logical Indexing

```python
value = numbers[index]
numbers[index] = replacement
```

Both operations validate the logical index first, then translate it with
`(head + index) % capacity`.

### Queue and Deque Operations

```python
numbers.append(value)       # right end
numbers.appendleft(value)    # left end
numbers.pop()                # remove right end
numbers.popleft()            # remove left end
```

The left-end operations update `head`; the right-end operations calculate the
tail slot from `head` and `size`.

---

## 9. Complete Python Reference

The full implementation is in `CircularArray.py`. Its public shape is:

```python
class CircularArray(Generic[T]):
    def append(self, value: T) -> None: ...
    def appendleft(self, value: T) -> None: ...
    def pop(self) -> T: ...
    def popleft(self) -> T: ...
    def clear(self) -> None: ...
    def to_list(self) -> List[T]: ...
```

The class also supports `len(array)`, `array[index]`, negative indexes,
iteration, `capacity`, `size`, `head_index`, and `debug_slots()`.

---

## 10. Complexity

| Operation | Typical complexity | Reason |
|:---|:---:|:---|
| Index lookup | `O(1)` | One modulo calculation |
| Index update | `O(1)` | One physical slot is written |
| `append` | `O(1)` amortized | Write one slot; resize is occasional |
| `appendleft` | `O(1)` amortized | Move head by one slot |
| `pop` | `O(1)` amortized | Clear the tail slot |
| `popleft` | `O(1)` amortized | Clear the head slot |
| Resize | `O(n)` | Copy values in logical order |
| Search by value | `O(n)` | No sorted-search guarantee |
| Extra storage | `O(capacity)` | Backing array plus metadata |

The word **amortized** matters. A single append that triggers a resize is
`O(n)`, but doubling means resizes are infrequent, so a long sequence of
appends costs `O(1)` per operation on average.

---

## 11. Worked Trace: Wrapping at the Boundary

Start with capacity `4`:

```text
    append(10), append(20), append(30)

    head = 0, size = 3
    slots = [ 10 ][ 20 ][ 30 ][    ]
```

Remove the front value:

```text
    popleft()

    returned = 10
    head = 1, size = 2
    slots = [    ][ 20 ][ 30 ][    ]
```

Add values at the right. The tail wraps to slot `0`:

```text
    append(40), append(50)

    head = 1, size = 4
    slots = [ 50 ][ 20 ][ 30 ][ 40 ]
                ^                 ^
              logical 1        logical 3

    logical values = [20, 30, 40, 50]
```

The array is full, but the sequence is not physically contiguous from index
`0`. That is the main behavior the technique provides.

---

## 12. Common Mistakes

### Mistake 1: Using `size` as a physical index

`size` tells how many values exist. It is not necessarily the physical tail
slot. Always use `(head + size) % capacity` for the next right-end position.

### Mistake 2: Forgetting modulo on `head`

```python
self._head = self._head - 1       # can become -1
self._head = (self._head - 1) % capacity  # wraps correctly
```

### Mistake 3: Copying physical order during resize

Copying `data[0:]` directly can change the logical sequence. Iterate from
logical index `0` to `size - 1` instead.

### Mistake 4: Confusing empty and full states

With only `head` and `tail`, an empty buffer and a full buffer can look the
same. Tracking `size` removes this ambiguity.

### Mistake 5: Assuming circular means sorted

A circular array preserves insertion order. It does not provide binary search
or sorted access automatically.

---

## 13. Where Is It Useful?

```text
    +---------------------------------------------------------------+
    | CIRCULAR ARRAY USE CASES                                      |
    +---------------------------------------------------------------+
    | Queue / deque             -> add and remove at both ends      |
    | Ring buffer               -> keep the newest fixed history    |
    | Sliding window           -> overwrite or expire old values   |
    | Producer / consumer      -> bounded stream buffer             |
    | Round-robin scheduling   -> move repeatedly through slots     |
    +---------------------------------------------------------------+
```

If a queue has a known maximum size, a fixed circular array can avoid dynamic
resizing entirely. The provided implementation is dynamic so it is easier to
reuse in general Python programs.

---

## 14. Running the Example

Run:

```text
python CircularArray.py
```

Expected output:

```text
Logical values: [20, 30, 40, 50]
Physical slots: [50, 20, 30, 40]
Head index: 1
After both-end operations: [20, 30, 40]
Capacity: 8
```

The physical slots show `[50, 20, 30, 40]`, while the logical sequence starts
at `head index = 1`. This difference is the circular representation.

---

## 15. Final Cheat Sheet

```text
    1. Track head, size, and capacity.
    2. Map logical i with (head + i) % capacity.
    3. Append right at (head + size) % capacity.
    4. Append left by moving head backward modulo capacity.
    5. Resize by copying logical order, not raw physical order.
    6. Track size so empty and full states are unambiguous.
    7. End operations are O(1) amortized; resize is O(n).
```

**Next Step:** Trace a queue by hand after several `popleft` and `append`
operations, then inspect `debug_slots()` to connect logical indexes with
physical storage.
