"""
Group Anagrams
Given a list of strings, group the anagrams together.

Idea: anagrams are the same when their characters are sorted.
Use the sorted string as the hash key.

Time: O(n * k log k) where k = max word length
Space: O(n * k)
"""

from collections import defaultdict


def group_anagrams(strs):
    groups = defaultdict(list)
    for s in strs:
        key = "".join(sorted(s))
        groups[key].append(s)
    return list(groups.values())


if __name__ == "__main__":
    print(group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"]))
    # [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]
    print(group_anagrams([""]))   # [[""]]
    print(group_anagrams(["a"]))  # [["a"]]
