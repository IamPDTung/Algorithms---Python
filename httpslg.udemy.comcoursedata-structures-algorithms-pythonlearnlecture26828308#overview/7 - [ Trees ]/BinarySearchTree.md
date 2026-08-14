
---

# Binary Search Tree (BST)

## 1. What is a Tree? — Terminology

A **Tree** is a hierarchical data structure made of **nodes** connected by **edges**. Unlike a Linked List, which is **linear** (each node points to the next one), a tree **branches out** — one node can point to several other nodes.

```
    LINKED LIST (linear):              TREE (branching):

    (head)                             (root)
       |                                  |
       v                                  v
     [4] -> [7] -> [2] -> null          (47)
                                       /    \
                                    (21)    (76)
```

### Tree Terminology:

Every tree in this course is described with the following vocabulary:

```
                        (47)  <------------------- ROOT
                       /    \                      (the one node with
                      /      \                      no parent)
                   (21)      (76)  <------------- CHILDREN of 47
                  /    \    /    \                 (47 is their PARENT)
                (18)  (27)(52)  (82)  <---------- LEAVES
                 ^      ^    ^      ^              (nodes with NO children)
                 |      |
                 +--+---+
                    |
               18 and 27 are SIBLINGS
               (same parent: 21)

    Each connecting line "/ \" is called an EDGE.
    A perfect tree has every level completely filled (like above).
```

| Term | Definition |
|:---|:---|
| **Root** | The topmost node; the only node with no parent |
| **Parent** | A node that has edges pointing down to other nodes |
| **Child** | A node that a parent points to |
| **Leaf** | A node with no children |
| **Siblings** | Nodes that share the same parent |
| **Edge** | The connection (pointer) between a parent and a child |

---

## 2. What is a Binary Search Tree?

A **Binary Tree** is a tree where **each node has at most 2 children** — conventionally called `left` and `right`.

```
        BINARY TREE:                  NOT A BINARY TREE:

            (47)                          (47)
           /    \                       /  |  \
        (21)    (76)                (21)(52)(76)   <- 3 children,
        /  \                          not allowed!
     (18)  (27)
```

A **Binary Search Tree (BST)** is a binary tree with **one extra ordering rule** that must hold at **EVERY node**, not just the root:

> **BST RULE:** For every node, **all values in its LEFT subtree are SMALLER** than the node's value, and **all values in its RIGHT subtree are GREATER**.

```
    THE BST RULE AT EVERY NODE:

              (parent)
              /      \
             /        \
      left child    right child
      < parent      > parent

    EXAMPLE — the rule holds everywhere:

                (47)                21 < 47 < 76   OK at root
               /    \
           (21)      (76)           18 < 21        OK at 21
          /    \    /    \          52 < 76 < 82   OK at 76
       (18)  (27)(52)    (82)

    Check node 47: EVERYTHING left  {21,18,27} < 47  OK
                   EVERYTHING right {76,52,82} > 47  OK
```

### Valid vs Invalid BST:

```
        VALID BST:                    INVALID BST:

            (47)                          (47)
           /    \                        /    \
        (21)    (76)                 (21)    (76)
        /  \                         /  \
     (18)  (27)                  (18)  (55)   <-- 55 is in the LEFT
                                                subtree of 47 but
                                                55 > 47. RULE BROKEN!
```

---

## 3. Why Were Binary Search Trees Created?

The two basic data structures we already know each fail at one job:

* A **Linked List** can insert at the head in `O(1)`, but **searching** for a value means walking node by node: **`O(n)`**.
* A **sorted List (array)** can search fast with binary search: `O(log n)`, but **inserting** a value requires shifting everything after the insertion point: **`O(n)`**.

```
    LINKED LIST — search for 82:        SORTED LIST — insert 50:

    (head)                              +----+----+----+----+
      |                                 | 21 | 47 | 76 | 82 |
      v                                 +----+----+----+----+
    [21]->[47]->[76]->[82]                   |    |
      x     x     x    x                insert 50 here => 76 and 82
    visit visit visit visit                 must SHIFT right => O(n)
    O(n) steps!

    BST — search AND insert:

                (47)                    search 82: 47 -> 76 -> 82
               /    \                   only 3 steps, not 4 levels deep!
           (21)      (76)
          /    \    /    \              insert 50: 47 -> 76 -> 52 -> attach
       (18)  (27)(52)    (82)           one pointer change, no shifting!
```

### The BST Insight:
> A balanced BST **halves** the remaining data at every comparison — exactly like binary search — but its nodes are connected by pointers, so inserting a new value is just **attaching one node**, not shifting an array.

```
    Each comparison ELIMINATES half the tree:

    Level 0:  1 node  to check
    Level 1:  2 nodes      => searching 15 nodes takes
    Level 2:  4 nodes          at most 4 comparisons
    Level 3:  8 nodes          (log2 of 15 ~ 4)
```

---

## 4. What Problems Does a BST Solve?

BSTs are the go-to structure whenever you need **ordered data** with **fast search AND fast insert** at the same time:

```
    +------------------------------------------------------+
    |              WHERE BSTS ARE USED                     |
    +------------------------------------------------------+
    |  * Dictionaries / maps keyed by sortable keys        |
    |  * Database indexes (B-trees are BST generalizations)|
    |  * File systems (sorted directory entries)           |
    |  * Autocomplete / range queries ("all names A-M")    |
    |  * Priority scheduling (next-smallest / next-largest)|
    +------------------------------------------------------+
```

### Classic Interview Problems (see the `Leetcode` folder):

| Problem | File | Core Idea |
|:---|:---|:---|
| **98. Validate Binary Search Tree** | `98. Validate Binary Search Tree.py` | Check the BST rule holds at every node |
| **450. Delete Node in a BST** | `450. Delete Node in a BST.py` | Remove a node while keeping the BST rule |
| **226. Invert Binary Tree** | `226. Invert Binary Tree.py` | Swap every left/right child recursively |
| **109. Convert Sorted List to BST** | `109. Convert Sorted List to Binary Search Tree.py` | Build a balanced BST from sorted data |

```
    Example — Validate BST (problem 98):

            (5)              Is this a valid BST?
           /   \
         (1)   (4)           Node 4 has right child 3:
              /   \          3 < 4 but sits in the RIGHT
            (3)   (6)        subtree => INVALID!
```

---

## 5. How It Works — Constructor & Insert

### The Constructor (from `SOLUTION-BST-Constructor.py`):

Each node stores a `value` and two pointers, `left` and `right`. The tree itself starts **empty** (`root = None`):

```python
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        

class BinarySearchTree:
    def __init__(self):
        self.root = None
```

```
    A fresh node:                 A fresh tree:

    +---------+                   root
    | value   |                    |
    | 47      |                    v
    | left: --+--> null          null     (empty tree)
    | right:--+--> null
    +---------+
```

### The Insert Algorithm:

> Start at the root. If the new value is **smaller**, walk **left**; if **larger**, walk **right**. Repeat until you find an **empty spot**, and attach the new node there.

```python
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
```

### Step-by-Step Trace — inserting `47, 21, 76, 18, 52, 82`:

```
    STEP 1: insert(47)                       STEP 2: insert(21)
    root is None -> attach at root           21 < 47 -> go left -> empty spot

        (47)                                     (47)
                                                /
                                             (21)

    STEP 3: insert(76)                       STEP 4: insert(18)
    76 > 47 -> go right -> empty spot        18 < 47 left, 18 < 21 left -> attach

        (47)                                     (47)
        /    \                                  /
     (21)    (76)                            (21)
                                            /
                                         (18)

    STEP 5: insert(52)                       STEP 6: insert(82)
    52 > 47 right, 52 < 76 left -> attach    82 > 47 right, 82 > 76 right -> attach

        (47)                                     (47)
        /    \                                  /    \
     (21)    (76)                            (21)    (76)
    /        /                              /        /    \
 (18)     (52)                           (18)     (52)    (82)
```

### How `temp` walks down (insert 52 in detail):

```
    temp = 47:  52 > 47  -> temp = temp.right
    temp = 76:  52 < 76  -> temp.left is None -> ATTACH here, return True

                (47)
               /    \
           (21)      (76)
          /         /
       (18)      (52)   <== new node attached as LEFT child of 76
```

---

## 6. How It Works — Contains (Search)

### The Contains Algorithm:

> Same left/right decision as insert — but we only **walk**, never attach. If we fall off the tree (`temp` becomes `None`), the value is **not there**.

```python
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
```

### Trace — `contains(52)` on our tree (FOUND):

```
    temp = [47]: 52 > 47 -> go right
    temp = [76]: 52 < 76 -> go left
    temp = [52]: 52 == 52 -> return True

                (47)  <== visited 1
               /    \
           (21)      (76)  <== visited 2
          /         /    \
       (18)      (52)    (82)
                  ^
                  visited 3 -> FOUND!
```

### Trace — `contains(30)` on our tree (NOT FOUND):

```
    temp = [47]: 30 < 47 -> go left
    temp = [21]: 30 > 21 -> go right
    temp = None  -> loop ends -> return False

                (47)  <== visited 1
               /    \
           (21)      (76)
          /  ^
       (18)  |
             visited 2 -> right child is None -> NOT FOUND
```

### Duplicates Policy (this course):

```
    insert(47) twice:

        (47)                     (47)
           |          =>             |      second insert returns False
       attach?                   NO CHANGE   (duplicates are NOT inserted)

    The line `if new_node.value == temp.value: return False`
    rejects any value already in the tree.
```

---

## 7. Big O Analysis

### Balanced vs Degenerate Tree:

The number of **levels** is what matters. A balanced tree has `log n` levels; a tree built from **already-sorted data** degenerates into a **chain** with `n` levels:

```
    BALANCED TREE — O(log n):           DEGENERATE CHAIN — O(n):
    (insert 47,21,76,18,27,52,82)       (insert 10,20,30,40,50 — sorted!)

                (47)                    (10)
               /    \                     \
           (21)      (76)                 (20)
          /    \    /    \                  \
       (18)  (27)(52)    (82)               (30)
                                              \
    7 nodes, 3 levels.                        (40)
    Search 82: 3 comparisons.                   \
                                                (50)
                                     5 nodes, 5 levels.
                                     Search 50: 5 comparisons.
                                     Looks EXACTLY like a Linked List!
```

### Big O Table:

| Operation | Balanced BST | Worst Case (Degenerate) |
|:---|:---|:---|
| **Search (`contains`)** | `O(log n)` | `O(n)` |
| **Insert** | `O(log n)` | `O(n)` |
| **Space** | `O(n)` | `O(n)` |

> **The catch:** a plain BST does **not** rebalance itself. If you insert sorted data (`10, 20, 30, ...`), you get the degenerate chain and lose the `O(log n)` advantage. (Self-balancing variants like AVL trees and Red-Black trees fix this.)

### BST vs Linked List vs Sorted List:

| Operation | Linked List | Sorted List (Array) | BST (Balanced) |
|:---|:---|:---|:---|
| **Search** | `O(n)` | `O(log n)` (binary search) | **`O(log n)`** |
| **Insert** | `O(1)` at head / `O(n)` sorted | `O(n)` (shifting) | **`O(log n)`** |
| **Delete** | `O(n)` (find first) | `O(n)` (shifting) | **`O(log n)`** |
| **Keeps order?** | No | Yes | Yes (in-order traversal) |

```
    THE BST SWEET SPOT:

    Search speed:   Sorted List  =  BST  >  Linked List
    Insert speed:   Linked List  =  BST  >  Sorted List

    => BST combines FAST LOOKUP (like a sorted array)
       with FAST INSERTION (like a linked list).
```

---

**Next Step:** Now let's apply the BST to the interview problems in the `Leetcode` folder — validate a BST, delete a node, invert a tree, and convert a sorted list into a balanced BST!
