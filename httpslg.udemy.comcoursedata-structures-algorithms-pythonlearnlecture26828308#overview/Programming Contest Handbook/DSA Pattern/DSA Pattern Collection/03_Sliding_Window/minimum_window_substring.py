"""
Minimum Window Substring
Given two strings s and t, return the minimum window substring of s such that
every character in t (including duplicates) is included in the window.

Idea: variable sliding window. Track how many required chars the window has
covered. Expand right; when all covered, shrink left to minimize length.

Time: O(n + m)
Space: O(|alphabet|)
"""


def min_window(s, t):
    if not s or not t:
        return ""
    need = {}
    for ch in t:
        need[ch] = need.get(ch, 0) + 1

    have = {}
    required = len(need)
    formed = 0
    left = 0
    best_len = float("inf")
    best_left = 0

    for right, ch in enumerate(s):
        have[ch] = have.get(ch, 0) + 1
        if ch in need and have[ch] == need[ch]:
            formed += 1

        while formed == required and left <= right:
            if right - left + 1 < best_len:
                best_len = right - left + 1
                best_left = left
            have[s[left]] -= 1
            if s[left] in need and have[s[left]] < need[s[left]]:
                formed -= 1
            left += 1

    return "" if best_len == float("inf") else s[best_left:best_left + best_len]


if __name__ == "__main__":
    print(min_window("ADOBECODEBANC", "ABC"))   # "BANC"
    print(min_window("a", "a"))                 # "a"
    print(min_window("a", "aa"))                # ""
