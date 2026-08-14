
---

# Big O Notation

## 1. What is Big O?

**Big O Notation** is the language we use to describe **how efficient an algorithm is** — specifically, how its **running time** or **memory usage grows** as the input size `n` grows.

It does **NOT** measure time in seconds. It measures the **number of operations** as a function of the input size, focusing on what happens when `n` gets **really large**.

### The Two Things Big O Measures:

1. **Time Complexity** — how the *number of operations* grows as `n` grows.
2. **Space Complexity** — how much *extra memory* the algorithm needs as `n` grows.

```
        +------------------------------------------------------+
        |                    BIG O NOTATION                    |
        +------------------------------------------------------+
        |                                                      |
        |   +----------------------+  +----------------------+ |
        |   |   TIME COMPLEXITY    |  |  SPACE COMPLEXITY    | |
        |   |  "How many ops?"     |  |  "How much memory?"  | |
        |   +----------------------+  +----------------------+ |
        |                                                      |
        |   Both are measured as a function of input size n    |
        +------------------------------------------------------+
```

### Best, Average, and Worst Case — The Three Greek Letters:

```
        +------------------------------------------------------+
        |              THE THREE GREEK LETTERS                 |
        +------------------------------------------------------+
        |  Omega   (Omega)  ->  BEST case    (the lucky run)   |
        |  Theta   (Theta)  ->  AVERAGE case (the typical run) |
        |  Omicron (O)      ->  WORST case   (== "Big O")      |
        +------------------------------------------------------+
```

### Example — Searching a List:

```
    Looking for 1 in:  [1, 2, 3, 4, 5, 6, 7]
                        ^
                        found on the FIRST check -> Omega(1) best case

    Looking for 7 in:  [1, 2, 3, 4, 5, 6, 7]
                                              ^
                        found on the LAST check  -> O(n) worst case
```

> When people say "Big O", they almost always mean the **worst case** — because the worst case is the **guarantee** we can rely on.

---

## 2. Why Was Big O Created?

### The Problem with Measuring Time Directly

You could time an algorithm with a stopwatch... but the result depends entirely on **which machine** runs it:

```
    The SAME algorithm, the SAME input, three machines:

    +---------------------------+--------------------+
    |  MACHINE                  |  MEASURED TIME     |
    +---------------------------+--------------------+
    |  2024 gaming PC           |  0.03 seconds      |
    |  2010 office laptop       |  1.20 seconds      |
    |  Raspberry Pi             |  8.50 seconds      |
    +---------------------------+--------------------+

    Which number is "the" running time?  None of them.
```

Wall-clock time depends on: **CPU speed, RAM, operating system, background processes, programming language, compiler**... The measurement is not portable.

### The Big O Solution:

> **Count operations, not seconds. Measure the GROWTH RATE, not the absolute time.**

```
    STOPWATCH APPROACH:               BIG O APPROACH:

    "It took 1.2 seconds"             "It performs ~n operations"
            |                                  |
            v                                  v
    Meaningless on any other          True on EVERY machine,
    machine, misleading even          for EVERY input size n.
    on this one tomorrow.
```

### What Big O Lets Us Do:

```
    +----------------------------------------------------------+
    |  "As n doubles, what happens to my algorithm?"           |
    +----------------------------------------------------------+
    |  O(1)    ->  nothing changes          (stays flat)       |
    |  O(n)    ->  work doubles             (proportional)     |
    |  O(n^2)  ->  work quadruples          (explodes)         |
    |  O(2^n)  ->  work SQUARES             (catastrophic)     |
    +----------------------------------------------------------+
```

---

## 3. What Problems Does Big O Solve?

### 1. Choosing Between Algorithms

Two functions solve the same problem. Which one do you ship? Big O gives you an **objective, hardware-independent** answer.

### 2. Interview Communication

Big O is the **shared vocabulary** of technical interviews. Saying *"this is O(n²), but I can make it O(n log n)"* communicates a complete idea in one sentence.

### 3. Predicting Scalability

Code that works today may collapse tomorrow. Big O tells you **before it happens**:

```
    Your code works today with n = 100 users.
    Will it survive n = 1,000,000 users?

    +---------------+---------------------------+------------------+
    |  ALGORITHM    |  OPS AT n = 1,000,000     |  VERDICT         |
    +---------------+---------------------------+------------------+
    |  O(n)         |  1,000,000                |  fine            |
    |  O(n log n)   |  ~20,000,000              |  fine            |
    |  O(n^2)       |  1,000,000,000,000        |  melts server    |
    +---------------+---------------------------+------------------+
```

---

## 4. O(1) — Constant Time

**O(1)** means the number of operations is **constant** — it does **not** depend on the input size `n`. Whether `n` is 10 or 10 million, the work is the same.

### The Code:

```python
def add_items(n):
    return n + n + n
 
 
print add_items(10)
```

### Analysis:

```
    add_items(n):
        n + n + n      <- 2 additions (some count it as 1 operation)

    n = 10        ->  same number of operations
    n = 1,000,000 ->  same number of operations

    Even if we say "2 operations", O(2) simplifies to O(1).
    "O(1)" just means: CONSTANT with respect to n.
```

### Visualization — The Flattest Line of All:

```
    operations
      ^
    2 +--------------------------------------------
      |   \________________ O(1): a flat line
    1 +--------------------------------------------
      |
      +------+------+------+------+------+------+-------> n
             10     100    1k     10k    100k   1M

    The input grows. The work does not.
```

> **O(1) is the most efficient Big O.** Examples: adding two numbers, looking up a dictionary key, `push`/`pop` on a stack.

---

## 5. O(n) — Linear Time

**O(n)** means the number of operations grows **proportionally** to the input size. Double the input, double the work.

### The Code:

```python
def print_items(n):
    for i in range(n):
        print(i)

print_items(10)
```

### Analysis:

```
    print_items(n):
        for i in range(n):      <- runs n times
            print(i)            <- 1 operation per iteration

    n = 10   ->  10  print operations
    n = 100  ->  100 print operations
    n = 1000 ->  1000 print operations

    operations = n   =>   O(n)  "linear"
```

### Visualization — A Straight Diagonal Line:

```
    operations
      ^
 1000 +                                              *
      |                                         *
  100 +                                  *
      |                             *
   10 +                     *
      |              *
    1 +      *
      |  *
      +------+------+------+------+------+------+-------> n
             10     100    1k

    A straight line: n grows -> work grows at the SAME rate.
```

---

## 6. O(n^2) — Quadratic Time

**O(n²)** appears when a loop runs **inside another loop**. For every one of the `n` outer iterations, the inner loop runs `n` times: `n * n = n²` operations.

### The Code:

```python
def print_items(n):
    for i in range(n):
        for j in range(n):
            print(i,j) 

print_items(10)
```

### Visualization — Nested Loops as a Grid (n = 4):

```
    Outer loop i picks a ROW, inner loop j walks every COLUMN:

              j=0     j=1     j=2     j=3
            +-------+-------+-------+-------+
      i=0   | (0,0) | (0,1) | (0,2) | (0,3) |   <- inner loop runs
            +-------+-------+-------+-------+      n times...
      i=1   | (1,0) | (1,1) | (1,2) | (1,3) |   <- ...for EVERY
            +-------+-------+-------+-------+      outer iteration
      i=2   | (2,0) | (2,1) | (2,2) | (2,3) |
            +-------+-------+-------+-------+
      i=3   | (3,0) | (3,1) | (3,2) | (3,3) |
            +-------+-------+-------+-------+
              \_____________________________/
                  n rows x n cols = n^2 cells

    n = 4    ->  4  x 4    =  16  print operations
    n = 10   ->  10 x 10   =  100 print operations
    n = 1000 ->  1000x1000 =  1,000,000 print operations
```

### Why It Hurts — The Explosion:

```
    operations
      ^
 1M   +                                                    *
      |                                              *
 10k  +                                       *
      |                                *
  100 +                        *
      |                 *
   10 +         *
      |    *
    1 + *
      +------+------+------+------+------+------+-------> n
             10     100    1k

    The curve bends UPWARD. Doubling n QUADRUPLES the work.
```

> **Rule of thumb:** one loop over `n` is `O(n)`; a loop **inside** a loop over `n` is `O(n²)`; three nested loops are `O(n³)` — and each extra level gets dramatically worse.

---

## 7. Rule — Drop the Constants

### The Code:

```python
def print_items(n):
    for i in range(n):
        print(i)

    for j in range(n):
        print(j)

print_items(10)
```

### Analysis:

```
    First loop   ->  n operations
    Second loop  ->  n operations
                     ___________
    Total          ->  n + n = 2n operations   =>  O(2n)
```

### The Rule:

> **Drop the constant multiplier.** `O(2n)` simplifies to `O(n)`.

### Why? Because Big O Cares About the SHAPE, Not the Slope:

```
    operations
      ^
      |                                       O(2n)  -,
      |                                  ,-''        |
      |                             ,-''             |  BOTH are
      |                       ,-''                   |  straight
      |                 ,-''       O(n)  -,          |  lines with
      |            ,-''           ,-''               |  the SAME
      |       ,-''         ,-''                      |  shape
      |  ,-''       , -''
      +--------------------------------------------------> n

    As n -> infinity, "2n" and "n" grow in the SAME WAY.
    The constant "2" is irrelevant to the growth RATE.
```

### Simplification Table:

| Exact Count | Drop the Constant | Big O |
|:---|:---|:---|
| `2n` | `2` is a constant | **`O(n)`** |
| `3n + 5` | drop `3` and `5` | **`O(n)`** |
| `500` | any fixed number | **`O(1)`** |
| `4n²` | `4` is a constant | **`O(n²)`** |

---

## 8. Rule — Drop the Non-Dominant Terms

### The Code:

```python
def print_items(n):
    for i in range(n):
        for j in range(n):
            print(i,j)
    
    for k in range(n):
        print(k)

print_items(10)
```

### Analysis:

```
    Nested loops  ->  n * n = n^2 operations   <- DOMINANT term
    Single loop   ->  n operations             <- non-dominant
                      ___________
    Total         ->  n^2 + n operations   =>  O(n^2 + n)
```

### The Rule:

> **Keep only the DOMINANT term** — the one that grows fastest. `O(n² + n)` simplifies to **`O(n²)`**.

### Why? Watch the `+n` Become Irrelevant:

```
    +-----------+-----------------+-----------------+----------------+
    |     n     |      n^2        |      + n        |  % caused by n |
    +-----------+-----------------+-----------------+----------------+
    |     10    |       100       |    100 + 10     |     9.1%       |
    |    100    |    10,000       |  10,000 + 100   |     0.99%      |
    |   1000    | 1,000,000       | 1,000,000+1000  |     0.099%     |
    +-----------+-----------------+-----------------+----------------+

    As n grows, the "n" term contributes almost NOTHING.
    The n^2 term DOMINATES -> it is all that matters.
```

```
    O(n^2 + n)  --drop non-dominant-->  O(n^2)
    O(n + 1)    --drop non-dominant-->  O(n)
    O(n^2 + n log n) --------------->   O(n^2)
```

---

## 9. Rule — Different Terms for Different Inputs

When a function takes **two different inputs**, you must track them with **two different variables** — you can no longer call everything `n`.

### The Code:

```python
def print_items(a,b):
    for i in range(a):
        print(i)

    for j in range(b):
        print(j)

print_items(1, 10)
```

### Analysis — Separate Loops: `O(a + b)`

```
    First loop   ->  runs a times
    Second loop  ->  runs b times
                     __________
    Total          ->  a + b operations   =>  O(a + b)

    You CANNOT write O(n): a and b are DIFFERENT inputs.
    There is no rule that "drops" this to O(a) or O(b).
```

### The Nested Variation: `O(a * b)`

```
    If the loops were NESTED instead of separate:

        for i in range(a):        <- runs a times
            for j in range(b):    <- runs b times for EACH i
                print(i, j)       <- a * b total operations

    Total -> a * b   =>  O(a * b)   (NOT O(n^2) — different inputs!)
```

### Side-by-Side:

```
    SEPARATE LOOPS:                    NESTED LOOPS:

    for i in range(a):  --+            for i in range(a):   --+
        print(i)          | a ops          for j in range(b): | a x b
    for j in range(b):  --+                  print(i,j)       |   ops
        print(j)          | b ops
                          |                                   |
    O(a + b)  <-----------+               O(a * b)  <---------+

    +------------------------+-------------------------+
    |  Structure             |  Big O                  |
    +------------------------+-------------------------+
    |  loops side by side    |  O(a + b)               |
    |  loops nested          |  O(a * b)               |
    +------------------------+-------------------------+
```

---

## 10. The Big O Growth Chart

### All the Complexities on One Picture:

```
    operations
      ^
      |                                              __-- O(2^n)
      |                                         __---
      |                                   __---
      |                              __--            __-- O(n^2)
      |                         __--            __---
      |                    __--            __--         __-- O(n log n)
      |               __--            __--         __--
      |          __--            __--         __--         __-- O(n)
      |     __--            __--         __--         __--      O(log n)
      | __--           __--        __--         __--        __-   O(1)
      +----------------------------------------------------------> n
                        input size grows  ------->

    From BEST to WORST:
    O(1) < O(log n) < O(n) < O(n log n) < O(n^2) < O(2^n)
```

### The Same Idea with Concrete Numbers:

| Big O | n = 10 | n = 100 | n = 1,000 |
|:---|---:|---:|---:|
| **O(1)** | 1 | 1 | 1 |
| **O(log n)** | ~3 | ~7 | ~10 |
| **O(n)** | 10 | 100 | 1,000 |
| **O(n log n)** | ~33 | ~664 | ~9,966 |
| **O(n²)** | 100 | 10,000 | 1,000,000 |
| **O(2ⁿ)** | 1,024 | ~1.27 x 10³⁰ | ~1.07 x 10³⁰¹ |

> At `n = 100`, `O(2ⁿ)` already exceeds the number of atoms in the observable universe. Growth rate — not hardware — is what matters.

---

## 11. Big O Cheat Sheet

### The Complexity Classes:

| Notation | Name | Typical Example | Verdict |
|:---|:---|:---|:---|
| `O(1)` | Constant | `add_items`, dict lookup | Excellent |
| `O(log n)` | Logarithmic | Binary search | Great |
| `O(n)` | Linear | Single loop | Good |
| `O(n log n)` | Linearithmic | Merge Sort, Quick Sort | Decent |
| `O(n²)` | Quadratic | Nested loops | Poor |
| `O(2ⁿ)` | Exponential | Naive recursive Fibonacci | Terrible |

### The Simplification Rules:

| Rule | Before | After |
|:---|:---|:---|
| **Drop Constants** | `O(2n)` | `O(n)` |
| **Drop Non-Dominant Terms** | `O(n² + n)` | `O(n²)` |
| **Different Inputs (separate)** | loops over `a` then `b` | `O(a + b)` |
| **Different Inputs (nested)** | loop over `b` inside loop over `a` | `O(a * b)` |

### One-Line Memory Hook:

```
    "Count the operations as n -> infinity,
     then keep only the part that GROWS the fastest."
```

---

**Next Step:** Now let's build the foundation for every data structure in this course — Classes and Pointers!
