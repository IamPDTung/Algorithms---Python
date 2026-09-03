# TREES

## What is it?

A Tree is a **hierarchical** data structure made of **nodes** connected by **edges**,
with a single **root**. Each node has children; nodes without children are **leaves**.
The **Binary Tree** (each node has at most 2 children) is the most common in problems.

Two fundamental ways to traverse:
- **DFS** — Preorder (root, left, right), Inorder (left, root, right),
  Postorder (left, right, root).
- **BFS / Level-order** — visit level by level.

## Why use it?

- Natural model for **hierarchical data** (filesystem, HTML, org charts, BST, heaps).
- Problems about **parent / child relations**, **path**, **depth / height**, **subtree**.
- Many problems decompose into: "solve for the root using answers from left & right
  subtrees" — a recursive pattern that visits every node once (**O(n)**).

## When to use?

| Signal in the problem | Why |
|---|---|
| "Binary tree", "BST" | tree structure given |
| "Path sum / depth / height / diameter" | recursion up the tree |
| "Lowest common ancestor" | DFS with up-propagation |
| "Level order" | BFS with a queue |
| "Subtree / serialization" | recursive comparison or flattening |

## Visualization — traversal orders

```
            1
          /   \
         2     3
        / \     \
       4   5     6

 Preorder:   1, 2, 4, 5, 3, 6     (root, left, right)
 Inorder:    4, 2, 5, 1, 3, 6     (left, root, right)
 Postorder:  4, 5, 2, 6, 3, 1     (left, right, root)
 BFS:        1, 2, 3, 4, 5, 6     (level by level)
```

## Visualization — diameter of a binary tree

```
 Diameter = longest path between any two nodes (in edges).

            1
           / \
          2   3
         / \
        4   5
       /     \
      6       7

 longest path: 6 -> 4 -> 2 -> 5 -> 7   (5 edges)
 computed as:  at node 2, leftHeight=2, rightHeight=2
               candidate = 2 + 2 = 4
               at node 1, leftHeight=3, rightHeight=0
               candidate = 3 + 0 = 3
 answer = max(4, 3) = 4? No—wait: recompute heights correctly:
 height(2) = 3 (via 6->4->2), height(5) = 2 -> path through 2 = 3 + 2 = 5
```

## Complexity

- **Time:** O(n) — each node visited once
- **Space:** O(h) — recursion stack, h = height (worst O(n) for skewed tree)

## Template (recursive DFS)

```python
def dfs(node):
    if node is None:
        return 0                    # base case
    left = dfs(node.left)
    right = dfs(node.right)
    return combine(left, right, node)   # combine into answer
```

## Example problems solved in this folder

| Problem | File | Idea |
|---|---|---|
| Lowest Common Ancestor | `lowest_common_ancestor.py` | recursive up-propagation |
| Diameter of Binary Tree | `diameter_of_binary_tree.py` | leftHeight + rightHeight |
| Serialize & Deserialize | `serialize_deserialize.py` | BFS with "null" markers |

## Practice

Try: Maximum Path Sum, Binary Tree Level Order Traversal, Validate BST,
Maximum Depth, Same Tree, Invert Tree.
