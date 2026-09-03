"""
Container With Most Water
Find two lines that together with the x-axis form a container holding the
most water. height[i] = height of line at position i.

Idea: start with widest container. Water = width * min(left, right).
Always move the SHORTER wall inward because the shorter one limits the water.

Time: O(n)
Space: O(1)
"""


def max_area(height):
    left, right = 0, len(height) - 1
    best = 0
    while left < right:
        h = min(height[left], height[right])
        best = max(best, (right - left) * h)
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    return best


if __name__ == "__main__":
    print(max_area([1, 8, 6, 2, 5, 4, 8, 3, 7]))  # 49
    print(max_area([1, 1]))                        # 1
