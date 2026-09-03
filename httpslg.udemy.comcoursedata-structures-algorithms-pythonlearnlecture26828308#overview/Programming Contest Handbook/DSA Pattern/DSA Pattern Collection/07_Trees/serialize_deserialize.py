"""
Serialize and Deserialize Binary Tree
Design an algorithm to serialize a binary tree to a string, and deserialize that
string back to the original tree.

Idea: BFS level-order. Encode null children as "null" so the structure is fully
preserved. Uses a deque.

Time: O(n)
Space: O(n)
"""

from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def serialize(root):
    if not root:
        return "null"
    parts = []
    q = deque([root])
    while q:
        node = q.popleft()
        if node:
            parts.append(str(node.val))
            q.append(node.left)
            q.append(node.right)
        else:
            parts.append("null")
    return ",".join(parts)


def deserialize(data):
    if data == "null":
        return None
    vals = data.split(",")
    root = TreeNode(int(vals[0]))
    q = deque([root])
    i = 1
    while q:
        node = q.popleft()
        if vals[i] != "null":
            node.left = TreeNode(int(vals[i]))
            q.append(node.left)
        i += 1
        if vals[i] != "null":
            node.right = TreeNode(int(vals[i]))
            q.append(node.right)
        i += 1
    return root


if __name__ == "__main__":
    tree = TreeNode(1, TreeNode(2), TreeNode(3, TreeNode(4), TreeNode(5)))
    s = serialize(tree)
    print(s)                          # "1,2,3,null,null,4,5,null,null,null,null"
    rebuilt = deserialize(s)
    print(serialize(rebuilt) == s)    # True
