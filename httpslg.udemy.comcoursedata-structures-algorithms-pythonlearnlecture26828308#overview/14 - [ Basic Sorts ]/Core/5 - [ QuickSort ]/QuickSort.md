
---

# Quick Sort

## 1. What is Quick Sort?

**Quick Sort** is an **in-place, divide-and-conquer sorting algorithm**. Instead of repeatedly selecting the smallest item or shifting every item one position, it chooses a **pivot**, rearranges the array around that pivot, and recursively sorts the two sides.

The algorithm has two essential pieces:

* `pivot(my_list, pivot_index, end_index)` — partitions one range so that the pivot lands in its final sorted position.
* `quick_sort_helper(my_list, left, right)` — recursively applies that partitioning process to the range on the left and the range on the right.

The key promise after partitioning is:

> Every value to the left of the pivot is smaller than the pivot, and every value to the right is greater than or equal to it.

The two sides are not necessarily sorted yet. They are only isolated into smaller independent problems. That is enough for recursion to finish the work.

```
        +--------------------------------------------------+
        |                    QUICK SORT                   |
        +--------------------------------------------------+
        |                                                  |
        |   1. CHOOSE A PIVOT                              |
        |          |                                       |
        |          v                                       |
        |   2. PARTITION: smaller | pivot | larger        |
        |          |                  |                    |
        |          +----------+-------+                    |
        |                     |                            |
        |        recursively sort both sides               |
        |                                                  |
        |   pivot()  ---------------->  quick_sort_helper() |
        +--------------------------------------------------+
```

---

## 2. Why Was Quick Sort Created?

The basic sorts in the course — Bubble Sort, Selection Sort, and Insertion Sort — can require **`O(n^2)`** comparisons and moves. Merge Sort breaks that time barrier with `O(n log n)`, but its usual array implementation creates auxiliary arrays and therefore uses `O(n)` extra space.

Quick Sort was created as a fast alternative for **in-memory arrays**:

* It keeps the useful `O(n log n)` average running time.
* It partitions **in place**, so it does not need a second array containing all `n` values.
* Its swaps and sequential scans often have good **cache locality**: nearby array positions are accessed while the partition is scanned.
* It uses the call stack for recursion rather than allocating a full merge buffer.

This is a trade-off, not a universal improvement. A poor pivot can still produce `O(n^2)`, and the simple implementation shown here is not stable.

```
    BASIC SORTS                         QUICK SORT
    +------------------+                +-------------------------+
    | compare many     |                | choose pivot             |
    | pairs repeatedly  |                | scan one contiguous range|
    | O(n^2)            |       --->     | swap in the same array   |
    +------------------+                | average O(n log n)      |
                                        +-------------------------+

```

---

## 3. What Problems Does Quick Sort Solve?

Quick Sort is a strong choice when the data is an array or list already in memory and the program wants speed without allocating another `O(n)` array.

It addresses several practical problems:

* **Large in-memory arrays** — the average time is much better than quadratic basic sorts.
* **Limited auxiliary memory** — partitioning rearranges the existing list instead of constructing a merged output list.
* **Contiguous data access** — each partition scans a bounded array range from left to right, which is friendly to CPU caches.
* **Recursive decomposition** — after a pivot is fixed, the left and right ranges can be solved independently.

It does not solve every sorting requirement:

* It does not guarantee `O(n log n)` when the pivot choices are consistently poor.
* Arbitrary swaps can change the relative order of equal values, so this implementation is not stable.
* Deeply unbalanced recursion can consume `O(n)` stack space.

```
        +--------------------------+-----------------------------+
        | PROBLEM                  | QUICK SORT'S RESPONSE       |
        +--------------------------+-----------------------------+
        | Too many O(n^2) moves    | Average O(n log n)         |
        +--------------------------+-----------------------------+
        | Extra array is expensive | Swap inside original list  |
        +--------------------------+-----------------------------+
        | Data is in memory        | Scan contiguous ranges      |
        +--------------------------+-----------------------------+
        | One problem is too large | Split around a pivot       |
        +--------------------------+-----------------------------+
        | Need guaranteed bound    | Use another strategy or    |
        |                          | improve pivot selection    |
        +--------------------------+-----------------------------+
```

---

## 4. Divide and Conquer

Quick Sort follows the three-part **divide-and-conquer** pattern:

1. **Divide:** choose a pivot and partition the current range around it.
2. **Conquer:** recursively sort the range before the pivot and the range after it.
3. **Combine:** no separate merge is necessary. Once both recursive calls return, the whole range is sorted because the pivot is already in its final position.

Suppose the first pivot is `4` in `[4,6,1,7,3,2,5]`. Partitioning produces:

```
    BEFORE:       [ 4, 6, 1, 7, 3, 2, 5 ]
                   ^
                 pivot = 4

    AFTER ONE PARTITION:
                  [ 2, 1, 3 | 4 | 6, 7, 5 ]
                    smaller   ^   greater/equal
                              final position

    The bars do NOT mean both sides are sorted.
    They mean no value on the left belongs after 4,
    and no value on the right belongs before 4.

    RECURSIVE PROBLEMS:
                  sort [ 2, 1, 3 ] and sort [ 6, 7, 5 ]
```

The base case is a range with zero or one element. In the source code, `left < right` is the recursive guard. A one-element range needs no work, and an empty range is also already sorted.

---

## 5. Pivot and Partition in Detail

The supplied implementation always starts with `pivot_index` as the pivot position. For the first call, that means the **first element** is the pivot. The value at that position is read repeatedly through `my_list[pivot_index]` while the scan proceeds.

`swap_index` has a precise meaning:

* It begins at `pivot_index`.
* It marks the end of the region containing values smaller than the pivot.
* When `my_list[i] < my_list[pivot_index]`, increment `swap_index` and swap the newly discovered smaller value into that boundary.
* At the end, swap the pivot with `my_list[swap_index]`.

```
    pivot_index                         end_index
         |                                  |
         v                                  v
    [ pivot ][ smaller ][ unknown ... ][ remaining ]
       4          < 4          ?              ?
                    ^             ^
              swap_index          i scans right

    After final swap:

    [ all values < 4 ][ 4 ][ all values >= 4 ]
```

The comparison is strict: `<`, not `<=`. Therefore values equal to the pivot remain on the right side. That is valid for correctness, but it also contributes to poor balance when many values are equal.

`i` asks, “What value have I not classified yet?” `swap_index` asks, “Where is the next slot for a value smaller than the pivot?” A value can be found far to the right and moved left into that next slot, while the scan continues from `i + 1`.

---

## 6. Full Partition Trace

Trace `pivot(my_list, 0, 6)` on:

```python
[4,6,1,7,3,2,5]
```

The pivot is the value at index `0`, so `pivot = 4`. Initially `swap_index = 0`, and `i` scans indices `1` through `6`.

### Every scan and every swap

```
    Initial: pivot = 4, pivot_index = 0, swap_index = 0
             [ 4, 6, 1, 7, 3, 2, 5 ]
               P  i
```

| Step | `i` | `my_list[i]` | `pivot` | `swap_index` (before -> after) | Action | Array after action |
|:---:|---:|---:|---:|---:|:---|:---|
| 1 | 1 | 6 | 4 | `0 -> 0` | `6 < 4` is false; no swap | `[4, 6, 1, 7, 3, 2, 5]` |
| 2 | 2 | 1 | 4 | `0 -> 1` | swap indices 1 and 2 | `[4, 1, 6, 7, 3, 2, 5]` |
| 3 | 3 | 7 | 4 | `1 -> 1` | `7 < 4` is false; no swap | `[4, 1, 6, 7, 3, 2, 5]` |
| 4 | 4 | 3 | 4 | `1 -> 2` | swap indices 2 and 4 | `[4, 1, 3, 7, 6, 2, 5]` |
| 5 | 5 | 2 | 4 | `2 -> 3` | swap indices 3 and 5 | `[4, 1, 3, 2, 6, 7, 5]` |
| 6 | 6 | 5 | 4 | `3 -> 3` | `5 < 4` is false; no swap | `[4, 1, 3, 2, 6, 7, 5]` |
| 7 | final | pivot `4` | 4 | `3 -> 3` | swap indices 0 and 3 | `[2, 1, 3, 4, 6, 7, 5]` |

At return, indices `0..2` contain values smaller than `4`, and indices `4..6` contain values greater than or equal to `4`. The right side is `[6,7,5]`, so it still needs a recursive call.

---

## 7. The Recursive Quick Sort Tree

After the first partition, the original problem becomes two smaller ranges. The source sorts the left range first, then the right range.

```
    quick_sort([4, 6, 1, 7, 3, 2, 5])
    pivot = 4, returned index 3
    /                                      \
   /                                        \
  sort [2, 1, 3]                         sort [6, 7, 5]
       pivot = 2                              pivot = 6
       index = 1                              index = 5
       /          \                           /          \
  sort [1]      sort [3]                 sort [5]      sort [7]
   base          base                     base          base

    final array: [1, 2, 3, 4, 5, 6, 7]
```

There is no explicit concatenation step. The recursive calls mutate the same list, and the already-fixed pivots remain between their sorted sides.

---

## 8. The Quick Sort Code

The code is split into a reusable swap, a partition function, a recursive helper, and a public wrapper:

```
    quick_sort(my_list)
          |
          v
    helper(0, len(my_list)-1)
       |       \
    pivot()   helper(left) + helper(right)
       |
    swap() while scanning
```

### The pivot source, verbatim

```python
def swap(my_list, index1, index2):
    temp = my_list[index1]
    my_list[index1] = my_list[index2]
    my_list[index2] = temp


def pivot(my_list, pivot_index, end_index):
    swap_index = pivot_index

    for i in range(pivot_index+1, end_index+1):
        if my_list[i] < my_list[pivot_index]:
            swap_index += 1
            swap(my_list, swap_index, i)
    swap(my_list, pivot_index, swap_index)
    return swap_index




my_list = [4,6,1,7,3,2,5]

print('List before running pivot():')
print(my_list)

returned_pivot_index = pivot(my_list, 0, 6)

print('\nList after running pivot():')
print(my_list)

print('\nPivot Index:')
print(returned_pivot_index)



"""
    EXPECTED OUTPUT:
    ----------------
    List before running pivot():
    [4, 6, 1, 7, 3, 2, 5]

    List after running pivot():
    [2, 1, 3, 4, 6, 7, 5]

    Pivot Index:
    3

 """
```

### The full Quick Sort source, verbatim

```python
def swap(my_list, index1, index2):
    temp = my_list[index1]
    my_list[index1] = my_list[index2]
    my_list[index2] = temp


def pivot(my_list, pivot_index, end_index):
    swap_index = pivot_index

    for i in range(pivot_index+1, end_index+1):
        if my_list[i] < my_list[pivot_index]:
            swap_index += 1
            swap(my_list, swap_index, i)
    swap(my_list, pivot_index, swap_index)
    return swap_index


def quick_sort_helper(my_list, left, right):
    if left < right:
        pivot_index = pivot(my_list, left, right)
        quick_sort_helper(my_list, left, pivot_index-1)  
        quick_sort_helper(my_list, pivot_index+1, right)       
    return my_list
    

def quick_sort(my_list):
    quick_sort_helper(my_list, 0, len(my_list)-1)

 
 


my_list = [4,6,1,7,3,2,5]

quick_sort(my_list)

print(my_list)



"""
    EXPECTED OUTPUT:
    ----------------
    [1, 2, 3, 4, 5, 6, 7]
 """
```

---

## 9. Best, Average, and Worst Behavior

The partition scan costs `O(n)` for a range of size `n`. The total time depends on how evenly the pivot divides the range.

### Best case: balanced partitions

If each pivot divides the range into two nearly equal pieces, the recursion has about `log n` levels. Each level scans a total of about `n` elements.

### Average case: usually useful splits

With varied input and representative pivots, partitions are often reasonably balanced, so the expected total remains `O(n log n)`.

### Worst case: one-sided partitions

If every pivot is the smallest or largest value in its range, one recursive side has size zero and the other has size `n - 1`.

```
    n
    |
    n-1       scan n-1 values
    |
    n-2       scan n-2 values
    |
    n-3       scan n-3 values
    |
    ...
    1

    work = n + (n-1) + (n-2) + ... + 1
         = n(n+1)/2
         = O(n^2)
```

The algorithm is therefore fast on average, not guaranteed fast for every input and pivot policy.

| Case | Partition shape | Recurrence | Time |
|:---|:---|:---|:---|
| **Best** | Two equal halves | `T(n) = 2T(n/2) + O(n)` | **`O(n log n)`** |
| **Average** | Generally reasonable splits | Expected balanced behavior | **`O(n log n)`** |
| **Worst** | `0` and `n-1` every time | `T(n) = T(n-1) + O(n)` | **`O(n^2)`** |

---

## 10. Already Sorted Input with the First Pivot

The supplied code chooses the first item of each range. That choice degenerates immediately on an already sorted list such as `[1,2,3,4,5,6,7]`.

For the first call, pivot `1` is smaller than every remaining value. The condition `my_list[i] < 1` is never true, so `swap_index` remains `0`. The final swap exchanges index `0` with itself, and recursion receives the ranges `[]` and `[2,3,4,5,6,7]`.

```
    [1, 2, 3, 4, 5, 6, 7]
     ^
    pivot = 1, no value is smaller

    [1] | [2, 3, 4, 5, 6, 7]
     ^                  ^
     fixed              recurse on n-1 values

    [1] | [2] | [3, 4, 5, 6, 7]
    [1] | [2] | [3] | [4, 5, 6, 7]
    [1] | [2] | [3] | [4] | ...

    The tree is a chain, not a balanced tree.
```

---

## 11. Big O, Space, Locality, and Stability

### Time and auxiliary space

Quick Sort's partitioning is in place: `swap()` changes positions in the original list, and no `combined` list is allocated. The recursion stack is separate from the array storage.

```
    ARRAY (reused): [ 2 | 1 | 3 | 4 | 6 | 7 | 5 ]
                         < pivot | pivot | >= pivot

    STACK: helper(...) -> helper(...) -> ...
    Balanced tree: O(log n) frames; chain: O(n) frames
```

| Property | Best | Average | Worst |
|:---|:---:|:---:|:---:|
| **Time** | `O(n log n)` | `O(n log n)` | `O(n^2)` |
| **Partition work** | `O(n)` per level | `O(n)` per level | `O(n)` per shrinking level |
| **Auxiliary array space** | `O(1)` | `O(1)` | `O(1)` |
| **Recursion stack** | `O(log n)` | `O(log n)` expected | `O(n)` |
| **Stable?** | No | No | No |

### Cache locality

An array is contiguous storage. During a partition, `i` advances through a contiguous range, and the values moved by `swap()` are still inside that range. This pattern often uses CPU cache lines well compared with algorithms that repeatedly allocate and traverse separate structures.

Cache locality is a practical performance reason, not a replacement for asymptotic analysis. A bad pivot still creates quadratic work even when each scan is cache-friendly.

### Stability

The swaps do not preserve the relative order of equal keys. If records have equal sort keys and their original order matters, use a stable algorithm or add an original-position tie breaker.

---

## 12. Merge Sort vs Quick Sort

Both algorithms use divide and conquer and average `O(n log n)` time, but they make opposite choices about memory and guarantees.

| Criteria | Merge Sort | Quick Sort |
|:---|:---|:---|
| **Best time** | `O(n log n)` | `O(n log n)` |
| **Average time** | `O(n log n)` | `O(n log n)` |
| **Worst time** | `O(n log n)` | `O(n^2)` with poor pivots |
| **Array auxiliary space** | `O(n)` | `O(1)` apart from stack |
| **Average stack space** | `O(log n)` | `O(log n)` |
| **Stable** | Yes, with stable merge handling | No in this implementation |
| **Data movement** | Copies into result arrays | Swaps inside the input |
| **Strong use case** | Stability, linked lists, external sorting, guarantees | In-memory arrays, low auxiliary memory, practical speed |

### Which one should be chosen?

Choose Merge Sort when stability, predictable worst-case time, linked-list structure, or external data is the priority. Choose Quick Sort when the data is in memory, auxiliary allocation matters, and average-case speed is valuable.

```
    GUARANTEE OR STABILITY?  --yes-->  MERGE SORT
              |
             no
              v
    LOW ARRAY AUXILIARY SPACE? --yes--> QUICK SORT
              |
             no -----> choose from the data and constraints
```

Neither name alone determines performance. Pivot policy, data shape, comparison cost, memory hierarchy, and recursion safeguards all matter in a real implementation.

---

## 13. Quick Sort Mental Model

The shortest reliable way to remember this implementation is:

1. Pick the first value in the current range as the pivot.
2. Scan with `i`.
3. Move `swap_index` only when a value smaller than the pivot is found.
4. Put the pivot between the smaller and greater-or-equal regions.
5. Recursively repeat on the two ranges that exclude the fixed pivot.

```
    scan                         place pivot                 recurse
    [ P | unknown ... ]  --->  [ smaller | P | >= P ]  --->  left + right
       i ->                              ^                    /       \
                                  final position          solve     solve

    Balanced partitions give average O(n log n).
    Repeated first-item extremes give worst O(n^2).
```

Quick Sort's main achievement is not that it avoids all work. It makes one linear partition pass, fixes one element permanently, and reuses the original storage while recursion reduces the remaining problem.

---

**Next Step:** Compare this partition trace with Merge Sort's merge trace. Merge Sort combines two sorted lists using extra space; Quick Sort places a pivot using swaps and then sorts the two remaining ranges.
