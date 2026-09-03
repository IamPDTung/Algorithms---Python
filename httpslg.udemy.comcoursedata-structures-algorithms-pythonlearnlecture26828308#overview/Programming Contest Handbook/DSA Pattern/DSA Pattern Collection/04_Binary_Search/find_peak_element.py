"""
Find Peak Element
A peak element is strictly greater than its neighbors. Given an array, return
an index of any peak. (nums[-1] = nums[n] = -infinity.)

Idea: binary search. If nums[mid] < nums[mid+1], a peak exists to the right
(we are on an ascending slope); otherwise a peak exists to the left.

Time: O(log n)
Space: O(1)
"""


def find_peak_element(nums):
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] < nums[mid + 1]:
            lo = mid + 1
        else:
            hi = mid
    return lo


if __name__ == "__main__":
    print(find_peak_element([1, 2, 3, 1]))      # 2 (value 3)
    print(find_peak_element([1, 2, 1, 3, 5, 6, 4]))  # 5 (value 6)
    print(find_peak_element([1]))               # 0
