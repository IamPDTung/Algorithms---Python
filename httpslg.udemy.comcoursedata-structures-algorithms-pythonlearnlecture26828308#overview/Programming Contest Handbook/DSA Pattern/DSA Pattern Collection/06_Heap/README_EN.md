# HEAP (PRIORITY QUEUE)

## What is it?

A Heap is a **complete binary tree** where every parent is ≤ (min-heap) or ≥ (max-heap)
its children. Python's `heapq` implements a **min-heap**. The smallest element is always
at the root and can be extracted in **O(log n)**; inserting takes **O(log n)**.

Key fact: `heapq` is min-heap only — for a max-heap, store **negated values**.

## Why use it?

- We only ever care about the **smallest / largest k** elements, not the full order.
- Maintains an "always sorted at the top" structure under **inserts and deletes** —
  ideal for **streaming / dynamic data**.
- Solves **Top K**, **Kth largest/smallest**, **merge k sorted lists**, **running median**.

## When to use?

| Signal in the problem | Why |
|---|---|
| "Top K frequent / largest / smallest" | pop k from heap |
| "Kth largest / smallest" | min-heap of size k |
| "Merge k sorted lists" | push heads, pop smallest each time |
| "Running median / median in stream" | two heaps (max + min) |
| "Smallest/cheapest x at each step" | greedy + heap |

## Visualization — min-heap and its array form

```
           1
         /   \
       3      2
      / \    / \
     6   5  7   4

 array (heapq): [1, 3, 2, 6, 5, 7, 4]
 index:          [0, 1, 2, 3, 4, 5, 6]
 children of i:  2i+1, 2i+2
 parent of i:    (i-1)//2
```

Two heaps for running median:

```
 numbers so far: 5, 15, 1, 3
 max-heap (left) | min-heap (right)
   [5]           | [15]
   [1,5]         | [15]     after 1
   [1,3,5]  <--> [15]       -> balance: move 5 over
   [1,3]         | [5,15]
 median = (max(left) + min(right)) / 2 = (3 + 5) / 2 = 4
```

## Complexity

- **Time:** O(log n) per push / pop; O(1) to peek min
- **Space:** O(n)

## Template

```python
import heapq

heap = []                       # min-heap
heapq.heappush(heap, x)
smallest = heapq.heappop(heap)
top = heap[0]

# max-heap trick:
heapq.heappush(heap, -x)        # store negated
largest = -heapq.heappop(heap)

# Kth largest: keep heap of size k
```

## Example problems solved in this folder

| Problem | File | Idea |
|---|---|---|
| Kth Largest Element in Array | `kth_largest_element.py` | min-heap of size k |
| Merge K Sorted Lists | `merge_k_sorted_lists.py` | heap of current heads |
| Find Median from Data Stream | `find_median_from_data_stream.py` | two heaps |

## Practice

Try: Top K Frequent Elements, K Closest Points to Origin, Task Scheduler,
Kth Smallest Element in a Sorted Matrix.
