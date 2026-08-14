
---

# Bubble Sort

## 1. What is Bubble Sort?

**Bubble Sort** is the simplest comparison-based sorting algorithm. It repeatedly walks through the list, compares **adjacent pairs** of elements, and **swaps** them if they are out of order. After each full pass, the **largest unsorted value** has "bubbled up" to its final position at the end of the list — like an air bubble rising to the surface of water.

### Key Idea:
> Compare neighbors. If the left one is bigger, swap them. Keep going. After every pass, one more value at the end is locked into its correct place forever.

### Core Characteristics:
* **Comparison sort** — decisions are made only by comparing two elements.
* **Adjacent swaps only** — elements move exactly one position per swap.
* **In-place** — no extra array needed, everything happens inside the original list.
* **Sorted region grows from the RIGHT** — the tail of the list fills up with final, correct values.

```
        +--------------------------------------------------+
        |                 BUBBLE SORT                      |
        +--------------------------------------------------+
        |                                                  |
        |   Repeat:                                        |
        |     +----------------------------------------+   |
        |     |  Compare pair (j, j+1)                 |   |
        |     |  if left > right  ->  SWAP them        |   |
        |     +----------------------------------------+   |
        |                                                  |
        |   Result of each pass:                           |
        |     LARGEST unsorted value lands at the end      |
        |                                                  |
        |   [ unsorted region | sorted region -> ]         |
        |        shrinks <-        grows ->                |
        +--------------------------------------------------+
```

---

## 2. Why Was It Created?

Bubble Sort is historically the **introductory sorting algorithm** — the first sort almost every programmer ever learns:

* **Easy to understand** — the logic is just "compare neighbors, swap if wrong".
* **Easy to implement** — two nested loops and a `temp` variable. That's all.
* **Easy to trace** — you can watch every swap happen step by step.

It is **rarely used in production** — it is simply too slow for large datasets. Its real value is **educational**: it is the **baseline** against which every other sorting algorithm is compared. When you later learn Selection Sort, Insertion Sort, Merge Sort, or Quick Sort, the first question is always: *"How much faster is it than Bubble Sort?"*

```
        +--------------------------------------------------+
        |  WHY BUBBLE SORT MATTERS                         |
        +--------------------------------------------------+
        |                                                  |
        |   1. First sort every programmer learns          |
        |   2. Teaches SWAP mechanics (temp variable)      |
        |   3. Teaches loop invariants (sorted tail)       |
        |   4. The BASELINE all other sorts beat           |
        |                                                  |
        |   Production use:  almost none                   |
        |   Teaching value:  enormous                      |
        +--------------------------------------------------+
```

---

## 3. What Problems Does It Solve?

* **Sorting tiny datasets** — for a handful of elements, simplicity beats everything.
* **Nearly-sorted data** — with the standard optimization (stop if a pass makes no swaps), it detects sorted input in `O(n)`.
* **Teaching swap mechanics** — the `temp` swap pattern appears everywhere in algorithms.
* **Teaching loop invariants** — "after pass k, the last k elements are in their final positions" is a perfect first invariant.

### In This Course:
The exact same bubbling logic is reused later to sort a **Linked List** — see **`Bubble Sort of LL`** in the `Interview` folder, where you bubble values along a chain of nodes instead of an array.

```
        +--------------------------------------------------+
        |  WHERE BUBBLE SORT FITS                          |
        +--------------------------------------------------+
        |                                                  |
        |   Tiny list (n < 10) .............. OK           |
        |   Nearly sorted list .............. OK (O(n))    |
        |   Teaching swaps/invariants ....... PERFECT      |
        |   Linked List sorting (course) .... YES          |
        |   Large random data ............... NEVER        |
        +--------------------------------------------------+
```

---

## 4. How Does It Work?

We trace the course's exact code on the list **`[4, 2, 6, 5, 1, 3]`**.

The outer loop runs `i` from `len-1` down to `1`. The inner loop runs `j` from `0` to `i-1`, comparing the adjacent pair `(j, j+1)`. Notice how the inner loop **shrinks by one** every pass — because the tail is already sorted.

### PASS 1 — every adjacent comparison and swap (i = 5):

```
    Start:   [ 4 , 2 , 6 , 5 , 1 , 3 ]

    j=0:  compare 4 and 2   ->  4 > 2  ->  SWAP
          [ 2 , 4 , 6 , 5 , 1 , 3 ]

    j=1:  compare 4 and 6   ->  4 < 6  ->  no swap
          [ 2 , 4 , 6 , 5 , 1 , 3 ]

    j=2:  compare 6 and 5   ->  6 > 5  ->  SWAP
          [ 2 , 4 , 5 , 6 , 1 , 3 ]

    j=3:  compare 6 and 1   ->  6 > 1  ->  SWAP
          [ 2 , 4 , 5 , 1 , 6 , 3 ]

    j=4:  compare 6 and 3   ->  6 > 3  ->  SWAP
          [ 2 , 4 , 5 , 1 , 3 , 6 ]
                                   ^
                    6 has BUBBLED UP to its final position!
```

### The array AFTER EVERY PASS — watch the sorted tail grow:

```
    Start:        [ 4 , 2 , 6 , 5 , 1 , 3 ]
                   <------ unsorted ------->

    After pass 1: [ 2 , 4 , 5 , 1 , 3 | 6 ]
                   <--- unsorted ---> |sorted|

    After pass 2: [ 2 , 4 , 1 , 3 | 5 , 6 ]
                   <-- unsorted --> | sorted |

    After pass 3: [ 2 , 1 , 3 | 4 , 5 , 6 ]
                   <- unsorted -> |  sorted  |

    After pass 4: [ 1 , 2 | 3 , 4 , 5 , 6 ]
                   unsorted |    sorted     |

    After pass 5: [ 1 | 2 , 3 , 4 , 5 , 6 ]
                           |  ALL SORTED    |

    Final:        [ 1 , 2 , 3 , 4 , 5 , 6 ]
```

### The inner loop shrinks every pass:

```
    Pass 1:  j runs 0..4   (5 comparisons)  -> locks in 6
    Pass 2:  j runs 0..3   (4 comparisons)  -> locks in 5
    Pass 3:  j runs 0..2   (3 comparisons)  -> locks in 4
    Pass 4:  j runs 0..1   (2 comparisons)  -> locks in 3
    Pass 5:  j runs 0..0   (1 comparison)   -> locks in 2

    Total comparisons: 5 + 4 + 3 + 2 + 1 = 15  =  n*(n-1)/2

    [ unsorted region shrinks | sorted region grows ]
             <------------- n-1 elements ----------->
```

### The swap mechanic in detail:

```
    To swap my_list[j] and my_list[j+1] we need a TEMP variable,
    otherwise one value gets overwritten and lost:

        temp = my_list[j]        <- rescue the left value
        my_list[j] = my_list[j+1]   <- right moves left
        my_list[j+1] = temp         <- rescued value moves right

        j       j+1                 j       j+1
      +-----+ +-----+             +-----+ +-----+
      |  4  | |  2  |    ==>      |  2  | |  4  |
      +-----+ +-----+             +-----+ +-----+
        |                            ^
        +-- saved in temp -----------+
```

---

## 5. The Code

This is the actual solution code from the course (`SOLUTION-Bubble_Sort.py`):

```python
def bubble_sort(my_list):
    for i in range(len(my_list) - 1, 0 ,-1):
        for j in range(i):
            if my_list[j] > my_list[j+1]:
                temp = my_list[j]
                my_list[j] = my_list[j+1]
                my_list[j+1] = temp
    return my_list





print(bubble_sort([4,2,6,5,1,3]))
```

```
    EXPECTED OUTPUT:
    ----------------
    [1, 2, 3, 4, 5, 6]
```

### Line-by-line breakdown:

```
    for i in range(len(my_list) - 1, 0, -1):
        i counts DOWN from 5 to 1.
        i = the boundary between unsorted and sorted regions.

        for j in range(i):
            j walks 0 .. i-1, touching only the UNSORTED region.

            if my_list[j] > my_list[j+1]:
                The adjacent pair is out of order -> SWAP.
                Using ">" (not ">=") means equal elements are
                never swapped -> Bubble Sort is STABLE.
```

---

## 6. Big O Analysis

### Time Complexity:

| Case | Comparisons | Swaps | Complexity | Why |
|:---|:---|:---|:---|:---|
| **Best** (already sorted) | `n-1` | `0` | **`O(n)`** | With the "no swaps => stop" check, one pass proves it is sorted (course note) |
| **Average** (random) | `n(n-1)/2` | ~`n(n-1)/4` | **`O(n^2)`** | Two nested loops over a shrinking region |
| **Worst** (reversed) | `n(n-1)/2` | `n(n-1)/2` | **`O(n^2)`** | Every comparison triggers a swap |

### Space Complexity:

| Complexity | Value | Why |
|:---|:---|:---|
| **Space** | **`O(1)`** | In-place — only the `temp` variable, no extra array |

### Visualizing the O(n^2) work:

```
    The comparison triangle for n = 6:

    Pass 1:  *  *  *  *  *        (5)
    Pass 2:  *  *  *  *           (4)
    Pass 3:  *  *  *              (3)
    Pass 4:  *  *                 (2)
    Pass 5:  *                    (1)

    Area of the triangle ~ n^2 / 2  =>  O(n^2)
    Double the input, QUADRUPLE the work.
```

---

## 7. Bubble Sort vs The Other Basic Sorts

All three basic sorts are `O(n^2)` comparison sorts — but they differ in the details:

| Feature | Bubble Sort | Selection Sort | Insertion Sort |
|:---|:---|:---|:---|
| **Time (best)** | `O(n)` | `O(n^2)` | `O(n)` |
| **Time (average)** | `O(n^2)` | `O(n^2)` | `O(n^2)` |
| **Time (worst)** | `O(n^2)` | `O(n^2)` | `O(n^2)` |
| **Space** | `O(1)` | `O(1)` | `O(1)` |
| **Swaps** | Many — up to `O(n^2)` | Minimal — `O(n)` total | Shifts — up to `O(n^2)` writes |
| **Adaptive** (fast on nearly-sorted) | Yes (with early-exit) | No | Yes |
| **Stable** | Yes | No | Yes |
| **Sorted region grows from** | Right (max bubbles up) | Left (min selected) | Left (cards inserted) |

```
    +-------------------+-------------------+-------------------+
    |    BUBBLE SORT    |  SELECTION SORT   |  INSERTION SORT   |
    +-------------------+-------------------+-------------------+
    | swap neighbors    | find MIN, swap    | insert next card  |
    | many times        | ONCE per pass     | into sorted hand  |
    +-------------------+-------------------+-------------------+
    | best case O(n)    | always O(n^2)     | best case O(n)    |
    | great teacher     | fewest writes     | best in practice  |
    +-------------------+-------------------+-------------------+
```

---

**Next Step:** Now let's look at **Selection Sort** — a cousin of Bubble Sort that makes only ONE swap per pass instead of many!
