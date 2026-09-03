"""
Combination Sum
Given an array of distinct integers candidates and a target, return all unique
combinations where the numbers sum to target. The same number may be used an
unlimited number of times.

Idea: backtracking. To avoid duplicate combinations, only use candidates at or
after the current index.

Time: O(2^(t/m)) in practice (pruned by target), Space: O(t/m)
"""


def combination_sum(candidates, target):
    result = []
    path = []

    def backtrack(start, remaining):
        if remaining == 0:
            result.append(path[:])
            return
        for i in range(start, len(candidates)):
            c = candidates[i]
            if c > remaining:
                continue
            path.append(c)                 # choose
            backtrack(i, remaining - c)    # explore (can reuse same index)
            path.pop()                     # unchoose

    backtrack(0, target)
    return result


if __name__ == "__main__":
    print(combination_sum([2, 3, 6, 7], 7))   # [[2, 2, 3], [7]]
    print(combination_sum([2, 3, 5], 8))      # [[2, 2, 2, 2], [2, 3, 3], [3, 5]]
