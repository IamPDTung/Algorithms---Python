
---

# Use Cases of DFS and BFS

## 1. Goal

In real algorithm problems, DFS is commonly used to enumerate all paths,
while BFS is often used to find the shortest path. This guide explains why,
using LeetCode 111 Minimum Depth of Binary Tree as the running example, and
then generalizes the reasoning to unweighted graphs.

The implementation in `DfsBfsUseCases.py` provides:

- `min_depth_bfs` and `min_depth_dfs` for LeetCode 111.
- `dfs_all_paths` and `bfs_all_paths` for enumerating root-to-leaf paths.
- `bfs_shortest_path` and `dfs_graph_paths` for unweighted graphs.
- Randomized checks proving BFS and DFS agree on the answers.

Source references:

- [Use cases of DFS and BFS](https://labuladong.online/en/algo/data-structure-basic/use-case-of-dfs-bfs/)
- [Binary Tree Recursive/Level Traversal](https://labuladong.online/en/algo/data-structure-basic/binary-tree-traverse-basic/)

## 2. The Two Rules of Thumb

The two questions this article answers:

```text
Why is BFS often used to find the shortest path?
Why is DFS commonly used to find all paths?
```

Recursive traversal and level-order traversal of binary trees are the
simplest forms of DFS and BFS. Both rules can be seen in this simple setting.

## 3. Why BFS Is Often Used to Find the Shortest Path

Level-order traversal is BFS on a tree. Its core structure is:

```text
process level 0 (the root)
process level 1
process level 2
...
```

A node at level `d` is exactly `d` steps away from the root. Therefore the
first time BFS reaches the goal node, the level counter is the minimum
distance. BFS visits nodes in strictly increasing distance order, so the
first target found is automatically the nearest target.

BFS expands like rings on water, one ring at a time:

```text
               (root) ............ ring 0  (distance 0)
              /      \
          (a)          (b) ...... ring 1  (distance 1)
         /  \          /  \
       (c)  (d)      (e)  (f) .. ring 2  (distance 2)

  any target found on ring 1 is closer than any target on ring 2,
  so the first ring that contains the target is the answer.
```

DFS does not have this property. It dives to a leaf as fast as possible and
returns an answer for one path only. It cannot know whether another branch
holds a closer goal until it has also examined that branch.

## 4. BFS on LeetCode 111: Minimum Depth

The task is the minimum depth of a binary tree: the number of nodes on the
shortest path from the root to the nearest leaf.

```python
def min_depth_bfs(root, trace=None):
    if root is None:
        return 0

    queue = deque([root])
    depth = 1

    while queue:
        level_size = len(queue)
        for _ in range(level_size):
            node = queue.popleft()

            if node.left is None and node.right is None:
                return depth

            if node.left is not None:
                queue.append(node.left)
            if node.right is not None:
                queue.append(node.right)

        depth += 1

    return depth
```

For the tree `[3, 9, 20, None, None, 15, 7]`:

```text
        3
       / \
      9   20
         /  \
        15   7
```

Step by step, the BFS queue evolves like this (a leaf is found at level 2):

```text
step 1   queue: [3]            visit 3          depth = 1
         enqueue its children 9, 20

step 2   queue: [9, 20]        visit 9          depth = 2
         9 is a leaf  ->  return 2  (done, 20 never visited)
```

The same tree under BFS with the visited order marked:

```text
   visit 1: (3) ..................... level 1
           /  \
visit 2: (9)  (20) .................. level 2
               /  \
            (15)   (7)             (never reached)
```

BFS processes level 1 (`3`), then level 2 (`9`, `20`). Node `9` is a leaf,
so the answer is `2`. Nodes `15` and `7` are never visited. The demo shows
the visit trace `[3, 9]` for BFS versus `[3, 9, 20, 15, 7]` for DFS.

## 5. Why DFS Cannot Stop at the First Leaf

The DFS version of LeetCode 111 must check every branch:

```python
def min_depth_dfs(root, trace=None):
    if root is None:
        return 0

    if root.left is None and root.right is None:
        return 1

    if root.left is None:
        return min_depth_dfs(root.right, trace) + 1

    if root.right is None:
        return min_depth_dfs(root.left, trace) + 1

    return min(
        min_depth_dfs(root.left, trace),
        min_depth_dfs(root.right, trace),
    ) + 1
```

The first leaf DFS meets is not necessarily the shallowest one, so DFS
keeps a running minimum over all branches. It always visits the whole tree
in this problem. The answer is the same, but the "first found is the
shortest" guarantee that makes BFS natural does not exist for DFS.

The DFS visit order for the same tree shows that every node is reached:

```text
  visit 1: ①(3)
          /    \
  visit 2: ②(9)   ③(20)
                  /    \
         visit 4: ④(15)   ⑤(7)
```

DFS dives down to `9` first, but it must still walk back up and check the
whole `20` branch before it can be sure that `2` is the minimum.

## 6. The Space Cost of BFS

BFS keeps a whole level in the queue at once. A complete binary tree has
about `N / 2` leaves, so the queue can hold `O(N)` nodes.

DFS keeps the recursion stack of the current path only, which is
`O(height)`, or `O(log N)` for a balanced tree.

This is the tradeoff: BFS buys the shortest-path guarantee with wider
memory usage, while DFS stores only one path at a time.

## 7. Why DFS Is Commonly Used to Find All Paths

DFS with backtracking carries the current path on the recursion stack.
Whenever the search reaches a leaf, the stack is exactly one root-to-leaf
path. Copying it records the path with no extra bookkeeping.

BFS can also enumerate all paths, but its queue holds independent nodes,
not a path structure. Every queued item must carry its own full path copy,
which wastes memory and complicates the code.

## 8. DFS with Backtracking Enumerates All Paths

```python
def dfs_all_paths(root):
    paths = []
    path = []

    def backtrack(node):
        if node is None:
            return

        path.append(node.val)

        if node.left is None and node.right is None:
            paths.append(list(path))
        else:
            backtrack(node.left)
            backtrack(node.right)

        path.pop()

    backtrack(root)
    return paths
```

For the tree `[1, 2, 3, None, 5]` the result is:

```text
[[1, 2, 5], [1, 3]]
```

The tree and the shared path stack during the backtracking:

```text
          1
         / \
        2   3
         \
          5

  dfs(1)        path = [1]
    dfs(2)      path = [1, 2]
      dfs(5)    path = [1, 2, 5]   -> record [1, 2, 5]
      pop 5     path = [1, 2]
    pop 2       path = [1]
    dfs(3)      path = [1, 3]      -> record [1, 3]
    pop 3       path = [1]
  pop 1         path = []
```

The shared `path` list acts like a stack: push on entering a node, pop on
leaving it. Because only one path list exists, memory usage stays
`O(height)` for the bookkeeping itself.

## 9. What BFS Must Do to Enumerate All Paths

The BFS version stores a path copy in every queue item:

```python
def bfs_all_paths(root):
    if root is None:
        return []

    paths = []
    queue = deque([(root, [root.val])])

    while queue:
        node, path = queue.popleft()

        if node.left is None and node.right is None:
            paths.append(path)
            continue

        if node.left is not None:
            queue.append((node.left, path + [node.left.val]))
        if node.right is not None:
            queue.append((node.right, path + [node.right.val]))

    return paths
```

It returns the same set of paths, but each queue item duplicates a prefix
of its path, so the total storage is `O(number of paths * path length)`
instead of the DFS stack's `O(height)`. This is why DFS is the customary
choice for enumerating all paths.

## 10. The Same Rule on General Graphs

The rule is not limited to trees. On an unweighted graph:

```python
def bfs_shortest_path(graph, start, target):
    if start not in graph or target not in graph:
        return None

    queue = deque([start])
    parent = {start: None}

    while queue:
        node = queue.popleft()
        if node == target:
            path = []
            cursor = node
            while cursor is not None:
                path.append(cursor)
                cursor = parent[cursor]
            path.reverse()
            return len(path) - 1, path

        for neighbor in graph[node]:
            if neighbor not in parent:
                parent[neighbor] = node
                queue.append(neighbor)

    return None
```

BFS discovers nodes in order of distance from the start, so the first
dequeue of the target is a shortest path. The demo verifies this against a
reference `dfs_graph_paths` that enumerates every simple path and takes the
minimum length.

The same ring idea on the demo graph (`A` is the start, `F` the target):

```text
        A --- B
        |     |
        C --- D --- F
         \   /
          E

  ring 0: A
  ring 1: B, C
  ring 2: D, E
  ring 3: F        <- first ring containing the target, distance = 3
```

DFS, by contrast, must enumerate the paths `A->B->D->F` (length 3) and
`A->C->E->F` (length 3), and also the longer routes such as
`A->C->D->B->A->...` that are pruned as not simple, before it can take the
minimum.

## 11. Complexity Comparison

For a tree with `N` nodes:

| Task | Algorithm | Time | Space |
|:---|:---|:---:|:---:|
| Minimum depth | BFS | `O(N)` worst, stops early | `O(N)` queue |
| Minimum depth | DFS | `O(N)` always | `O(height)` stack |
| All root-to-leaf paths | DFS backtracking | `O(N)` calls | `O(height)` plus output |
| All root-to-leaf paths | BFS with path copies | `O(N)` visits | `O(paths * length)` |
| Graph shortest path | BFS | `O(V + E)` | `O(V)` |
| Graph all paths | DFS backtracking | `O(paths)` | `O(V)` plus output |

## 12. How to Choose Between DFS and BFS

```text
Shortest distance, fewest steps, nearest target   -> BFS
Enumerate all paths, all solutions, backtracking  -> DFS
Memory matters and the tree is wide               -> DFS
Need early exit when the answer is close          -> BFS
```

DFS and BFS visit the same nodes in the end for exhaustive search. The
difference is the order of visiting and the shape of the working memory,
and that difference determines which task each one fits naturally.

## 13. Public Python API

```python
root = build_tree([3, 9, 20, None, None, 15, 7])

min_depth_bfs(root)            # 2, with optional trace list
min_depth_dfs(root)            # 2, with optional trace list

dfs_all_paths(root)            # list of lists of values
bfs_all_paths(root)            # same set, different order

graph = {"A": ["B", "C"], ...}
bfs_shortest_path(graph, "A", "F")   # (distance, path) or None
dfs_graph_paths(graph, "A", "F")     # every simple path

count_nodes(root)              # helper for verification
```

## 14. Example

Run:

```text
python DfsBfsUseCases.py
```

The demo prints the visit traces for LeetCode 111, the all-paths output of
both algorithms, a graph shortest path verified against exhaustive DFS, and
the result of 200 randomized tree checks and 200 randomized graph checks.

## 15. Sources and LeetCode Links

- [Use cases of DFS and BFS](https://labuladong.online/en/algo/data-structure-basic/use-case-of-dfs-bfs/)
- [111. Minimum Depth of Binary Tree](https://leetcode.com/problems/minimum-depth-of-binary-tree/)
