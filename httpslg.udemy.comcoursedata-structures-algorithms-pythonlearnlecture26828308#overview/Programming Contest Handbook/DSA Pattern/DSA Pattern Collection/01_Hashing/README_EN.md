# HASHING

## What is it?

Hashing is a technique that maps keys to values using a **hash function**, storing them
in a **hash table** (dictionary in Python, `dict`). The hash function computes an index
from the key, giving **O(1) average** access — insert, lookup, and delete.

Python data structures:
- `dict` (HashMap) — key → value pairs
- `set` (HashSet) — unique keys only

## Why use it?

- **Fast lookup / membership check** — check if an element exists in O(1).
- **Frequency counting** — count how many times each element appears.
- **Duplicate detection** — track what we have already seen.
- **Pair / complement problems** — find `b` such that `a + b = target` using `target - a`.

## When to use?

| Signal in the problem | Why |
|---|---|
| "Find if an element exists" | O(1) membership via `set` |
| "Count frequency of elements" | `dict` value = count |
| "Find duplicates" | `set` of seen items |
| "Find pair that sums to target" | store complement in `dict` |
| "Group by key" | `dict` key → list of items |

## How it works (visualization)

Hash function `h(k) = k % 7` maps keys to buckets:

```
 Keys                 Hash table (array of buckets)
 ─────                ─────────────────────────────────
  42 ── h(42) ──► 0: [42]
  15 ── h(15) ──► 1: [15]
  29 ── h(29) ──► 2: []      <-- 29 % 7 = 1? No...
  34 ── h(34) ──► 3: [34]

 But 29 % 7 = 1, same as 15!  -> COLLISION (chaining)
 ─────────────────────────────────────────────────────
  15 ──► 1: [15] -> [29]      (linked list, chaining)

 Lookup 29:  compute h(29) = 1, walk bucket 1 -> found in O(1 + len)
```

Two Sum — the classic pairing idea:

```
 nums = [2, 7, 11, 15],  target = 9

 step 1: x = 2  -> need 9 - 2 = 7  (not seen, store {2: 0})
 step 2: x = 7  -> need 9 - 7 = 2  (SEEN at index 0!) -> answer (0, 1)

 seen = { 2:0, 7:1, 11:2, 15:3 }
```

## Complexity

- **Time:** O(1) average per operation (worst O(n) with collisions, rare)
- **Space:** O(n) for the table

## Template

```python
# 1) Frequency count
freq = {}
for x in nums:
    freq[x] = freq.get(x, 0) + 1

# 2) Duplicate / complement
seen = set()          # or dict {value: index}
for x in nums:
    complement = target - x
    if complement in seen:
        return ...    # found the pair
    seen.add(x)
```

## Example problems solved in this folder

| Problem | File | Idea |
|---|---|---|
| Two Sum | `two_sum.py` | store complement in dict |
| Group Anagrams | `group_anagrams.py` | sorted word as key |
| Longest Consecutive Sequence | `longest_consecutive_sequence.py` | `set` + look left neighbor |

## Practice

Try: Top K Frequent Elements, Contains Duplicate, Valid Anagram, Intersection of Two Arrays.
