
---

# Dynamic Programming

## 1. What is Dynamic Programming?

**Dynamic Programming (DP)** is an optimization technique used to solve complex problems by breaking them down into **smaller subproblems**, solving each subproblem **only once**, and **storing** the results so they can be reused.

It is mainly an optimization over **plain recursion**. Wherever we see a recursive solution that has repeated calls for the same inputs, we can optimize it using Dynamic Programming.

### Key Idea:
> "Those who cannot remember the past are condemned to repeat it."
> — Dynamic Programming remembers the past (stores answers) so it never solves the same problem twice.

### The Two Requirements:
For a problem to be solved using Dynamic Programming, it **MUST** have both of these properties:

1. **Overlapping Subproblems** — the same subproblems are solved over and over again.
2. **Optimal Substructure** — an optimal solution can be constructed from optimal solutions of its subproblems.

### Where is DP used?
* Fibonacci sequence
* Shortest path problems (e.g., Google Maps)
* Knapsack problems
* Longest Common Subsequence (LCS)
* Coin change problems

```
        +--------------------------------------------------+
        |             DYNAMIC PROGRAMMING                  |
        +--------------------------------------------------+
        |                                                  |
        |   Requirement 1          Requirement 2           |
        |   +------------------+   +--------------------+  |
        |   |   OVERLAPPING    |   |      OPTIMAL       |  |
        |   |   SUBPROBLEMS    | + |    SUBSTRUCTURE    |  |
        |   +------------------+   +--------------------+  |
        |                                                  |
        |   Two ways to implement:                         |
        |   +------------------+   +--------------------+  |
        |   |    MEMOIZATION   |   |     BOTTOM-UP      |  |
        |   |    (Top-Down)    |   |   (Tabulation)     |  |
        |   +------------------+   +--------------------+  |
        +--------------------------------------------------+
```

---

## 2. Overlapping Subproblems

A problem has **Overlapping Subproblems** if finding its solution involves solving the **same subproblem multiple times**.

### Example: Fibonacci Recursion Tree

Look at what happens when we compute `fib(5)` with plain recursion:

```
                            fib(5)
                           /      \
                    fib(4)          fib(3)
                   /     \          /    \
              fib(3)    fib(2)  fib(2)  fib(1)
              /   \     /    \   /   \
         fib(2) fib(1) .................
          /  \
     fib(1) fib(0)
```

### Count the repeated work:

```
    fib(5)  ->  calculated 1 time
    fib(4)  ->  calculated 1 time
    fib(3)  ->  calculated 2 times   <== REPEATED!
    fib(2)  ->  calculated 3 times   <== REPEATED!
    fib(1)  ->  calculated 5 times   <== REPEATED!
    fib(0)  ->  calculated 3 times   <== REPEATED!
```

The subtree `fib(3)` is computed **twice**, `fib(2)` is computed **three times**... As `n` grows, this repeated work explodes **exponentially** — `O(2^n)` time!

```
    n = 5    ->   ~15 function calls
    n = 10   ->   ~177 function calls
    n = 20   ->   ~21,000 function calls
    n = 50   ->   ~20 BILLION function calls  (too slow!)
```

### The DP Insight:
> Why recompute `fib(3)` the second time? We already know the answer!
> **Solve each subproblem ONCE, store the answer, and look it up next time.**

```
    +-------------------+        +-----------------------+
    |  WITHOUT DP       |        |  WITH DP              |
    +-------------------+        +-----------------------+
    | fib(3) -> compute |        | fib(3) -> compute,    |
    | fib(3) -> compute |   =>   |          STORE result |
    | fib(3) -> compute |        | fib(3) -> LOOKUP (O(1))|
    | fib(3) -> compute |        | fib(3) -> LOOKUP (O(1))|
    +-------------------+        +-----------------------+
         O(2^n) time                    O(n) time
```

---

## 3. Optimal Substructure

A problem has **Optimal Substructure** if an **optimal solution** to the problem can be constructed from **optimal solutions of its subproblems**.

### Example: Fibonacci

```
    fib(5) = fib(4) + fib(3)
      |         |        |
      |         |        +-- optimal answer for subproblem 3
      |         +----------- optimal answer for subproblem 4
      +--------------------- optimal answer for problem 5
```

The optimal (correct) answer for `fib(5)` is **built directly** from the optimal answers of `fib(4)` and `fib(3)`. No extra information is needed.

### Real-World Analogy: Shortest Path

```
    If the shortest path from A to D goes through B:

        A --------> B --------> C --------> D
         \_________ Shortest Path _________/

    Then:  Shortest(A, D) = Shortest(A, B) + Shortest(B, D)

    The shortest path A->D CONTAINS the shortest paths of
    its subproblems (A->B and B->D).
```

### Counter-Example (NOT Optimal Substructure):
The **Longest Path** problem does NOT have optimal substructure — the longest path from A to D is not necessarily composed of the longest paths between intermediate nodes (you could create cycles). So DP **cannot** be applied to it.

### Summary:

```
    +----------------------------------------------------------+
    |  OPTIMAL SUBSTRUCTURE CHECKLIST                          |
    +----------------------------------------------------------+
    |  Can I break the problem into subproblems?          YES  |
    |  Can I build the optimal solution from the optimal       |
    |  solutions of those subproblems?                    YES  |
    |                                                          |
    |  => Dynamic Programming can be used!                     |
    +----------------------------------------------------------+
```

---

## 4. Fibonacci Sequence

The **Fibonacci Sequence** is the classic "Hello World" of Dynamic Programming. Each number is the **sum of the two preceding ones**.

```
    Index:   0    1    2    3    4    5    6    7
             |    |    |    |    |    |    |    |
    Value:   0    1    1    2    3    5    8    13
                          \___|___/
                              |
                    fib(4) = fib(3) + fib(2)
                           =   2    +   1
                           =   3
```

### The Recursive Definition:

```
                    |  0                       if n = 0
    fib(n) =        |  1                       if n = 1
                    |  fib(n-1) + fib(n-2)     if n > 1
```

### The Naive Recursive Solution:

```python
def fib(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fib(n - 1) + fib(n - 2)
```

### The Problem — Exponential Time `O(2^n)`:

Every call branches into **two** more calls, creating an exponentially growing tree:

```
    Level 0:                     fib(n)                     1 call
                                /        \
    Level 1:             fib(n-1)        fib(n-2)           2 calls
                        /       \        /       \
    Level 2:        fib(n-2) fib(n-3) fib(n-3) fib(n-4)     4 calls
                    ...              ...                    8 calls
                                                                 |
    The tree DOUBLES at every level  =>  O(2^n)  <=  EXPLOSION!  v
```

### Big O Analysis (Naive Recursion):

| Complexity | Value | Why |
|:---|:---|:---|
| **Time** | `O(2^n)` | Each call spawns 2 more calls; the tree has ~2^n nodes |
| **Space** | `O(n)` | The recursion call stack goes `n` levels deep |

> For `n = 50`, that's roughly **2^50 = 1 quadrillion operations**. Your computer would need years. This is exactly why we need Dynamic Programming.

---

## 5. Memoization (Top-Down)

**Memoization** is the **Top-Down** approach to Dynamic Programming:
* Start from the **top** (the original problem, `fib(n)`)
* Recurse **down** to the base cases
* **Store (cache)** every result in a table the first time it is computed
* Before computing anything, **check the table first**

> **Memoization = Recursion + Cache (memory)**

### Visualization — How the Memo Table Works:

```
    Computing fib(5) with memoization:

    Step 1: fib(5) -> not in memo, need fib(4) + fib(3)
    Step 2: fib(4) -> not in memo, need fib(3) + fib(2)
    Step 3: fib(3) -> not in memo, need fib(2) + fib(1)
    Step 4: fib(2) -> not in memo, need fib(1) + fib(0)
    Step 5: fib(1) -> BASE CASE, return 1
    Step 6: fib(0) -> BASE CASE, return 0
    Step 7: fib(2) = 1 + 0 = 1  ->  STORE memo[2] = 1
    Step 8: fib(3) = 1 + 1 = 2  ->  STORE memo[3] = 2
    Step 9: fib(4) -> fib(3) is IN MEMO! Just look it up (2)
            fib(4) = 2 + 1 = 3  ->  STORE memo[4] = 3
    Step 10: fib(5) -> fib(3) is IN MEMO! Just look it up (2)
             fib(5) = 3 + 2 = 5 ->  STORE memo[5] = 5
```

### The Pruned Recursion Tree:

```
                            fib(5)
                           /      \
                    fib(4)          [fib(3)] -----> LOOKUP IN MEMO (O(1))
                   /     \                ^
              fib(3)    [fib(2)] ---------+---> LOOKUP IN MEMO (O(1))
              /   \           ^
         fib(2)  [fib(1)] ----+---> LOOKUP IN MEMO (O(1))
          /  \
     fib(1) fib(0)     <--- BASE CASES

    [boxed] = never recomputed, just a dictionary lookup!
```

Only the **leftmost spine** of the tree is ever actually computed. Everything else is a lookup. **Each value of `fib(k)` is computed exactly ONCE.**

### The Code:

```python
memo = [None] * 100

def fib_memo(n):
    # Base case: already computed? Just look it up! O(1)
    if memo[n] is not None:
        return memo[n]

    # Base cases
    if n == 0 or n == 1:
        return n

    # Compute ONCE, then STORE in the memo table
    memo[n] = fib_memo(n - 1) + fib_memo(n - 2)
    return memo[n]
```

### The Memo Table (after computing fib(5)):

```
    Index:    0     1     2     3     4     5
            +-----+-----+-----+-----+-----+-----+
    memo:   |  -  |  -  |  1  |  2  |  3  |  5  |
            +-----+-----+-----+-----+-----+-----+
                              ^
                    Each cell filled in EXACTLY ONCE
                    => n computations instead of 2^n
```

### Big O Analysis (Memoization):

| Complexity | Before (Naive) | After (Memoization) |
|:---|:---|:---|
| **Time** | `O(2^n)` | **`O(n)`** — each subproblem solved once |
| **Space** | `O(n)` | `O(n)` — memo table + call stack |

---

## 6. Bottom-Up (Tabulation)

**Bottom-Up** is the **iterative** approach to Dynamic Programming:
* Start from the **bottom** (the smallest base cases, `fib(0)` and `fib(1)`)
* Build **up** a table of solutions, one step at a time
* Use **loops** instead of recursion — no call stack needed
* By the time you need `fib(k)`, `fib(k-1)` and `fib(k-2)` are already in the table

> **Bottom-Up = Iteration + Table**

### Visualization — Building the Table Upwards:

```
    GOAL: compute fib(7)

    Start with the base cases, then build UP:

    Index:    0     1     2     3     4     5     6     7
            +-----+-----+-----+-----+-----+-----+-----+-----+
    fib:    |  0  |  1  |     |     |     |     |     |     |
            +-----+-----+-----+-----+-----+-----+-----+-----+
              ^     ^
           base   base
           case   case

    i = 2:  fib[2] = fib[1] + fib[0] = 1 + 0 = 1
    i = 3:  fib[3] = fib[2] + fib[1] = 1 + 1 = 2
    i = 4:  fib[4] = fib[3] + fib[2] = 2 + 1 = 3
    i = 5:  fib[5] = fib[4] + fib[3] = 3 + 2 = 5
    i = 6:  fib[6] = fib[5] + fib[4] = 5 + 3 = 8
    i = 7:  fib[7] = fib[6] + fib[5] = 8 + 5 = 13

    FINAL TABLE:
            +-----+-----+-----+-----+-----+-----+-----+-----+
    fib:    |  0  |  1  |  1  |  2  |  3  |  5  |  8  |  13 |
            +-----+-----+-----+-----+-----+-----+-----+-----+
                                                            ^
                                                      ANSWER: fib(7) = 13
```

### Direction of Computation — Top-Down vs Bottom-Up:

```
    MEMOIZATION (Top-Down):              BOTTOM-UP (Tabulation):

    fib(7)  <---- START here             fib(0), fib(1)  <---- START here
       |                                        |
    fib(6)                                   fib(2)
       |                                        |
    fib(5)                                   fib(3)
       |                                        |
      ...                                     ...
       |                                        |
    fib(1)  <---- base cases               fib(7)  <---- ANSWER

    Recursion drills DOWN                  Loop climbs UP
    then bubbles back UP                   step by step
```

### The Code:

```python
def fib_bottom_up(n):
    # Create the table and seed the base cases
    fib_list = [0, 1]

    # Build UP from the bottom to n
    for index in range(2, n + 1):
        next_fib = fib_list[index - 1] + fib_list[index - 2]
        fib_list.append(next_fib)

    return fib_list[n]
```

### Big O Analysis (Bottom-Up):

| Complexity | Value | Why |
|:---|:---|:---|
| **Time** | **`O(n)`** | A single loop from 2 to n |
| **Space** | `O(n)` | The table stores `n+1` values |

### Bonus — Space Optimization to `O(1)`:

Since we only ever need the **last two** values, we don't need the whole table:

```python
def fib_optimized(n):
    if n == 0 or n == 1:
        return n

    prev, curr = 0, 1
    for _ in range(2, n + 1):
        prev, curr = curr, prev + curr

    return curr
```

```
    Instead of storing ALL n values:

    Table:  [0, 1, 1, 2, 3, 5, 8, 13, ...]   <- O(n) space

    Just keep a sliding window of 2:

    i=2:   prev=0, curr=1  ->  new = 0+1 = 1
    i=3:   prev=1, curr=1  ->  new = 1+1 = 2
    i=4:   prev=1, curr=2  ->  new = 1+2 = 3
    i=5:   prev=2, curr=3  ->  new = 2+3 = 5
                    \________/
                      window slides right  <- O(1) space!
```

---

## 7. Memoization vs Bottom-Up — Comparison

```
    +-----------------------+-----------------------+-----------------------+
    |                       |    MEMOIZATION        |     BOTTOM-UP         |
    |                       |    (Top-Down)         |    (Tabulation)       |
    +-----------------------+-----------------------+-----------------------+
    | Approach              | Recursive             | Iterative             |
    +-----------------------+-----------------------+-----------------------+
    | Direction             | n -> 0 (down)         | 0 -> n (up)           |
    +-----------------------+-----------------------+-----------------------+
    | Storage               | Dictionary / list     | List (table)          |
    +-----------------------+-----------------------+-----------------------+
    | Subproblems solved    | Only the ones NEEDED  | ALL subproblems       |
    +-----------------------+-----------------------+-----------------------+
    | Call stack risk       | Stack overflow for    | None (no recursion)   |
    |                       | very large n          |                       |
    +-----------------------+-----------------------+-----------------------+
    | Time Complexity       | O(n)                  | O(n)                  |
    +-----------------------+-----------------------+-----------------------+
    | Space Complexity      | O(n) (table + stack)  | O(n), optimizable     |
    |                       |                       | to O(1)               |
    +-----------------------+-----------------------+-----------------------+
```

---

## 8. The Full Evolution of Fibonacci

```
    +------------------------+------------+------------+------------------+
    |      APPROACH          |    TIME    |   SPACE    |     TECHNIQUE    |
    +------------------------+------------+------------+------------------+
    | Naive Recursion        |   O(2^n)   |    O(n)    | Just recursion   |
    +------------------------+------------+------------+------------------+
    | Memoization (Top-Down) |    O(n)    |    O(n)    | Recursion + cache|
    +------------------------+------------+------------+------------------+
    | Bottom-Up (Tabulation) |    O(n)    |    O(n)    | Loop + table     |
    +------------------------+------------+------------+------------------+
    | Bottom-Up Optimized    |    O(n)    |    O(1)    | 2 variables only |
    +------------------------+------------+------------+------------------+

    From 1 QUADRILLION operations (n=50) to just 50. That is the
    power of Dynamic Programming.
```

---

## 9. How to Solve ANY DP Problem — The Recipe

```
    Step 1:  IDENTIFY — Does the problem have Overlapping Subproblems
             AND Optimal Substructure?

    Step 2:  DEFINE the state — What does fib(n) / dp[i] represent?

    Step 3:  WRITE the recurrence relation —
             e.g., fib(n) = fib(n-1) + fib(n-2)

    Step 4:  IDENTIFY the base cases —
             e.g., fib(0) = 0, fib(1) = 1

    Step 5:  CHOOSE an implementation —
             Memoization (top-down) or Tabulation (bottom-up)?

    Step 6:  (Optional) OPTIMIZE the space if you only need
             a few previous values.
```

---

**Next Step:** Now let's practice applying Dynamic Programming to classic interview problems like Climbing Stairs, Coin Change, and the Knapsack problem!
