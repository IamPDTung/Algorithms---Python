# TreeMap Structure and Visualization

## 1. Goal

A TreeMap is a Map whose keys live in a binary search tree, so the keys stay sorted at all times. It was born because a HashMap cannot answer ordering questions at all: it cannot tell you the smallest key, the largest key, the keys between two bounds, or the k-th smallest key, because its bucket array has no notion of order. A LinkedHashMap only preserves insertion order, which is the sequence in which keys were added, not an ordering by the key value itself. A TreeMap answers all of those ordered questions in O(logN) time by walking a BST.

Source references:

- [TreeMap Structure and Visualization](https://labuladong.online/en/algo/data-structure-basic/tree-map-basic/)

The implementation in `TreeMapStructure.py` provides:

- A `BSTNode` that stores key, value, and the subtree size.
- A full `TreeMap` with `put`, `get`, `remove`, `contains_key`, `keys`, `first_key`, `last_key`, `floor_key`, `ceiling_key`, `select`, `rank`, and `range_keys`.
- Ordered navigation (`first_key`, `floor_key`, ...) powered by the BST invariant.
- `select`/`rank` powered by subtree sizes.
- A `search_steps` helper and a `draw` helper that visualize the search path and the tree shape, proving why a balanced BST beats a degenerate one.

## 2. Advantages of a BST

A binary search tree is a binary tree with one extra rule per node: every key in the left subtree is smaller than the node key, and every key in the right subtree is larger.

```text
            (8)
           /    \
       (3)        (10)
      /   \      /    \
   (1)    (6)  (9)   (12)
         /   \
      (4)    (7)

   left subtree  : every key < node.key
   right subtree : every key > node.key
```

This single rule turns a tree into a sorted structure and gives the search a direction. An ordinary tree gives the search no clue whether to go left or right, so in the worst case it must examine every node. A BST compares the target key against the current node and discards one whole half of the remaining nodes at every step.

```text
   ordinary tree (no order)          BST (ordered)

        (5)                              (8)
       / |  \                          /      \
    (9) (1) (7)                     (3)        (10)
     |     |   |                   /   \      /    \
   (4)   (2) (6)                (1)    (6)  (9)  (12)
                                          / \
   search(6): visits 5, 9, 1, 2, 4      (4) (7)
   ...every node is a candidate...
          O(N)                    search(6): 8 -> 3 -> 6
   worst case                       one path, 3 steps
                                    O(logN) when balanced
```

## 3. How TreeMap / TreeSet Work

A TreeMap node is a BST node that holds both the key and the value. The BST invariant orders the keys; the value just rides along.

```text
   BSTNode(key=8, value=80)
        +-----------------+
        |  key  = 8       |
        |  value = 80     |      a TreeMap node = key + value + size
        |  size = 3       |
        |  left  -> (7)   |
        |  right -> (9)   |
        +-----------------+
```

In Python the node is a small class with those five fields:

```python
class BSTNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.size = 1
```

A TreeSet is exactly a TreeMap that ignores the value: it stores keys in the same sorted BST and treats the value as a dummy. In many libraries the TreeSet is literally a wrapper around a TreeMap.

```text
   TreeMap<TKey, TValue>   stores (key, value) in the BST
   TreeSet<TKey>           same BST, every value is a dummy
```

The decisive difference against a HashMap is order. A HashMap scatters keys over a bucket array by hash code, so the smallest key could be anywhere; a TreeMap keeps the same keys in a tree that is always sorted.

```text
   HashMap (bucket array)                  TreeMap (BST)
   keys placed by hash code                keys placed by value

   +------+------+------+------+             (6)
   |      |      |      |      |            /    \
   +------+------+------+------+         (3)      (9)
   hash(1)->bucket 2                     /  \    /   \
   hash(3)->bucket 0                  (1)  (4)(8)  (12)
   hash(6)->bucket 1
   hash(9)->bucket 3

   smallest key?   unknown,             first_key()   = 1
                   must scan all        last_key()    = 12
   keys in [3,9]?  must scan all        range_keys(3,9) = [3,4,6,8,9]
```

## 4. API Overview

| Method | Meaning | Complexity (balanced BST) |
|:---|:---|:---:|
| `put(key, value)` | insert or update; returns the old value | `O(logN)` |
| `get(key)` | value of the key, or `None` | `O(logN)` |
| `remove(key)` | delete the key; returns the old value | `O(logN)` |
| `contains_key(key)` | whether the key exists | `O(logN)` |
| `keys()` | all keys in ascending order | `O(N)` |
| `first_key()` | smallest key | `O(logN)` |
| `last_key()` | largest key | `O(logN)` |
| `floor_key(key)` | largest key <= key | `O(logN)` |
| `ceiling_key(key)` | smallest key >= key | `O(logN)` |
| `select(k)` | k-th smallest key, 1-based | `O(logN)` |
| `rank(key)` | 1-based rank of the key | `O(logN)` |
| `range_keys(low, high)` | sorted keys with low <= key <= high | `O(logN + k)` |

The `get`/`put`/`remove` family is the same interface as a HashMap, so the TreeMap can be used anywhere a HashMap is used. The second family of ordered methods is what a HashMap cannot offer.

```text
   HashMap  : get / put / remove / contains   (unordered, O(1) average)
   TreeMap  : get / put / remove / contains   (ordered,  O(logN))
            + first_key / last_key / floor_key / ceiling_key
            + select / rank / range_keys / keys
```

A short usage example:

```python
tm = TreeMap()
tm.put("b", 2)
tm.put("a", 1)
tm.put("c", 3)
tm.keys()              # ['a', 'b', 'c']
tm.first_key()         # 'a'
tm.ceiling_key("bb")   # 'c'
tm.select(2)           # 'b'
tm.rank("b")           # 2
tm.range_keys("a", "b")  # ['a', 'b']
```

## 5. Basic Operations: Add, Delete, Find, Update

Finding a key is a guided descent: compare at each node, go left when the key is smaller, go right when it is larger.

```text
   get(4) on the sample tree

        (5)         4 < 5  -> go left
       /   \
    (3)     (8)     4 > 3  -> go right
   /   \   /   \
 (2)   (4)(7)  (9)  4 == 4 -> found, return value
```

Adding a key walks the same path and attaches a new node in the empty slot. Every ancestor on the path then increments its `size`.

```text
   put(6) on the sample tree

   step 0   start at root (5), 6 > 5  -> go right
   step 1   node (8),      6 < 8      -> go left
   step 2   node (7),      6 < 7      -> go left
   step 3   empty slot, attach new node (6)

        (5)                              (5)
       /   \                            /   \
    (3)     (8)                      (3)     (8)
   /   \   /   \                    /   \   /   \
 (2)   (4)(7)  (9)                (2)   (4)(7)  (9)
                                      /
                                    (6)

   before insert                    after insert
```

Updating an existing key is the same walk but with a write at the end instead of a new node, so the size never changes.

Deleting is the hardest case. A leaf is removed directly; a node with one child is replaced by that child; a node with two children is replaced by its in-order successor, the smallest key of the right subtree.

```text
   remove(5) from the sample tree

   case 1: leaf (2) -> just cut it off

   case 2: one child -> splice the child up

   case 3: two children -> successor deletion
        (5)                  successor = min of right subtree = (7)
       /   \
    (3)     (8)
   /   \   /   \
 (2)   (4)(7)  (9)

   copy (7) over (5), then delete the min from the right subtree
        (7)
       /   \
    (3)     (8)
   /   \     \
 (2)   (4)  (9)
```

## 6. firstKey / lastKey and keys() (In-Order Traversal)

The smallest key lives at the leftmost node, the largest key at the rightmost node. Both are pure walks.

```text
   first_key(): always walk left          last_key(): always walk right

        (5)         <- root                    (5)         <- root
       /   \                                 /   \
    (3)     (8)     (5).left = (3)          (3)     (8)     (5).right = (8)
   /   \   /   \                           /   \   /   \
 (2)   (4)(7)  (9)  (3).left = (2)       (2)   (4)(7)  (9)  (8).right = (9)
   (2).left = None                       (9).right = None
   first_key = 2                         last_key = 9
```

Collecting all keys in order is a plain in-order traversal: visit the left subtree, then the node, then the right subtree. The output is automatically sorted.

```text
   in-order visits:  (2) -> (3) -> (4) -> (5) -> (7) -> (8) -> (9)
   keys() = [2, 3, 4, 5, 7, 8, 9]
```

`floor_key` and `ceiling_key` are bounded versions of these walks. `floor_key(6)` keeps the largest key that is still below or equal to 6, `ceiling_key(6)` keeps the smallest key above or equal to 6.

```text
   floor_key(6) -> 5       ceiling_key(6) -> 7
   (largest key <= 6)      (smallest key >= 6)

        (5)                     (5)
       /   \                   /   \
    (3)     (8)              (3)     (8)
   /   \   /   \             /   \   /   \
 (2)   (4)(7)  (9)         (2)   (4)(7)  (9)
        ^                       ^
     5 is the closest        7 is the closest
     key below 6             key above 6
```

## 7. select / rank Using Subtree Sizes

Each node stores `size`, the total number of nodes in its subtree. This single number lets `select` and `rank` jump to the answer without visiting everything.

```text
   size = 1 + size(left) + size(right)

        (5) size = 7
       /   \
   (3) sz=3 (8) sz=3
   /   \      /   \
 (2) 1 (4) 1 (7) 1 (9) 1
```

`select(k)` returns the k-th smallest key. At each node it compares `k` with the left subtree size: if the k-th key is inside the left subtree, go left; if it is exactly the node itself, stop; otherwise subtract the left part and go right.

```text
   select(4) on the sample tree
   root (5): size(left) = 3, k = 4 = 3 + 1  -> the node itself -> 5

   select(6) on the sample tree
   root (5): 6 > 3 + 1  -> go right, k = 6 - 3 - 1 = 2
   node (8): size(left) = 1, k = 2 = 1 + 1   -> the node itself -> 8

   result: select(1)=2, select(4)=5, select(7)=9
```

The recursive shape of `_select`:

```python
def _select(node, k):
    if node is None:
        return None
    left_size = size_of(node.left)
    if k == left_size + 1:
        return node.key
    if k <= left_size:
        return _select(node.left, k)
    return _select(node.right, k - left_size - 1)
```

`rank(key)` is the inverse: the number of keys strictly smaller than the key, plus one. Every time the search turns right, it adds the whole left subtree and the node itself; turning left adds nothing.

```text
   rank(7) on the sample tree
   (5): 7 > 5  -> add size(left)+1 = 3+1 = 4, go right
   (8): 7 < 8  -> go left, add nothing
   (7): 7 == 7 -> add size(left)+1 = 0+1 = 1
   total = 4 + 1 = 5

   rank(2) = 1, rank(5) = 4, rank(9) = 7
```

Because the tree is balanced, both operations cost O(logN) instead of scanning the whole list.

## 8. Range Search

`range_keys(low, high)` returns every key in `[low, high]` in sorted order. The BST lets the search prune whole subtrees that cannot contain a key inside the range.

```text
   range_keys(3, 8) on the sample tree

        (5)
       /   \
    (3)     (8)
   /   \   /   \
 (2)   (4)(7)  (9)

   (5): low 3 < 5 -> visit left subtree;   3<=5<=8 -> keep 5;  5 < high 8 -> visit right
   (3): low 3 < 3? no -> prune left (2 excluded)
        3<=3<=8 -> keep 3;  3 < high 8 -> visit right
   (4): 3<=4<=8 -> keep 4
   (8): low 3 < 8 -> visit left (7);
        3<=8<=8 -> keep 8;  8 < high 8? no -> prune right (9 excluded)
   (7): 3<=7<=8 -> keep 7

   result = [3, 4, 5, 7, 8]
```

The two pruning rules: the left subtree is visited only when `low < node.key` (otherwise every key there is below the range), and the right subtree is visited only when `node.key < high` (otherwise every key there is above the range). Keys 2 and 9 are never examined.

The recursive shape of `_range`:

```python
def _range(node, low, high, out):
    if node is None:
        return
    if low < node.key:
        _range(node.left, low, high, out)
    if low <= node.key <= high:
        out.append(node.key)
    if node.key < high:
        _range(node.right, low, high, out)
```

## 9. Performance Problem: Unbalanced BST Degrades to O(N)

All of the O(logN) promises above hold only when the tree stays balanced. If keys are inserted in sorted order, the BST becomes a linked list and every promise collapses to O(N).

```text
   balanced BST (height 4)            degenerate BST = linked list (height 8)

        (4)                                     (1)
       /   \                                     \
    (2)     (6)                                  (2)
   /   \   /   \                                  \
 (1)   (3)(5)  (7)                                (3)
                   \                               ...
                    (8)                           (8)

   search(8): 4 -> 6 -> 7 -> 8          search(8): 1 -> 2 -> ... -> 8
   4 steps,  O(logN)                    8 steps,  O(N)
```

The height of the balanced tree is 4, the height of the degenerate tree is 8, and `search_steps(8)` counts exactly 4 visits against 8. This is why production TreeMaps do not use a plain BST: they use a self-balancing variant, the red-black tree, which keeps the height bounded by O(logN) no matter what order the keys arrive in. Red-black rebalancing guarantees the worst case, not just the average.

## 10. Demo Walkthrough

Run:

```text
python TreeMapStructure.py
```

The demo first builds the tree `5,3,8,2,4,7,9` with value = key*10 and checks every ordered query by hand:

```text
len = 7 | height = 3
keys() = [2, 3, 4, 5, 7, 8, 9]
first_key = 2 | last_key = 9
floor_key(6) = 5 | ceiling_key(6) = 7
select(1) = 2 | select(4) = 5
rank(5) = 4 | rank(2) = 1
range_keys(3, 8) = [3, 4, 5, 7, 8]
```

Then it exercises update and delete: `put(5, 999)` overwrites the value in place, `remove(5)` uses successor deletion, and removing the leaf `2` and the node `7` keeps the keys sorted.

Finally it compares a degenerate tree (insert `1..8` in order) against a balanced tree (insert mid-first: `4,2,1,3,6,5,7,8`):

```text
Degenerate BST: height = 8, search_steps(8) = [1, 2, 3, 4, 5, 6, 7, 8]
Balanced BST:   height = 4, search_steps(8) = [4, 6, 7, 8]
```

The balanced tree wins on both metrics, and its shape is printed with the `draw` helper.

## 11. Limitations and Summary

The plain BST implementation here is educational: it is correct, sorted, and ordered-query capable, but it does not self-balance. Inserting sorted data turns it into a linked list. Real libraries solve this with red-black trees (Java TreeMap/TreeSet), AVL trees, or B-trees.

Summary of what was learned:

```text
- A TreeMap is a Map whose keys live in a BST, so keys stay sorted.
- Ordered queries (first/last/floor/ceiling/select/rank/range) come from
  the BST invariant and subtree sizes.
- Subtree sizes turn select/rank into O(logN) operations.
- Range search prunes whole subtrees and never touches out-of-range keys.
- Without balancing, a BST degrades to a linked list and O(N) behavior.
```

## 12. Complexity Table

| Operation | HashMap | TreeMap (balanced BST) |
|:---|:---:|:---:|
| `get` / `contains_key` | `O(1)` average | `O(logN)` |
| `put` | `O(1)` average | `O(logN)` |
| `remove` | `O(1)` average | `O(logN)` |
| `keys()` (sorted) | requires sort `O(N logN)` | `O(N)` in-order |
| `first_key` / `last_key` | not supported | `O(logN)` |
| `floor_key` / `ceiling_key` | not supported | `O(logN)` |
| `select` / `rank` | not supported | `O(logN)` |
| `range_keys(low, high)` | not supported | `O(logN + k)`, `k` = results |

## 13. Sources and References

- [TreeMap Structure and Visualization](https://labuladong.online/en/algo/data-structure-basic/tree-map-basic/)
