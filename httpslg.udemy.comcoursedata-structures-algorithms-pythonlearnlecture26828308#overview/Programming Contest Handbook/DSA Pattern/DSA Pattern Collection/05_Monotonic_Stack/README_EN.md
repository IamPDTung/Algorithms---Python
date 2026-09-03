# MONOTONIC STACK

## What is it?

A Monotonic Stack is a **stack that keeps its elements in sorted order** (strictly
increasing or strictly decreasing) at all times. Before pushing a new element, we
**pop all elements that violate the order**. Because each element is pushed once and
popped once, the total work is **O(n)** — this is why it resolves "next greater/smaller"
type problems in linear time.

## Why use it?

- Naive "for each element, scan the rest" is **O(n²)**. Monotonic stack makes it **O(n)**.
- It answers: for each index, the **next** (or previous) **greater** (or smaller) element.
- Great for **histogram / area** problems where a bar's extent depends on nearest
  smaller bars on both sides.

## When to use?

| Signal in the problem | Why |
|---|---|
| "Next / previous greater element" | classic use |
| "Next / previous smaller element" | same idea, inverted order |
| "Histogram / max rectangle area" | nearest smaller left & right |
| "Trapping rain water" | nearest higher boundaries |
| Nested / bracket-like structure | monotonic stack keeps useful history |

## Visualization — next greater element

```
 nums = [2, 1, 4, 3]
                result (next greater)
  index 0: 2 -> 4
  index 1: 1 -> 4
  index 2: 4 -> -1
  index 3: 3 -> -1

 Stack holds indices with decreasing values (bottom -> top): smaller on top.

 Step i=0: stack []  -> push 0      stack: [0]      (value 2)
 Step i=1: nums[1]=1 < 2 -> push 1  stack: [0,1]    (2,1)
 Step i=2: nums[2]=4 > 1 -> pop 1,  result[1]=4
           nums[2]=4 > 2 -> pop 0,  result[0]=4
           push 2                  stack: [2]       (4)
 Step i=3: nums[3]=3 < 4 -> push 3  stack: [2,3]
 Done: remaining stack elements have no greater -> -1
```

```
 2  1  4  3
 |  |  |  |
 |  |  |  -1
 |  |  4
 |  4
 4
```

## Complexity

- **Time:** O(n) — each element pushed once, popped once
- **Space:** O(n) — the stack

## Template (next greater element)

```python
result = [-1] * len(nums)
stack = []                     # indices, decreasing values
for i, x in enumerate(nums):
    while stack and nums[stack[-1]] < x:   # x is greater than stack top
        result[stack.pop()] = x
    stack.append(i)
```

## Example problems solved in this folder

| Problem | File | Idea |
|---|---|---|
| Daily Temperatures | `daily_temperatures.py` | next warmer day = next greater index |
| Largest Rectangle in Histogram | `largest_rectangle_histogram.py` | nearest smaller left & right |
| Trapping Rain Water | `trapping_rain_water.py` | bounded by min(max left, max right) |

## Practice

Try: Next Greater Element I/II, Sum of Subarray Minimums, Remove K Digits,
Asteroid Collision.
