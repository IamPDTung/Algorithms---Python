# BACKTRACKING

## What is it?

Backtracking is a **systematic way to generate all possibilities** by building a solution
incrementally, piece by piece. At each step we **choose** an option, **explore** the
consequences recursively, and then **unchoose (backtrack)** to try the next option.
It's essentially DFS on a **decision tree**, with pruning when a partial solution
violates constraints.

**Template: Choose → Explore → Unchoose**

## Why use it?

- When the answer is **all combinations / permutations / subsets / configurations** and
  brute force (nested loops) can't adapt to variable depth.
- Natural for **constraint problems**: Sudoku, N-Queens, crossword, regex-like matching.
- The recursion stack gives an elegant "undo" mechanism for building paths.

## When to use?

| Signal in the problem | Why |
|---|---|
| "Generate all / find all ..." | enumerate every possibility |
| "Combinations / permutations / subsets" | choose from remaining elements |
| "Constraint satisfaction" | prune invalid partial solutions |
| "Grid / board exploration" | place & test (N-Queens, Sudoku) |

## Visualization — subsets of [1, 2]

```
                  []                       (start: empty set)
          include 1      exclude 1
          /                    \
        [1]                    []
        /  \                  /  \
  include2 exclude2      include2 exclude2
      /        \            /        \
   [1,2]      [1]        [2]         []

 All 4 subsets: [], [1], [2], [1,2]
 The recursion tree has 2^n leaves.
```

## Visualization — N-Queens (4x4), place queens row by row

```
 Q . . .     Q . . .     . Q . .     . Q . .
 . . Q .     . . . Q     Q . . .     . . . Q
 . . . Q     Q . . .     . . Q .     Q . . .
 . Q . .     . Q . .     . . . Q     . . Q .

 (4 valid solutions for 4-Queens; each queen checks column + both diagonals)
```

## Complexity

- **Time:** exponential — O(2^n) subsets, O(n!) permutations (pruning helps a lot)
- **Space:** O(n) recursion stack

## Template

```python
def backtrack(path, choices):
    if is_solution(path):
        add copy of path to result
        return
    for option in choices:
        if valid(path, option):
            path.append(option)      # choose
            backtrack(path, updated_choices)  # explore
            path.pop()               # unchoose (backtrack)
```

## Example problems solved in this folder

| Problem | File | Idea |
|---|---|---|
| Subsets | `subsets.py` | include / exclude each element |
| Combination Sum | `combination_sum.py` | unlimited reuse, sorted order |
| N-Queens | `n_queens.py` | place row by row, check conflicts |

## Practice

Try: Sudoku Solver, Permutations, Letter Combinations of a Phone Number,
Word Search, Palindrome Partitioning.
