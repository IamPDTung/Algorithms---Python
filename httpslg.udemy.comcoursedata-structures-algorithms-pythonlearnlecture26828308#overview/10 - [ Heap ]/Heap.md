
---

# Heap

## 1. Complete Trees and Max-Heaps

A **heap** is a tree-shaped structure for keeping an important extreme value easy to access. These notes use a **binary max-heap**: each node has at most two children, the tree is complete, and every parent is greater than or equal to its children.

A **complete binary tree** fills each level from left to right. Only the final level may be incomplete, and it cannot contain a hole before another node. A max-heap adds the parent-child ordering rule; it does not sort siblings or entire branches.

```
    COMPLETE TREE                         MAX-HEAP PROPERTY

             95                                  95
           /    \                              /    \
         75      80                           75      80
        /  \    /  \                         /  \    /  \
      55   60  50   65                      55  60  50  65

    The final level fills left to right.      95 >= 75,80; 75 >= 55,60;
                                               80 >= 50,65.

    largest value = root = heap[0]            not a globally sorted tree
```

If a right child appears while an earlier left position is empty, the tree is not complete. Completeness is what lets the implementation use a compact list instead of node pointers.

---

## 2. Max-Heap, Min-Heap, and Why Heaps Exist

A **max-heap** keeps the largest item at the root. A **min-heap** reverses the comparison and keeps the smallest item at the root; the shape and index formulas remain the same.

```
    MAX-HEAP (parent larger)                 MIN-HEAP (parent smaller)

             95                                  10
           /    \                              /    \
         75      80                            20     15
        /  \    /  \                           / \    / \
      55   60  50   65                        40 30  25 35

    root = maximum                          root = minimum
    bubble if child > parent                bubble if child < parent
```

An unsorted list scans all values to find its maximum. A sorted list exposes an extreme quickly but can cost `O(n)` to maintain after insertion. A heap keeps only the ordering needed at the root, giving `O(1)` peek and `O(log n)` updates.

```
    UNSORTED: [55, 95, 50, 80, 65, 75] -> scan every value -> O(n)
    MAX-HEAP:              95           -> read heap[0]       -> O(1)
                          /  \
                        75    80
```

This supports **priority queues (priority queue)**, **heap sort (heap sort)**, kth-element queries, streaming maximums, scheduling, and graph algorithms. A priority queue repeatedly removes the root rather than keeping every item globally sorted.

```
    incoming work -> heap ordered by priority -> next work
    [low, high, mid] -> [high, low, mid]       -> high (root)
```

---

## 3. Tree, Array, and Index Formulas

The logical tree is stored as the Python list `self.heap`. Level-order placement makes every parent and child addressable by arithmetic; no `left` or `right` pointers are required.

```
    TREE                                  ARRAY (level order)

             95                           index:  0  1  2  3  4  5  6
           /    \                         value: [95,75,80,55,60,50,65]
         75      80
        /  \    /  \                      0=95, 1=75, 2=80, 3=55,
      55   60  50   65                    4=60, 5=50, 6=65
```

For zero-based index `i`:

```text
left child  = 2 * i + 1
right child = 2 * i + 2
parent      = (i - 1) // 2
```

```
    i = 1 (75): left=3 (55), right=4 (60), parent=0 (95)

                 95 (0)
                /
             75 (1)
             /   \
          55 (3) 60 (4)
```

Child bounds must be checked: a leaf has no children, and the final node can have only a left child.

---

## 4. Insert: Append Then Bubble Up

Insertion appends the value at the next open list position, preserving completeness, then swaps it with its parent while it is larger. This upward repair is **bubble-up (bubble-up)** or sift-up and follows one root path at most.

Concrete trace: start with `[99, 72, 61, 58]` and insert `100` at index `4`; its parent is `72` at index `1`.

```
    append: [99,72,61,58,100]       100 > 72

          99                 swap index 4 <-> 1       99
         /  \              --------------------->    /  \
       72    61                                      100  61
      /  \                                            / \
    58  100                                          58  72

    array after swap 1: [99,100,61,58,72]
    100 > root 99, so swap index 1 <-> 0:

          100
         /   \
       99     61       array: [100,99,61,58,72]
      /  \
    58   72            index 0 has no parent: stop
```

Appending `75` to `[100,99,61,58,72]` gives `[100,99,61,58,72,75]`; compare with parent `61`, swap once, and stop at `[100,99,75,58,72,61]` because `75 < 99`.

---

## 5. Remove Root: Move Last Then Sink Down

To remove the maximum, save `heap[0]`, move the last value to index `0`, pop the last slot, and **sink down (sink-down)**. At each level compare both valid children and swap with the larger child when it is larger than the replacement.

### Trace all comparisons for the source example

Start with `[95,75,80,55,60,50,65]`. Save `95`; move last `65` to root: `[65,75,80,55,60,50]`.

```
    before:                 95                 after moving 65:
                           /  \                         65
                         75    80                      /  \
                        / \   / \                    75    80
                      55  60 50 65                  / \   /
                                                    55 60 50

    index 0: compare left 75 and right 80; choose 80 because it is larger.
    80 > 65: SWAP 1 -> [80,75,65,55,60,50].
    index 2: left index 5 is 50; right index 6 is out of bounds.
    compare 50 with 65: no swap. Return 95.
```

The second removal makes the multi-level path explicit: move `50` to `[50,75,65,55,60]`; compare `75` versus `65`, swap to `[75,50,65,55,60]`; at index `1` compare `55` versus `60`, swap with `60` to `[75,60,65,55,50]`; index `4` has no children, so return `80`.

```
    [80,75,65,55,60,50] -> move 50 -> [50,75,65,55,60]
    compare 75,65 -> swap -> [75,50,65,55,60]
    compare 55,60 -> swap -> [75,60,65,55,50]
```

### Edge cases

```
    []       remove() -> None       [42]       remove() -> 42, then []
    insert into [] -> [value]       [42,17]    remove -> [17]
```

The solution checks the empty heap before `heap[0]`, uses `pop()` for one item, ignores a missing right child, and uses strict `>` so equal values need not swap.

---

## 6. Actual Solution: Insert

This is the complete contents of `Core/SOLUTION-Heap-Insert.py`, copied verbatim.

```
    append -> compare parent -> swap upward -> stop at root or valid parent
```

```python
class MaxHeap:
    def __init__(self):
        self.heap = []

    def _left_child(self, index):
        return 2 * index + 1

    def _right_child(self, index):
        return 2 * index + 2

    def _parent(self, index):
        return (index - 1) // 2

    def _swap(self, index1, index2):
        self.heap[index1], self.heap[index2] = self.heap[index2], self.heap[index1]

    def insert(self, value):
        self.heap.append(value)
        current = len(self.heap) - 1

        while current > 0 and self.heap[current] > self.heap[self._parent(current)]:
            self._swap(current, self._parent(current))
            current = self._parent(current)



myheap = MaxHeap()
myheap.insert(99)
myheap.insert(72)
myheap.insert(61)
myheap.insert(58)

print(myheap.heap)  


myheap.insert(100)

print(myheap.heap)  


myheap.insert(75)

print(myheap.heap)


"""
    EXPECTED OUTPUT:
    ----------------
    [99, 72, 61, 58]
    [100, 99, 61, 58, 72]
    [100, 99, 75, 58, 72, 61]

"""

```

---

## 7. Actual Solutions: Remove and Sink-Down

Both remaining core files contain the full class and demonstration below. They are separate files but have the same implementation, so both are included verbatim.

```
    remove root -> move last to root -> choose larger child -> repeat
```

### `SOLUTION-Heap-Remove.py`

```python
class MaxHeap:
    def __init__(self):
        self.heap = []

    def _left_child(self, index):
        return 2 * index + 1

    def _right_child(self, index):
        return 2 * index + 2

    def _parent(self, index):
        return (index - 1) // 2

    def _swap(self, index1, index2):
        self.heap[index1], self.heap[index2] = self.heap[index2], self.heap[index1]

    def insert(self, value):
        self.heap.append(value)
        current = len(self.heap) - 1

        while current > 0 and self.heap[current] > self.heap[self._parent(current)]:
            self._swap(current, self._parent(current))
            current = self._parent(current)


    def _sink_down(self, index):
        max_index = index
        while True:
            left_index = self._left_child(index)
            right_index = self._right_child(index)

            if (left_index < len(self.heap) and 
                    self.heap[left_index] > self.heap[max_index]):
                max_index = left_index

            if (right_index < len(self.heap) and 
                    self.heap[right_index] > self.heap[max_index]):
                max_index = right_index

            if max_index != index:
                self._swap(index, max_index)
                index = max_index
            else:
                return
                       
    def remove(self):
        if len(self.heap) == 0:
            return None

        if len(self.heap) == 1:
            return self.heap.pop()

        max_value = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._sink_down(0)

        return max_value



myheap = MaxHeap()
myheap.insert(95)
myheap.insert(75)
myheap.insert(80)
myheap.insert(55)
myheap.insert(60)
myheap.insert(50)
myheap.insert(65)

print(myheap.heap)


myheap.remove()

print(myheap.heap)


myheap.remove()

print(myheap.heap)


"""
    EXPECTED OUTPUT:
    ----------------
    [95, 75, 80, 55, 60, 50, 65]
    [80, 75, 65, 55, 60, 50]
    [75, 60, 65, 55, 50]

"""

```

### `SOLUTION-Heap-Sink_Down.py`

```python
class MaxHeap:
    def __init__(self):
        self.heap = []

    def _left_child(self, index):
        return 2 * index + 1

    def _right_child(self, index):
        return 2 * index + 2

    def _parent(self, index):
        return (index - 1) // 2

    def _swap(self, index1, index2):
        self.heap[index1], self.heap[index2] = self.heap[index2], self.heap[index1]

    def insert(self, value):
        self.heap.append(value)
        current = len(self.heap) - 1

        while current > 0 and self.heap[current] > self.heap[self._parent(current)]:
            self._swap(current, self._parent(current))
            current = self._parent(current)


    def _sink_down(self, index):
        max_index = index
        while True:
            left_index = self._left_child(index)
            right_index = self._right_child(index)

            if (left_index < len(self.heap) and 
                    self.heap[left_index] > self.heap[max_index]):
                max_index = left_index

            if (right_index < len(self.heap) and 
                    self.heap[right_index] > self.heap[max_index]):
                max_index = right_index

            if max_index != index:
                self._swap(index, max_index)
                index = max_index
            else:
                return
                       
    def remove(self):
        if len(self.heap) == 0:
            return None

        if len(self.heap) == 1:
            return self.heap.pop()

        max_value = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._sink_down(0)

        return max_value



myheap = MaxHeap()
myheap.insert(95)
myheap.insert(75)
myheap.insert(80)
myheap.insert(55)
myheap.insert(60)
myheap.insert(50)
myheap.insert(65)

print(myheap.heap)


myheap.remove()

print(myheap.heap)


myheap.remove()

print(myheap.heap)


"""
    EXPECTED OUTPUT:
    ----------------
    [95, 75, 80, 55, 60, 50, 65]
    [80, 75, 65, 55, 60, 50]
    [75, 60, 65, 55, 50]

"""

```

---

## 8. Interview Files and Applications

The `Interview` folder contains `Heap-Maximum Element in a Stream.py` and `Heap-Kth Smallest Element in an Array.py`. Each provides `MaxHeap` and leaves a separate top-level function for the learner.

```
    STREAM MAX: insert each arrival, read the root
    1 -> 3 -> 2 -> 5 -> 4       roots: 1 -> 3 -> 3 -> 5 -> 5
    output: [1, 3, 3, 5, 5]
```

For the stream problem, insert every `nums[i]` and append `heap.heap[0]`. The tests cover empty, one-item, increasing, duplicate, and negative inputs; an empty input returns `[]`.

```
    KTH SMALLEST, k=2: keep only two values in a max-heap
    [3,2,1,5,6,4] -> add/remove as needed -> [2,1] -> root 2
```

For the kth-smallest problem, insert each number and remove the largest root whenever the heap exceeds `k`. The remaining root is the kth smallest; duplicates count as separate positions. The interview files are the problem statements, not additional core solution files.

---

## 9. Big O and Comparison with Lists

The height of a complete tree is `O(log n)`, so bubble-up and sink-down follow at most one logarithmic path.

| Operation | Heap | Unsorted list | Sorted list |
|:---|:---:|:---:|:---:|
| Peek maximum | **`O(1)`** | `O(n)` | `O(1)` |
| Insert | **`O(log n)`** | `O(1)` at end | `O(n)` |
| Remove maximum | **`O(log n)`** | `O(n)` | `O(1)` |
| Search arbitrary value | `O(n)` | `O(n)` | `O(log n)` |
| Space | `O(n)` | `O(n)` | `O(n)` |

```
    BUILDING AND SPECIAL QUERIES

    n repeated inserts: O(n log n)       bottom-up heapify: O(n)
    heap sort: O(n log n)                kth smallest, size k: O(n log k)
    stream maximum with this heap: O(n log n), heap space O(n)
```

Use a sorted list when full order or binary search matters. Use a heap when the next largest or smallest item is repeatedly needed without paying to keep every item sorted.

---

## 10. Checklist

```
    SHAPE: fill left to right       ORDER: max parent >= children
    INSERT: append, bubble up       REMOVE: move last, sink down
    BOUNDS: check children          ROOT: heap[0] is the maximum
```

Check empty and one-item removals before child access, choose the larger child during max-heap sink-down, and remember that a heap is partially ordered rather than a sorted list. The central pattern is **append then bubble up; replace the root then sink down**.
