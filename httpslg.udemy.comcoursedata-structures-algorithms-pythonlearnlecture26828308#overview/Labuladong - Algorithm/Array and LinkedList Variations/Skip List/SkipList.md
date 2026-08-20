
---

# Skip List

## 1. What Is a Skip List?

A **skip list** is an ordered linked-list structure with extra forward links.
The bottom level contains every value in sorted order. Higher levels contain a
sample of those values and let a search skip over many nodes at once.

```text
    Level 3:  HEAD -------------------------------> 40 ----------> None
    Level 2:  HEAD -------------> 20 ------------> 40 ----------> None
    Level 1:  HEAD ------> 10 ---> 20 ---> 30 ---> 40 ---> 50 --> None
```

The structure combines:

* linked-list flexibility
* sorted traversal
* expected `O(log n)` search, insertion, and deletion

The implementation in `SkipList.py` stores a unique ordered set of comparable
values. A duplicate insertion returns `False` and does not add another node.

---

## 2. Why Add Express Lanes to a Linked List?

A normal sorted linked list has only one next pointer per node:

```text
    HEAD -> 10 -> 20 -> 30 -> 40 -> 50 -> 60 -> None
```

Searching for `50` requires visiting each earlier node. The search is `O(n)`.

A skip list adds links that jump farther:

```text
    slow lane:  HEAD -> 10 -> 20 -> 30 -> 40 -> 50 -> 60 -> None
    fast lane:  HEAD --------> 20 --------> 40 --------> 60 -> None
```

The search first moves on a high level. When the next jump would pass the
target, it drops down one level and continues. This is similar to taking an
express train and changing to a local train near the destination.

---

## 3. Node Anatomy

Unlike a normal linked-list node, a skip-list node owns an array of forward
pointers.

```text
    node 30 with height 3:

    +------------------+
    | value = 30       |
    | forward[0] -----> next node on bottom level
    | forward[1] -----> next node on level 1
    | forward[2] -----> next node on level 2
    +------------------+
```

The node's **height** is the number of forward pointers it owns. A node with
height `1` appears only on the bottom level. A node with height `3` appears on
levels `0`, `1`, and `2`.

```text
    Height 1:  +-------+   bottom level only
               |  10   |
               +-------+

    Height 3:  +-------+
               |  30   |   level 2 pointer
               |       |   level 1 pointer
               |       |   level 0 pointer
               +-------+
```

The list also has a sentinel `head` node. The sentinel does not represent a
user value; it gives every level a stable starting point.

---

## 4. Random Height and the Probability Rule

When a value is inserted, the implementation flips a virtual coin:

```text
    start at level 1
    while random() < probability:
        promote the node to the next level
```

With `probability = 0.5`, roughly half the nodes reach level `1`, one quarter
reach level `2`, and so on:

```text
    expected population by level:

    Level 3:  1/8 of nodes
    Level 2:  1/4 of nodes
    Level 1:  1/2 of nodes
    Level 0:  all nodes
```

The levels are not perfectly balanced. They are probabilistically balanced.
That is why the normal complexity is called **expected** `O(log n)`, not a
guaranteed `O(log n)`.

The constructor accepts a `seed` so examples and tests can produce repeatable
levels:

```python
skip_list = SkipList[int](max_level=5, probability=0.5, seed=7)
```

Do not use the seeded generator for security-sensitive randomness. It exists
only to make this data-structure example reproducible.

---

## 5. Searching from the Top Down

To search for `37`, begin at the highest active level:

```text
    Level 2:  HEAD ----------------------> 30 -----------------> 50
                                               ^
                                               | 50 is too large
                                               | drop down
    Level 1:  HEAD ------> 10 -------> 30 --> 40 --> 50
                                               ^
                                               | 40 is too large
                                               | drop down
    Level 0:  HEAD -> 10 -> 20 -> 30 -> 35 -> 40
                                      ^
                                      candidate region for 37
```

At each level:

1. Look at the next node.
2. If its value is smaller than the target, move forward.
3. Otherwise, drop down one level.
4. At level `0`, check the next node for equality.

The algorithm never moves backward. The `update` array records the last node
visited at every level, which is needed for insertion and deletion.

---

## 6. The Predecessor Table

For insertion or deletion, the search records predecessors:

```text
    target = 35

    update[2] = 30   -> last node before 35 on level 2
    update[1] = 30   -> last node before 35 on level 1
    update[0] = 30   -> last node before 35 on level 0
```

If a new node gets height `2`, it is linked after `update[0]` and
`update[1]`. If a node is deleted, each matching forward pointer skips over
that node.

```text
    before insert(35):
    30 -------------------------------> 40
    30 ---------> 35? no -------------> 40

    after insert(35), height 2:
    level 1: 30 -----------------------> 35 ----------> 40
    level 0: 30 ---------> 35 ---------> 40
```

The pointers at levels higher than the new node's height are unchanged.

---

## 7. Insertion Steps

`insert(value)` follows this sequence:

```text
    1. Walk from the highest active level to level 0.
    2. Store each level's predecessor in update[].
    3. Reject the value if the level-0 candidate is equal.
    4. Generate a random height for the new node.
    5. Splice the new node into every level it reaches.
```

Pointer splicing at one level looks like this:

```text
    BEFORE:

    previous ----------------------> next

    AFTER:

    previous -------------> new -------------> next
```

The order of assignment matters. Save the old `next` pointer before replacing
`previous.forward[level]`, or the remainder of the list can become detached.

---

## 8. Deletion Steps

To delete `30`, first collect the predecessors:

```text
    BEFORE:

    Level 2: HEAD -----------------> 30 -----------------> 50
    Level 1: HEAD --------> 20 ----> 30 --------> 40 ----> 50
    Level 0: HEAD -> 10 -> 20 -> 30 -> 40 -> 50

    AFTER:

    Level 2: HEAD ---------------------------------------> 50
    Level 1: HEAD --------> 20 ----------------> 40 ----> 50
    Level 0: HEAD -> 10 -> 20 -> 40 -> 50
```

Only levels containing the deleted node are rewired. Empty top levels are
then removed from the active height of the list.

---

## 9. Implementation Interface

The complete implementation is in `SkipList.py`:

```python
skip_list = SkipList[int](max_level=16, probability=0.5)

skip_list.insert(30)       # True when the set changes
skip_list.search(30)       # 30, or None
skip_list.contains(30)     # True or False
skip_list.delete(30)       # True when a node was removed
skip_list.to_list()        # sorted bottom-level values
skip_list.levels()         # values on every active level
```

Values must support ordering with `<` and equality with `==`. The reference
implementation rejects `None` because the sentinel uses `None` internally and
normal skip-list values need to be comparable.

---

## 10. Complexity

| Operation | Expected | Worst case | Reason |
|:---|:---:|:---:|:---|
| Search | `O(log n)` | `O(n)` | Random levels may be unlucky |
| Insert | `O(log n)` | `O(n)` | Search plus pointer splicing |
| Delete | `O(log n)` | `O(n)` | Search plus pointer rewiring |
| Sorted iteration | `O(n)` | `O(n)` | Follow level `0` |
| Extra space | `O(n)` expected | `O(n * max_level)` bound | Forward pointers |

The expected space is `O(n)` because the probability of reaching another
level decreases geometrically. A deterministic balanced tree gives stronger
worst-case guarantees; a skip list is attractive when simple pointer logic,
ordered iteration, and easy implementation are valuable.

---

## 11. Skip List vs Other Structures

| Structure | Search | Insert | Delete | Ordered iteration |
|:---|:---:|:---:|:---:|:---:|
| Unsorted linked list | `O(n)` | `O(1)` at known position | `O(n)` search | `O(n)` |
| Sorted linked list | `O(n)` | `O(n)` search | `O(n)` search | `O(n)` |
| Skip list, expected | `O(log n)` | `O(log n)` | `O(log n)` | `O(n)` |
| Balanced search tree | `O(log n)` | `O(log n)` | `O(log n)` | `O(n)` |
| Hash table | `O(1)` average | `O(1)` average | `O(1)` average | Not naturally sorted |

Skip lists are often used for ordered indexes, in-memory databases, and
systems where a probabilistic alternative to a balanced tree is acceptable.

---

## 12. Common Mistakes

### Mistake 1: Searching only level `0`

That is a sorted linked list and loses the skip-list speedup. Search from the
highest active level and drop down when the next jump is too large.

### Mistake 2: Updating only one forward pointer

A node of height `3` must be linked at levels `0`, `1`, and `2`. Missing one
level makes that express lane inconsistent.

### Mistake 3: Forgetting the predecessor table

Deletion needs the node before the target at every level. Finding only the
target is not enough to rewire singly linked forward pointers.

### Mistake 4: Treating expected complexity as a guarantee

Random levels normally balance the structure, but an unlucky sequence can
degrade toward `O(n)`. The implementation is educational and does not promise
deterministic balancing.

### Mistake 5: Allowing incomparable values

The search compares values with `<`. Mixing strings and integers, or inserting
`None`, causes ordering failures.

---

## 13. Visualizing the Levels

`levels()` returns the values in each active level, highest first:

```text
    levels() result:

    [ [30], [10, 30, 50], [10, 20, 30, 40, 50] ]
      ^       ^                  ^
      |       |                  bottom level
      |       middle level
      highest active level
```

The exact shape depends on the random generator. The bottom list is always
sorted and always contains every inserted value.

---

## 14. Running the Example

Run:

```text
python SkipList.py
```

Expected stable output for the seeded example:

```text
Ordered values: [10, 30, 40, 50]
Contains 40: True
Contains 25: False
Levels: [[30, 50], [10, 30, 40, 50], [10, 30, 40, 50]]
```

The exact `Levels` line depends on the random-number implementation and Python
version. The important invariants are that every level is sorted and the
bottom level contains `[10, 30, 40, 50]` after deletion.

---

## 15. Final Cheat Sheet

```text
    1. Level 0 contains every value in sorted order.
    2. Higher levels are express lanes made from sampled nodes.
    3. Search from the highest level and drop down when needed.
    4. Keep update[level] for insertion and deletion.
    5. A node's height determines which levels it joins.
    6. Duplicates are rejected by this implementation.
    7. Search, insert, and delete are expected O(log n).
    8. Worst-case time can still be O(n).
    9. Values must be mutually comparable.
```

**Next Step:** Draw the predecessor table for an insertion, then manually
rewire one node at two different levels before running `SkipList.py`.
