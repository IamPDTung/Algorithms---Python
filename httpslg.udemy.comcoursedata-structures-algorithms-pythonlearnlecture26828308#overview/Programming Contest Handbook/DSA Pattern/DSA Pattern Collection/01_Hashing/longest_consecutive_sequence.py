"""
Longest Consecutive Sequence
Given an unsorted array of integers, return the length of the longest
consecutive elements sequence.

Idea: put all numbers in a set. A number starts a new sequence only if
num - 1 is NOT in the set. Then count forward.

Time: O(n)
Space: O(n)
"""


def longest_consecutive(nums):
    num_set = set(nums)
    best = 0
    for x in num_set:
        if x - 1 not in num_set:      # x is the start of a sequence
            length = 1
            while x + length in num_set:
                length += 1
            best = max(best, length)
    return best


if __name__ == "__main__":
    print(longest_consecutive([100, 4, 200, 1, 3, 2]))   # 4  (1,2,3,4)
    print(longest_consecutive([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]))  # 9
