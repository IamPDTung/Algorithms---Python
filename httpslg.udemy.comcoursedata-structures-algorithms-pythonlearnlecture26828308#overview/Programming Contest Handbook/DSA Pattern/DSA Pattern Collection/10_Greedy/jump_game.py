"""
Jump Game
You are given an integer array nums where nums[i] = maximum jump length from
position i. Return True if you can reach the last index.

Idea: greedily track the farthest index reachable. If any index is beyond the
farthest, you are stuck.

Time: O(n)
Space: O(1)
"""


def can_jump(nums):
    farthest = 0
    for i, jump in enumerate(nums):
        if i > farthest:
            return False
        farthest = max(farthest, i + jump)
    return True


if __name__ == "__main__":
    print(can_jump([2, 3, 1, 1, 4]))   # True
    print(can_jump([3, 2, 1, 0, 4]))   # False
