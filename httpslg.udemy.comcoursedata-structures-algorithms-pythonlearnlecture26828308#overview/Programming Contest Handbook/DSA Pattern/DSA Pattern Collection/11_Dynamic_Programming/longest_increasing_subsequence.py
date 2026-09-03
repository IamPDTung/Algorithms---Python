"""
Longest Increasing Subsequence
Given an integer array nums, return the length of the longest strictly increasing
subsequence.

Idea (O(n^2)): dp[i] = length of LIS ending at index i.
dp[i] = 1 + max(dp[j] for j < i if nums[j] < nums[i]).
The answer is max(dp).

Time: O(n^2)
Space: O(n)
"""


def length_of_lis(nums):
    n = len(nums)
    dp = [1] * n
    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp) if n else 0


if __name__ == "__main__":
    print(length_of_lis([10, 9, 2, 5, 3, 7, 101, 18]))   # 4  (2,3,7,101)
    print(length_of_lis([0, 1, 0, 3, 2, 3]))             # 4
    print(length_of_lis([7, 7, 7, 7, 7, 7, 7]))          # 1
