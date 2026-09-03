"""
Search in Rotated Sorted Array
Given a rotated sorted array (e.g. [4,5,6,7,0,1,2]) with distinct values, find
the index of a target, or -1.

Idea: binary search. At each step at least one half is fully sorted. Check if
the target lies in the sorted half; if so search there, else search the other.

Time: O(log n)
Space: O(1)
"""


def search(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[lo] <= nums[mid]:          # left half sorted
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:                              # right half sorted
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1


if __name__ == "__main__":
    print(search([4, 5, 6, 7, 0, 1, 2], 0))   # 4
    print(search([4, 5, 6, 7, 0, 1, 2], 3))   # -1
    print(search([1], 0))                     # -1
