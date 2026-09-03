# BINARY SEARCH

## What is it?

Binary Search finds a target in a **sorted** collection by repeatedly **eliminating
half** of the search space. It compares the target with the middle element and decides
which half to keep. This gives **O(log n)** time — each step halves the problem.

Two flavors:
1. **Classic search** — target exists in sorted array.
2. **Answer on monotonic predicate** — "find the smallest/largest x such that f(x) is true".

## Why use it?

- **O(log n)** beats O(n) scanning on large data (n = 1,000,000 → ~20 steps).
- Works whenever you can ask "can we eliminate half?" of the search space.
- **Search space on an answer value** (like "minimum speed", "minimum days") — even when
  the array itself isn't sorted, as long as the feasibility function is monotonic.

## When to use?

| Signal in the problem | Why |
|---|---|
| "Sorted array" | classic half-elimination |
| "Find min/max answer" | binary search the answer |
| "Monotonic / non-decreasing property" | predicate is True then False (or reverse) |
| "Can we eliminate half?" | guarantee each step discards half |
| Large constraints | O(n) too slow, need O(log n) |

## Visualization — classic search for 23 in sorted array

```
 index:  0   1   2   3   4   5   6
 value:  3   7   9  15  23  30  42
        lo              mid          hi
                       (15)

 15 < 23  -> search RIGHT half: eliminate [0..3]
                  lo      mid    hi
                 (23)        (42)
         index 4..6, mid=5 (30)
 30 > 23  -> search LEFT half: eliminate [5..6]
            lo=4 hi=4 mid=4 (23)  -> FOUND!

 Steps: 7 elements -> found in 3 comparisons
```

## Visualization — binary search the answer (Koko eating bananas)

```
 piles = [3, 6, 7, 11], h = 8.  Speed can be 1..11.
 f(speed) = "can finish in <= 8 hours"  (monotonic: faster => easier)

 speed: 1  2  3  4 ... 11
 f:     F  F  T  T ...  T        <-- find FIRST True

 lo=1, hi=11
 mid=6 -> f(6)=True  -> hi=6 (maybe smaller works)
 mid=3 -> f(3)=True  -> hi=3
 mid=2 -> f(2)=False -> lo=3
 answer = 3  (minimum speed that works)
```

## Complexity

- **Time:** O(log n)
- **Space:** O(1)

## Template (search the answer)

```python
def feasible(x):   # monotonic predicate
    ...

lo, hi = 0, MAX      # search range
while lo < hi:
    mid = (lo + hi) // 2
    if feasible(mid):
        hi = mid     # mid works, try smaller (for "first True")
    else:
        lo = mid + 1
return lo
```

## Example problems solved in this folder

| Problem | File | Idea |
|---|---|---|
| Search in Rotated Sorted Array | `search_rotated_sorted_array.py` | find pivot or branch by sorted half |
| Koko Eating Bananas | `koko_eating_bananas.py` | binary search the speed |
| Find Peak Element | `find_peak_element.py` | move toward the higher neighbor |

## Practice

Try: Median of Two Sorted Arrays, Search Insert Position, First Bad Version,
Minimum in Rotated Sorted Array, Split Array Largest Sum.
