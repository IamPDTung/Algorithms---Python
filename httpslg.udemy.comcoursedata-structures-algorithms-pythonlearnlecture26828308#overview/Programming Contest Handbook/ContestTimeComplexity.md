
---

# Programming Contest Handbook: Time Complexity

This guide explains how to read a programming contest statement, estimate the work performed by your code, choose an algorithm that fits the limits, and avoid confusing asymptotic complexity with an exact running time.

The central contest habit is:

> Read the constraints before choosing the algorithm.

```
    CONTEST STATEMENT
           |
           v
    maximum input size
           |
           v
    allowed operation count
           |
           v
    target complexity
           |
           v
    algorithm + data structure
           |
           v
    implementation and tests
```

---

## 1. What Does `n` Mean?

In Big O analysis, `n` normally represents the size of the input. It is a **variable**, not a constant.

Examples:

```python
# n is the number of values in the list
numbers = [4, 2, 7, 1]
n = len(numbers)

# n is the number of characters in the string
text = "algorithm"
n = len(text)
```

The statement:

```text
1 <= n <= 2 * 10^5
```

does not say that `n` is always `200,000`. It says that the judge may give any valid input up to `200,000`, including the largest case.

```
    possible inputs:

    1, 2, 3, 4, ..., 199,999, 200,000
                                      ^
                              important worst case
```

### `n` Is Not the Same as a Constant

There are two different ideas:

```text
    n = input size                variable; changes per test case
    c = fixed multiplier           constant; independent of input size
    2 * 10^5 = 200,000             constraint value; maximum allowed n
```

For example:

```text
5n + 20
```

has a variable part `n` and fixed constants `5` and `20`. In asymptotic notation:

```text
5n + 20 -> O(n)
```

The constants are removed when describing growth, but they can still matter in a real contest. That difference is discussed later.

---

## 2. Read the Contest Statement as a Contract

The input constraints describe the largest amount of work your program must handle. Read every constraint, not only the first one.

Look for:

| Statement information | What it tells you |
|:---|:---|
| `n <= ...` | Size of one main input |
| `T <= ...` | Number of test cases |
| `sum(n) <= ...` | Total input size across all cases |
| `V, E` | Graph vertices and edges |
| `a[i] <= ...` | Value range; may suggest counting or frequency arrays |
| `time limit` | Maximum wall-clock time on the judge |
| `memory limit` | Maximum extra memory allowed |
| Values are sorted | Binary search, two pointers, or greedy methods may be possible |
| Values are distinct | Some duplicate-handling work may be unnecessary |

### Constraint Diagram

```
    n <= 20              -> exponential / bitmask may be possible
    n <= 500             -> O(n^2) may be possible
    n <= 2,000           -> O(n^2) often possible, check time limit
    n <= 2 * 10^5        -> O(n) or O(n log n) is the usual target
    n <= 10^6            -> usually O(n), careful with constants and I/O
    n is extremely large -> O(log n), O(1), or mathematical reasoning
```

This is a **guideline**, not a law. A two-second C++ solution and a two-second Python solution do not have the same practical budget. The exact time limit and implementation still matter.

### The Constraint Is a Signal

If a problem gives `n <= 2 * 10^5`, the author probably does not expect you to compare every pair of elements. The constraint is often a clue that you should use:

* A hash set or dictionary
* Sorting plus a linear scan
* Two pointers or a sliding window
* Prefix sums
* A heap
* A graph traversal with `O(V + E)` complexity
* Dynamic programming with a linear or near-linear state count

---

## 3. What Does Big O Actually Tell You?

Big O describes how work grows as the input grows. It does **not** directly give seconds.

```text
    Big O asks:

    If the input becomes 2 times larger,
    how does the amount of work change?
```

| Complexity | If `n` doubles | Typical meaning |
|:---|:---|:---|
| `O(1)` | Almost unchanged | Direct lookup or fixed work |
| `O(log n)` | Increases slightly | Repeatedly halve the search space |
| `O(n)` | About 2 times more work | One pass |
| `O(n log n)` | A little more than 2 times | Efficient sorting or divide-and-conquer |
| `O(n^2)` | About 4 times more work | All-pairs comparison |
| `O(2^n)` | About 2 times more work for one extra item | Exhaustive subset choices |

### Growth Visualization

```text
    work
      ^
      |                                      O(2^n)
      |                                _____/
      |                         O(n^2) /
      |                    _____/     /
      |             O(n log n)       /
      |          __/                 /
      |       __/ O(n)              /
      |______/_____________________/____________> n
       O(1)   O(log n)
```

The diagram is not drawn to an exact scale. It shows why a quadratic algorithm can be fine for `n = 1,000` but impossible for `n = 200,000`.

---

## 4. Convert Source Code into an Operation Count

To estimate complexity from source code:

1. Define what `n` represents.
2. Identify the operation that repeats.
3. Count how many times each loop or recursive call runs.
4. Multiply nested work and add sequential work.
5. Keep the dominant term.
6. Evaluate the result at the maximum constraint.

### Constant Work: `O(1)`

```python
    return numbers[0]
```

There is one array access regardless of whether the list has 10 or 200,000 values.

```text
    1 access -> O(1)
```

### One Pass: `O(n)`

```python
    result = 0
    for number in numbers:
        result += number
    return result
```

The loop executes once for every input value:

```text
    n iterations -> O(n)
```

### Two Separate Passes: Still `O(n)`

```python
    positive = 0
    even = 0

    for number in numbers:
        if number > 0:
            positive += 1

    for number in numbers:
        if number % 2 == 0:
            even += 1

    return positive, even
```

The work is:

```text
    n + n = 2n
    Drop the fixed constant 2
    O(2n) = O(n)
```

```text
    first pass:   [--------------------]  n
    second pass:  [--------------------]  n
                   total = 2n -> O(n)
```

### Independent Nested Loops: `O(n^2)`

```python
    for first in numbers:
        for second in numbers:
            print(first, second)
```

The outer loop runs `n` times. For each outer iteration, the inner loop runs `n` times:

```text
    n * n = n^2
    O(n^2)
```

```text
              inner index
             0 1 2 3 ... n-1
          +-------------------+
    outer | x x x x ... x      | 0
    index | x x x x ... x      | 1
          | x x x x ... x      | 2
          |       ...         |
          | x x x x ... x      | n-1
          +-------------------+

          n rows * n columns = n^2 operations
```

### Triangular Nested Loops: Still `O(n^2)`

```python
    for i in range(len(numbers)):
        for j in range(i):
            compare(numbers[i], numbers[j])
```

The inner loop performs:

```text
    0 + 1 + 2 + ... + (n - 1)
    = n(n - 1) / 2
    = O(n^2)
```

Even though only half of an `n * n` grid is used, half of `n^2` is still quadratic.

---

## 5. Common Complexity Patterns

### Repeatedly Halve the Problem: `O(log n)`

```python
    steps = 0
    while n > 1:
        n //= 2
        steps += 1
    return steps
```

```text
    n -> n/2 -> n/4 -> n/8 -> ... -> 1

    number of divisions = log2(n)
    complexity = O(log n)
```

This is the pattern behind binary search.

### Divide and Process Every Level: `O(n log n)`

Merge sort divides the input into `log n` levels. Each level processes all `n` elements during merging:

```text
    level 0:                  n work
    level 1:              n + n work
    level 2:          n/2 + n/2 + ... = n work
    ...
    number of levels:        log n

    total = n * log n
    O(n log n)
```

### Nested Loop with a Monotonic Pointer: Often `O(n)`

Nested syntax does not automatically mean `O(n^2)`.

```python
    left = 0
    current = 0

    for right in range(len(numbers)):
        current += numbers[right]

        while current > target and left <= right:
            current -= numbers[left]
            left += 1

        if current == target:
            return True

    return False
```

`right` moves forward at most `n` times. `left` also moves forward at most `n` times across the entire function:

```text
    right: 0 -> 1 -> 2 -> ... -> n-1       at most n moves
    left:  0 -> 1 -> 2 -> ... -> n-1       at most n moves total

    n + n = 2n -> O(n)
```

The inner `while` does not restart from zero for every `right`. This is called **amortized analysis**.

### Different Input Sizes

```python
    for value in first:
        use(value)

    for value in second:
        use(value)
```

If the lists have sizes `a` and `b`, the complexity is:

```text
    O(a + b)
```

Do not write `O(n)` unless the statement guarantees that both sizes are represented by the same `n`.

For nested loops over different inputs:

```python
for x in first:
    for y in second:
        use(x, y)
```

the complexity is:

```text
    O(a * b)
```

---

## 6. Constraint Size and Expected Algorithm

The following table is a practical first estimate. It is not a substitute for exact analysis.

| Maximum input size | Usually consider | Usually avoid |
|:---|:---|:---|
| `n <= 20` | Backtracking, bitmask, `O(2^n)` | Nothing automatically |
| `n <= 40` | Meet-in-the-middle, optimized exponential | Full `O(2^n)` if possible |
| `n <= 500` | `O(n^2)`, some `O(n^3)` with a generous limit | Large exponential work |
| `n <= 2,000` | `O(n^2)`, sorting, prefix sums | `O(n^3)` unless very small constants |
| `n <= 2 * 10^5` | `O(n)`, `O(n log n)`, hashing, heaps, DP | Ordinary `O(n^2)` |
| `n <= 10^6` | `O(n)`, efficient I/O, compact memory | Large constants and nested scans |
| `n <= 10^9` | `O(log n)`, formulas, binary search, matrix methods | Any loop to `n` |

### Maximum Work Examples

```text
    n = 2 * 10^5

    O(n)       = 200,000
    O(n log2n) = about 3,600,000
    O(n sqrt n)= about 89,000,000
    O(n^2)     = 40,000,000,000
```

```text
    acceptable region                 danger region
    <--------------------------|---------------------------->
    O(n), O(n log n)            O(n sqrt n), O(n^2), O(2^n)
```

An `O(n sqrt n)` algorithm may pass in optimized C++ with a generous limit and fail in Python with a strict limit. Always inspect the actual statement.

---

## 7. Constants: Big O Hides Them, Contests Do Not

In asymptotic notation:

```text
    O(5n)       -> O(n)
    O(100n)     -> O(n)
    O(2n + 50)  -> O(n)
```

Why are constants removed? Because as `n` approaches infinity, the growth category is still linear.

But a contest has a finite maximum input and a finite time limit. At that size, constants can decide whether code passes.

### Same Big O, Different Practical Work

```text
    Algorithm A:  n operations
    Algorithm B:  100n operations

    Both are O(n), but B performs about 100 times more work.
```

At `n = 200,000`:

```text
    n       = 200,000 operations
    100n     = 20,000,000 operations
```

Both may pass, but the second algorithm has less safety margin.

### Comparing Different Growth Categories

At `n = 200,000`:

```text
    100n       = 20,000,000
    n log2 n   = about 3,600,000
    n^2        = 40,000,000,000
```

```text
    100n       is still linear
    n log n    grows faster eventually, but is smaller at this particular n
    n^2        is many orders of magnitude too large
```

The correct process is not “constants never matter.” It is:

1. Reject the wrong growth category first.
2. Compare constants among algorithms with acceptable growth.
3. Benchmark only when the result is close to the limit.

### Constants Come from More Than Multiplication

The constant factor includes:

* Number of instructions in the inner loop
* Function-call overhead
* Hashing cost
* Memory allocation
* Cache behavior
* Input/output
* Python interpreter overhead
* Data structure operations hidden inside library calls

```text
    simple integer addition       small constant
    dictionary lookup             larger, average O(1)
    sorting a slice               allocation + O(k log k)
    printing every iteration      extremely large practical cost
```

---

## 8. Time Limits and Operation Estimates

Big O does not provide an official conversion from operations to seconds. There is no universal rule such as “exactly `10^8` operations always equal one second.”

A common contest heuristic is that roughly `10^7` to `10^8` simple operations may be feasible per second on some judge environments, but this varies greatly by language, operation, compiler, hardware, and time limit.

Treat it as a warning scale, not a guarantee:

```text
    estimated time ~= actual work / environment throughput
```

### Why `O(n^2)` Is Dangerous for `n = 200,000`

```python
for i in range(n):
    for j in range(n):
        do_constant_work()
```

The body executes:

```text
    200,000 * 200,000
    = 40,000,000,000 times
```

Even if an environment handled `10^8` simple iterations per second, this would be roughly:

```text
    40,000,000,000 / 100,000,000
    = 400 seconds
```

Most contest limits are much smaller than that. The exact throughput is not important here; the gap is enormous.

### Use the Time Limit as a Budget

```text
    time limit
        |
        v
    practical budget
        |
        +--> input parsing
        +--> algorithm work
        +--> output
        +--> safety margin
```

If the time limit is 2 seconds, do not design an algorithm that needs the full theoretical maximum. Leave room for parsing, allocation, and language overhead.

---

## 9. Hidden Costs in Python

The visible loop is not always the real complexity. A single line can contain a loop internally.

| Python operation | Typical complexity | Contest warning |
|:---|:---:|:---|
| `numbers[i]` | `O(1)` | Direct list access |
| `numbers.append(x)` | Amortized `O(1)` | Occasional resize |
| `numbers.pop()` | `O(1)` | Removes from the end |
| `numbers.pop(0)` | `O(n)` | Shifts every remaining item |
| `x in numbers` | `O(n)` | List scan |
| `x in my_set` | Average `O(1)` | Hash lookup |
| `x in my_dict` | Average `O(1)` | Hash lookup |
| `numbers.sort()` | `O(n log n)` | In-place sort |
| `sorted(numbers)` | `O(n log n)` | Creates another list |
| `numbers[a:b]` | `O(b-a)` | Copies the slice |
| `text += piece` repeatedly | Can become expensive | Prefer a list and `join` |
| `print(...)` in a large loop | Depends on output size | Buffer output |

### The Hidden Quadratic Pattern

This looks like two simple operations:

```python
for value in numbers:
    if value in numbers:
        print(value)
```

But `value in numbers` is itself `O(n)`:

```text
    outer loop:       n
    list membership:  n for each outer iteration

    n * n = O(n^2)
```

Use a set when the problem allows it:

```python
seen = set(numbers)

for value in numbers:
    if value in seen:
        print(value)
```

This changes the membership check to average `O(1)`, so the whole scan is average `O(n)`.

### `pop(0)` in a Queue

```python
while items:
    current = items.pop(0)
```

If the list has `n` items, the shifts cost:

```text
    (n - 1) + (n - 2) + ... + 1
    = O(n^2)
```

Use `collections.deque` for efficient queue operations:

```python
from collections import deque

items = deque(values)
while items:
    current = items.popleft()
```

---

## 10. Multiple Test Cases

Always multiply the complexity for one test case by the number of test cases, unless the statement gives a total-size constraint.

### Independent Maximums

```text
    T <= 10
    n <= 200,000 for every test case
    algorithm = O(n)

    total work <= 10 * 200,000
                   = 2,000,000
```

For an `O(n^2)` algorithm:

```text
    10 * (200,000)^2
    = 400,000,000,000 operations
```

### Sum Constraint

Many problems instead say:

```text
    T <= 200,000
    sum of n over all test cases <= 200,000
```

Then the total input size is bounded:

```text
    n1 + n2 + n3 + ... + nT <= 200,000
```

An `O(n)` algorithm per case remains `O(sum(n))` overall:

```text
    O(n1) + O(n2) + ... + O(nT)
    = O(sum(n))
    = O(200,000)
```

But an `O(n^2)` algorithm per case is not automatically safe. The sum of squares can still be large:

```text
    one case of 200,000:
    (200,000)^2 = 40,000,000,000
```

### Test Case Visualization

```text
    Case 1: [---------] n1
    Case 2: [---]     n2
    Case 3: [------]  n3
    ...
    total:  n1 + n2 + n3 + ... <= limit
```

Read whether the bound applies to each case or to the sum across all cases.

---

## 11. Worst Case Covers All Valid Inputs

When a contest asks for a solution for all valid inputs, analyze the worst case.

```python
    for value in numbers:
        if value == target:
            return True
    return False
```

Best case:

```text
    target is first -> O(1)
```

Worst case:

```text
    target is absent or last -> O(n)
```

The algorithm is described as `O(n)` because the judge can choose the worst valid input.

### Early Exit Does Not Automatically Change Big O

```python
for i in range(n):
    for j in range(n):
        if answer_found:
            return result
```

If `answer_found` can remain false until the final iteration, the worst case is still `O(n^2)`.

```text
    lucky input:       stops early
    adversarial input: visits the entire search space
                         ^
                         complexity must cover this case
```

Early exits can improve average performance, but they only improve the worst-case Big O if the code guarantees a smaller bound for every input.

---

## 12. Space Complexity and Memory Limits

Time is not the only contest resource. Estimate extra memory as a function of input size.

| Structure | Extra space |
|:---|---:|
| A few variables | `O(1)` |
| Set containing all `n` values | `O(n)` |
| Prefix-sum array | `O(n)` |
| Adjacency list | `O(V + E)` |
| Adjacency matrix | `O(V^2)` |
| DP table with `n` states | `O(n)` |
| Two-dimensional DP table | `O(nm)` |
| Recursion depth `n` | `O(n)` call stack |

### Memory Visualization

```text
    Input array:       [--------------------]  O(n) input
    Set copy:          {--------------------}  O(n) extra
    Prefix array:      [--------------------]  O(n) extra

    Total extra memory = two additional structures of size n
```

For `n = 2 * 10^5`, an `O(n)` array is often reasonable, but the element type and language representation matter. Python integers and object references use more memory than C++ integers.

### Matrix Warning

If `V = 2 * 10^5`, an adjacency matrix would need approximately:

```text
    V^2 = 40,000,000,000 cells
```

That is impossible for ordinary contest memory limits. Use an adjacency list for a sparse graph.

---

## 13. Worked Contest Examples

### Example A: Detect a Duplicate

Constraint:

```text
1 <= n <= 2 * 10^5
```

Naive approach:

```python
for i in range(n):
    for j in range(i + 1, n):
        if numbers[i] == numbers[j]:
            return True
```

Complexity:

```text
    O(n^2)
    maximum work ~= 40,000,000,000 comparisons
    likely too slow
```

Hash-set approach:

```python
seen = set()

for number in numbers:
    if number in seen:
        return True
    seen.add(number)

return False
```

Complexity:

```text
    average time: O(n)
    extra space:  O(n)
```

The constraint suggests trading memory for time.

### Example B: Pair Sum with Sorting

Constraint:

```text
n <= 2 * 10^5
```

Sort first, then use two pointers:

```python
numbers.sort()
left = 0
right = len(numbers) - 1

while left < right:
    current = numbers[left] + numbers[right]

    if current == target:
        return True
    if current < target:
        left += 1
    else:
        right -= 1

return False
```

```text
    sort:       O(n log n)
    scan:       O(n)
    total:      O(n log n)
    extra space: depends on sort and implementation
```

The two pointers move only inward:

```text
    left  -> -> ->
    [ 1  3  4  7  9  12 ]
                    <- <- right

    each pointer moves at most n times total
```

### Example C: Range Sum Queries

Constraint:

```text
n <= 2 * 10^5
q <= 2 * 10^5
```

If each query scans the array:

```text
    O(nq) = about 40,000,000,000 operations
```

Use prefix sums:

```python
prefix = [0]

for number in numbers:
    prefix.append(prefix[-1] + number)

def range_sum(left, right):
    return prefix[right + 1] - prefix[left]
```

Complexity:

```text
    preprocessing: O(n)
    each query:    O(1)
    all queries:   O(n + q)
```

### Example D: Graph Traversal

Constraint:

```text
V <= 2 * 10^5
E <= 2 * 10^5
```

Depth-first search or breadth-first search with an adjacency list:

```text
    O(V + E)
```

An adjacency matrix would require:

```text
    O(V^2)
```

which is far beyond the limit for `V = 200,000`.

---

## 14. Choosing an Algorithm from the Statement

Use this decision path:

```text
    Read n, T, values, time limit, memory limit
                     |
                     v
    Estimate the maximum work of the obvious solution
                     |
             +-------+-------+
             |               |
          small enough?    too large?
             |               |
             v               v
       implement it       find repeated work
                             |
                             v
       hash? sort? prefix sum? two pointers? heap? DP?
                             |
                             v
                     re-calculate complexity
```

### Replacement Patterns

| Slow pattern | Common replacement |
|:---|:---|
| Nested search for membership | Set or dictionary |
| Repeated range sum | Prefix sums |
| All pairs for sorted data | Two pointers |
| Repeated minimum/maximum | Heap |
| Recomputing recursive states | Memoization or bottom-up DP |
| Repeated substring construction | Prefix structures, indices, or a list plus `join` |
| `pop(0)` queue | `collections.deque` |
| Repeated graph scan | Adjacency list and traversal |
| Compare every interval | Sort, sweep line, or interval structure |

---

## 15. Benchmarking: Useful but Not a Proof

A local benchmark can reveal constants and implementation mistakes, but it cannot replace complexity analysis.

```python
from time import perf_counter

start = perf_counter()
answer = solve(input_data)
elapsed = perf_counter() - start

print(f"elapsed: {elapsed:.3f}s")
```

### Why Local Timing Can Mislead

```text
    local computer != judge computer
    local input    != worst-case hidden input
    one run        != all test cases
    warm cache     != cold cache
```

Use benchmarks to compare two already-valid approaches or to detect a large constant factor. Do not use a fast small sample to justify an algorithm with the wrong worst-case growth.

### Stress Testing

Build tests near the maximum constraint:

```text
    tiny input       -> correctness
    random input     -> normal behavior
    sorted input     -> bad pivot / best-case traps
    reversed input   -> worst-case patterns
    maximum input    -> performance and memory
    empty/minimum    -> boundary behavior
```

---

## 16. Contest Pre-Submission Checklist

Before submitting, ask:

```text
    [ ] What exactly does n represent?
    [ ] Did I read every constraint?
    [ ] Is there a T test-case constraint?
    [ ] Is there a sum(n) constraint?
    [ ] What is my worst-case time complexity?
    [ ] What is my extra space complexity?
    [ ] Did I count hidden costs such as list membership or slicing?
    [ ] Are nested loops truly independent?
    [ ] Do pointers move only forward or backward once?
    [ ] Does an early exit improve the worst case or only the average case?
    [ ] Can the input force the maximum loop count?
    [ ] Is input/output a significant part of the work?
    [ ] Did I test the largest practical input?
```

### The Five-Second Estimate

For a new problem, quickly calculate:

```text
    maximum work = complexity formula evaluated at maximum constraints
```

Example:

```text
    n <= 2 * 10^5
    nested loops -> n^2
    n^2 = 4 * 10^10
    reject this approach
```

Then look for the repeated work and replace it with a data structure or a stronger algorithm.

---

## 17. Final Cheat Sheet

```text
    1. n is the input size, not a fixed constant.
    2. The maximum constraint represents the judge's hardest valid input.
    3. Big O describes growth, not exact seconds.
    4. Constants disappear in Big O notation but matter in real contests.
    5. Time limits and language determine the practical budget.
    6. Count hidden work inside library operations.
    7. Analyze the worst case when the solution must pass every input.
    8. Multiply by T unless a total sum constraint replaces it.
    9. Check both time and memory.
   10. Benchmark near the limit, but never replace analysis with a small test.
```

### Typical Target for `n <= 2 * 10^5`

```text
    preferred:      O(n), O(n log n)
    sometimes:      O(n sqrt n), depending on language and limit
    usually reject: O(n^2), O(2^n)
```

The goal is not to memorize one magic operation-per-second number. The goal is to connect the statement's limits to the amount of work your source code can perform in the worst case.

---

**Next Step:** Practice reading constraints first, predict the target complexity, and then solve classic contest patterns such as frequency counting, prefix sums, binary search, two pointers, sliding windows, graph traversal, and dynamic programming.
