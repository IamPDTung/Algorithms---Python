# DSA Pattern Collection

> Master the 12 core DSA patterns: What, Why, How, Visualize, and Code.

## How to use this collection

Each pattern folder contains:

```
01_Hashing/
├── README_EN.md        # Full explanation (English)
├── README_VI.md        # Full explanation (Vietnamese)
├── two_sum.py          # Example solution
├── group_anagrams.py
└── ...
```

1. Read the **EN** (or **VI**) markdown file to understand the pattern.
2. Study the **ASCII visualization** — draw it yourself on paper.
3. Read the Python solutions and **dry-run** them with small inputs.
4. Re-implement from memory, then solve similar problems.

## Pattern index

| # | Pattern | Use when... | Time / Space |
|---|---------|-------------|--------------|
| 01 | [Hashing](./01_Hashing/README_EN.md) | Fast lookup, frequency count, duplicates | O(1) avg / O(n) |
| 02 | [Two Pointers](./02_Two_Pointers/README_EN.md) | Sorted arrays, pairs, reverse traversal | O(n) / O(1) |
| 03 | [Sliding Window](./03_Sliding_Window/README_EN.md) | Subarray / substring, longest / shortest | O(n) / O(k) |
| 04 | [Binary Search](./04_Binary_Search/README_EN.md) | Sorted data, monotonic property, can we eliminate half? | O(log n) / O(1) |
| 05 | [Monotonic Stack](./05_Monotonic_Stack/README_EN.md) | Next / previous greater or smaller | O(n) / O(n) |
| 06 | [Heap](./06_Heap/README_EN.md) | Top K, Kth largest / smallest, running median | O(log n) / O(n) |
| 07 | [Trees](./07_Trees/README_EN.md) | Hierarchical data, path / depth / subtree | O(n) / O(h) |
| 08 | [Graphs](./08_Graphs/README_EN.md) | Relationships, shortest path, cycles, ordering | O(V + E) / O(V) |
| 09 | [Backtracking](./09_Backtracking/README_EN.md) | Generate all possibilities | Exponential / O(n) |
| 10 | [Greedy](./10_Greedy/README_EN.md) | Local optimum → global optimum | O(n log n) or O(n) |
| 11 | [Dynamic Programming](./11_Dynamic_Programming/README_EN.md) | Overlapping subproblems, optimal substructure | Varies |
| 12 | [Union Find (DSU)](./12_Union_Find/README_EN.md) | Connected components, dynamic connectivity | O(α(n)) ~ O(1) |

## How to choose the right pattern?

```
Need fast lookup or counting?     -> HASHING
Sorted array?                     -> TWO POINTERS or BINARY SEARCH
Subarray / Substring?             -> SLIDING WINDOW
Next Greater / Smaller?           -> MONOTONIC STACK
Top K / Kth?                      -> HEAP
Tree structure?                   -> TREES
Graph problem?                    -> GRAPHS or UNION FIND
All possibilities?                -> BACKTRACKING
Optimization problem?             -> GREEDY or DP
```

## Golden rules

1. ✅ Understand the pattern, don't memorize the solution.
2. ✅ Solve similar problems to master the pattern.
3. ✅ Always analyze Time & Space complexity.
4. ✅ Dry-run before coding.
5. ★ PRACTICE. PRACTICE. PRACTICE.
