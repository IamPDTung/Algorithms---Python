# HT: Two Sum ( ** Interview Question)
# two_sum()

# Problem:
# Given an array of integers nums and a target integer target, find the indices of two numbers in the array that add up to the target.

# The main challenge here is to implement this function in one pass through the array. This means you should not iterate over the array more than once. Therefore, your solution should have a time complexity of O(n), where n is the number of elements in nums.



# Input:

# A list of integers nums .

# A target integer target.



# Output:

# A list of two integers representing the indices of the two numbers in the input array nums that add up to the target. If no two numbers in the input array add up to the target, return an empty list [].



# Example:



# Input: nums = [5, 1, 7, 2, 9, 3], target = 10
# Output: [1, 4]
# Explanation: The numbers at indices 1 and 4 in the array add up to the target 10.

# Input: nums = [3, 2, 4], target = 6
# Output: [1, 2]
# Explanation: The numbers at indices 1 and 2 in the array add up to the target 6.

# Input: nums = [3, 3], target = 6
# Output: [0, 1]
# Explanation: The numbers at indices 0 and 1 in the array add up to the target 6.

# Input: nums = [2, 1, 2, 7, 11, 15], target = 9
# Output: [2, 3]
# Explanation: Notice there are two 2s in the array.  The second one will be used.

# Input: nums = [1, 2, 3, 4, 5], target = 10
# Output: []
# Explanation: There are no two numbers in the array add up to the target 10.

# Input: nums = [], target = 0
# Output: []
# Explanation: There are no numbers in the input array, so the function returns an empty list [].

# WRITE TWO_SUM FUNCTION HERE #
#                             #
#                             #
#                             #
#                             #
###############################




print(two_sum([5, 1, 7, 2, 9, 3], 10))
print(two_sum([4, 2, 11, 7, 6, 3], 9))
print(two_sum([10, 15, 5, 2, 8, 1, 7], 12))
print(two_sum([1, 3, 5, 7, 9], 10))
print ( two_sum([1, 2, 3, 4, 5], 10) )
print ( two_sum([1, 2, 3, 4, 5], 7) )
print ( two_sum([1, 2, 3, 4, 5], 3) )
print ( two_sum([], 0) )



"""
    EXPECTED OUTPUT:
    ----------------
    [1, 4]
    [1, 3]
    [0, 3]
    [1, 3]
    []
    [2, 3]
    [0, 1]
    []

"""
