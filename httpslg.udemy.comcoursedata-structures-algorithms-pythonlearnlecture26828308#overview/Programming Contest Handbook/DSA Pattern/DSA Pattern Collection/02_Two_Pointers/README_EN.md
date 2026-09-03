# TWO POINTERS

## What is it?

Two Pointers uses **two indices (pointers)** that move through the data structure —
usually an array — from opposite ends or at different speeds, to solve the problem
in a **single pass**. Instead of nested loops (O(n²)), each element is touched at
most a few times.

## Why use it?

- Turns **O(n²) nested loops into O(n)**.
- **No extra memory** — operates in place, O(1) space.
- Natural fit for **sorted arrays** where direction is meaningful.

## When to use?

| Signal in the problem | Why |
|---|---|
| Array is **sorted** | move left/right based on sum comparison |
| "Find a pair / triplet" | sum too big → move right, too small → move left |
| "Remove duplicates in place" | slow pointer keeps position |
| "Reverse / palindrome" | compare from both ends |
| Need O(1) space | no hash table allowed |

## Two pointer styles

**1) Opposite ends (squeeze)**

```
 nums = [-4, -1, 0, 1, 2, 5]   target sum = 3
        ┌───────────────────────────────┐
 left = 0                          right = n-1

 sum = -4 + 5 = 1  < 3   -> too small, move left  →
 sum = -1 + 5 = 4  > 3   -> too big,   move right ←
 sum = -1 + 2 = 1  < 3   -> too small, move left  →
 sum =  0 + 2 = 2  < 3   -> too small, move left  →
 sum =  1 + 2 = 3  == 3  -> FOUND (indices 3, 5)
```

**2) Same direction (slow & fast)**

```
 Remove duplicates:  nums = [0, 0, 1, 1, 1, 2, 2, 3]
                            s
                            f
   nums[f] != nums[s]  -> s++, copy nums[s] = nums[f]
 result: [0, 1, 2, 3]
```

**3) Palindrome check (compare ends)**

```
 "racecar"
  l →             ← r
  r == r, a == a, c == c ... -> palindrome
```

## Complexity

- **Time:** O(n) — each pointer moves at most n times
- **Space:** O(1)

## Template (opposite ends)

```python
left, right = 0, len(arr) - 1
while left < right:
    if condition(arr[left], arr[right]):
        # move right inward (need smaller)
        right -= 1
    elif condition(arr[left], arr[right]):
        # move left forward (need bigger)
        left += 1
    else:
        # found what we need
        break
```

## Example problems solved in this folder

| Problem | File | Idea |
|---|---|---|
| 3Sum | `three_sum.py` | sort + fix one, two pointers for the rest |
| Container With Most Water | `container_with_most_water.py` | move the shorter wall inward |
| Valid Palindrome | `valid_palindrome.py` | compare from both ends |

## Practice

Try: Remove Duplicates from Sorted Array, Trapping Rain Water, Two Sum II, Sort Colors.
