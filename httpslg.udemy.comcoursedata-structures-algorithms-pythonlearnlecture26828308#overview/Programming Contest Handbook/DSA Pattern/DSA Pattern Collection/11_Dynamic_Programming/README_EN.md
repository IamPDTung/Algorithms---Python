# DYNAMIC PROGRAMMING (DP)

## What is it?

Dynamic Programming solves problems by breaking them into **overlapping subproblems**,
solving each **once**, and **reusing** the results. It requires two properties:
1. **Optimal substructure** — the optimal solution is built from optimal sub-solutions.
2. **Overlapping subproblems** — the same subproblem is solved many times.

**Approach:** Recursion → Memoization → Tabulation → Space Optimization.

## Why use it?

- Turns **exponential** solutions into **polynomial** (e.g. O(2^n) → O(n)).
- Best for **counting / max / min / ways** problems with repeated sub-computation.
- Works whenever you can define a state `dp[i]` and a recurrence `dp[i] = f(dp[i-1], ...)`.

## When to use?

| Signal in the problem | Why |
|---|---|
| "Maximum / minimum ... " | optimize over choices |
| "How many ways to ..." | count paths / combinations |
| "Can we reach ..." | reachability (boolean DP) |
| Recurrence / repeated subproblems | memoize / tabulate |
| "Subsequence / substring (non-contiguous)" | DP typical (unlike sliding window) |

## Visualization — Fibonacci with tabulation

```
 fib: 0 1 1 2 3 5 8
 dp[0]=0, dp[1]=1
 dp[2]=dp[1]+dp[0]=1
 dp[3]=dp[2]+dp[1]=2
 dp[4]=dp[3]+dp[2]=3
 ...

        ┌───────┐
 fib(5)│  = 5  │
        └───────┘
      /           \
  fib(4)=3     fib(3)=2
    /  \         /  \
 f(3)=2 f(2)=1 f(2)=1 f(1)=1
  / \
f(2)=1 f(1)=1        <- overlapping! solved once with memoization

 Without DP: fib(5) calls fib(2) 3 times -> O(2^n)
 With DP:    each state computed once -> O(n)
```

## Visualization — coin change (min coins to make amount)

```
 coins = [1, 2, 5], amount = 11
 dp[a] = min coins to make amount a

 dp[0] = 0
 dp[1] = 1 (1)
 dp[2] = 1 (2)
 dp[3] = 2 (1+2)
 ...
 dp[11] = min(dp[10]+1, dp[9]+1, dp[6]+1) = min(3, 3, 2+1=3) = 3  (5+5+1)

 recurrence: dp[a] = min(dp[a - c] + 1 for c in coins if a - c >= 0)
```

## Complexity

- **Time:** states × transitions (varies: O(n), O(n²), O(n×W)...)
- **Space:** O(states) → can often optimize to O(1) or O(n)

## Template

```python
# 1) Memoization (top-down)
from functools import lru_cache

@lru_cache(None)
def solve(state):
    if base_case(state):
        return ...
    best = min/max(solve(next_state) for next_state in moves(state))
    return best

# 2) Tabulation (bottom-up)
dp = [0] * (n + 1)
dp[0] = base
for i in range(1, n + 1):
    dp[i] = f(dp[i - 1], dp[i - 2], ...)
```

## Example problems solved in this folder

| Problem | File | Idea |
|---|---|---|
| Fibonacci | `fibonacci.py` | memo + tabulation + O(1) space |
| House Robber | `house_robber.py` | dp[i] = max(rob i, skip i) |
| Coin Change | `coin_change.py` | min coins for each amount |
| Longest Increasing Subsequence | `longest_increasing_subsequence.py` | dp[i] = best ending at i |

## Practice

Try: Edit Distance, Climbing Stairs, Unique Paths, 0/1 Knapsack, Partition Equal
Subset Sum, Word Break, Decode Ways.
