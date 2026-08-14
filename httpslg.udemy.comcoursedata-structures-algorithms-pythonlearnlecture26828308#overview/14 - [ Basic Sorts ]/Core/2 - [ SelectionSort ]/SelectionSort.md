
---

# Selection Sort

## 1. What is Selection Sort?

**Selection Sort** is a comparison-based sorting algorithm that repeatedly selects the smallest value from the unsorted part of a list and places it at the next position in the sorted part. Instead of moving values every time it sees an inversion, it first completes a scan, remembers the location of the minimum, and then performs at most one swap.

### Key idea:
> Find the minimum in the unsorted region. Put that minimum at the left edge of the unsorted region. Repeat until no unsorted region remains.

### Core characteristics:
* **Comparison sort** - the algorithm learns order by comparing values.
* **In-place** - it rearranges the original list without an auxiliary list.
* **Sorted region grows from the LEFT** - each pass locks one minimum into its final position.
* **One swap at most per pass** - the scan can be long, but writes are deliberately limited.
* **Not adaptive** - even an already sorted list still receives the complete minimum scan for every suffix.

```
        +--------------------------------------------------+
        |                 SELECTION SORT                  |
        +--------------------------------------------------+
        |                                                  |
        |   Repeat for each position i:                    |
        |     1. Assume i is the minimum                   |
        |     2. Scan the rest of the list                 |
        |     3. Remember min_index                        |
        |     4. Swap into position i                      |
        |                                                  |
        |   [ sorted prefix | unsorted region ]             |
        |        grows ->        shrinks <-                |
        |                                                  |
        |   Result of each pass: one minimum is locked      |
        +--------------------------------------------------+
```

---

## 2. Why Was It Created?

Selection Sort was created around a simple trade-off: spend comparisons to avoid unnecessary writes. Bubble Sort can swap adjacent values many times while a large value travels through the list. Selection Sort scans first, waits until it knows the minimum, and moves that value directly to its destination.

This design matters when writing is more expensive than reading. The algorithm is still quadratic in time, so it is not a universal production solution, but its small write count makes the idea useful for understanding write-sensitive algorithms and constrained storage.

### The write budget:
* A pass performs many **comparisons** while scanning the suffix.
* A pass performs **zero or one swap** after the scan.
* The course code implements a swap with three assignments using `temp`.
* Across the whole run there are at most `n - 1` swaps, or at most `3(n - 1)` assignments from those swaps.

```
     BUBBLE SORT                         SELECTION SORT
     -------------                       ---------------
     compare -> swap                     compare -> remember
     compare -> swap                     compare -> remember
     compare -> swap                     compare -> remember
     ... many writes ...                 finish scan
                                           one direct swap

     Goal: move values gradually         Goal: choose first,
           with adjacent swaps                  write once
```

---

## 3. What Problems Does It Solve?

Selection Sort solves the basic problem of ordering a finite list in place while keeping data movement low. It is a reasonable teaching or small-input algorithm when predictable behavior and a tiny memory footprint matter more than speed.

### Useful situations:
* **Very small lists** where code simplicity is valuable.
* **Write-sensitive environments** where unnecessary writes should be avoided.
* **Teaching loop invariants**: after pass `i`, the first `i + 1` values are final.
* **Teaching minimum selection**: a scan can identify the next item without sorting the entire suffix.
* **Predictable work**: the number of comparisons does not depend on the input order.

### Problems it does not solve well:
* It does not become linear for an already sorted list.
* It does not exploit a nearly sorted input the way Insertion Sort does.
* It is much slower than `O(n log n)` algorithms on large lists.
* It is not stable in its usual in-place form.

```
        +--------------------------------------------------+
        |             WHERE SELECTION SORT FITS           |
        +--------------------------------------------------+
        |  Tiny input / simple implementation ....... YES  |
        |  Few writes required ...................... YES  |
        |  Predictable comparison count ............ YES  |
        |  Nearly sorted input ..................... NO   |
        |  Large random input ...................... NO   |
        |  Stable records must keep order .......... NO*  |
        +--------------------------------------------------+
        * The usual swap-based implementation is not stable.
```

---

## 4. How Does the `min_index` Scan Work?

The outer loop chooses the boundary `i`. Everything before `i` is already sorted and must not be touched again. The inner loop starts at `i + 1` and searches the remaining unsorted region.

### One pass, step by step:
1. Set `min_index = i`. The first unsorted value is the best minimum known so far.
2. Let `j` visit every later index from `i + 1` through the final index.
3. If `my_list[j] < my_list[min_index]`, update `min_index` to `j`.
4. After the scan, swap positions `i` and `min_index` only when they differ.
5. Increase `i`; the sorted prefix now contains one more final value.

```
     i                  j scans to the right
     |                  -------------------->
     v
     [ sorted | candidate |       unsorted       ]
                      ^
                 min_index starts here

     Every smaller value changes min_index,
     but the array does not change until the scan ends.
```

---

## 5. Pass-by-Pass Trace on `[4, 2, 6, 5, 1, 3]`

We trace the exact course algorithm. The list has six values, so the outer loop executes five passes: `i = 0, 1, 2, 3, 4`. Every pass scans its complete unsorted suffix, even if no swap is needed.

### PASS 1 - `i = 0`

Start with `min_index = 0`, value `4`.

```
     Start: [ 4 , 2 , 6 , 5 , 1 , 3 ]
              ^
          min_index = 0, value 4

     j=1: 2 < 4  -> min_index = 1
     j=2: 6 < 2  -> no change
     j=3: 5 < 2  -> no change
     j=4: 1 < 2  -> min_index = 4
     j=5: 3 < 1  -> no change

     Minimum found: value 1 at index 4
     Swap index 0 with index 4
```

After pass 1:

```
     [ 1 | 2 , 6 , 5 , 4 , 3 ]
       sorted prefix | unsorted region
       final value: 1
```

### PASS 2 - `i = 1`

`min_index` starts at index 1, where the value is already `2`.

```
     Current: [ 1 | 2 , 6 , 5 , 4 , 3 ]
                    ^
                min_index = 1

     j=2: 6 < 2  -> no change
     j=3: 5 < 2  -> no change
     j=4: 4 < 2  -> no change
     j=5: 3 < 2  -> no change

     Minimum found: value 2 at index 1
     i == min_index -> no swap
```

After pass 2:

```
     [ 1 , 2 | 6 , 5 , 4 , 3 ]
       sorted prefix | unsorted region
       final values: 1, 2
```

### PASS 3 - `i = 2`

The current value is `6`, but the smallest suffix value is `3`.

```
     Current: [ 1 , 2 | 6 , 5 , 4 , 3 ]
                         ^
                     min_index = 2, value 6

     j=3: 5 < 6  -> min_index = 3
     j=4: 4 < 5  -> min_index = 4
     j=5: 3 < 4  -> min_index = 5

     Minimum found: value 3 at index 5
     Swap index 2 with index 5
```

After pass 3:

```
     [ 1 , 2 , 3 | 5 , 4 , 6 ]
       sorted prefix | unsorted region
       final values: 1, 2, 3
```

### PASS 4 - `i = 3`

The suffix begins with `5`; the next value `4` becomes the new minimum.

```
     Current: [ 1 , 2 , 3 | 5 , 4 , 6 ]
                              ^
                          min_index = 3, value 5

     j=4: 4 < 5  -> min_index = 4
     j=5: 6 < 4  -> no change

     Minimum found: value 4 at index 4
     Swap index 3 with index 4
```

After pass 4:

```
     [ 1 , 2 , 3 , 4 | 5 , 6 ]
       sorted prefix | unsorted region
       final values: 1, 2, 3, 4
```

### PASS 5 - `i = 4`

Only two values remain. The value at index 4 is already the smaller one.

```
     Current: [ 1 , 2 , 3 , 4 | 5 , 6 ]
                                  ^
                              min_index = 4

     j=5: 6 < 5  -> no change
     Minimum found: value 5 at index 4
     i == min_index -> no swap
```

After pass 5:

```
     [ 1 , 2 , 3 , 4 , 5 | 6 ]
       sorted prefix      | last value

     Final: [ 1 , 2 , 3 , 4 , 5 , 6 ]
```

### All array states after every pass:

```
     Start:        [ 4 , 2 , 6 , 5 , 1 , 3 ]
     After pass 1: [ 1 | 2 , 6 , 5 , 4 , 3 ]
     After pass 2: [ 1 , 2 | 6 , 5 , 4 , 3 ]
     After pass 3: [ 1 , 2 , 3 | 5 , 4 , 6 ]
     After pass 4: [ 1 , 2 , 3 , 4 | 5 , 6 ]
     After pass 5: [ 1 , 2 , 3 , 4 , 5 | 6 ]
     Final:        [ 1 , 2 , 3 , 4 , 5 , 6 ]

     The bar moves one position to the right after each pass.
```

---

## 6. The Actual Course Code

This is the actual solution code from `SOLUTION-Selection_Sort.py`. The code below is reproduced verbatim, including its explicit temporary-variable swap and its output example.

```python
def selection_sort(my_list):
    for i in range(len(my_list)-1):
        min_index = i
        for j in range(i+1, len(my_list)):
            if my_list[j] < my_list[min_index]:
                min_index = j
        if i != min_index:
            temp = my_list[i]
            my_list[i] = my_list[min_index]
            my_list[min_index] = temp
    return my_list





print(selection_sort([4,2,6,5,1,3]))

 

"""
    EXPECTED OUTPUT:
    ----------------
    [1, 2, 3, 4, 5, 6]
 """

```

```
     EXECUTION FLOW
     --------------
     input list
          |
          v
     choose i and min_index
          |
          v
     scan j through suffix
          |
          v
     swap once, or skip
          |
          v
     return the same list object
```

### Expected output:

```
     [1, 2, 3, 4, 5, 6]
```

---

## 7. Line-by-Line Logic and Invariants

### The outer loop:
`range(len(my_list) - 1)` produces indices `0` through `n - 2`. There is no need to run a pass for the final index: once the first `n - 1` positions contain the smallest values in order, the last position is forced to contain the largest remaining value.

### The minimum candidate:
`min_index = i` is important. It says the first value in the suffix is the best candidate until evidence proves otherwise. The algorithm stores an index, not a copied minimum value, so it can swap directly with the value at the end of the scan.

### The inner loop:
`range(i + 1, len(my_list))` excludes the sorted prefix and checks every remaining candidate. It never changes the list while comparing; it only changes `min_index`.

### The strict comparison:
`my_list[j] < my_list[min_index]` updates the candidate only for a strictly smaller value. If values are equal, the earlier candidate stays selected. That reduces needless candidate changes, but it does not make the final algorithm stable because a distant swap can cross equal values.

### The guarded swap:
`if i != min_index` avoids a self-swap. If the current position already holds the smallest suffix value, the pass still costs comparisons but performs no writes.

```
     Before pass i:  [ sorted prefix | unsorted suffix ]
                       never touched       scan only

     During scan:    [ sorted prefix | same values      ]
                                        min_index moves

     After scan:     [ sorted prefix | minimum | rest   ]
                                      swap into i

     Invariant: every value left of i is final and sorted.
```

---

## 8. Big O Analysis

### Time, space, and stability table:

| Measure | Result | Explanation |
|:---|:---|:---|
| **Best time** | **`O(n^2)`** | A sorted list still scans every suffix; there is no early-exit test. |
| **Average time** | **`O(n^2)`** | The nested loops perform the same number of comparisons for any ordering. |
| **Worst time** | **`O(n^2)`** | A reverse list still needs every suffix scan and often a swap. |
| **Comparisons** | `n(n-1)/2` | `n-1` passes, then `n-2`, down to `1`. |
| **Best swaps** | `0` | Already sorted input keeps each `min_index` equal to `i`. |
| **Average swaps** | `O(n)` | At most one swap per pass; random data usually causes far fewer than `n` swaps. |
| **Worst swaps** | `n-1` | Every pass can select a different minimum. |
| **Space** | **`O(1)`** | In-place; only `i`, `j`, `min_index`, and `temp` are extra variables. |
| **Stability** | **No** | A long-distance swap can reverse equal values. |

### Comparison triangle for `n = 6`:

```
     Pass 1:  *  *  *  *  *        5 comparisons
     Pass 2:  *  *  *  *           4 comparisons
     Pass 3:  *  *  *              3 comparisons
     Pass 4:  *  *                 2 comparisons
     Pass 5:  *                    1 comparison
                               -------------------
                                15 total comparisons

     5 + 4 + 3 + 2 + 1 = 15 = n(n - 1) / 2
     The triangle remains full even when the input is sorted.
```

### Why best, average, and worst are all quadratic:
The outer loop always advances from the first index to the next-to-last index. For each `i`, the inner loop always visits the entire suffix. Input order changes which index is selected and whether a swap occurs, but it does not remove the scans.

---

## 9. Stability, Writes, and Comparison with Other Basic Sorts

### Why Selection Sort is not stable:
Imagine records with equal keys and identity labels. The first pass on the following list chooses `1` and swaps it with the first `2`:

```
     Before:  [ (2,A), (2,B), (1,X) ]
                         ^ minimum

     Swap index 0 and index 2:
     After:   [ (1,X), (2,B), (2,A) ]

     Equal keys changed order: A was before B, now B is before A.
     Therefore the usual selection-sort swap is NOT stable.
```

### Basic-sort comparison:

| Feature | Bubble Sort | Selection Sort | Insertion Sort |
|:---|:---|:---|:---|
| **Best time** | `O(n)` with early exit | `O(n^2)` | `O(n)` |
| **Average time** | `O(n^2)` | `O(n^2)` | `O(n^2)` |
| **Worst time** | `O(n^2)` | `O(n^2)` | `O(n^2)` |
| **Space** | `O(1)` | `O(1)` | `O(1)` |
| **Movement** | Many adjacent swaps | At most one swap per pass | Shifts larger values right |
| **Write count** | Can be `O(n^2)` | `O(n)` swaps | Can be `O(n^2)` |
| **Adaptive** | Yes with early exit | No | Yes |
| **Stable** | Yes | No | Yes |
| **Sorted region** | Right, largest values | Left, selected minima | Left, inserted values |

```
     +-------------------+-------------------+-------------------+
     |    BUBBLE SORT    |  SELECTION SORT   |  INSERTION SORT   |
     +-------------------+-------------------+-------------------+
     | many neighbor     | find MIN, then    | take next value   |
     | swaps              | ONE swap          | and shift right   |
     +-------------------+-------------------+-------------------+
     | adaptive possible  | fewest writes     | adaptive + stable |
     | stable             | but always scans  | excellent for     |
     |                    | the whole suffix  | nearly sorted data|
     +-------------------+-------------------+-------------------+
```

### Decision rule:
* Choose Selection Sort when minimizing swaps is the main educational or practical constraint and `n` is small.
* Choose Insertion Sort for streaming, online, nearly sorted, or stable data.
* Choose Bubble Sort mainly to learn adjacent swaps or to demonstrate a loop invariant.
* Choose an `O(n log n)` algorithm for large general-purpose datasets.

Selection Sort's lasting lesson is precise: comparisons can be plentiful while writes stay limited. The sorted-prefix invariant and the `min_index` scan are the foundation for understanding more advanced selection and partitioning techniques.

---

**Next Step:** Continue with **Insertion Sort**, which also grows a sorted prefix but inserts each new value by shifting larger values instead of selecting a minimum and swapping.
