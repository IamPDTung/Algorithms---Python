
---

# N-ary Tree Recursive and Level Traversal

## 1. Goal

An N-ary tree is an extension of a binary tree: each node can have any
number of children. Its traversal is an extension of binary tree traversal
with two forms only: recursive traversal (DFS) and level order traversal
(BFS). This guide implements both, plus the three standard level-order
variants, and explains the forest concept.

The implementation in `NaryTreeTraversal.py` provides:

- A `Node` class with `children` and a LeetCode-format builder.
- The DFS framework with pre-order and post-order positions.
- Level order Method One (queue with level size), Method Two (recursive
  DFS with depth), and Method Three (weighted queue with depth state).
- A `forest_preorder` helper that traverses every root in a forest.
- Randomized checks proving the three level-order methods agree.

Source references:

- [N-ary Tree Recursive/Level Traversal](https://labuladong.online/en/algo/data-structure-basic/n-ary-tree-traverse-basic/)
- [Binary Tree Recursive/Level Traversal](https://labuladong.online/en/algo/data-structure-basic/binary-tree-traverse-basic/)

## 2. N-ary Node vs Binary Node

A binary tree node has two named children:

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

An N-ary tree node stores a list of children instead:

```python
class Node:
    def __init__(self, val, children=None):
        self.val = val
        self.children = children if children is not None else []
```

That is the only difference. A binary tree is the special case where the
children list has at most two entries.

Side by side:

```text
   binary node                 n-ary node
      (v)                        (v)
     /   \                  /   |   |   \
  (left)(right)          (c1) (c2) (c3) (c4)
```

## 3. Forest

A forest is a collection of several N-ary trees; a single tree is a special
kind of forest. In code it is just a list of root nodes:

```python
forest = [root_a, root_b, root_c]
```

Running DFS or BFS on each root visits every node of the forest. The Union
Find algorithm keeps the roots of several N-ary trees, and those roots
together form a forest.

```python
def forest_preorder(roots):
    visited = []
    for root in roots:
        traverse_dfs(root, on_preorder=lambda node: visited.append(node.val))
    return visited
```

A forest with three roots:

```text
  roots:  (A)     (B)      (C)
         /   \     |      /   \
       (a1) (a2) (b1)   (c1)  (c2)

  DFS each root in order:
  A, a1, a2,  B, b1,  C, c1, c2
```

## 4. Recursive Traversal (DFS): The Framework

The binary tree traversal framework is:

```python
def traverse(root):
    if root is None:
        return
    # pre-order position
    traverse(root.left)
    # in-order position
    traverse(root.right)
    # post-order position
```

The N-ary framework replaces the two recursive calls with a loop:

```python
def traverse_dfs(root, on_preorder=None, on_postorder=None):
    if root is None:
        return

    if on_preorder is not None:
        on_preorder(root)

    for child in root.children:
        traverse_dfs(child, on_preorder, on_postorder)

    if on_postorder is not None:
        on_postorder(root)
```

Because a node can have any number of children, the code cannot name
`left` and `right` separately. The loop over `children` is the
generalization of those two calls.

The two hook positions of the framework:

```text
traverse_dfs(root)
  |
  +-- [pre-order position]  visit root            <-- before children
  |
  +-- for each child c in root.children:
  |       traverse_dfs(c)          (repeat for every child)
  |
  +-- [post-order position]  visit root           <-- after children
```

The call tree for the sample tree `1 -> [3, 2, 4], 3 -> [5, 6]`:

```text
                 traverse(1)
                /     |     \
          traverse(3) traverse(2) traverse(4)
           /        \
    traverse(5)  traverse(6)

  pre-order visits:  1, 3, 5, 6, 2, 4
  post-order visits: 5, 6, 3, 2, 4, 1
```

## 5. Preorder and Postorder (LC 589 and 590)

LeetCode 589 collects values in the pre-order position:

```python
def preorder(root):
    result = []
    traverse_dfs(root, on_preorder=lambda node: result.append(node.val))
    return result
```

LeetCode 590 collects values in the post-order position:

```python
def postorder(root):
    result = []
    traverse_dfs(root, on_postorder=lambda node: result.append(node.val))
    return result
```

For the tree `1 -> [3, 2, 4], 3 -> [5, 6]`:

```text
preorder:  [1, 3, 5, 6, 2, 4]
postorder: [5, 6, 3, 2, 4, 1]
```

## 6. Why There Is No In-Order Position

The binary framework has a middle position between the two children. An
N-ary node does not have exactly two children, so "the middle" is not
defined. Only the pre-order and post-order positions survive in the N-ary
framework.

The pre-order position runs before the subtree work, which suits top-down
tasks such as copying the value. The post-order position runs after all
children, which suits bottom-up tasks such as collecting subtree results.

## 7. Level Order Traversal (BFS) Overview

Level order traversal visits the tree one level at a time. There are three
standard ways to implement it, listed next. All three return the same
levels, so the choice is a matter of style and habit.

For the tree `1 -> [3, 2, 4], 3 -> [5, 6]` the levels are:

```text
[[1], [3, 2, 4], [5, 6]]
```

Visualized by level:

```text
  level 0   (1)
  level 1   (3)  (2)  (4)
  level 2   (5)  (6)

  1 -> [3, 2, 4]
  3 -> [5, 6]
```

## 8. Method One: Queue with Level Size

The most common BFS framework counts the nodes of the current level before
processing them:

```python
def level_order_traverse(root):
    if root is None:
        return []

    levels = []
    queue = deque([root])

    while queue:
        level_size = len(queue)
        level = []

        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)
            for child in node.children:
                queue.append(child)

        levels.append(level)

    return levels
```

The `level_size` boundary groups exactly one level, because every node of
the next level enters the queue only after its parent is processed.

Queue evolution for the sample tree:

```text
start     queue: [1]
level 1   pop 1, enqueue 3, 2, 4
          queue: [3, 2, 4]          level = [1]
level 2   pop 3, enqueue 5, 6
          pop 2, pop 4
          queue: [5, 6]             level = [3, 2, 4]
level 3   pop 5, pop 6
          queue: []                 level = [5, 6]
```

## 9. Method Two: Recursive DFS with Depth

Method Two is a DFS in structure but produces level-order output. Each call
appends its value to the list at its own depth:

```python
def level_order_recursive(root):
    levels = []

    def traverse(node, depth):
        if node is None:
            return

        if len(levels) <= depth:
            levels.append([])
        levels[depth].append(node.val)

        for child in node.children:
            traverse(child, depth + 1)

    traverse(root, 0)
    return levels
```

The depth parameter replaces the level boundary. This is the classic shape
of the LeetCode 429 solutions.

The recursion with its depth argument:

```text
traverse(1, 0)   -> levels[0] = [1]
  traverse(3, 1) -> levels[1] = [3]
    traverse(5, 2) -> levels[2] = [5]
    traverse(6, 2) -> levels[2] = [5, 6]
  traverse(2, 1) -> levels[1] = [3, 2]
  traverse(4, 1) -> levels[1] = [3, 2, 4]
```

The output list grows one level at a time, and each value lands in the list
indexed by its own depth.

## 10. Method Three: Weighted Queue with Depth State

Method Three stores the depth together with the node in the queue:

```python
class LevelState:
    def __init__(self, node, depth):
        self.node = node
        self.depth = depth


def level_order_states(root):
    if root is None:
        return []

    levels = []
    queue = deque([LevelState(root, 0)])

    while queue:
        state = queue.popleft()
        node = state.node
        depth = state.depth

        if len(levels) <= depth:
            levels.append([])
        levels[depth].append(node.val)

        for child in node.children:
            queue.append(LevelState(child, depth + 1))

    return levels
```

The queue items carry their own state, so levels no longer depend on the
queue size. This weighted-queue idea generalizes to Dijkstra and other BFS
variants where the state is more than a single number.

Queue evolution with the depth carried inside each item:

```text
start    queue: [(1, 0)]
step 1   pop (1, 0), enqueue (3, 1), (2, 1), (4, 1)
         queue: [(3, 1), (2, 1), (4, 1)]
step 2   pop (3, 1), enqueue (5, 2), (6, 2)
         queue: [(2, 1), (4, 1), (5, 2), (6, 2)]
step 3   pop (2, 1)
step 4   pop (4, 1)
         queue: [(5, 2), (6, 2)]
step 5   pop (5, 2)
step 6   pop (6, 2)
         queue: []
```

## 11. Which Method to Use

```text
Method One  -> the default; simplest loop with an explicit level boundary
Method Two  -> when you already think recursively and track depth
Method Three -> when each queue item needs extra state beyond the level
```

All three run in `O(N)` time. The first is usually enough, but knowing the
other two makes weighted BFS and hybrid DFS/BFS problems easier to read.

## 12. Complexity

For an N-ary tree with `N` nodes and height `H`:

| Traversal | Time | Extra space |
|:---|:---:|:---|
| Recursive DFS (pre/post) | `O(N)` | `O(H)` recursion stack |
| Method One (queue + size) | `O(N)` | `O(W)` queue, `W` = widest level |
| Method Two (recursive + depth) | `O(N)` | `O(H)` stack plus level lists |
| Method Three (weighted queue) | `O(N)` | `O(N)` queue of states |
| Forest traversal | `O(N)` | same as the traversal used |

## 13. Public Python API

```python
root = Node.from_level_order([1, None, 3, 2, 4, None, 5, 6])

preorder(root)             # [1, 3, 5, 6, 2, 4]      (LC 589)
postorder(root)            # [5, 6, 3, 2, 4, 1]      (LC 590)
level_order_traverse(root) # [[1], [3, 2, 4], [5, 6]] (LC 429, Method One)
level_order_recursive(root)   # same levels (Method Two)
level_order_states(root)      # same levels (Method Three)

forest_preorder([root_a, root_b])   # DFS over every root

traverse_dfs(root, on_preorder=fn, on_postorder=fn)  # the framework itself
```

## 14. Example

Run:

```text
python NaryTreeTraversal.py
```

The demo builds the sample tree, prints the preorder, postorder, and the
level order from all three methods, verifies they match, walks a small
forest, and then runs 200 randomized trees where the three level-order
methods and the DFS outputs are cross-checked.

## 15. Sources and LeetCode Links

- [N-ary Tree Recursive/Level Traversal](https://labuladong.online/en/algo/data-structure-basic/n-ary-tree-traverse-basic/)
- [589. N-ary Tree Preorder Traversal](https://leetcode.com/problems/n-ary-tree-preorder-traversal/)
- [590. N-ary Tree Postorder Traversal](https://leetcode.com/problems/n-ary-tree-postorder-traversal/)
- [429. N-ary Tree Level Order Traversal](https://leetcode.com/problems/n-ary-tree-level-order-traversal/)
