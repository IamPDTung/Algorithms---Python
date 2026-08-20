from __future__ import annotations

import random
from collections import deque
from typing import Dict, List, Optional, Sequence, Tuple, TypeVar


T = TypeVar("T")


class TreeNode:
    def __init__(
        self,
        val: int,
        left: Optional[TreeNode] = None,
        right: Optional[TreeNode] = None,
    ):
        self.val = val
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f"TreeNode({self.val})"


def build_tree(values: Sequence[Optional[int]]) -> Optional[TreeNode]:
    """Build a binary tree from a level-order list with None placeholders."""
    if not values or values[0] is None:
        return None

    root = TreeNode(values[0])
    queue = deque([root])
    index = 1

    while queue and index < len(values):
        node = queue.popleft()

        if index < len(values) and values[index] is not None:
            node.left = TreeNode(values[index])
            queue.append(node.left)
        index += 1

        if index < len(values) and values[index] is not None:
            node.right = TreeNode(values[index])
            queue.append(node.right)
        index += 1

    return root


def min_depth_bfs(
    root: Optional[TreeNode], trace: Optional[List[int]] = None
) -> int:
    """Minimum depth of a binary tree using level-order BFS (LeetCode 111).

    Level-order traversal is BFS. Each level is one step away from the root,
    so the first leaf that the queue reaches sits at the minimum depth.
    """
    if root is None:
        return 0

    queue = deque([root])
    depth = 1

    while queue:
        level_size = len(queue)
        for _ in range(level_size):
            node = queue.popleft()
            if trace is not None:
                trace.append(node.val)

            if node.left is None and node.right is None:
                return depth

            if node.left is not None:
                queue.append(node.left)
            if node.right is not None:
                queue.append(node.right)

        depth += 1

    return depth


def min_depth_dfs(
    root: Optional[TreeNode], trace: Optional[List[int]] = None
) -> int:
    """Minimum depth of a binary tree using recursive DFS (LeetCode 111).

    DFS cannot stop at the first leaf it finds, because a deeper branch may
    contain a shallower leaf. Every branch must be examined.
    """
    if root is None:
        return 0

    if trace is not None:
        trace.append(root.val)

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


def dfs_all_paths(root: Optional[TreeNode]) -> List[List[int]]:
    """Enumerate every root-to-leaf path using DFS with backtracking.

    The recursion stack stores the current path. At each leaf the path is
    copied into the result list, then backtracking removes the leaf again.
    """
    paths: List[List[int]] = []
    path: List[int] = []

    def backtrack(node: Optional[TreeNode]) -> None:
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


def bfs_all_paths(root: Optional[TreeNode]) -> List[List[int]]:
    """Enumerate every root-to-leaf path using BFS for comparison.

    BFS can enumerate all paths, but the queue loses the path structure, so
    every queued item must carry a full copy of the path built so far.
    """
    if root is None:
        return []

    paths: List[List[int]] = []
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


def bfs_shortest_path(
    graph: Dict[T, Sequence[T]], start: T, target: T
) -> Optional[Tuple[int, List[T]]]:
    """Shortest path in an unweighted graph using BFS.

    BFS visits nodes in increasing distance order from the start node, so
    the first time the target is dequeued the distance is minimal.
    """
    if start not in graph or target not in graph:
        return None

    queue = deque([start])
    parent: Dict[T, Optional[T]] = {start: None}

    while queue:
        node = queue.popleft()
        if node == target:
            path: List[T] = []
            cursor: Optional[T] = node
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


def dfs_graph_paths(
    graph: Dict[T, Sequence[T]], start: T, target: T
) -> List[List[T]]:
    """Enumerate every simple path from start to target using DFS.

    Used as a reference to verify that BFS really returns the minimum
    distance among all paths.
    """
    paths: List[List[T]] = []
    path: List[T] = []

    def backtrack(node: T) -> None:
        path.append(node)

        if node == target:
            paths.append(list(path))
        else:
            for neighbor in graph[node]:
                if neighbor not in path:
                    backtrack(neighbor)

        path.pop()

    if start in graph and target in graph:
        backtrack(start)

    return paths


def count_nodes(root: Optional[TreeNode]) -> int:
    if root is None:
        return 0
    return 1 + count_nodes(root.left) + count_nodes(root.right)


def _random_tree(rng: random.Random, max_nodes: int) -> Optional[TreeNode]:
    if max_nodes <= 0:
        return None

    node = TreeNode(rng.randint(0, 99))
    left_budget = rng.randrange(0, max_nodes)
    right_budget = max_nodes - 1 - left_budget
    node.left = _random_tree(rng, left_budget)
    node.right = _random_tree(rng, right_budget)
    return node


def _random_graph(
    rng: random.Random, node_count: int, edge_count: int
) -> Dict[int, List[int]]:
    graph: Dict[int, List[int]] = {i: [] for i in range(node_count)}
    for _ in range(edge_count):
        a = rng.randrange(node_count)
        b = rng.randrange(node_count)
        if a != b and b not in graph[a]:
            graph[a].append(b)
            graph[b].append(a)
    return graph


if __name__ == "__main__":
    tree = build_tree([3, 9, 20, None, None, 15, 7])

    bfs_trace: List[int] = []
    bfs_depth = min_depth_bfs(tree, bfs_trace)
    dfs_trace: List[int] = []
    dfs_depth = min_depth_dfs(tree, dfs_trace)

    assert bfs_depth == 2
    assert dfs_depth == 2
    assert bfs_trace == [3, 9]
    assert dfs_trace == [3, 9, 20, 15, 7]

    print("Tree: [3, 9, 20, None, None, 15, 7]")
    print("BFS min depth:", bfs_depth, "visited:", bfs_trace)
    print("DFS min depth:", dfs_depth, "visited:", dfs_trace)

    paths_tree = build_tree([1, 2, 3, None, 5])
    dfs_paths = dfs_all_paths(paths_tree)
    bfs_paths = bfs_all_paths(paths_tree)

    assert dfs_paths == [[1, 2, 5], [1, 3]]
    assert sorted(map(tuple, bfs_paths)) == sorted(map(tuple, dfs_paths))

    print("Tree: [1, 2, 3, None, 5]")
    print("DFS all paths:", dfs_paths)
    print("BFS all paths:", bfs_paths)

    graph: Dict[str, List[str]] = {
        "A": ["B", "C"],
        "B": ["A", "D"],
        "C": ["A", "D", "E"],
        "D": ["B", "C", "F"],
        "E": ["C", "F"],
        "F": ["D", "E"],
    }
    result = bfs_shortest_path(graph, "A", "F")
    assert result is not None
    distance, path = result
    assert distance == 3
    assert len(path) == 4

    all_distances = [len(p) - 1 for p in dfs_graph_paths(graph, "A", "F")]
    assert distance == min(all_distances)

    print("Graph shortest path A -> F:", distance, "steps,", "->".join(path))
    print("All path lengths by DFS:", sorted(set(all_distances)))

    rng = random.Random(7)
    for _ in range(200):
        random_root = _random_tree(rng, rng.randint(1, 30))
        assert min_depth_bfs(random_root) == min_depth_dfs(random_root)
        dfs_paths = dfs_all_paths(random_root)
        bfs_paths = bfs_all_paths(random_root)
        assert sorted(map(tuple, dfs_paths)) == sorted(map(tuple, bfs_paths))
        assert count_nodes(random_root) >= 1

    for _ in range(200):
        node_count = rng.randint(2, 8)
        random_graph = _random_graph(rng, node_count, node_count * 3)
        start = rng.randrange(node_count)
        target = rng.randrange(node_count)
        shortest = bfs_shortest_path(random_graph, start, target)

        all_paths = dfs_graph_paths(random_graph, start, target)
        if shortest is None:
            assert all_paths == []
        else:
            shortest_distance, _ = shortest
            assert all_paths != []
            assert shortest_distance == min(len(p) - 1 for p in all_paths)

    print("Randomized checks passed: BFS matches DFS on", 200, "trees and", 200, "graphs")
