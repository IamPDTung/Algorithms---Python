
---

# Binary Heap / Priority Queue Code Implementation

## 1. Goal

A **priority queue** is a queue where the item with the highest priority
always leaves first. The classic way to build one is a binary heap: the
heap keeps the top-priority item at the root, and only two local fixes --
`swim` and `sink` -- are needed to keep that true after every change.

**Why does the array representation matter here?** Because the tree is
*implicit*: there are no pointers at all. A node's parent and children are
pure index arithmetic. That makes the implementation tiny, fast, and
cache-friendly.

The implementation in `BinaryHeapImplementation.py` provides:

- A generic `PriorityQueue` with a pluggable comparator (max-heap or
  min-heap), `push`, `pop`, `peek`, `update`, `remove`, `is_valid`.
- An `IndexMinPQ` (indexed priority queue) used by graph algorithms, with
  `insert`, `decrease_key`, `increase_key`, `del_min`, `min_index`.
- A Dijkstra shortest-path demo that uses the `IndexMinPQ`.

Source references:

- [Binary Heap/Priority Queue Code Implementation](https://labuladong.online/en/algo/data-structure-basic/binary-heap-implement/)
- [Basic Concept of Binary Heap](https://labuladong.online/en/algo/data-structure-basic/binary-heap-basic/)

## 2. Key Challenges

A heap-based priority queue must answer two questions on every mutation:

```text
challenge 1: the tree is 2D but the array is 1D
  -> map indices: parent(i)=(i-1)//2, left(i)=2i+1, right(i)=2i+2

challenge 2: after insert or delete, the heap order may break
  -> restore it with exactly two local fixes:
       swim : a child became too "big"  -> bubble it up
       sink : a parent became too "small" -> push it down
```

Everything else (peek, size, contains) is trivial bookkeeping. Getting
`swim` and `sink` right is the whole battle.

## 3. Insertion: push / swim

Inserting appends at the end of the array, then swims the new item up until
its parent is no longer smaller:

```text
push(7)  into max-heap [9,6,8,5,3,2,1]  (0-indexed: [9,6,8,5,3,2,1])

  append 7 at the end:
     [9,6,8,5,3,2,1,7]
      index:0 1 2 3 4 5 6 7
                        ^

  swim(7): parent = (7-1)//2 = 3  -> 5 < 7, swap
     [9,6,8,7,3,2,1,5]
      index:0 1 2 3 ...
  swim(3): parent = (3-1)//2 = 1  -> 6 < 7, swap
     [9,7,8,6,3,2,1,5]
  swim(1): parent = 0  -> 9 >= 7, stop
```

```text
swim(k):
  while k > 0:
      parent = (k-1)//2
      if parent >= heap[k]: break
      swap(parent, k)
      k = parent
```

## 4. Deletion: pop / sink

The top item is the root. To pop it: move the last element to the root,
then sink it down, always swapping with the larger child:

```text
pop() from [9,6,8,5,3,2,1]  (max = 9)

  save 9; move last element (1) to the root:
     [1,6,8,5,3,2]          9 is returned

  sink(0): children 6,8 -> larger is 8 -> swap
     [8,6,1,5,3,2]
  sink(2): children 3,2 -> larger is 3 -> 1 < 3, swap
     [8,6,3,5,1,2]
  sink(4): no children. done.
```

```text
sink(k):
  while 2k+1 < n:
      j = 2k+1
      if j+1 < n and heap[j] < heap[j+1]: j += 1   # larger child
      if heap[k] >= heap[j]: break
      swap(k, j)
      k = j
```

## 5. Query: peek

The maximum is always at index 0, so peek is O(1) and requires no fix at
all:

```text
peek() -> heap[0]
```

`is_empty` and `len` are just array-length checks.

## 6. Simulating the Binary Tree with an Array

This implementation uses **0-indexed** indexing (a slightly different
convention from the 1-indexed one in the "Basic Concept" article -- both
are valid):

```text
0-indexed array [_, a, b, c, d, e, f, g]:

        a (index 0)
       / \
    b (1) c (2)
   / \   / \
d(3) e(4) f(5) g(6)

  parent(i)  = (i-1)//2
  left(i)    = 2*i+1
  right(i)   = 2*i+2

  check: parent(5)=2 (f's parent is c)          OK
         left(1)=3 (b's left child is d)        OK
         right(1)=4 (b's right child is e)      OK
```

The index math is the only "tree" the code ever touches -- no `Node`
objects, no `left`/`right` pointers.

## 7. Code Implementation of the Generic PriorityQueue

The comparator `less(a, b)` is the single knob that switches between a
max-heap and a min-heap:

```python
class PriorityQueue(Generic[T]):
    def __init__(self, less=None):
        self._data = []
        self._less = less if less is not None else (lambda a, b: a < b)
```

```text
default:  less(a,b) = a < b   -> a "smaller" sinks, largest pops first
                                = MAX-heap
pass:     less(a,b) = a > b   -> smallest pops first
                                = MIN-heap
```

The public API:

```text
push(item)     O(log N)   append + swim
pop()          O(log N)   swap root/last + sink
peek()         O(1)       read heap[0]
update(a, b)   O(N)       replace a with b, then swim + sink
remove(a)      O(N)       remove a, then swim + sink
len / is_empty O(1)
```

`update` and `remove` search the array linearly (O(N)) because a heap has
no way to find an arbitrary item faster; once found, the fix is still just
swim + sink.

## 8. Improved Priority Queue: Dynamic Priority and IndexMinPQ

A plain priority queue cannot lower an item's priority efficiently, because
it has no handle to find that item. Dijkstra's algorithm needs exactly
this: when a shorter path to a node is discovered, its distance must
decrease.

The **indexed priority queue** fixes it by keying items by integer index:

```text
IndexMinPQ arrays:
   pq       : the heap itself, holding INDICES
   qp       : index -> its position in pq   (-1 if absent)
   priority : index -> its current priority

   min-heap by priority: pq[0] is the index with the smallest priority.

   decrease_key(i, p): update priority[i], then swim only at qp[i]
                       -> O(log N), no search needed
```

```text
        pq (heap of indices)          priority array
   pos:  0     1     2            idx:  0     1     2     3
         [2]   [0]   [3]               [4.0] [7.0] [1.5] [2.0]
          ^                                 ^
    smallest priority                     qp: [1, -1, 0, 2]
    is index 2 (1.5)
```

Dijkstra on the demo graph uses `decrease_key` every time a distance
improves:

```text
demo graph (undirected):
        1
  0 --------- 1
  |           |
  | 4      5  |
  |           |
  2 --------- 3
        1

  edge weights: 0-1 = 1, 0-2 = 4, 1-3 = 5, 2-3 = 1
  (the diagonal edge 1-2 = 2 is omitted from the drawing)

  shortest distances from node 0:
        dist[0]=0, dist[1]=1, dist[2]=3, dist[3]=4
```

## 9. Complexity

```text
PriorityQueue            IndexMinPQ
----------------------   ----------------------
push      O(log N)       insert          O(log N)
pop       O(log N)       del_min         O(log N)
peek      O(1)           min_index       O(1)
update    O(N)           decrease_key    O(log N)
remove    O(N)           increase_key    O(log N)
contains  O(N)           contains        O(1)
memory    O(N)           memory          3*O(N)
```

The IndexMinPQ trades a `qp` array for O(1) lookup and O(log N)
decrease-key -- the reason Dijkstra runs in O(E log V).

## 10. Demo Walkthrough

Running `BinaryHeapImplementation.py` prints:

```text
=== Priority queue demo ===
max-heap pop order: [9, 6, 5, 4, 3, 2, 1, 1]
min-heap pop order: [1, 1, 2, 3, 4, 5, 6, 9]
after update(5,100) and remove(10): [100, 3]

IndexMinPQ basic ops...
IndexMinPQ basic ops passed.

Dijkstra with IndexMinPQ...
shortest distances from node 0: [0.0, 1.0, 3.0, 4.0]
```

What the demo proves:

```text
- the same pushes give [9,6,5,4,3,2,1,1] with the default max-heap
- flipping the comparator gives the min-heap [1,1,2,3,4,5,6,9]
- update(5,100) reprioritizes and 100 pops first; remove works
- decrease_key/increase_key flip the minimum instantly
- Dijkstra with the IndexMinPQ returns the correct distances
```

## 11. Limitations and Summary

```text
strengths:
  - O(log N) push/pop, O(1) peek, no pointers
  - one comparator turns a max-heap into a min-heap
  - the IndexMinPQ supports O(log N) decrease-key for graph algorithms

trade-offs:
  - arbitrary-item search/update is O(N) in a plain PQ
  - no iteration in sorted order (a heap is not a BST)
  - duplicate items complicate "remove by value" semantics

when to use:
  - repeated push/pop of the current max/min
  - Dijkstra / Prim / A* need the IndexMinPQ form
```

Summary in one sentence: a priority queue is a binary heap in an array whose
only two maintenance operations are swim (on push) and sink (on pop), and
adding an index mapping upgrades it into the O(log N) decrease-key structure
that Dijkstra needs.
