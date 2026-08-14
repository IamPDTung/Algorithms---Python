
---

# Recursion

## 1. What is Recursion?

**Recursion** is a programming technique where a function **calls itself** in order to solve a problem. Each call works on a **smaller piece** of the problem until the problem becomes so small that it can be answered directly.

Every recursive function **MUST** have two parts:

1. **Base Case** — the condition that **STOPS** the recursion. It returns a value directly, without making another recursive call.
2. **Recursive Case** — the part where the function **calls itself** on a smaller input, moving one step closer to the base case.

### The Golden Rule:
> No base case = no stopping point = the function calls itself forever...
> until Python kills it with a **Stack Overflow** (`RecursionError`).

```
        +--------------------------------------------------+
        |                  RECURSION                       |
        +--------------------------------------------------+
        |                                                  |
        |   Part 1                   Part 2                |
        |   +------------------+     +------------------+  |
        |   |    BASE CASE     |     |  RECURSIVE CASE  |  |
        |   |  "stop calling"  |     |  "call yourself  |  |
        |   |  return directly |     |  on SMALLER in"  |  |
        |   +------------------+     +------------------+  |
        |                                                  |
        |   Missing base case?                             |
        |   +------------------+                           |
        |   |  STACK OVERFLOW  |  <== infinite recursion   |
        |   +------------------+                           |
        +--------------------------------------------------+
```

### What does it look like?

```
    factorial(4)
        |
        +-- 4 * factorial(3)
                  |
                  +-- 3 * factorial(2)
                            |
                            +-- 2 * factorial(1)
                                      |
                                      +-- 1   <== BASE CASE (stops!)
```

Notice how each call is the **same problem**, just **smaller**. That is the heart of recursion.

---

## 2. Why Was Recursion Created?

Some problems are **naturally self-similar** — the big problem contains smaller copies of itself:

* **Factorial / Fibonacci** — `factorial(n)` is defined *in terms of* `factorial(n-1)`.
* **Trees** — the left child of a tree is... a tree. The right child is also a tree.
* **File directories** — a folder contains files *and more folders*, which contain more folders...
* **Divide-and-Conquer** — Merge Sort and Quick Sort split a list in half, sort each half (recursively!), and merge.

Trying to solve these with nested loops requires you to **know in advance how deep the nesting goes**. With recursion, you don't — the function just keeps calling itself until it hits the bottom.

```
    +------------------------+------------------------------------------+
    |   ITERATIVE MINDSET    |         RECURSIVE MINDSET                |
    +------------------------+------------------------------------------+
    | "How many loops do I   | "What is the smallest version of this    |
    |  need to nest? What if |  problem I can answer instantly? How do  |
    |  the tree is 100 deep?"|  I reduce everything else toward it?"    |
    +------------------------+------------------------------------------+
    | Complex, fragile       | A few readable lines                     |
    +------------------------+------------------------------------------+
```

### Recursion is the Foundation For:

```
        Recursion
            |
    +-------+--------+-----------+-----------+
    |                |           |           |
 Tree/Graph     Merge Sort    Quick Sort   Dynamic
 Traversals     (folder 14)   (folder 14)  Programming
 (folder 13)                               (folder 15)
```

Everything in the next folders — tree traversals, sorting, Dynamic Programming — is built on top of the mental model you build here.

---

## 3. What Problems Does Recursion Solve?

| Problem Domain | Example | Why Recursion Fits |
|:---|:---|:---|
| **Math definitions** | `factorial(n)`, `fibonacci(n)` | Defined in terms of themselves |
| **Tree structures** | BST search/insert/delete (folder 12) | Children of a tree are trees |
| **File systems** | Walking nested directories | Folders contain folders |
| **Nested data** | Parsing JSON, XML, nested lists | Objects contain objects |
| **Divide & Conquer** | Merge Sort, Quick Sort | Split -> solve halves -> combine |
| **Backtracking** | Sudoku, mazes, N-Queens | Try a path, undo, try another |

```
    Walking a folder tree:

    /project
        |-- main.py
        |-- src/
        |       |-- utils.py
        |       |-- core/
        |       |       |-- engine.py     <== how deep does it go?
        |-- tests/
                |-- test_core.py

    With loops:  you must hardcode the depth... but depth is UNKNOWN.
    With recursion:  visit(item):
                         if item is a file  -> process it      (BASE CASE)
                         if item is a folder -> visit each child (RECURSIVE)
```

---

## 4. The Call Stack — How Function Calls Actually Work

Before we can understand recursion, we must understand the mechanism that makes it possible: **The Call Stack**.

### What is the Call Stack?

The **Call Stack** is a region of memory that keeps track of **which function is currently running** and **where to return to** when it finishes. It works **LIFO — Last In, First Out**:

* When a function is **called**, it is **PUSHED** on top of the stack.
* When a function **finishes (returns)**, it is **POPPED** off the stack.
* The function **on top** of the stack is the one currently executing.

### The Code (from `CallStack.py`):

```python
def funcThree():
    print('Three')

def funcTwo():
    funcThree()
    print('Two')

def funcOne():
    funcTwo()
    print('One')


funcOne()
```

### Output:

```
    Three
    Two
    One
```

Notice the order! `funcOne` was called **first**, but prints **last**. Why? The call stack.

### Step-by-Step — The Stack Growing DOWN (Pushing):

```
    STEP 1                STEP 2                STEP 3
    call funcOne()        funcOne calls         funcTwo calls
                          funcTwo()             funcThree()

    +---------------+     +---------------+     +---------------+
    |               |     |               |     |               |
    +---------------+     +---------------+     +---------------+
    |               |     |               |     |  funcThree()  | <== TOP
    +---------------+     +---------------+     +---------------+
    |               |     |   funcTwo()   |     |   funcTwo()   |
    +---------------+     +---------------+     +---------------+
    |   funcOne()   |     |   funcOne()   |     |   funcOne()   |
    +---------------+     +---------------+     +---------------+

    funcThree is pushed LAST => it is on TOP => it runs FIRST.
```

### Step-by-Step — The Stack Unwinding UP (Popping):

```
    STEP 4                STEP 5                STEP 6
    funcThree prints      funcTwo resumes,      funcOne resumes,
    'Three' & RETURNS     prints 'Two',         prints 'One',
    (popped off)          RETURNS (popped)      RETURNS (popped)

    +---------------+     +---------------+     +---------------+
    |               |     |               |     |               |
    +---------------+     +---------------+     +---------------+
    |               |     |               |     |               |
    +---------------+     +---------------+     +---------------+
    |   funcTwo()   |     |               |     |               |
    +---------------+     +---------------+     +---------------+
    |   funcOne()   |     |   funcOne()   |     |               |
    +---------------+     +---------------+     +---------------+

    Output so far:        Output so far:        Output so far:
    Three                 Three                 Three
                          Two                   Two
                                                One
```

### The LIFO Rule in One Picture:

```
        PUSH ORDER (going down):        POP ORDER (coming back up):

            funcOne    (1st)                funcThree  (1st out)
            funcTwo    (2nd)                funcTwo    (2nd out)
            funcThree  (3rd, last in)       funcOne    (3rd, last out)

            LAST IN  ==================>  FIRST OUT
```

> **Key Insight:** When `funcOne` calls `funcTwo`, `funcOne` does not disappear — it is **paused**, frozen mid-execution, waiting on the stack. Only when everything above it has popped off does it resume exactly where it left off (right before its `print('One')`).

**Recursion uses this exact same mechanism** — except instead of three *different* functions, it is the *same* function pushed onto the stack over and over again, each time with a smaller input.

---

## 5. Factorial — Recursion in Action

The **factorial** of a number `n` (written `n!`) is the product of all positive integers up to `n`:

```
    4!  =  4 * 3 * 2 * 1  =  24
```

Mathematically, factorial is **defined recursively**:

```
                    |  1                    if n = 1     (BASE CASE)
    factorial(n) =  |
                    |  n * factorial(n-1)   if n > 1     (RECURSIVE CASE)
```

### The Code (from `Factorial.py`):

```python
def factorial(n):
    if n == 1:
        return 1
    return n * factorial(n-1)


print(factorial(4))
```

### Output:

```
    24
```

### Reading the Code — The Two Mandatory Parts:

```
    def factorial(n):
        if n == 1:            <--+-- BASE CASE: stops the recursion
            return 1           --+   (no more calls, direct answer)
        return n * factorial(n-1)
                          ^      ^
                          |      |
                          +------+-- RECURSIVE CASE: calls itself
                                     on a SMALLER input (n-1)
```

### The Full Trace — Drilling DOWN, then Bubbling UP:

```
        CALLS GOING DOWN (pushing onto the stack)
        |                                    RETURNS COMING UP (popping off)
        |                                    |
        v                                    |
    factorial(4)                             |
        = 4 * factorial(3)  ----------+      |
        |                             |      |
        v                             v      |
    factorial(3)                 6 * 4 = 24 -+----->  returns 24
        = 3 * factorial(2)  ------+      ^
        |                         |      |
        v                         v      |
    factorial(2)             2 * 3 = 6 --+-------->  returns 6
        = 2 * factorial(1)  --+      ^
        |                     |      |
        v                     v      |
    factorial(1)         1 * 2 = 2 --+----------->  returns 2
        = 1  <== BASE CASE!       ^
            |                     |
            +---- returns 1 ------+
```

### The Same Trace on the Call Stack:

```
    MAXIMUM DEPTH (4 frames):            UNWINDING (results multiply on the way up):

    +-----------------------+            factorial(1) returns 1
    |    factorial(1)       | <== TOP    factorial(2) returns 2 * 1 = 2
    |    n = 1, BASE CASE   |            factorial(3) returns 3 * 2 = 6
    +-----------------------+            factorial(4) returns 4 * 6 = 24
    |    factorial(2)       |
    |    n = 2, waits...    |                 FINAL ANSWER: 24
    +-----------------------+
    |    factorial(3)       |            Each frame was PAUSED at:
    |    n = 3, waits...    |            "return n * factorial(n-1)"
    +-----------------------+            waiting for the child call to
    |    factorial(4)       |            hand back its result.
    |    n = 4, waits...    |
    +-----------------------+
```

### What Happens With NO Base Case?

```
    def factorial(n):
        return n * factorial(n-1)    # forgot the base case!

    factorial(4) -> factorial(3) -> factorial(2) -> factorial(1)
                 -> factorial(0) -> factorial(-1) -> factorial(-2)
                 -> ... FOREVER ...

    The stack keeps growing:
        |  factorial(-995)  |
        |  factorial(-994)  |
        |       ...         |
        |  factorial(2)     |
        |  factorial(3)     |
        |  factorial(4)     |
        +-------------------+
              |
              v
    RecursionError: maximum recursion depth exceeded
                    (a.k.a. STACK OVERFLOW)
```

---

## 6. Big O Analysis

For the recursive `factorial(n)`:

```
    Calls:    factorial(n) -> factorial(n-1) -> ... -> factorial(1)

    That's exactly n calls. Each call does O(1) work (one multiply).

    Stack depth at its peak:
        |  factorial(1)   |
        |      ...        |     <- n frames deep
        |  factorial(n)   |
        +-----------------+
```

| Complexity | Value | Why |
|:---|:---|:---|
| **Time** | `O(n)` | Exactly `n` recursive calls, each doing `O(1)` work |
| **Space** | `O(n)` | The call stack grows to `n` frames deep before unwinding |

> **Important:** Even though factorial only *uses* one number at a time logically, the recursion still *costs* `O(n)` space in memory because every paused call keeps its own frame (its own copy of `n`, its own return address) on the stack.

---

## 7. Recursion vs Iteration — Comparison

Anything recursion can do, a loop can also do (and vice versa). So when should you use which?

```
    +-----------------------+-----------------------+-----------------------+
    |                       |      RECURSION        |      ITERATION        |
    +-----------------------+-----------------------+-----------------------+
    | Readability           | Excellent for self-   | Better for simple,    |
    |                       | similar problems      | linear problems       |
    +-----------------------+-----------------------+-----------------------+
    | Code length           | Very short            | Often longer for      |
    |                       | (mirrors the math)    | nested/tree problems  |
    +-----------------------+-----------------------+-----------------------+
    | Memory usage          | O(depth) call stack   | O(1) extra space      |
    |                       | frames                | (just loop variables) |
    +-----------------------+-----------------------+-----------------------+
    | Risk                  | Stack overflow if     | Infinite loop if      |
    |                       | base case is missing  | condition is wrong    |
    +-----------------------+-----------------------+-----------------------+
    | Best for              | Trees, graphs, divide | Simple counting,      |
    |                       | & conquer, nested data| flat loops            |
    +-----------------------+-----------------------+-----------------------+
```

| Factor | Recursion | Iteration |
|:---|:---|:---|
| **factorial code** | 4 lines, mirrors the definition | Needs explicit loop + accumulator |
| **Space cost** | `O(n)` stack frames | `O(1)` |
| **Python depth limit** | ~1000 frames (`RecursionError`) | No limit |
| **Debugging** | Harder (many active frames) | Easier (one loop state) |
| **When to choose** | Problem is naturally recursive (trees!) | Problem is a simple repetition |

> **Rule of thumb:** If the problem is a *tree* or *divide-and-conquer* shape, reach for recursion. If it is a flat repetition, reach for a loop. Next folder, you'll see why trees make this decision for you.

---

## 8. Summary

```
    +----------------------------------------------------------+
    |  RECURSION CHECKLIST                                     |
    +----------------------------------------------------------+
    |  1. Does my function call ITSELF?                        |
    |                                                          |
    |  2. Do I have a BASE CASE that stops the calls?          |
    |     (Missing it => stack overflow!)                      |
    |                                                          |
    |  3. Does every recursive call move CLOSER to the         |
    |     base case?  (n-1, smaller subtree, shorter list...)  |
    |                                                          |
    |  4. Am I okay paying O(depth) space on the call stack?   |
    +----------------------------------------------------------+
```

```
    The mental model to keep forever:

        CALLS DRILL DOWN:        RETURNS BUBBLE UP:
        factorial(4)             factorial(1) = 1
            |                        |
        factorial(3)             2 * 1 = 2
            |                        |
        factorial(2)             3 * 2 = 6
            |                        |
        factorial(1)  ======>    4 * 6 = 24
        BASE CASE                ANSWER
```

---

**Next Step:** Now that you understand recursion and the call stack, let's apply it to a data structure where it truly shines — rewriting our Binary Search Tree operations recursively (folder 12)!
