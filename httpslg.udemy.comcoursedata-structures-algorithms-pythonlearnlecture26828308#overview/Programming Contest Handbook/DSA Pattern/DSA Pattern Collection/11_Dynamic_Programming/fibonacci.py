"""
Fibonacci — three DP styles
Show recursion -> memoization -> tabulation -> space optimization.

Time: O(n), Space: O(1) for the last version
"""

from functools import lru_cache


def fib_memo(n):
    @lru_cache(None)
    def f(k):
        if k < 2:
            return k
        return f(k - 1) + f(k - 2)
    return f(n)


def fib_tab(n):
    if n < 2:
        return n
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]


def fib_optimized(n):
    if n < 2:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


if __name__ == "__main__":
    for i in range(10):
        assert fib_memo(i) == fib_tab(i) == fib_optimized(i) == (
            0, 1, 1, 2, 3, 5, 8, 13, 21, 34)[i]
    print(fib_optimized(10))   # 55
    print("All versions agree for n = 0..9")
