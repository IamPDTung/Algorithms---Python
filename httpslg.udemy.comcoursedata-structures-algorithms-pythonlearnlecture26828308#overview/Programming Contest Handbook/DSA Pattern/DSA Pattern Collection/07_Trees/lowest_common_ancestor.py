"""
Lowest Common Ancestor of a Binary Tree
Given a binary tree, find the lowest common ancestor (LCA) of two given nodes
p and q.

Idea: recursive DFS. If the root matches p or q, return root. Otherwise search
left and right. If both sides return non-null, the root is the LCA. If only one
side is non-null, that side holds the LCA.

Time: O(n)
Space: O(h)
"""


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def lowest_common_ancestor(root, p, q):
    if root is None or root == p or root == q:
        return root
    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)
    if left and right:
        return root
    return left if left else right


if __name__ == "__main__":
    # Build: 3 / 5 1 / 6 2 0 8 / 7 4
    tree = TreeNode(3,
                    TreeNode(5, TreeNode(6), TreeNode(2, TreeNode(7), TreeNode(4))),
                    TreeNode(1, TreeNode(0), TreeNode(8)))
    p = tree.left          # 5
    q = tree.right         # 1
    print(lowest_common_ancestor(tree, p, q).val)      # 3
    q2 = tree.left.right.right   # 4
    print(lowest_common_ancestor(tree, p, q2).val)     # 5
