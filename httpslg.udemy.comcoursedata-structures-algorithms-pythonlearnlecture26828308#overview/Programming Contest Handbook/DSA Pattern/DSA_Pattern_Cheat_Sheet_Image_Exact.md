# DSA PATTERN CHEAT SHEET

> How to Identify the Right Algorithm in Seconds

---

# 1. HASHING

## When to use?
- Fast lookup
- Frequency count
- Duplicate detection
- Pair / complement problems

## DS
- HashMap
- HashSet

## Examples
- Two Sum
- Group Anagrams
- Top K Frequent Elements
- Longest Consecutive Sequence

**Time:** O(1) avg  
**Space:** O(n)

---

# 2. TWO POINTERS

## When to use?
- Sorted array / list
- Pair problems
- Remove duplicates
- Reverse traversal

## Examples
- 3Sum
- Container With Most Water
- Valid Palindrome
- Remove Duplicates from Sorted Array

**Time:** O(n)  
**Space:** O(1)

---

# 3. SLIDING WINDOW

## When to use?
- Subarray / Substring
- Longest / Shortest
- Fixed / Variable window

## Examples
- Longest Substring Without Repeating Chars
- Minimum Window Substring
- Maximum Average Subarray
- Permutation in String

**Time:** O(n)  
**Space:** O(k)

> k = window size

---

# 4. BINARY SEARCH

## When to use?
- Sorted data
- Monotonic property
- Find min / max answer
- Can we eliminate half?

## Examples
- Search in Rotated Sorted Array
- Koko Eating Bananas
- Find Peak Element
- Median of Two Sorted Arrays

**Time:** O(log n)  
**Space:** O(1)

---

# 5. MONOTONIC STACK

## When to use?
- Next Greater / Smaller
- Previous Greater / Smaller
- Histogram problems
- Resolve in linear time

## Examples
- Daily Temperatures
- Next Greater Element
- Largest Rectangle in Histogram
- Trapping Rain Water

**Time:** O(n)  
**Space:** O(n)

---

# 6. HEAP (PRIORITY QUEUE)

## When to use?
- Top K elements
- Kth largest / Smallest
- Merge K sorted lists
- Running median

## Examples
- Top K Frequent Elements
- Kth Largest Element in Array
- Merge K Sorted Lists
- Find Median from Data Stream

**Time:** O(log n)  
**Space:** O(n)

---

# 7. TREES

## When to use?
- Hierarchical data
- Parent / Child relation
- Path / Depth / Height
- Subtree problems

## Traversals
- DFS (Pre, In, Post)
- BFS (Level Order)

## Examples
- Lowest Common Ancestor
- Diameter of Binary Tree
- Maximum Path Sum
- Serialize / Deserialize Tree

**Time:** O(n)  
**Space:** O(h)

> h = height

---

# 8. GRAPHS

## When to use?
- Relationship / Connection
- Cycle detection
- Shortest path
- Topological order

## Algorithms
- DFS
- BFS
- Dijkstra
- Topological Sort
- Union Find

## Examples
- Number of Islands
- Course Schedule
- Network Delay Time
- Clone Graph

**Time:** O(V + E)  
**Space:** O(V)

---

# 9. BACKTRACKING

## When to use?
- Generate all possibilities
- Combinations / Permutations
- Constraint problems

## Template
- Choose → Explore → Unchoose (Backtrack)

## Examples
- Subsets
- Combination Sum
- Sudoku Solver
- N-Queens

**Time:** Exponential  
**Space:** O(n) (recursion stack)

---

# 10. GREEDY

## When to use?
- Local optimum leads to global optimum
- Sorting helps

## Examples
- Jump Game
- Gas Station
- Task Scheduler
- Merge Intervals

**Time:** O(n log n) or O(n)  
**Space:** O(1) (depends)

---

# 11. DYNAMIC PROGRAMMING

## When to use?
- Overlapping subproblems
- Optimal substructure
- Count / Max / Min ways

## Approach
Recursion → Memoization → Tabulation

↓

Space Optimization

## Examples
- Fibonacci
- House Robber
- Longest Increasing Subsequence
- Edit Distance
- Coin Change

**Time:** Varies  
**Space:** Varies

---

# 12. UNION FIND (DSU)

## When to use?
- Connected components
- Dynamic connectivity
- Cycle detection in undirected graph

## Operations
- Find (with path compression)
- Union (by rank / size)

## Examples
- Redundant Connection
- Number of Provinces
- Accounts Merge

**Time:** O(α(n)) ~ O(1)  
**Space:** O(n)

---

# HOW TO CHOOSE THE RIGHT PATTERN?

```text
Need fast lookup or counting?
    Yes -> HASHING

Sorted array?
    Yes -> TWO POINTERS
           or BINARY SEARCH

Subarray / Substring?
    Yes -> SLIDING WINDOW

Next Greater / Smaller?
    Yes -> MONOTONIC STACK

Top K / Kth?
    Yes -> HEAP

Tree structure?
    Yes -> TREES

Graph problem?
    Yes -> GRAPHS
           or UNION FIND

All possibilities?
    Yes -> BACKTRACKING

Optimization problem?
    Yes -> GREEDY
           or DP
```

---

# TIPS

✅ Understand the pattern, don't memorize the solution.

✅ Solve similar problems to master the pattern.

✅ Analyze Time & Space Complexity.

✅ Dry run before coding.

★ PRACTICE. PRACTICE. PRACTICE.
