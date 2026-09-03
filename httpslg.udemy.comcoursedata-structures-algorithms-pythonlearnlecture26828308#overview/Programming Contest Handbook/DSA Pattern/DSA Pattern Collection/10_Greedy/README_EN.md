# GREEDY

## What is it?

A Greedy algorithm makes the **best local choice at each step**, hoping the sequence of
local optima produces the **global optimum**. No backtracking, no reconsidering — decide
once, move on. It works only when the problem has **greedy-choice property** (a local
best choice is always safe) and **optimal substructure**.

## Why use it?

- **Simple and fast** — O(n log n) or O(n).
- **Little/no extra memory**.
- Easy to reason about when the greedy choice is provably safe.

## When to use?

| Signal in the problem | Greedy choice |
|---|---|
| "Sorting helps / intervals" | sort by start/end, merge greedily |
| "Jump / reach the end" | always jump as far as possible |
| "Min/max tasks scheduling" | sort by deadline / frequency |
| "Can we always improve by taking the best next?" | local choice is safe |
| DP also works but greedy is simpler | use greedy when valid |

## Visualization — jump game

```
 nums = [2, 3, 1, 1, 4]
 index: 0   1   2   3   4

 At index 0, max reach = 0 + 2 = 2
 At index 1, max reach = max(2, 1 + 3) = 4  -> can reach the end!

 Greedy: track farthest reachable index; if i > farthest, stuck -> False
```

## Visualization — merge intervals

```
 intervals: [1,3] [2,6] [8,10] [15,18]
 after sort by start: [1,3] [2,6] [8,10] [15,18]

 [1,3] then [2,6]: 2 <= 3 -> merge -> [1,6]
 [1,6] then [8,10]: 8 > 6 -> new interval -> [8,10]
 [8,10] then [15,18]: 15 > 10 -> new -> [15,18]

 result: [[1,6], [8,10], [15,18]]
```

## Complexity

- **Time:** O(n log n) if sorting, else O(n)
- **Space:** O(1) or O(n) for output

## Template

```python
def greedy(items):
    items.sort(key=...)                 # sorting often enables greedy
    result = initial
    for item in items:
        if good_to_take(item):
            take it / update result     # local best choice
    return result
```

## Example problems solved in this folder

| Problem | File | Idea |
|---|---|---|
| Jump Game | `jump_game.py` | track farthest reach |
| Gas Station | `gas_station.py` | single pass, restart at deficit |
| Merge Intervals | `merge_intervals.py` | sort + merge overlaps |

## Practice

Try: Task Scheduler (greedy + counting), Non-overlapping Intervals, Candy,
Jump Game II, Interval Scheduling, Meeting Rooms II.
