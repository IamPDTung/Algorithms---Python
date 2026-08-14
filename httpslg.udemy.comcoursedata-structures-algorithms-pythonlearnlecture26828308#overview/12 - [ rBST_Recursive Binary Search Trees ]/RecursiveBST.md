
---

# Recursive Binary Search Tree (rBST)
These notes extend folder 7's BST: the invariant stays the same, but operations walk by recursion.
## 1. BST and rBST
Folder 7 uses `while` and `temp`; this folder uses a public wrapper and a private helper.
`ASCII: ITERATIVE root -> temp -> child     RECURSIVE root -> helper(root) -> helper(child) -> return node`
The rule remains `left < node < right`; equal values are rejected, as in folder 7.
---
## 2. Why the Tree Is Naturally Recursive
Each child is the root of a smaller BST, so one operation has the same shape at every level.
`ASCII: (47) /\ (21) (76)   solve(47) -> solve(21 or 76) -> solve(child or None)`
| State | `current_node` is the current subtree root |
| Base case | `None`, or the requested value is found |
| Progress | Recurse into exactly one smaller child |
---
## 3. Wrapper and Private Helper Pattern
Public `r_contains`, `r_insert`, and `delete_node` hide `root`; their helpers receive `current_node`.
`ASCII: public(value) -> private(current_node, value) -> private(left/right, value)`
The helper returns the processed subtree root, allowing the parent to reconnect `.left` or `.right`.
---
## 4. Recursive Contains Trace
For `27`: `47` compares left, `21` compares right, and `27` matches; for `17`, `47 -> 21 -> 18 -> None` returns `False`.
`ASCII: [47] 27<47 -> [21] 27>21 -> [27] equal -> True; missing path -> None -> False`
The `None` base case and equality test stop the recursion before a child access fails.
---
## 5. Recursive Insert and Returned-Node Attachment
`__r_insert(None, value)` is the base case and returns `Node(value)`; the waiting caller assigns that result to its child pointer.
`ASCII: (2).right -> None; helper(None,3) returns (3); caller sets (2).right = (3)`
Equality takes no branch, so the existing node is returned. `r_insert` creates an empty root and, unlike iterative `insert`, returns no Boolean.
---
## 6. `min_value` Walk
The supplied method is iterative: move left until there is no left child. It assumes `current_node` is not `None`.
`ASCII: (76) -> left (52) -> left None; return 52; used as successor from a right subtree`
This leftmost value is the smallest value greater than a two-child deletion target.
---
## 7. Delete and Its Three Cases
`__delete_node` searches recursively, then returns a replacement subtree to the parent. The before/after links show what each case returns.
`ASCII LEAF: BEFORE (21).left=(18) -> AFTER (21).left=None`
`ASCII ONE CHILD: BEFORE (47).left=(21).right=(27) -> AFTER (47).left=(27)`
`ASCII TWO CHILDREN: BEFORE (47) with (21) and (76.left=52) -> copy successor 52 -> AFTER root=(52), then delete old 52`
Leaf returns `None`; one child returns that child; two children copy `min_value(current_node.right)` and recursively delete the duplicate successor.
---
## 8. Edge Cases and Call Stack
Empty contains is `False`, first recursive insert creates `root`, a missing delete preserves the tree, deleting its only node makes `root=None`, and duplicates do nothing.
`ASCII STACK: __r_contains(47) waits -> (76) waits -> (52) returns True -> True bubbles to root`
The maximum stack depth is height `h`; a sorted chain has `h=n` and can hit Python's recursion limit.
---
## 9. Complexity and Iterative Comparison
Every operation follows one root-to-leaf path: balanced `h=O(log n)`, degenerate `h=O(n)`, and recursive auxiliary space is `O(h)`.
`ASCII BALANCED: (47)/\(21)(76)     DEGENERATE: (10) -> (20) -> ... -> (n)`
| Operation | Balanced | Degenerate | Recursive stack |
|:---|:---:|:---:|:---:|
| contains / insert / delete | `O(log n)` | `O(n)` | `O(h)` |
| min walk | `O(log n)` | `O(n)` | `O(1)` |
| storage | `O(n)` | `O(n)` | - |
| Iterative BST | loop, `O(1)` traversal space | same `O(n)` worst case | no call stack |
| Recursive BST | mirrors tree; returned attachment | same `O(n)` worst case | possible stack limit |
Recursion changes control flow, not the Big O; only self-balancing trees control height for arbitrary insertion order.
---
## 10. Actual Source Solutions
The following four blocks are copied verbatim from the four `Core/SOLUTION-*.py` files, including their examples and comments.
### 10.1 `SOLUTION-BST-R_Insert.py`
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
        temp = self.root
        while (temp is not None):
            if value < temp.value:
                temp = temp.left
            elif value > temp.value:
                temp = temp.right
            else:
                return True
        return False 


    def __r_contains(self, current_node, value):
        if current_node == None: 
            return False      
        if value == current_node.value:
            return True 
        if value < current_node.value:
            return self.__r_contains(current_node.left, value) 
        if value > current_node.value:
            return self.__r_contains(current_node.right, value)

    def r_contains(self, value):
        return self.__r_contains(self.root, value)

                  
    def __r_insert(self, current_node, value):
        if current_node == None: 
            return Node(value)   
        if value < current_node.value:
            current_node.left = self.__r_insert(current_node.left, value)
        if value > current_node.value:
            current_node.right = self.__r_insert(current_node.right, value) 
        return current_node    

    def r_insert(self, value):
        if self.root == None: 
            self.root = Node(value)
        self.__r_insert(self.root, value)  




my_tree = BinarySearchTree()
my_tree.r_insert(2)
my_tree.r_insert(1)
my_tree.r_insert(3)

"""
    THE LINES ABOVE CREATE THIS TREE:
                 2
                / \
               1   3
"""


print('Root:', my_tree.root.value)            
print('Root -> Left:', my_tree.root.left.value)        
print('Root -> Right:', my_tree.root.right.value)    



"""
    EXPECTED OUTPUT:
    ----------------
	Root: 2
	Root -> Left: 1
	Root -> Right: 3

"""




```
### 10.2 `SOLUTION-BST-R_Contains.py`
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
        temp = self.root
        while (temp is not None):
            if value < temp.value:
                temp = temp.left
            elif value > temp.value:
                temp = temp.right
            else:
                return True
        return False
        
    def __r_contains(self, current_node, value):
        if current_node == None: 
            return False      
        if value == current_node.value:
            return True 
        if value < current_node.value:
            return self.__r_contains(current_node.left, value) 
        if value > current_node.value:
            return self.__r_contains(current_node.right, value)


    def r_contains(self, value):
        return self.__r_contains(self.root, value)
        



my_tree = BinarySearchTree()
my_tree.insert(47)
my_tree.insert(21)
my_tree.insert(76)
my_tree.insert(18)
my_tree.insert(27)
my_tree.insert(52)
my_tree.insert(82)

print('BST Contains 27:')
print(my_tree.r_contains(27))

print('\nBST Contains 17:')
print(my_tree.r_contains(17))
                


"""
    EXPECTED OUTPUT:
    ----------------
    BST Contains 27:
    True

    BST Contains 17:
    False

"""
```
### 10.3 `SOLUTION-BST-Min_Value.py`
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
        temp = self.root
        while temp is not None:
            if value < temp.value:
                temp = temp.left
            elif value > temp.value:
                temp = temp.right
            else:
                return True
        return False
    
    
    def min_value(self, current_node):
        while current_node.left is not None:
            current_node = current_node.left
        return current_node.value
        

        

my_tree = BinarySearchTree()
my_tree.insert(47)
my_tree.insert(21)
my_tree.insert(76)
my_tree.insert(18)
my_tree.insert(27)
my_tree.insert(52)
my_tree.insert(82)


print( my_tree.min_value(my_tree.root) )

print( my_tree.min_value(my_tree.root.right) )

            

"""
    EXPECTED OUTPUT:
    ----------------
	18
	52

"""
```
### 10.4 `SOLUTION-BST-Delete.py`
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
        temp = self.root
        while (temp is not None):
            if value < temp.value:
                temp = temp.left
            elif value > temp.value:
                temp = temp.right
            else:
                return True
        return False
 

    def __r_contains(self, current_node, value):
        if current_node == None: 
            return False      
        if value == current_node.value:
            return True 
        if value < current_node.value:
            return self.__r_contains(current_node.left, value) 
        if value > current_node.value:
            return self.__r_contains(current_node.right, value)

    def r_contains(self, value):
        return self.__r_contains(self.root, value)

 
          
    def __r_insert(self, current_node, value):
        if current_node == None: 
            return Node(value)   
        if value < current_node.value:
            current_node.left = self.__r_insert(current_node.left, value)
        if value > current_node.value:
            current_node.right = self.__r_insert(current_node.right, value) 
        return current_node    

    def r_insert(self, value):
        if self.root == None: 
            self.root = Node(value)
        self.__r_insert(self.root, value)  


    def min_value(self, current_node):
        while (current_node.left is not None):
            current_node = current_node.left
        return current_node.value 

    def __delete_node(self, current_node, value):
	    if current_node == None: 
		    return None
	    if value < current_node.value:
		    current_node.left = self.__delete_node(current_node.left, value)
	    elif value > current_node.value: 
		    current_node.right = self.__delete_node(current_node.right, value)
	    else:
		    if current_node.left == None and current_node.right == None:
			    return None
		    elif current_node.left == None:
			    current_node = current_node.right
		    elif current_node.right == None:
			    current_node = current_node.left
		    else:
			    sub_tree_min = self.min_value(current_node.right)
			    current_node.value = sub_tree_min
			    current_node.right = self.__delete_node(current_node.right, sub_tree_min)
	    return current_node
    
    def delete_node(self, value):
        self.root = self.__delete_node(self.root, value)




my_tree = BinarySearchTree()
my_tree.r_insert(2)
my_tree.r_insert(1)
my_tree.r_insert(3)

"""
       2
      / \
     1   3
"""

print("root:", my_tree.root.value)
print("root.left =", my_tree.root.left.value)
print("root.right =", my_tree.root.right.value)


my_tree.delete_node(2)

"""
       3
      / \
     1   None
"""


print("\nroot:", my_tree.root.value)
print("root.left =", my_tree.root.left.value)
print("root.right =", my_tree.root.right)



"""
    EXPECTED OUTPUT:
    ----------------
	root: 2
	root.left = 1
	root.right = 3

	root: 3
	root.left = 1
	root.right = None

"""
```
