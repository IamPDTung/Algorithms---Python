"""
Clone Graph
Given a reference of a node in a connected undirected graph, return a deep copy.

Idea: DFS with a hash map from original node -> clone. When visiting a node,
create its clone if missing, then recursively clone all neighbors.

Time: O(V + E)
Space: O(V)
"""


class Node:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []


def clone_graph(node):
    if node is None:
        return None
    clones = {}

    def dfs(original):
        if original in clones:
            return clones[original]
        copy = Node(original.val)
        clones[original] = copy
        for neighbor in original.neighbors:
            copy.neighbors.append(dfs(neighbor))
        return copy

    return dfs(node)


if __name__ == "__main__":
    # 1 -- 2
    # |    |
    # 4 -- 3
    n1, n2, n3, n4 = Node(1), Node(2), Node(3), Node(4)
    n1.neighbors = [n2, n4]
    n2.neighbors = [n1, n3]
    n3.neighbors = [n2, n4]
    n4.neighbors = [n1, n3]

    clone = clone_graph(n1)
    print(clone.val)               # 1
    print(clone is not n1)         # True (deep copy)
    print(sorted(x.val for x in clone.neighbors))  # [2, 4]
