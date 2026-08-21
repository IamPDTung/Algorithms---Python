
---

# Basic Concept of Binary Heap

## 1. Goal

A **binary heap** is a complete binary tree that satisfies the **heap order
property**: in a max-heap, every parent is greater than or equal to its
children, so the largest element always sits at the root. Because the tree
is complete, it needs no pointers at all -- it lives inside a flat array.

**Why was it born?** We often need to repeatedly pull "the largest so far"
out of a changing collection. A sorted array makes that O(1) but inserting
costs O(N). A binary heap is the sweet spot: it keeps items "dynamically
sorted" so both **insert and delete-max are O(log N)** and the maximum is
always visible in O(1). It is the engine behind priority queues and heap
sort.

The implementation in `BinaryHeapBasics.py` provides:

- A `MaxHeap` with `insert`, `del_max`, `peek`, `is_valid`.
- The two core helpers `_swim` and `_sink` that maintain the invariant.
- An O(N) `heapify` build from any list (bottom-up sinking).
- A `heap_sort` that returns the list in ascending order.
- An ASCII `draw()` that renders the array back into a tree.

Source references:

- [Basic Concept of Binary Heap](https://labuladong.online/en/algo/data-structure-basic/binary-heap-basic/)
- [Binary Heap/Priority Queue Code Implementation](https://labuladong.online/en/algo/data-structure-basic/binary-heap-implement/)

## 2. Two Properties: Complete Tree + Heap Order

A binary heap is the intersection of two ideas:

```text
1. COMPLETE binary tree:
   every level is full, except possibly the last,
   and the last level is filled left to right.

        (a)                     (a)
       /   \                   /   \
     (b)   (c)   OK          (b)   (c)   NOT complete
     / \   /                / \     \
   (d)(e)(f)              (d)(e)    (f)
                              ^ gap in the middle

2. HEAP ORDER (max-heap):
   parent >= child, recursively.

        (9)                     (9)
       /   \                   /   \
     (6)   (8)    OK         (10)  (8)   broken: 10 > 9
     / \   / \               / \
   (5)(3)(2)(7)            (5)(3)
```

The complete-tree property is what makes the array representation possible.
The heap-order property is what makes the maximum findable in O(1).

## 3. The Array Representation

A complete tree maps onto an array with no pointers. Using 1-based
indexing (index 0 is a dummy), the math is:

```text
parent(i) = i // 2
left(i)   = 2*i
right(i)  = 2*i + 1

        index:      1
                   / \
                 2     3
                / \   / \
               4   5 6   7

  array (index 0 unused):
  [X, a, b, c, d, e, f, g]
   0  1  2  3  4  5  6  7

  check: parent of index 5 (e) is 5//2 = 2 (b)      OK
         left of index 2 (b) is 4 (d)               OK
         right of index 2 (b) is 5 (e)              OK
```

The heap from the demo, drawn from its array:

```text
          9
      6     8
    5   3   2   7
   4  1
```

corresponds to the array `[_, 9, 6, 8, 5, 3, 2, 7, 4, 1]`.

## 4. swim: Inserting an Element

Insertion is two steps: append at the end, then **swim** the new value up
until its parent is no longer smaller.

```text
insert(7) into [9,6,8,5,3,2,1]:

  step 1: append at the end
          9
       6     8
     5   3  2   1
    7  <- swim starts here

  step 2: swim up (7 vs parent 5 -> swap)
          9
       6     8
     7   3  2   1
    5

  step 3: swim up (7 vs parent 6 -> swap)
          9
       7     8
     6   3  2   1
    5

  step 4: 7 vs parent 9 -> 9 > 7, stop.
  heap order restored, O(log N).
```

`swim` only ever moves a value upward along the root path:

```text
swim(k):
  while k > 1 and parent(k) < heap[k]:
      swap(k, parent(k))
      k = parent(k)
```

## 5. sink: Deleting the Maximum

The maximum is the root. To delete it: move the last element to the root,
then **sink** it down, always swapping with the larger child.

```text
del_max() from [9,6,8,5,3,2,1]  (max = 9)

  step 1: put the last element (1) at the root
          1
       6     8
     5   3  2  X

  step 2: sink (children 6, 8 -> larger is 8, swap)
          8
       6     1
     5   3  2

  step 3: sink (children 2, X -> larger is 2, swap with 1? 1 < 2)
          8
       6     2
     5   3  X
  stop: no more children. O(log N).
```

`sink` swaps with the **larger** child so the max-heap property survives:

```text
sink(k):
  while 2*k <= n:
      j = 2*k
      if j < n and heap[j] < heap[j+1]: j += 1   # pick larger child
      if heap[k] >= heap[j]: break
      swap(k, j)
      k = j
```

## 6. Building a Heap: O(N) heapify

Naively inserting N elements one by one costs O(N log N). But if we start
from an arbitrary array, we can fix it in **O(N)** by sinking every
non-leaf from the bottom up:

```text
array (not a heap yet):
  [_, 5, 3, 8, 1, 9, 2, 7, 4, 6]

  bottom-up sink from n//2 = 4 down to 1:

  sink(4): 1 has child 6 -> swap      -> 6
  sink(3): 8 has children 2,7 -> swap with 7 -> 7
  sink(2): 3 has children 6,9 -> swap with 9 -> 9, then 3 sinks again
  sink(1): 5 vs 9/7 -> swap with 9 -> 9, sink 5 down...

  final heap:
            9
        6       8
      5   3   2   7
     4  1
```

Why is it O(N)? Most nodes are near the bottom and sink only one or two
levels. Formally, the total work is a geometric sum:

```text
N/2 nodes sink <= 1 level,  N/4 sink <= 2,  N/8 sink <= 3, ...

sum = N/2*1 + N/4*2 + N/8*3 + ... = O(N)
```

## 7. The Most Common Use: Priority Queue

A priority queue is a queue where the element with the highest priority
leaves first. A binary heap implements it directly:

```text
            push               pop
         (insert+swim)     (swap+sink)
   input -------> [max-heap] -------> largest first
                    O(log N)           O(log N)

  peek: look at the root            O(1)
```

Typical jobs: Dijkstra's shortest paths, scheduling tasks by urgency,
merging K sorted streams, top-K problems -- anything that repeatedly asks
"what is the current maximum/minimum?"

## 8. Another Use: Heap Sort

Heap sort reuses the same heap: build, then repeatedly swap the root with
the last element and sink.

```text
[5,3,8,1,9,2,7,4,6]

  step 1: heapify                    step 2: swap root with last
           9                          1
        6     8                    6     8
      5  3  2  7                  5  3  2  7
     4  1                         4  [9]  <- 9 is now sorted

  step 3: sink the new root, shrink the heap
           8
        6     7
      5  3  2  1
     4  [9]

  repeat ... the "sorted" zone grows from the right end:
  [1,2,3,4,5,6,7,8,9]
```

Total cost is O(N log N): O(N) to build, then N-1 sink operations each
O(log N). It sorts in place with no extra memory.

## 9. Complexity

```text
operation        cost
---------------- ---------
peek (max)       O(1)
insert (push)    O(log N)
del_max (pop)    O(log N)
heapify (build)  O(N)
heap_sort        O(N log N)
memory           O(N), in place (no extra pointers)
```

The height of a complete tree with N nodes is exactly floor(log2(N)), which
bounds every swim/sink path.

## 10. Demo Walkthrough

Running `BinaryHeapBasics.py` prints:

```text
=== Binary heap basics demo ===
insert/pop order (max first): [9, 6, 5, 4, 3, 2, 1, 1]

heapify([5,3,8,1,9,2,7,4,6]) tree:
          9
      6     8
    5   3   2   7
   4  1

heap_sort randomized check passed for 50 arrays.
All assertions passed.
```

What the demo proves:

```text
- inserting 3,1,4,1,5,9,2,6 keeps the heap valid after every insert
- popping returns [9,6,5,4,3,2,1,1], largest first
- heapify produces a valid heap whose root is the maximum
- heap_sort matches Python's sorted() on 50 random arrays
```

## 11. Limitations and Summary

```text
strengths:
  - O(log N) insert AND delete-max, O(1) peek
  - no pointers: cache-friendly flat array
  - in-place heap sort with no extra memory

trade-offs:
  - cannot search for an arbitrary element efficiently (O(N))
  - no locality of keys: it is NOT a sorted structure like a BST
  - no easy merge of two heaps (O(N) unless using a meldable heap)

when to use:
  - you only need the max/min and repeated push/pop
  - for arbitrary-element search, prefer a BST or hash table
```

Summary in one sentence: a binary heap is a complete binary tree in an array
that keeps the largest element at the root using just two local fixes --
swim on insert and sink on delete.
