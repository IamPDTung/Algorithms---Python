"""
Largest Rectangle in Histogram
Given an array of heights, find the largest rectangle that can be formed by
contiguous bars.

Idea: for each bar, its rectangle width extends to the nearest smaller bar on
the left and the nearest smaller bar on the right. Compute both using a
monotonic (increasing) stack.

Time: O(n)
Space: O(n)
"""


def largest_rectangle_area(heights):
    n = len(heights)
    left = [0] * n
    right = [n - 1] * n

    stack = []                      # indices, increasing heights
    for i in range(n):
        while stack and heights[stack[-1]] >= heights[i]:
            stack.pop()
        left[i] = stack[-1] + 1 if stack else 0
        stack.append(i)

    stack = []
    for i in range(n - 1, -1, -1):
        while stack and heights[stack[-1]] >= heights[i]:
            stack.pop()
        right[i] = stack[-1] - 1 if stack else n - 1
        stack.append(i)

    best = 0
    for i in range(n):
        best = max(best, heights[i] * (right[i] - left[i] + 1))
    return best


if __name__ == "__main__":
    print(largest_rectangle_area([2, 1, 5, 6, 2, 3]))   # 10
    print(largest_rectangle_area([2, 4]))               # 4
