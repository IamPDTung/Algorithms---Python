from __future__ import annotations

import random
from collections import deque
from typing import Callable, Deque, List, Optional, Sequence


class Node:
    def __init__(self, val: int, children: Optional[List[Node]] = None):
        self.val = val
        self.children = children if children is not None else []

    def __repr__(self) -> str:
        return f"Node({self.val})"

    @classmethod
    def from_level_order(cls, values: Sequence[Optional[int]]) -> Optional[Node]:
        """Build an N-ary tree from the LeetCode level-order format.

        A `None` marker separates sibling groups: the values after the
        marker are the children of the next pending parent node.
        """
        if not values or values[0] is None:
            return None

        root = Node(values[0])
        queue: Deque[Node] = deque([root])
        index = 1

        while queue and index < len(values):
            parent = queue.popleft()

            if index < len(values) and values[index] is None:
                index += 1

            while index < len(values) and values[index] is not None:
                child = Node(values[index])
                parent.children.append(child)
                queue.append(child)
                index += 1

        return root


def traverse_dfs(
    root: Optional[Node],
    on_preorder: Optional[Callable[[Node], None]] = None,
    on_postorder: Optional[Callable[[Node], None]] = None,
) -> None:
    """The DFS framework for N-ary trees.

    The binary tree framework recurses on `left` and `right`; the N-ary
    framework replaces them with a loop over `children`. There is no
    in-order position because a node can have any number of children.
    """
    if root is None:
        return

    if on_preorder is not None:
        on_preorder(root)

    for child in root.children:
        traverse_dfs(child, on_preorder, on_postorder)

    if on_postorder is not None:
        on_postorder(root)


def preorder(root: Optional[Node]) -> List[int]:
    """LeetCode 589: visit each node before its children."""
    result: List[int] = []
    traverse_dfs(root, on_preorder=lambda node: result.append(node.val))
    return result


def postorder(root: Optional[Node]) -> List[int]:
    """LeetCode 590: visit each node after all of its children."""
    result: List[int] = []
    traverse_dfs(root, on_postorder=lambda node: result.append(node.val))
    return result


def level_order_traverse(root: Optional[Node]) -> List[List[int]]:
    """LeetCode 429, Method One: count the size of each level in the queue.

    This is the most common BFS framework. The `level_size` boundary groups
    the nodes of one level together.
    """
    if root is None:
        return []

    levels: List[List[int]] = []
    queue: Deque[Node] = deque([root])

    while queue:
        level_size = len(queue)
        level: List[int] = []

        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)
            for child in node.children:
                queue.append(child)

        levels.append(level)

    return levels


def level_order_recursive(root: Optional[Node]) -> List[List[int]]:
    """LeetCode 429, Method Two: recursive DFS that records the depth.

    Each call appends its value to the level list at its depth. This is a
    DFS in structure but produces level-order output.
    """
    levels: List[List[int]] = []

    def traverse(node: Optional[Node], depth: int) -> None:
        if node is None:
            return

        if len(levels) <= depth:
            levels.append([])
        levels[depth].append(node.val)

        for child in node.children:
            traverse(child, depth + 1)

    traverse(root, 0)
    return levels


class LevelState:
    """A queue item for Method Three: the node plus its depth."""

    def __init__(self, node: Node, depth: int):
        self.node = node
        self.depth = depth


def level_order_states(root: Optional[Node]) -> List[List[int]]:
    """LeetCode 429, Method Three: weighted queue with a depth per item.

    Each queued state carries the node and its depth, so levels do not need
    to be inferred from the queue size. This is the pattern behind weighted
    BFS variants such as Dijkstra.
    """
    if root is None:
        return []

    levels: List[List[int]] = []
    queue: Deque[LevelState] = deque([LevelState(root, 0)])

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


def forest_preorder(roots: Sequence[Optional[Node]]) -> List[int]:
    """Traverse a forest: run DFS on every root node in the list."""
    visited: List[int] = []
    for root in roots:
        traverse_dfs(root, on_preorder=lambda node: visited.append(node.val))
    return visited


def count_nodes(root: Optional[Node]) -> int:
    if root is None:
        return 0
    return 1 + sum(count_nodes(child) for child in root.children)


def height(root: Optional[Node]) -> int:
    if root is None:
        return 0
    if not root.children:
        return 1
    return 1 + max(height(child) for child in root.children)


def _random_tree(rng: random.Random, max_nodes: int) -> Optional[Node]:
    if max_nodes <= 0:
        return None

    node = Node(rng.randint(0, 99))
    remaining = max_nodes - 1
    while remaining > 0:
        child_budget = rng.randint(1, remaining)
        child = _random_tree(rng, child_budget)
        if child is not None:
            node.children.append(child)
        remaining -= child_budget

    return node


if __name__ == "__main__":
    root = Node.from_level_order([1, None, 3, 2, 4, None, 5, 6])

    pre = preorder(root)
    post = postorder(root)
    method_one = level_order_traverse(root)
    method_two = level_order_recursive(root)
    method_three = level_order_states(root)

    assert pre == [1, 3, 5, 6, 2, 4]
    assert post == [5, 6, 3, 2, 4, 1]
    assert method_one == [[1], [3, 2, 4], [5, 6]]
    assert method_two == method_one
    assert method_three == method_one

    print("Tree: 1 -> [3, 2, 4], 3 -> [5, 6]")
    print("Preorder (LC 589):", pre)
    print("Postorder (LC 590):", post)
    print("Level order Method One (LC 429):", method_one)
    print("Level order Method Two:", method_two)
    print("Level order Method Three:", method_three)

    forest = [
        Node.from_level_order([10, None, 11, 12]),
        Node.from_level_order([20, None, 21]),
    ]
    visited = forest_preorder(forest)
    assert visited == [10, 11, 12, 20, 21]
    print("Forest preorder:", visited)

    rng = random.Random(7)
    for _ in range(200):
        random_root = _random_tree(rng, rng.randint(1, 40))
        size = count_nodes(random_root)

        pre = preorder(random_root)
        post = postorder(random_root)
        assert len(pre) == size
        assert len(post) == size
        assert set(pre) == set(post)

        method_one = level_order_traverse(random_root)
        method_two = level_order_recursive(random_root)
        method_three = level_order_states(random_root)
        assert method_one == method_two == method_three
        assert len(method_one) == height(random_root)
        assert sum(len(level) for level in method_one) == size

    print("Randomized checks passed on", 200, "random N-ary trees")
