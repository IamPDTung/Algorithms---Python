"""
Subsets
Given an integer array nums of unique elements, return all possible subsets
(the power set).

Idea: backtracking with include / exclude choice for each element.

Time: O(2^n)
Space: O(n) recursion depth
"""


def subsets(nums):
    result = []
    path = []

    def backtrack(start):
        result.append(path[:])          # every prefix is a valid subset
        for i in range(start, len(nums)):
            path.append(nums[i])        # choose
            backtrack(i + 1)            # explore (only later elements)
            path.pop()                  # unchoose

    backtrack(0)
    return result


if __name__ == "__main__":
    print(subsets([1, 2, 3]))
    # [[], [1], [1, 2], [1, 2, 3], [1, 3], [2], [2, 3], [3]]
