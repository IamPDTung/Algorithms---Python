"""
Maximum Average Subarray
Given an integer array nums and an integer k, find a contiguous subarray of
length k that has the maximum average value, and return the max average.

Idea: fixed-size sliding window of size k. Maintain running sum; slide by
adding the new element and subtracting the old one.

Time: O(n)
Space: O(1)
"""


def find_max_average(nums, k):
    window_sum = sum(nums[:k])
    best = window_sum
    for right in range(k, len(nums)):
        window_sum += nums[right] - nums[right - k]
        best = max(best, window_sum)
    return best / k


if __name__ == "__main__":
    print(find_max_average([1, 12, -5, -6, 50, 3], 4))  # 12.75
    print(find_max_average([5], 1))                     # 5.0
