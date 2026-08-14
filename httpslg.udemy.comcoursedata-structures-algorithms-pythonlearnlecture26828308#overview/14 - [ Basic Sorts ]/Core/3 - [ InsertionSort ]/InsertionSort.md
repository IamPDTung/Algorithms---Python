
---

# Insertion Sort

## 1. What is Insertion Sort?

**Insertion Sort** is a comparison-based sorting algorithm that builds a sorted prefix from left to right. On each pass it takes the next value, temporarily holds it as `temp`, shifts every larger value in the sorted prefix one position to the right, and places `temp` into the gap.

### Key idea:
> Keep the left side sorted. Take one new value from the right side and insert it into the correct position in the sorted side.

### Core characteristics:
* **Comparison sort** - order is discovered by comparing the current value with earlier values.
* **In-place** - it uses the original list and constant extra variables.
* **Adaptive** - it does very little work when the input is already or nearly sorted.
* **Online** - it can keep a prefix sorted while values arrive one at a time.
* **Stable** - equal values are not moved past one another when the comparison is strict.
* **Sorted region grows from the LEFT** - each pass extends the sorted prefix by one item.

```
        +--------------------------------------------------+
        |                 INSERTION SORT                  |
        +--------------------------------------------------+
        |                                                  |
        |   [ sorted prefix | current | unsorted suffix ]  |
        |          ^            ^                          |
        |       keep sorted    temp                        |
        |                                                  |
        |   Shift larger prefix values right               |
        |   Insert temp into the opened position            |
        |                                                  |
        |   sorted prefix grows ->                         |
        +--------------------------------------------------+
```

---

## 2. The Playing-Card Analogy

Insertion Sort behaves like a person arranging playing cards in their hand. The cards already held are sorted. When a new card arrives, the player compares it with cards from right to left, moves larger cards one slot to the right, and inserts the new card into the gap.

```
     Cards already in hand:  [ 2 , 4 , 6 ]   sorted
     New card:                         5    temp

     Compare 5 with 6: move 6 right
     Hand:                    [ 2 , 4 , 6 , 6 ]

     Compare 5 with 4: stop; 4 is not larger
     Insert 5 after 4:
     Hand:                    [ 2 , 4 , 5 , 6 ]
```

The analogy explains why the algorithm scans backward: the correct insertion position is found by moving left through the already ordered hand, not by searching the unsorted suffix.

---

## 3. Why Was It Created?

Insertion Sort was created to solve a different set of constraints from Selection Sort. It does not try to minimize the number of comparisons on every input. Instead, it makes the amount of work depend on how far each value is from its correct location.

### The three central motivations:
1. **Adaptive behavior** - nearly sorted input should require only a few shifts.
2. **Online behavior** - a sorted result can be maintained as values arrive incrementally.
3. **Stability** - records with equal keys should preserve their original order.

It is also simple, in-place, and practical for small lists. Many production sorting implementations use an insertion-sort strategy for small partitions because its constant factors are low even though its asymptotic worst case is quadratic.

```
     INPUT CONDITION       INSERTION SORT RESPONSE
     ----------------       ----------------------
     already sorted         compare, shift nothing
     nearly sorted          a few short shifts
     values arriving         insert each new value now
     equal-key records       keep their original order
     reverse sorted          many shifts, O(n^2)
```

---

## 4. What Problems Does It Solve?

Insertion Sort is especially useful when the input is small, arrives over time, or is close to sorted order. It solves the problem of extending an ordered collection without needing a second collection.

### Useful situations:
* **Nearly sorted arrays** with a small number of inversions.
* **Online streams** where each new value should be placed immediately.
* **Stable sorting of records** where equal keys carry meaningful identity.
* **Small subarrays** inside more advanced hybrid sorting algorithms.
* **In-place sorting** when `O(1)` auxiliary space is required.

### Limitations:
* A reverse-sorted input causes a shift for every earlier value on every pass.
* It is not the best choice for a large random array.
* It still uses `O(n^2)` time on average.
* It does not provide the `O(n log n)` worst-case guarantee of Merge Sort or Heap Sort.

```
        +--------------------------------------------------+
        |             WHERE INSERTION SORT FITS           |
        +--------------------------------------------------+
        |  Small input .............................. YES  |
        |  Nearly sorted input ..................... YES  |
        |  Values arrive online .................... YES  |
        |  Equal records must preserve order ........ YES  |
        |  Large random input ...................... NO   |
        |  Reverse-sorted input .................... SLOW |
        +--------------------------------------------------+
```

---

## 5. The Sorted-Prefix Invariant

The most important invariant is:

> Before pass `i`, the slice `my_list[0:i]` is sorted. After pass `i`, the slice `my_list[0:i+1]` is sorted and contains exactly the same values as before the pass.

The item at index `i` is the next value to insert. The values before it are already sorted, and the values after it remain an unsorted suffix.

```
     Before pass i:
     [ sorted prefix of length i | value to insert | unsorted suffix ]
       <--------- invariant ------>       temp

     During pass:
     [ sorted prefix | shifted values | open gap | unsorted suffix ]
                         larger -> right

     After pass i:
     [ sorted prefix of length i+1 | unsorted suffix ]
       <----------- invariant restored ------------>
```

### Why shifting preserves correctness:
The prefix begins sorted. Moving a larger value one position right does not disturb the order among the values that remain to its left. Once the first value that is not larger than `temp` is reached, `temp` belongs immediately after it. If every prefix value is larger, `temp` belongs at index `0`.

### Boundary meanings:
* `i` marks the first unsorted value.
* `temp` remembers that value while the list positions are rearranged.
* `j` walks backward through the sorted prefix.
* `j + 1` is the insertion position when the loop stops.

---

## 6. Pass-by-Pass Trace on `[4, 2, 6, 5, 1, 3]`

The first value, `4`, is a one-item sorted prefix. The outer loop then processes `i = 1` through `i = 5`. Every pass below shows the shifts, the insertion position, and the complete array state after the pass.

### PASS 1 - insert `2` at `i = 1`

The sorted prefix is `[4]`. Since `2 < 4`, shift `4` right and put `2` at index `0`.

```
     Before:  [ 4 | 2 , 6 , 5 , 1 , 3 ]
                sorted  temp

     temp = 2, j = 0
     2 < 4 -> shift 4 right:
              [ 4 , 4 , 6 , 5 , 1 , 3 ]
     write temp at j = 0:
              [ 2 , 4 , 6 , 5 , 1 , 3 ]
     insertion position: 0
```

After pass 1:

```
     [ 2 , 4 | 6 , 5 , 1 , 3 ]
       sorted prefix | unsorted suffix
```

### PASS 2 - insert `6` at `i = 2`

The sorted prefix `[2, 4]` is already smaller than `6`, so no shift is needed.

```
     Before:  [ 2 , 4 | 6 , 5 , 1 , 3 ]
                       temp = 6, j = 1

     6 < 4 -> false
     Stop immediately; insertion position: j + 1 = 2
```

After pass 2:

```
     [ 2 , 4 , 6 | 5 , 1 , 3 ]
       sorted prefix | unsorted suffix
```

### PASS 3 - insert `5` at `i = 3`

The first comparison is with `6`, so `6` shifts right. The next comparison is with `4`, which stops the scan.

```
     Before:  [ 2 , 4 , 6 | 5 , 1 , 3 ]
                             temp = 5, j = 2

     5 < 6 -> shift 6 right:
              [ 2 , 4 , 6 , 6 , 1 , 3 ]
     write temp at index 2:
              [ 2 , 4 , 5 , 6 , 1 , 3 ]
     j becomes 1; 5 < 4 -> false
     insertion position: 2
```

After pass 3:

```
     [ 2 , 4 , 5 , 6 | 1 , 3 ]
       sorted prefix    | unsorted suffix
```

### PASS 4 - insert `1` at `i = 4`

Every value in the sorted prefix is larger than `1`, so four values shift right. The insertion position is the beginning of the list.

```
     Before:  [ 2 , 4 , 5 , 6 | 1 , 3 ]
                                  temp = 1

     shift 6: [ 2 , 4 , 5 , 6 , 6 , 3 ] -> write 1 at index 3
              [ 2 , 4 , 5 , 1 , 6 , 3 ]
     shift 5: [ 2 , 4 , 5 , 5 , 6 , 3 ] -> write 1 at index 2
              [ 2 , 4 , 1 , 5 , 6 , 3 ]
     shift 4: [ 2 , 4 , 4 , 5 , 6 , 3 ] -> write 1 at index 1
              [ 2 , 1 , 4 , 5 , 6 , 3 ]
     shift 2: [ 2 , 2 , 4 , 5 , 6 , 3 ] -> write 1 at index 0
              [ 1 , 2 , 4 , 5 , 6 , 3 ]

     insertion position: 0
```

After pass 4:

```
     [ 1 , 2 , 4 , 5 , 6 | 3 ]
       sorted prefix      | unsorted suffix
```

### PASS 5 - insert `3` at `i = 5`

The values `6`, `5`, and `4` are larger than `3` and shift right. The value `2` is not larger, so the insertion position is after `2`.

```
     Before:  [ 1 , 2 , 4 , 5 , 6 | 3 ]
                                  temp = 3

     shift 6: [ 1 , 2 , 4 , 5 , 6 , 6 ] -> write 3 at index 4
              [ 1 , 2 , 4 , 5 , 3 , 6 ]
     shift 5: [ 1 , 2 , 4 , 5 , 5 , 6 ] -> write 3 at index 3
              [ 1 , 2 , 4 , 3 , 5 , 6 ]
     shift 4: [ 1 , 2 , 4 , 4 , 5 , 6 ] -> write 3 at index 2
              [ 1 , 2 , 3 , 4 , 5 , 6 ]
     j = 1; 3 < 2 -> false

     insertion position: 2
```

After pass 5:

```
     [ 1 , 2 , 3 , 4 , 5 , 6 ]
       sorted prefix covers the whole list
```

### All array states after every pass:

```
     Start:        [ 4 , 2 , 6 , 5 , 1 , 3 ]
     After pass 1: [ 2 , 4 | 6 , 5 , 1 , 3 ]
     After pass 2: [ 2 , 4 , 6 | 5 , 1 , 3 ]
     After pass 3: [ 2 , 4 , 5 , 6 | 1 , 3 ]
     After pass 4: [ 1 , 2 , 4 , 5 , 6 | 3 ]
     After pass 5: [ 1 , 2 , 3 , 4 , 5 , 6 ]

     The sorted prefix grows by exactly one position per pass.
```

---

## 7. The Actual Course Code

This is the actual solution code from `SOLUTION-Insertion_Sort.py`. It is reproduced verbatim, including the course implementation's placement of `j > -1` in the `while` condition and the explicit writes of `temp` during each shift.

```python
def insertion_sort(my_list):
    for i in range(1, len(my_list)):
        temp = my_list[i]
        j = i-1
        while temp < my_list[j] and j > -1:
            my_list[j+1] = my_list[j] 
            my_list[j] = temp
            j -= 1
    return my_list





print(insertion_sort([4,2,6,5,1,3]))



"""
    EXPECTED OUTPUT:
    ----------------
    [1, 2, 3, 4, 5, 6]
 """

```

```
     EXECUTION FLOW
     --------------
     take my_list[i] as temp
                |
                v
     compare backward through sorted prefix
                |
          larger value?
           /          \
         yes           no
          |             |
     shift right       stop
          |             |
          +------> insert temp
                         |
                         v
                 prefix is sorted again
```

### Expected output:

```
     [1, 2, 3, 4, 5, 6]
```

---

## 8. Line-by-Line Logic

### The outer loop:
`range(1, len(my_list))` starts at index `1` because a one-item prefix at index `0` is already sorted. Each new `i` identifies the next value to insert.

### Saving `temp`:
`temp = my_list[i]` preserves the value while larger prefix values move right. Without this saved value, the first shift could overwrite the item that must be inserted.

### Moving `j` backward:
`j = i - 1` points at the rightmost value in the sorted prefix. The algorithm compares `temp` with that value first, because that is the closest possible insertion position.

### The `while` condition:
`temp < my_list[j]` means only values larger than `temp` move right. The source code places `j > -1` second. Python evaluates the comparison first and then checks the boundary; when `j` becomes `-1`, the guard prevents the body from running. The code is kept exactly as supplied by the course.

### The shift:
`my_list[j+1] = my_list[j]` copies a larger value one position right. `my_list[j] = temp` places the saved value into the newly opened position for that step. Then `j -= 1` continues left.

```
     One shift, with temp = 5:

     before:       [ 2 , 4 , 6 , 6 ]
                               ^ j+1
                           j = 2
     write right:  [ 2 , 4 , 6 , 6 ]
     write temp:   [ 2 , 4 , 5 , 6 ]
                         ^ temp now sits here

     If another value is larger, the process repeats one slot left.
```

---

## 9. Big O Analysis

### Time, space, stability, and adaptiveness table:

| Measure | Result | Explanation |
|:---|:---|:---|
| **Best time** | **`O(n)`** | A sorted list makes one failed comparison per pass and performs no shifts. |
| **Average time** | **`O(n^2)`** | A random list has a quadratic expected number of inversions and shifts. |
| **Worst time** | **`O(n^2)`** | Reverse order shifts every prefix value on every pass. |
| **Best shifts** | `0` | Every new value is already after a value no larger than it. |
| **Average shifts** | `O(n^2)` | Expected inversions are proportional to `n^2`. |
| **Worst shifts** | `n(n-1)/2` | Passes shift `1 + 2 + ... + (n-1)` values. |
| **Space** | **`O(1)`** | In-place; only a constant number of variables are used. |
| **Stability** | **Yes** | The strict `<` test does not move an equal value past its predecessor. |
| **Adaptive** | **Yes** | Work is proportional to existing disorder, especially inversions. |
| **Online** | **Yes** | A sorted prefix can be maintained as new values arrive. |

### Work triangle for reverse order with `n = 6`:

```
     Insert item 2:  *                 1 shift
     Insert item 3:  *  *              2 shifts
     Insert item 4:  *  *  *           3 shifts
     Insert item 5:  *  *  *  *        4 shifts
     Insert item 6:  *  *  *  *  *     5 shifts
                                      -----------
                                       15 shifts

     1 + 2 + 3 + 4 + 5 = 15 = n(n - 1) / 2
```

### Inversions explain adaptiveness:
An **inversion** is a pair `(p, q)` where `p < q` but `my_list[p] > my_list[q]`. Insertion Sort performs roughly one rightward shift for each inversion. A nearly sorted list has few inversions, so it receives little work; a reverse list has the maximum number.

---

## 10. Insertion Sort Compared with Bubble and Selection Sort

All three basic algorithms are comparison sorts and can take `O(n^2)` time, but they react to disorder differently.
| Feature | Bubble Sort | Selection Sort | Insertion Sort |
|:---|:---|:---|:---|
| **Best time** | `O(n)` with early exit | `O(n^2)` | `O(n)` |
| **Average time** | `O(n^2)` | `O(n^2)` | `O(n^2)` |
| **Worst time** | `O(n^2)` | `O(n^2)` | `O(n^2)` |
| **Space** | `O(1)` | `O(1)` | `O(1)` |
| **Main movement** | Swap adjacent values repeatedly | Swap selected minimum once | Shift larger values right |
| **Writes** | Potentially `O(n^2)` | At most `O(n)` swaps | Potentially `O(n^2)` shifts |
| **Adaptive** | Yes with early exit | No | Yes, strongly |
| **Online** | No in its basic course form | No | Yes |
| **Stable** | Yes | No | Yes |
| **Sorted region** | Right, largest values | Left, selected minima | Left, inserted prefix |

```
     +-------------------+-------------------+-------------------+
     |    BUBBLE SORT    |  SELECTION SORT   |  INSERTION SORT   |
     +-------------------+-------------------+-------------------+
     | compare neighbors  | find global MIN   | compare backward  |
     | and swap often     | then write once   | and shift locally |
     +-------------------+-------------------+-------------------+
     | improves with      | ignores existing  | improves with     |
     | early exit         | sortedness        | existing order   |
     +-------------------+-------------------+-------------------+
```

### Decision rule:
* Choose Insertion Sort for small, nearly sorted, streaming, or stable data.
* Choose Selection Sort when the number of swaps matters more than adaptive speed.
* Choose Bubble Sort mainly to demonstrate adjacent swaps and a growing sorted tail.
* Choose an `O(n log n)` method for large general-purpose data.

Insertion Sort's central lesson is that a sorted prefix is useful information. Instead of repeatedly rediscovering the global minimum, it preserves the order already built and repairs only the position of the next value.

---

**Next Step:** Compare these basic sorts with Merge Sort to see how dividing the input can improve the quadratic time bound to `O(n log n)`.
