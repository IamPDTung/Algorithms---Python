"""
Valid Palindrome
A phrase is a palindrome if, after converting all uppercase letters into
lowercase and removing all non-alphanumeric characters, it reads the same
forward and backward.

Idea: two pointers from both ends, skip non-alphanumeric characters.

Time: O(n)
Space: O(1)
"""


def is_palindrome(s):
    left, right = 0, len(s) - 1
    while left < right:
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1
        if s[left].lower() != s[right].lower():
            return False
        left += 1
        right -= 1
    return True


if __name__ == "__main__":
    print(is_palindrome("A man, a plan, a canal: Panama"))  # True
    print(is_palindrome("race a car"))                      # False
    print(is_palindrome(" "))                               # True
