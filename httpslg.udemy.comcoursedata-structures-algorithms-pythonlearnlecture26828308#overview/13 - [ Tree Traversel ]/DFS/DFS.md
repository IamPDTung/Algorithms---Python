---

# Depth-First Search (DFS)
## 1. What is DFS?
**Depth-First Search (DFS)** is a tree/graph traversal algorithm that visits a node, follows one branch as deeply as possible, then backtracks to another branch. It visits every reachable node once; the important choice is the order in which each node is recorded.
```
    DFS: start -> branch -> leaf -> backtrack -> next
    mechanism: recursion + call stack
```
---

## 2. Why Was DFS Created?
Hierarchical data has branches: folders, syntax trees, and search trees all need a systematic way to explore a complete branch without losing the parent position. DFS supplies that depth-first strategy.
```
    Root -> A -> C -> D -> B -> E -> F
    /  \     backtrack to parent, then choose another branch
```
---

## 3. The Sample Tree
All three supplied solutions insert `47, 21, 76, 18, 27, 52, 82` into the same **Binary Search Tree (BST)**; the numbered tree is re-labeled for each order below.
```
    [1]47
     / \
[2]21 [5]76 -> [3]18 [4]27 [6]52 [7]82
```
---

## 4. Recursion and the Call Stack
The helper solves **traverse this node's subtree**. A leaf returns to its parent; the newest call resumes first: **LIFO (Last In, First Out)**. Each frame remembers the node and continuation point.
```
    traverse(47) [node=47]
       | traverse(21) [node=21]
        +-- traverse(18) -> leaf -> return upward
```
---

## 5. The Visit Point
```
    PRE: root -> left -> right | IN: left -> root -> right
    POST: left -> right -> root
```
---

## 6. Pre-Order: Root-Left-Right
Pre-order appends as soon as a node is entered, before either child call.
```
                         [1] 47
                       /          \
                 [2] 21            [5] 76
                 /    \            /    \
            [3] 18  [4] 27    [6] 52  [7] 82
```
```
    call traverse(47): append47; call traverse(21): append21
    call traverse(18): append18 -> return; call traverse(27): append27 -> return21
    append47's left done; call traverse(76): append76; call traverse(52): append52 -> return
    call traverse(82): append82 -> return76 -> return47
```
```text
[47, 21, 18, 27, 76, 52, 82]
```
Pre-order is useful for **copying and serialization**: record the parent before children; general trees also need null markers.
### Verbatim `SOLUTION-DFS_Pre_Order.py`

```python
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, value):
        new_node = Node(value)
        if self.root is None:
            self.root = new_node
            return True
        temp = self.root
        while (True):
            if new_node.value == temp.value:
                return False
            if new_node.value < temp.value:
                if temp.left is None:
                    temp.left = new_node
                    return True
                temp = temp.left
            else: 
                if temp.right is None:
                    temp.right = new_node
                    return True
                temp = temp.right

    def contains(self, value):
        if self.root is None:
            return False
        temp = self.root
        while (temp):
            if value < temp.value:
                temp = temp.left
            elif value > temp.value:
                temp = temp.right
            else:
                return True
        return False
        
    def BFS(self):
        current_node = self.root
        queue = []
        results = []
        queue.append(current_node)

        while len(queue) > 0:
            current_node = queue.pop(0)
            results.append(current_node.value)
            if current_node.left is not None:
                queue.append(current_node.left)
            if current_node.right is not None:
                queue.append(current_node.right)
        return results
    
    def dfs_pre_order(self):
        results = []
        def traverse(current_node):
            results.append(current_node.value)
            if current_node.left is not None:
                traverse(current_node.left)
            if current_node.right is not None:
                traverse(current_node.right)
        traverse(self.root)
        return results





my_tree = BinarySearchTree()
my_tree.insert(47)
my_tree.insert(21)
my_tree.insert(76)
my_tree.insert(18)
my_tree.insert(27)
my_tree.insert(52)
my_tree.insert(82)

print(my_tree.dfs_pre_order())



"""
    EXPECTED OUTPUT:
    ----------------
    [47, 21, 18, 27, 76, 52, 82]

 """

                

```
---

## 7. In-Order: Left-Root-Right
In-order appends between the left and right calls.

```
                         [4] 47
                       /          \
                 [2] 21            [6] 76
                 /    \            /    \
            [1] 18  [3] 27    [5] 52  [7] 82
append position: LEFT, then ROOT, then RIGHT
```
```
    traverse(47) -> left -> traverse(21) -> left -> 18 append -> return
      append 21; traverse(27) append -> return; append 47
    traverse(76) -> 52 append -> return; append 76; 82 append -> return 47
```
```text
[18, 21, 27, 47, 52, 76, 82]
```
For a valid BST, left values are smaller and right values larger, so in-order output is sorted. `BST-Kth Smallest Node.py` counts it for kth smallest; `BST-Validate BST.py` checks that `dfs_in_order()` is strictly increasing.
### Verbatim `SOLUTION-DFS_In_Order.py`

```python
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, value):
        new_node = Node(value)
        if self.root is None:
            self.root = new_node
            return True
        temp = self.root
        while (True):
            if new_node.value == temp.value:
                return False
            if new_node.value < temp.value:
                if temp.left is None:
                    temp.left = new_node
                    return True
                temp = temp.left
            else: 
                if temp.right is None:
                    temp.right = new_node
                    return True
                temp = temp.right


    def contains(self, value):
        if self.root is None:
            return False
        temp = self.root
        while (temp):
            if value < temp.value:
                temp = temp.left
            elif value > temp.value:
                temp = temp.right
            else:
                return True
        return False
        

    def BFS(self):
        current_node = self.root
        queue = []
        results = []
        queue.append(current_node)

        while len(queue) > 0:
            current_node = queue.pop(0)
            results.append(current_node.value)
            if current_node.left is not None:
                queue.append(current_node.left)
            if current_node.right is not None:
                queue.append(current_node.right)
        return results
    

    def dfs_pre_order(self):
        results = []

        def traverse(current_node):
            results.append(current_node.value)
            if current_node.left is not None:
                traverse(current_node.left)
            if current_node.right is not None:
                traverse(current_node.right)

        traverse(self.root)
        return results

    def dfs_post_order(self):
        results = []
        def traverse(current_node):
            if current_node.left is not None:
                traverse(current_node.left)
            if current_node.right is not None:
                traverse(current_node.right)
            results.append(current_node.value)
        traverse(self.root)
        return results

    def dfs_in_order(self):
        results = []
        def traverse(current_node):
            if current_node.left is not None:
                traverse(current_node.left)
            results.append(current_node.value) 
            if current_node.right is not None:
                traverse(current_node.right)          
        traverse(self.root)
        return results
        




my_tree = BinarySearchTree()
my_tree.insert(47)
my_tree.insert(21)
my_tree.insert(76)
my_tree.insert(18)
my_tree.insert(27)
my_tree.insert(52)
my_tree.insert(82)

print(my_tree.dfs_in_order())



"""
    EXPECTED OUTPUT:
    ----------------
    [18, 21, 27, 47, 52, 76, 82]

 """

                



 
```

---

## 8. Post-Order: Left-Right-Root
Post-order appends only after both child calls finish.

```
                         [7] 47
                       /          \
                 [3] 21            [6] 76
                 /    \            /    \
            [1] 18  [2] 27    [4] 52  [5] 82
append position: LEFT, then RIGHT, then ROOT
```
```
    traverse(47) -> left -> traverse(21) -> left -> 18 append -> [18]
      right 27 append -> [18,27]; both children done, append 21
    right traverse(76) -> left 52 append -> [...,52]; right 82 append -> [...,82]
      both children done, append 76; both children of 47 done, append 47
```
```text
[18, 27, 21, 52, 82, 76, 47]
```
Post-order is natural for **deletion** (children before parent) and **expression evaluation** (operands before operator).
```
        +       post-order: 2 -> 3 -> * -> 5 -> +
       / \
    *(2,3) 5    (2 * 3) + 5 = 11
```
### Verbatim `SOLUTION-DFS_Post_Order.py`

```python
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, value):
        new_node = Node(value)
        if self.root is None:
            self.root = new_node
            return True
        temp = self.root
        while (True):
            if new_node.value == temp.value:
                return False
            if new_node.value < temp.value:
                if temp.left is None:
                    temp.left = new_node
                    return True
                temp = temp.left
            else: 
                if temp.right is None:
                    temp.right = new_node
                    return True
                temp = temp.right

    def contains(self, value):
        if self.root is None:
            return False
        temp = self.root
        while (temp):
            if value < temp.value:
                temp = temp.left
            elif value > temp.value:
                temp = temp.right
            else:
                return True
        return False
        
    def BFS(self):
        current_node = self.root
        queue = []
        results = []
        queue.append(current_node)

        while len(queue) > 0:
            current_node = queue.pop(0)
            results.append(current_node.value)
            if current_node.left is not None:
                queue.append(current_node.left)
            if current_node.right is not None:
                queue.append(current_node.right)
        return results
    
    def dfs_pre_order(self):
        results = []
        def traverse(current_node):
            results.append(current_node.value)
            if current_node.left is not None:
                traverse(current_node.left)
            if current_node.right is not None:
                traverse(current_node.right)
        traverse(self.root)
        return results

    def dfs_post_order(self):
        results = []
        def traverse(current_node):
            if current_node.left is not None:
                traverse(current_node.left)
            if current_node.right is not None:
                traverse(current_node.right)
            results.append(current_node.value)
        traverse(self.root)
        return results





my_tree = BinarySearchTree()
my_tree.insert(47)
my_tree.insert(21)
my_tree.insert(76)
my_tree.insert(18)
my_tree.insert(27)
my_tree.insert(52)
my_tree.insert(82)

print(my_tree.dfs_post_order())



"""
    EXPECTED OUTPUT:
    ----------------
    [18, 27, 21, 52, 82, 76, 47]

 """
```

---

## 9. Comparison and Complexity
For `n` nodes and height `h`, every order takes `O(n)` time, `O(h)` call-stack space, and `O(n)` output space. Balanced: `h = O(log n)`; skewed: `h = O(n)`; including output: `O(n + h)`.

| Measure | Complexity |
|:---|:---|:---|
| **Time** | `O(n)` |
| **Call stack** | `O(h)` |
| **Maximum depth** | `O(log n)` balanced, `O(n)` skewed |
```
    balanced: o       skewed: o -> o -> o -> ... -> o
              / \      one active frame per depth level
```

---

## 10. BFS versus DFS
**Breadth-First Search (BFS)** uses a FIFO queue and visits by level; DFS uses recursion or a LIFO stack and follows a branch.
| Feature | BFS | DFS |
|:---|:---|:---|
| Visit order | level by level | deep branch, then backtrack |
| Storage | queue/FIFO | call stack/LIFO |
| Time | `O(n)` | `O(n)` |
| Space | `O(w)`, maximum width | `O(h)`, height |
| Best question | closest to root? | what is down this branch? |
| Typical use | levels and shortest unweighted paths | ordered output and subtree work |
```
    BFS follows width: o o o o       DFS follows height: o
                        queue                         |
                                                      o
```

---

## 11. Interview Files and Checklist
| Filename | Purpose |
|:---|:---|
| `BST-Kth Smallest Node.py` | in-order count finds the kth smallest BST value |
| `BST-Validate BST.py` | in-order output must be strictly increasing for a valid BST |
```
    BST in-order stream: 18 -> 21 -> 27 -> 47 -> 52 -> 76 -> 82
                         ^ kth value       ^ ordered invariant
```
**Summary:** DFS explores deeply, backtracks through the call stack, runs in `O(n)` time, and uses `O(h)` traversal-stack space. The visit point gives pre-order, in-order, and post-order their different meanings.
