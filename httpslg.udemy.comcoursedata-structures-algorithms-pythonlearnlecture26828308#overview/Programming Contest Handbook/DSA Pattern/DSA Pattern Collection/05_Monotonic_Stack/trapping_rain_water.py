"""
Trapping Rain Water
Given n non-negative integers representing an elevation map where the width of
each bar is 1, compute how much water it can trap after raining.

Idea (two pointers, O(1) space): water above a bar = min(maxLeft, maxRight) - h.
Move the pointer with the smaller side wall inward.

Time: O(n)
Space: O(1)
"""


def trap(height):
    if not height:
        return 0
    left, right = 0, len(height) - 1
    left_max = right_max = 0
    total = 0
    while left < right:
        if height[left] <= height[right]:
            if height[left] >= left_max:
                left_max = height[left]
            else:
                total += left_max - height[left]
            left += 1
        else:
            if height[right] >= right_max:
                right_max = height[right]
            else:
                total += right_max - height[right]
            right -= 1
    return total


if __name__ == "__main__":
    print(trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]))   # 6
    print(trap([4, 2, 0, 3, 2, 5]))                      # 9
