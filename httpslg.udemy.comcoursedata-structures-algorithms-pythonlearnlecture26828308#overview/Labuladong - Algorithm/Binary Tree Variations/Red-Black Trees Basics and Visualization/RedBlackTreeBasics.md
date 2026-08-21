
---

# Red-Black Trees Basics and Visualization

## 1. Goal

A red-black tree is a **self-balancing binary search tree**. It keeps its
height at O(log N) at all times, so insertion, deletion, search, and update
all stay in O(log N).

**Why was it born?** A plain binary search tree (like the TreeMap from the
previous article) has one fatal flaw: it does not balance itself. If you
insert keys in sorted order, every new key lands on the far right and the
tree degenerates into a linked list. All operations then degrade to O(N).
The red-black tree fixes this by automatically rebalancing after every
insert and delete, so the height can never blow up.

This guide implements a **left-leaning red-black tree (LLRB)**, the cleanest
variant to write and reason about.

The implementation in `RedBlackTreeBasics.py` provides:

- A `RedBlackTree` mapping comparable keys to values with `put`, `get`,
  `delete`, `delete_min`, `delete_max`, `min`, `max`, `keys`.
- A `height` metric and an ASCII `draw()` renderer that marks red links.
- An `is_valid()` checker that verifies every red-black invariant.
- A deliberately naive `PlainBST` used to demonstrate degeneration.
- Randomized stress tests proving the invariants hold after every
  operation.

Source references:

- [Red-Black Trees Basics and Visualization](https://labuladong.online/en/algo/data-structure-basic/rbtree-basic/)
- [TreeMap Structure and Visualization](https://labuladong.online/en/algo/data-structure-basic/tree-map-basic/)

## 2. The Problem: a Plain BST Degrades into a Linked List

A binary search tree is fast only while it stays balanced. Its height
determines the cost of every operation.

Inserting keys in increasing order is the worst case. Every new key is
larger than all previous ones, so it becomes the right child of the
previous rightmost node:

```text
insert 1          insert 2          insert 3          insert 4
  (1)               (1)               (1)               (1)
                     \                 \                 \
                     (2)               (2)               (2)
                                        \                 \
                                        (3)               (3)
                                                           \
                                                           (4)
```

The "tree" is really a linked list of length N. Searching for the largest
key must walk all N nodes:

```text
plain BST after inserting 1..5 in order:
   height = 4 edges, search(5) visits: 1, 2, 3, 4, 5  (5 steps)

   (1)
     \
     (2)
       \
       (3)
         \
         (4)
           \
           (5)
```

The demo in `RedBlackTreeBasics.py` inserts `1..15` in order into both a
plain BST and a red-black tree:

```text
plain BST : height 14  (a linked list of 15 nodes)
red-black : height  3  (the perfect balanced tree)
```

## 3. Red-Black Tree Properties and the Color Convention

A red-black tree is a binary search tree with one extra bit per node: the
color **red** or **black**. The color stored on a node is really the color
of the link coming from its parent.

```text
black link (default)          red link (marked R)
     (P)                          (P)
      |                            |
     (C) black                  (C) red   <-- parent's left child is red
```

The rules that keep the tree balanced:

```text
1. every node is red or black
2. the root is black
3. red links lean left: a red node is always the LEFT child of its parent
4. no node has two red children in a row
5. every path from the root to a null leaf has the SAME number of black links
   (this is the "black height" and it is the true balancing rule)
```

Rule 5 is the heart of the matter: if all root-to-leaf paths carry the same
number of black links, the tree cannot become a long thin stick. The red
links are "room" that lets nodes grow temporarily; rule 3 keeps the shape
canonical.

A valid red-black tree with 15 nodes, drawn by the demo:

```text
       8(B)
      /    \
   4(B)    12(B)
  /   \    /    \
2(B) 6(B) 10(B) 14(B)
  ...  ...
```

## 4. The 2-3-4 Tree Correspondence

The red-black tree is not magic: it is a binary encoding of a **2-3-4
tree**, a search tree whose nodes may hold one, two, or three keys.

```text
2-node                3-node                   4-node
  (a)                 (a|b)                   (a|b|c)
                      /    \                  /  |  \
                   (<a)   (>b)            (<a)(a,b)(>c)
```

A red-black tree encodes the same structure by "gluing" the keys of a
multi-key node together with red links:

```text
2-node (one key, two children):
     (a)
    /   \
  left  right

3-node (two keys, three children)  ==  black parent + red left child:
       (b)
      /   \
    (a)   right
    /  \
 left  mid

4-node (three keys, four children) ==  black parent + two red children:
       (b)
      /   \
    (a)   (c)
    / \   / \
  l1  l2 l3  l4
```

Rule 4 ("no two red links in a row") and rule 5 ("equal black height") are
exactly the statement that the red-black tree is a 2-3-4 tree: red links
only glue nodes together, and black links are the "real" tree structure.

## 5. Rotations and Color Flips

Balance is restored with three local operations that never change the
in-order sequence of keys.

**Rotate left** moves a red right child up:

```text
     (h)                    (x)
       \                   /   \
      (x)      ==>       (h)  (c)
      /  \                 \
    (a)  (c)              (a)
```

**Rotate right** is the mirror image:

```text
       (h)                  (x)
      /                    /   \
    (x)        ==>       (a)  (h)
    /  \                      /
  (a)  (c)                 (c)
```

**Color flip** splits a 4-node: the two red children become black and the
parent turns red, pushing the "overflow" upward:

```text
      (b)  black                (b)  red
     /   \          ==>        /   \
   (a)  (c)  red             (a)  (c)  black
```

## 6. Insert Algorithm

Inserting a key into an LLRB is a normal BST insert (always with a red
new node), followed by a `fix_up` pass on the way back up that applies the
three local operations:

```text
put(key, value):
  1. BST-insert a RED node
  2. walk back up, at every node fix_up:
       if right child red and left child black   -> rotate left
       if left child red and left.left red       -> rotate right
       if left child red and right child red     -> flip colors
  3. paint the root black
```

An example: inserting keys `5, 3, 8, 2`.

```text
insert 5            insert 3                insert 8 (fix_up flips):
  (5)                 (5)                     (5)            (5)
                    /                        /   \    ==>   /   \
                  (3)R                    (3)R  (8)R      (3)   (8)

insert 2:
     (5)               (5)
    /   \             /   \
  (3)   (8)   ==>   (3)   (8)
                   /
                 (2)R
```

Step by step:

```text
1. 5 is the root, painted black.
2. 3 becomes the red left child of 5.
3. 8 becomes the red right child of 5. Now 5 has two red children,
   so fix_up flips colors: 3 and 8 turn black, 5 turns red, and
   the root is repainted black.
4. 2 becomes the red left child of 3. No rotation is needed; the
   final tree has height 2 and black height 2 on every path.
```

The invariant is simpler to state than to draw at every step: after
`fix_up`, no red link points right, no two red links stack in a row, and no
node has two red children.

Inserting `1..15` in order into an LLRB produces the perfectly balanced
all-black tree shown in section 3: height 3 instead of 14.

## 7. Delete Algorithm

Deleting from a red-black tree is harder than inserting, because removing a
node can break the equal-black-height rule. The LLRB strategy is to "make
the path red as we go down": before descending into a child, ensure that
child (or its child) is red, so deleting from it cannot change black height.

```text
delete(key):
  0. if both children of the root are black, paint the root red
  1. descend toward the key:
       if key < h.key  -> ensure h.left is red  (move_red_left)
       else            -> ensure h.right is red (move_red_right)
  2. when the key is found:
       if it has no right child        -> remove it
       else replace it with its
            in-order successor, then
            delete the successor       (delete_min on the right subtree)
  3. fix_up on the way back up
  4. paint the root black
```

The `move_red_left` / `move_red_right` helpers borrow a red link from a
sibling so the descent stays "red all the way":

```text
move_red_left(h)  --  h is red, h.left is black:
   h        (h red, left black, right black)
  / \   ==> flip colors -> h black, both children red
(a) (b)     then if b.left is red, rotate right then left, flip again

   result: h.left is now red, so we can safely descend and delete.
```

## 8. Complexity

Because rule 5 forces every path to have the same number of black links,
the black height is at most log2(N+1), and red links can at most double it:

```text
height  <=  2 * log2(N+1)

N=1000   ->  height <= 20   (a plain BST could be 1000)
N=1e6    ->  height <= 42
```

All operations are O(log N):

```text
operation     plain BST (worst)     red-black tree
------------- -------------------  --------------
put           O(N) linked list     O(log N)
get           O(N)                 O(log N)
delete        O(N)                 O(log N)
min / max     O(N)                 O(log N)
height        O(N)                 O(log N)
```

The price is a small constant factor: every insert/delete does at most two
rotations and O(log N) color flips.

## 9. Invariant Checking

The `is_valid()` method is a miniature unit test that runs inside the demo.
It verifies:

```text
check 1: in-order keys are strictly sorted          (BST ordering)
check 2: the root is black
check 3: no red node has a red child                (rule 4)
check 4: no node has a red right child              (rule 3, red leans left)
check 5: every root-to-null path has the same
         number of black links                      (rule 5, black height)
```

Recursively it returns the black height of each subtree, or -1 on the first
violation:

```text
black_height(node):
    if node is None:            return 0
    if node red and has a red child:  return -1
    if node.right is red:       return -1
    L = black_height(node.left)
    R = black_height(node.right)
    if L == -1 or R == -1 or L != R:  return -1
    return L + (0 if node is red else 1)
```

The demo calls `is_valid()` after **every** random insert and delete, so any
bug in `put`/`delete` fails immediately.

## 10. Demo Walkthrough

Running `RedBlackTreeBasics.py` prints:

```text
=== Red-Black Tree demo ===
Inserted 1..15 in increasing order.
Plain BST height : 14  (degenerated into a linked list)
Red-black height : 3  (stays logarithmic)

Red-black tree drawn with colors:
       8(B)
      4(B)  12(B)
     2(B)  6(B)  10(B)  14(B)
    1(B)  3(B)  5(B)  7(B)  9(B)  11(B)  13(B)  15(B)

Random insert / delete stress test...
Stress test passed: invariants held after every put/delete.
Final size: 0
```

What the demo proves:

```text
- the same 15 keys give height 14 in a plain BST but 3 in a red-black tree
- the 1..15 tree is a perfect all-black tree (black height 3)
- 80 random inserts keep every invariant (is_valid after each put)
- 80 random deletes keep every invariant (is_valid after each delete)
- deleting all keys leaves an empty, still-valid tree
```

## 11. Limitations and Summary

```text
strengths:
  - guaranteed O(log N) for every operation, no matter the input order
  - in-order keys stay sorted: min/max/rank/select all available
  - the standard library TreeMap/TreeSet in Java is a red-black tree

trade-offs:
  - more complex than a plain BST or an AVL tree
  - a constant-factor slowdown from rotations and color flips
  - if you only need O(1) lookups, a hash table is still faster

when to use:
  - you need sorted keys AND guaranteed log-time operations
  - you cannot tolerate the worst-case O(N) of a plain BST
```

Summary in one sentence: a red-black tree is a plain binary search tree that
colors its links so it can never tilt into a linked list, keeping every
operation at O(log N).
