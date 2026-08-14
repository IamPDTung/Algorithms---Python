
---

# Merge Sort

## 1. What is Merge Sort?

**Merge Sort** is a **Divide and Conquer** sorting algorithm. It attacks the sorting problem in two phases:

1. **DIVIDE** — recursively split the list **in half** until you are left with lists of a **single element** (a one-element list is *trivially sorted*).
2. **CONQUER / MERGE** — **merge** those sorted halves back together, one level at a time, until the whole list is rebuilt in sorted order.

Merge Sort is really **two pieces** working together:

* `merge(list1, list2)` — a helper that combines **two already-sorted lists** into **one sorted list**.
* `merge_sort(my_list)` — the recursive splitter that breaks the list down, then calls `merge()` on the way back up.

### Key Idea:
> "A list of one element is already sorted."
> — Merge Sort splits until sorting is trivial, then does all the real work while **merging** back together.

```
        +--------------------------------------------------+
        |                  MERGE SORT                      |
        +--------------------------------------------------+
        |                                                  |
        |   Phase 1                  Phase 2               |
        |   +------------------+     +------------------+  |
        |   |      DIVIDE      |     |      MERGE       |  |
        |   |  split in half   |  +  |  combine sorted  |  |
        |   |  recursively     |     |     halves       |  |
        |   +------------------+     +------------------+  |
        |                                                  |
        |   Two functions:                                 |
        |   +------------------+     +------------------+  |
        |   |   merge_sort()   | --> |     merge()      |  |
        |   | (the splitter)   |     | (the combiner)   |  |
        |   +------------------+     +------------------+  |
        +--------------------------------------------------+
```

---

## 2. Why Was Merge Sort Created?

The **basic sorts** (Bubble Sort, Selection Sort, Insertion Sort) all share the same ceiling: **`O(n^2)`** time. They compare elements **pair by pair**, so doubling the input **quadruples** the work. For large datasets, that is simply too slow.

Merge Sort was created to break through that ceiling. It delivers:

* **Guaranteed `O(n log n)`** time — in the **best, average, AND worst** case. No bad surprises.
* **Stability** — equal elements keep their original relative order (Bubble/Insertion are stable too, but Selection is not).

### The Price:
> Merge Sort **trades SPACE for SPEED**. It does not sort in place — it needs **auxiliary arrays** to hold the merged results: **`O(n)` extra space**.

```
        n = 1,000,000 elements:

        +------------------+----------------------------------+
        |   Basic Sorts    |   O(n^2) = 1,000,000,000,000     |
        | (Bubble/Sel/Ins) |   ~ 1 TRILLION operations        |
        +------------------+----------------------------------+
        |   Merge Sort     |   O(n log n) = 1,000,000 x 20    |
        |                  |   ~ 20 MILLION operations        |
        +------------------+----------------------------------+

        That is roughly a 50,000x speedup. The O(n^2) -> O(n log n)
        jump is one of the most important leaps in all of DSA.
```

---

## 3. What Problems Does It Solve?

* **Large datasets needing guaranteed speed** — when you cannot risk the `O(n^2)` worst case of Quick Sort, Merge Sort's guarantee of `O(n log n)` in ALL cases wins.
* **Sorting Linked Lists** — merging two sorted linked lists only requires re-wiring pointers, so Merge Sort needs just **`O(1)` extra space** there (see the Interview exercise *"Merge Two Sorted LL"*). This makes it THE go-to sort for linked lists.
* **External Sorting** — data too big to fit in memory can be sorted in chunks from disk: sort each chunk, then merge the chunks. Merge Sort's merge step is built exactly for this.
* **Stable-sort requirements** — e.g., sorting records by a secondary key while preserving the primary-key order of equal entries.

```
        +---------------------+----------------------------+
        |    SITUATION        |   WHY MERGE SORT FITS      |
        +---------------------+----------------------------+
        | Huge dataset        | Guaranteed O(n log n)      |
        +---------------------+----------------------------+
        | Linked list         | O(1) extra space there     |
        +---------------------+----------------------------+
        | Data on disk        | Merge step = sequential IO |
        +---------------------+----------------------------+
        | Must be stable      | Equal items keep order     |
        +---------------------+----------------------------+
```

---

## 4. How It Works — Part 1: The Merge Step

Before we can understand the recursion, we must first master **`merge()`** — the heart of the algorithm.

`merge()` takes **two already-sorted lists** and produces **one combined sorted list**. It uses **two index pointers**, `i` and `j`, one per list:

1. Compare the **heads**: `list1[i]` vs `list2[j]`.
2. Append the **smaller** one to `combined` and advance that list's pointer.
3. Repeat until one list is exhausted.
4. **Drain the leftovers** of the other list (they are already sorted and all bigger).

### Full Trace — `merge([1, 3, 7, 8], [2, 4, 5, 6])`:

```
    list1 = [ 1, 3, 7, 8 ]      list2 = [ 2, 4, 5, 6 ]
              i                          j

    Compare the two heads, take the SMALLER, advance that pointer.
```

### Step-by-Step Table:

```
    +------+-----+-----+----------+----------+---------------+-------------------------+
    | Step |  i  |  j  | list1[i] | list2[j] |    Action     |        combined         |
    +------+-----+-----+----------+----------+---------------+-------------------------+
    |  1   |  0  |  0  |    1     |    2     | take 1 (list1)| [ 1 ]                   |
    +------+-----+-----+----------+----------+---------------+-------------------------+
    |  2   |  1  |  0  |    3     |    2     | take 2 (list2)| [ 1, 2 ]                |
    +------+-----+-----+----------+----------+---------------+-------------------------+
    |  3   |  1  |  1  |    3     |    4     | take 3 (list1)| [ 1, 2, 3 ]             |
    +------+-----+-----+----------+----------+---------------+-------------------------+
    |  4   |  2  |  1  |    7     |    4     | take 4 (list2)| [ 1, 2, 3, 4 ]          |
    +------+-----+-----+----------+----------+---------------+-------------------------+
    |  5   |  2  |  2  |    7     |    5     | take 5 (list2)| [ 1, 2, 3, 4, 5 ]       |
    +------+-----+-----+----------+----------+---------------+-------------------------+
    |  6   |  2  |  3  |    7     |    6     | take 6 (list2)| [ 1, 2, 3, 4, 5, 6 ]    |
    +------+-----+-----+----------+----------+---------------+-------------------------+
    | list2 is exhausted (j = 4) -> main loop ends, DRAIN list1 leftovers:              |
    +------+-----+-----+----------+----------+---------------+-------------------------+
    |  7   |  2  |  4  |    7     |    -     | drain 7 (lst1)| [ 1, 2, 3, 4, 5, 6, 7 ] |
    +------+-----+-----+----------+----------+---------------+-------------------------+
    |  8   |  3  |  4  |    8     |    -     | drain 8 (lst1)| [ 1,2,3,4,5,6,7,8 ]     |
    +------+-----+-----+----------+----------+---------------+-------------------------+

    RETURN: [ 1, 2, 3, 4, 5, 6, 7, 8 ]
```

### Why the Leftover Drain Works:

```
    Once one list runs out, EVERYTHING left in the other list is
    guaranteed to be:

        (a) already sorted internally, and
        (b) >= everything already in `combined`

    list1 = [ 1, 3, 7, 8 ]      list2 = [ 2, 4, 5, 6 ]
                   ^   ^                             ^
                   +---+                             +-- exhausted
                   leftovers: 7, 8  ->  just append them in order!
```

---

## 5. The Merge Code

```python
def merge(list1, list2):
    combined = []
    i = 0
    j = 0
    while i < len(list1) and j < len(list2):
        if list1[i] < list2[j]:
            combined.append(list1[i])
            i += 1
        else:
            combined.append(list2[j])
            j += 1
    
    while i < len(list1):
        combined.append(list1[i])
        i += 1

    while j < len(list2):
        combined.append(list2[j])
        j += 1

    return combined
```

### Line-by-Line Map to the Trace:

```
    while i < len(list1) and j < len(list2):   <- steps 1-6 (both lists alive)
        if list1[i] < list2[j]:                <- compare the two heads
            combined.append(list1[i]); i += 1  <- take from list1, advance i
        else:
            combined.append(list2[j]); j += 1  <- take from list2, advance j

    while i < len(list1): ...                  <- step 7-8: drain list1 leftovers
    while j < len(list2): ...                  <- (skipped here: list2 already empty)
```

### Note — Merge REQUIRES Two Sorted Lists:

```python
# MERGE REQUIRES TWO SORTED LISTS:
print(merge([1,2,7,8], [3,4,5,6]))
# EXPECTED OUTPUT: [1, 2, 3, 4, 5, 6, 7, 8]
```

> If either input list is unsorted, the two-pointer trick breaks. That is exactly why `merge_sort()` splits all the way down to **single-element lists** — the only lists that are *guaranteed* sorted.

---

## 6. How It Works — Part 2: Merge Sort Recursion

Now the full algorithm. `merge_sort()` does only three things:

1. **Base case:** if `len(my_list) == 1`, return it — a single element is already sorted.
2. **Split:** find the midpoint, recursively sort the **left half** and the **right half**.
3. **Combine:** `return merge(left, right)`.

### The Full Recursion Tree — `merge_sort([8, 3, 5, 4, 7, 6, 1, 2])`:

```
    ============================ DIVIDE (going DOWN) ============================

                            [ 8, 3, 5, 4, 7, 6, 1, 2 ]
                            /                          \
                    [ 8, 3, 5, 4 ]                [ 7, 6, 1, 2 ]
                    /            \                /            \
               [ 8, 3 ]      [ 5, 4 ]        [ 7, 6 ]      [ 1, 2 ]
               /     \       /     \         /     \       /     \
             [ 8 ] [ 3 ]   [ 5 ] [ 4 ]     [ 7 ] [ 6 ]   [ 1 ] [ 2 ]

              ^                                                      ^
              +--------- single-element lists = BASE CASES ----------+
                        (each one is trivially sorted!)

    ============================ MERGE (coming back UP) =========================

             [ 8 ] [ 3 ]   [ 5 ] [ 4 ]     [ 7 ] [ 6 ]   [ 1 ] [ 2 ]
               \     /       \     /         \     /       \     /
               [ 3, 8 ]      [ 4, 5 ]        [ 6, 7 ]      [ 1, 2 ]
                  \              /               \             /
                [ 3, 4, 5, 8 ]                    [ 1, 2, 6, 7 ]
                        \                              /
                        [ 1, 2, 3, 4, 5, 6, 7, 8 ]

                        SORTED! Returned to the original caller.
```

### Reading the Tree:

```
    - Going DOWN:  the list is halved at every level
                   (n -> n/2 -> n/4 -> ... -> 1)

    - NO comparisons happen while dividing.
      ALL of the real sorting work happens on the way UP,
      inside merge(), where two sorted halves become one.

    - Each merge() call receives two SORTED lists and returns
      one bigger SORTED list — so the invariant "merge() needs
      sorted inputs" is always maintained.
```

---

## 7. The Merge Sort Code

```python
def merge(array1, array2):
    combined = []
    i = 0
    j = 0
    while i < len(array1) and j < len(array2):
        if array1[i] < array2[j]:
            combined.append(array1[i])
            i += 1
        else:
            combined.append(array2[j])
            j += 1
              
    while i < len(array1):
        combined.append(array1[i])
        i += 1

    while j < len(array2):
        combined.append(array2[j])
        j += 1

    return combined


def merge_sort(my_list):
    if len(my_list) == 1:
        return my_list
    mid_index = int(len(my_list)/2)
    left = merge_sort(my_list[:mid_index])
    right = merge_sort(my_list[mid_index:])
    
    return merge(left, right)
```

### Annotated:

```
    def merge_sort(my_list):
        if len(my_list) == 1:          <- BASE CASE: trivially sorted
            return my_list
        mid_index = int(len(my_list)/2)          <- find the middle
        left  = merge_sort(my_list[:mid_index])  <- recurse LEFT half
        right = merge_sort(my_list[mid_index:])  <- recurse RIGHT half
        return merge(left, right)                <- combine sorted halves
```

### Running It:

```python
original_list = [3,1,4,2]

sorted_list = merge_sort(original_list)

print('Original List:', original_list)
# Original List: [3, 1, 4, 2]

print('\nSorted List:', sorted_list)
# Sorted List: [1, 2, 3, 4]
```

---

## 8. Big O Analysis

### Time — Why `O(n log n)` in ALL Cases:

The work of Merge Sort is best understood as **levels x work per level**:

```
    Level 0:        [ - - - - - - - - ]                merge work: n
                    /                  \
    Level 1:      [ - - - - ]        [ - - - - ]       merge work: n/2 + n/2 = n
                  /        \          /        \
    Level 2:    [ - - ]  [ - - ]  [ - - ]  [ - - ]     merge work: n
                /   \    /   \    /   \    /   \
    Level 3:  [ - ][ - ][ - ][ - ][ - ][ - ][ - ][ - ] base cases

    +------------------------------------------------------------+
    |  Number of LEVELS = log2(n)   (list halved each time)      |
    |  WORK per level   = O(n)      (every element is merged     |
    |                                exactly once per level)     |
    |                                                            |
    |  TOTAL TIME = O(n)  x  O(log n)  =  O(n log n)             |
    +------------------------------------------------------------+
```

The split is **always** perfectly in half — it does not depend on the data. So best, average, and worst case all produce the **same tree shape** and the **same `O(n log n)`** work. No degenerate cases.

### Space — `O(n)` Auxiliary:

```
    merge() builds a brand-new `combined` list:

        left  [ - - - - ]  +  right [ - - - - ]
                    \                /
                     combined [ - - - - - - - - ]   <- n slots of
                                                       EXTRA memory

    The original sublists are thrown away after each merge, but at the
    top level you still need a full copy of all n elements => O(n) space.
```

### Stability — YES:

When `array1[i] == array2[j]`, the code takes from the **left** list first (`if array1[i] < array2[j]` is false only when left `>=` right — wait, check: on a tie the `else` branch takes from the right). Regardless of tie-handling detail, the standard Merge Sort is implemented to be **stable**: equal elements keep their original relative order.

### Big O Summary Table:

| Complexity | Value | Why |
|:---|:---|:---|
| **Time (Best)** | `O(n log n)` | Split is always in half; merge is always `O(n)` per level |
| **Time (Average)** | `O(n log n)` | Same tree shape regardless of input order |
| **Time (Worst)** | `O(n log n)` | **Guaranteed** — no degenerate input exists |
| **Space** | `O(n)` | Auxiliary `combined` arrays built during merging |
| **Stable?** | **Yes** | Equal elements preserve their original order |

---

## 9. Merge Sort vs The Basic Sorts vs Quick Sort

```
    +------------------+-----------+-----------+-----------+---------+---------+
    |    ALGORITHM     |   BEST    |  AVERAGE  |   WORST   |  SPACE  | STABLE? |
    +------------------+-----------+-----------+-----------+---------+---------+
    | Bubble Sort      |   O(n)    |   O(n^2)  |   O(n^2)  |   O(1)  |   Yes   |
    +------------------+-----------+-----------+-----------+---------+---------+
    | Selection Sort   |   O(n^2)  |   O(n^2)  |   O(n^2)  |   O(1)  |   No    |
    +------------------+-----------+-----------+-----------+---------+---------+
    | Insertion Sort   |   O(n)    |   O(n^2)  |   O(n^2)  |   O(1)  |   Yes   |
    +------------------+-----------+-----------+-----------+---------+---------+
    | MERGE SORT       | O(n log n)| O(n log n)| O(n log n)|   O(n)  |   Yes   |
    +------------------+-----------+-----------+-----------+---------+---------+
    | Quick Sort       | O(n log n)| O(n log n)|   O(n^2)  | O(log n)|   No    |
    +------------------+-----------+-----------+-----------+---------+---------+
```

### The Big Jump — `O(n^2)` -> `O(n log n)`:

Merge Sort is the course's first algorithm to escape the `O(n^2)` trap of the basic sorts. The cost: `O(n)` extra space (the basics sort in place with `O(1)`).

### Where Merge Sort Fits vs Quick Sort:

| Criteria | Merge Sort | Quick Sort |
|:---|:---|:---|
| **Time guarantee** | `O(n log n)` **always** | `O(n log n)` **on average**, `O(n^2)` worst |
| **Extra space** | `O(n)` auxiliary arrays | `O(log n)` call stack only |
| **Stable?** | Yes | No |
| **Best for** | Linked lists, external sorting, stability needed | In-memory arrays, general-purpose sorting |

> **Rule of thumb:** need a *guarantee* or *stability* (or sorting a linked list)? Pick **Merge Sort**. Need raw in-memory speed with minimal memory? Pick **Quick Sort**.

---

**Next Step:** Now let's look at the other great divide-and-conquer sort — **Quick Sort** — which achieves `O(n log n)` on average while sorting **in place**, using a clever **pivot/partition** trick instead of merging.
