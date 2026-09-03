"""
Longest Substring Without Repeating Characters
Given a string s, find the length of the longest substring without repeating
characters.

Idea: sliding window. Keep a set of chars currently in the window. When a
duplicate appears, shrink from the left until the window is valid again.

Time: O(n)
Space: O(min(n, alphabet))
"""


def length_of_longest_substring(s):
    seen = set()
    left = 0
    best = 0
    for right, ch in enumerate(s):
        while ch in seen:
            seen.remove(s[left])
            left += 1
        seen.add(ch)
        best = max(best, right - left + 1)
    return best


if __name__ == "__main__":
    print(length_of_longest_substring("abcabcbb"))   # 3  ("abc")
    print(length_of_longest_substring("bbbbb"))      # 1
    print(length_of_longest_substring("pwwkew"))     # 3  ("wke")
