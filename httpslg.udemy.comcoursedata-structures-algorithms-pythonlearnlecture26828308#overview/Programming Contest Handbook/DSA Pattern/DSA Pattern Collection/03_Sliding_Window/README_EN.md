# SLIDING WINDOW

## What is it?

Sliding Window maintains a **contiguous window** (subarray / substring) and **slides**
its right edge in, while shrinking its left edge when needed, to keep a window that
satisfies the problem's condition. It converts problems that naively check every
subarray (O(n²)) into a **single pass O(n)**.

## Why use it?

- **Subarray / substring problems** usually want longest / shortest / count of windows.
- Recomputing every window from scratch is wasteful — a slide only adds/removes one
  element at each step, so the window state is **updated incrementally**.
- Two styles: **fixed-size window** and **variable-size window**.

## When to use?

| Signal in the problem | Style |
|---|---|
| "Longest substring/subarray ..." | variable window (expand, then shrink) |
| "Shortest substring ... containing ..." | variable window |
| "... of size k ..." | fixed window |
| "At most / at least k ..." | variable window |
| Contiguous segment | window (not subsequence!) |

## Visualization — variable window (longest substring w/o repeating chars)

```
 s = "a b c a b c b b"        window chars: a b c
        L R                   longest = 3

 "a b c a" -> duplicate 'a', shrink L
        L   R
  L moves past first 'a': "b c a"   longest stays 3

 "b c a b" -> duplicate 'b', shrink L -> "c a b"
                L R

 ...keep sliding; longest stays 3. Final answer: 3
```

Window = the segment between `L` (left) and `R` (right). At every step we add
`R` and possibly drop from `L`:

```
 Fixed window k = 3, array [2, 1, 5, 1, 3, 2]
 max sum window:
  [2 1 5] -> 8
   [1 5 1] -> 7
    [5 1 3] -> 9   <-- max
     [1 3 2] -> 6

  slide: add new right, subtract old left
  sum += nums[right] - nums[right - k]
```

## Complexity

- **Time:** O(n) — each element enters once, leaves once
- **Space:** O(k) or O(|alphabet|) depending on what the window stores

## Template (variable window)

```python
left = 0
best = 0
window_state = {}          # or a count structure
for right in range(len(s)):
    add s[right] to window_state
    while window invalid:      # shrink from the left
        remove s[left] from window_state
        left += 1
    best = max(best, right - left + 1)
return best
```

## Example problems solved in this folder

| Problem | File | Idea |
|---|---|---|
| Longest Substring Without Repeating | `longest_substring_without_repeating.py` | set of chars in window |
| Minimum Window Substring | `minimum_window_substring.py` | counts + need counter |
| Maximum Average Subarray | `maximum_average_subarray.py` | fixed window of size k |

## Practice

Try: Permutation in String, Longest Repeating Character Replacement, Fruit Into Baskets,
Maximum Sum of Distinct Subarrays With Length K.
