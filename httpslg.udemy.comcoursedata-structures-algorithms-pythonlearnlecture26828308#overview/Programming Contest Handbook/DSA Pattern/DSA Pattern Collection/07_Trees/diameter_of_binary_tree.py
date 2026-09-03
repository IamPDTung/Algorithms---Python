"""
Diameter of Binary Tree
The diameter is the length of the longest path between any two nodes in a tree
(counted in edges).

Idea: for each node, the longest path passing through it = leftHeight +
rightHeight. Track the max while computing heights recursively.

Time: O(n)
Space: O(h)
"""


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def diameter_of_binary_tree(root):
    best = [0]

    def height(node):
        if node is None:
            return 0
        left = height(node.left)
        right = height(node.right)
        best[0] = max(best[0], left + right)
        return 1 + max(left, right)

    height(root)
    return best[0]


if __name__ == "__main__":
    # 1 / 2 3 / 4 5
    tree = TreeNode(1,
                    TreeNode(2, TreeNode(4), TreeNode(5)),
                    TreeNode(3))
    print(diameter_of_binary_tree(tree))   # 3 (4-2-5 or 4-2-1-3)
    print(diameter_of_binary_tree(TreeNode(1)))  # 0
