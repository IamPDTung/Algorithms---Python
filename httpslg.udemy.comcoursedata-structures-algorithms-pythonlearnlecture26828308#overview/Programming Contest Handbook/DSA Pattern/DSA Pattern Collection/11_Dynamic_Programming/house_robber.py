"""
House Robber
Given an array of money in houses (cannot rob two adjacent houses), return the
maximum amount you can rob tonight.

Idea: dp[i] = max(dp[i-1] (skip i), dp[i-2] + nums[i] (rob i)).
Can be space-optimized to two variables.

Time: O(n)
Space: O(1)
"""


def rob(nums):
    prev2, prev1 = 0, 0     # dp[i-2], dp[i-1]
    for x in nums:
        cur = max(prev1, prev2 + x)
        prev2, prev1 = prev1, cur
    return prev1


if __name__ == "__main__":
    print(rob([1, 2, 3, 1]))        # 4  (1 + 3)
    print(rob([2, 7, 9, 3, 1]))     # 12 (2 + 9 + 1)
