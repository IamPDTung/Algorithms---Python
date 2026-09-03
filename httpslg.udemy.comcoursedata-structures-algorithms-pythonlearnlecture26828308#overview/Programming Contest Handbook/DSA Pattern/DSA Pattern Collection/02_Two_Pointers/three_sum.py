"""
3Sum
Find all unique triplets in the array which gives the sum of zero.

Idea: sort, fix the first element, then two pointers for the remaining pair.
Skip duplicates.

Time: O(n^2)
Space: O(1) extra (besides output)
"""


def three_sum(nums):
    nums.sort()
    result = []
    n = len(nums)
    for i in range(n - 2):
        if i > 0 and nums[i] == nums[i - 1]:
            continue  # skip duplicate first element
        target = -nums[i]
        left, right = i + 1, n - 1
        while left < right:
            s = nums[left] + nums[right]
            if s == target:
                result.append([nums[i], nums[left], nums[right]])
                left += 1
                right -= 1
                while left < right and nums[left] == nums[left - 1]:
                    left += 1
                while left < right and nums[right] == nums[right + 1]:
                    right -= 1
            elif s < target:
                left += 1
            else:
                right -= 1
    return result


if __name__ == "__main__":
    print(three_sum([-1, 0, 1, 2, -1, -4]))  # [[-1, -1, 2], [-1, 0, 1]]
    print(three_sum([0, 0, 0]))              # [[0, 0, 0]]
