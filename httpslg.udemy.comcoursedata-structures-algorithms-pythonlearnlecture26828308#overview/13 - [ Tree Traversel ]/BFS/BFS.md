
---

# Breadth-First Search (BFS)

## 1. What is Breadth-First Search?

**Breadth-First Search (BFS)** is a tree/graph traversal algorithm that visits nodes **LEVEL BY LEVEL**, from **left to right**, before going any deeper into the tree.

Instead of diving down one branch all the way to a leaf (like DFS does), BFS explores **outward** from the root — it completely finishes one level before moving on to the next one.

### Key Idea:
> "Visit everyone on your level before you meet their children."
> BFS works like a ripple in a pond — it spreads outward from the starting point, one ring at a time.

### The Data Structure Behind BFS: The QUEUE
BFS is powered by a **Queue (FIFO — First In, First Out)** — the exact same structure we built in the **Queues section (folder 6)**:
* Nodes are **enqueued** (added to the back of the queue) as they are discovered.
* Nodes are **dequeued** (removed from the front of the queue) to be visited.
* Because a queue is FIFO, nodes discovered **earlier** are always visited **earlier** — this is what forces the level-by-level order.

```
        +--------------------------------------------------+
        |              BREADTH-FIRST SEARCH                |
        +--------------------------------------------------+
        |                                                  |
        |   Visit order:  LEVEL BY LEVEL, left to right    |
        |                                                  |
        |        Level 0:   [ 47 ]                         |
        |                   /    \                         |
        |        Level 1: [21]  [76]                       |
        |                  / \    / \                      |
        |        Level 2: [18][27][52][82]                 |
        |                                                  |
        |   Powered by:  QUEUE (FIFO)                      |
        |   enqueue -> back  |  dequeue <- front           |
        +--------------------------------------------------+
```

---

## 2. Why Was BFS Created?

Some problems are not about "what is at the bottom of the tree" — they are about **proximity to the root** (or to a starting node).

DFS (Depth-First Search) dives down a branch to a leaf **before** it ever visits that node's siblings. If the answer you want is "the node CLOSEST to the start", DFS wastes time exploring deep, far-away nodes first.

BFS answers exactly one question perfectly:

> **"What is closest to the start?"**

Because BFS visits nodes in order of their **distance (number of edges) from the root**, the first time BFS reaches a node, it has arrived by the **shortest possible path** (in an unweighted graph).

```
        THE QUESTION EACH ALGORITHM ANSWERS:

        DFS:   "What is at the END of this branch?"
                        |
                        v   (dives deep first)

        BFS:   "What is CLOSEST to the root?"
                        o   (spreads outward first)
                      / | \
                     o  o  o
```

### Real-World Intuition:
If you wanted to find the person in your social network with the **fewest degrees of separation** from you who works at Google, you would check:
1. All your direct friends (distance 1)
2. All friends-of-friends (distance 2)
3. All friends-of-friends-of-friends (distance 3)

That **is** BFS. You would never check a friend-of-friend-of-friend before checking ALL direct friends — that would be DFS, and it would give you a far-away answer first.

---

## 3. What Problems Does BFS Solve?

* **Shortest path in an unweighted graph** — BFS guarantees the first path found to any node is the shortest (fewest edges). This is the foundation of algorithms like Dijkstra's (for weighted graphs).
* **Level-order printing** — print a tree one level per line.
* **Social networks — degrees of separation** — "people you may know" features are BFS to depth 2 or 3.
* **Web crawlers by depth** — crawl all pages linked from the home page before going deeper, so the crawler stays "near" the seed site.
* **Finding nodes closest to the root** — e.g., "nearest gas station" on an unweighted map.
* **Interview problems** — see the `Interview` folder in this section: `BST-Kth Smallest Node.py` and `BST-Validate BST.py` are both solved with tree traversal techniques like the ones in this folder.

```
        +----------------------------------------------------------+
        |  WHERE BFS SHOWS UP IN THE REAL WORLD                    |
        +----------------------------------------------------------+
        |                                                          |
        |   Google Maps (unweighted roads)  -> shortest route      |
        |   LinkedIn "2nd degree connection" -> BFS to depth 2     |
        |   Web crawler "stay near seed"    -> BFS by depth        |
        |   Print tree level-by-level       -> BFS naturally       |
        |                                                          |
        +----------------------------------------------------------+
```

---

## 4. The Tree We Will Use

This is the **exact tree** built by the test code at the bottom of `SOLUTION-BFS.py` (inserts: 47, 21, 76, 18, 27, 52, 82):

```
                    47
                  /    \
                21      76
               /  \    /  \
             18   27  52   82
```

### Its levels:

```
        Level 0:                          47
                                       /      \
        Level 1:                     21        76
                                    /  \      /  \
        Level 2:                  18    27  52    82

        Width of Level 0 = 1
        Width of Level 1 = 2
        Width of Level 2 = 4   <== max width of this tree (w = 4)
```

### The BFS visiting order over this tree (1..7):

```
                 [1] 47
                 /      \
                /        \
           [2] 21        [3] 76
           /    \        /    \
      [4] 18  [5] 27 [6] 52 [7] 82

      Expected result list:  [47, 21, 76, 18, 27, 52, 82]
```

---

## 5. How BFS Works — Step by Step

The algorithm in plain English:

```
    1. Put the ROOT in the queue.
    2. While the queue is NOT empty:
         a. DEQUEUE the front node  -> this node is now VISITED.
         b. APPEND its value to the results list.
         c. ENQUEUE its LEFT child  (if it exists).
         d. ENQUEUE its RIGHT child (if it exists).
    3. Return the results list.
```

### Queue mechanics (FIFO):

```
        back                                              front
          |                                                 |
          v                                                 v
        +-----+-----+-----+-----+-----+-----+-----+
        |  82 |  52 |  27 |  18 |  76 |  21 |  47 |
        +-----+-----+-----+-----+-----+-----+-----+
          ^                                                 ^
          |                                                 |
    new children enter here              nodes leave here to be visited
```

### Full Step-by-Step Trace (queue, dequeue, enqueue, results):

| Step | Queue (front -> back) | Dequeued / Visited | Children Enqueued | Results So Far |
|:---|:---|:---|:---|:---|
| 0 | `[47]` | — | — | `[]` |
| 1 | `[21, 76]` | `47` | `21, 76` | `[47]` |
| 2 | `[76, 18, 27]` | `21` | `18, 27` | `[47, 21]` |
| 3 | `[18, 27, 52, 82]` | `76` | `52, 82` | `[47, 21, 76]` |
| 4 | `[27, 52, 82]` | `18` | (none — leaf) | `[47, 21, 76, 18]` |
| 5 | `[52, 82]` | `27` | (none — leaf) | `[47, 21, 76, 18, 27]` |
| 6 | `[82]` | `52` | (none — leaf) | `[47, 21, 76, 18, 27, 52]` |
| 7 | `[]` | `82` | (none — leaf) | `[47, 21, 76, 18, 27, 52, 82]` |

Queue is now **empty** — the loop ends and the results list is returned.

### The same trace, drawn step by step:

```
    STEP 1:  dequeue 47, enqueue 21 & 76
             queue = [21, 76]          results = [47]

    STEP 2:  dequeue 21, enqueue 18 & 27
             queue = [76, 18, 27]      results = [47, 21]

    STEP 3:  dequeue 76, enqueue 52 & 82
             queue = [18, 27, 52, 82]  results = [47, 21, 76]
                         ^
             widest the queue ever gets = 4 = width of bottom level

    STEP 4:  dequeue 18 (leaf, nothing to enqueue)
             queue = [27, 52, 82]      results = [47, 21, 76, 18]

    STEP 5:  dequeue 27 (leaf)
             queue = [52, 82]          results = [47, 21, 76, 18, 27]

    STEP 6:  dequeue 52 (leaf)
             queue = [82]              results = [47, 21, 76, 18, 27, 52]

    STEP 7:  dequeue 82 (leaf)
             queue = []                results = [47, 21, 76, 18, 27, 52, 82]

    QUEUE EMPTY  =>  DONE.  Notice: the queue's MAX size was the tree's max width.
```

### Level-by-level visiting order with arrows:

```
                          47  <------ visit #1
                 -------- Level 0 --------------------
                         /    \
                       21      76  <-- visit #2, #3
                 -------- Level 1 --------------------
                      /  \    /  \
                    18   27  52   82  <- visit #4, #5, #6, #7
                 -------- Level 2 --------------------

        Direction of travel:  ===============================>

        A level is ALWAYS completely finished before the
        next level begins — that is the QUEUE doing its job.
```

---

## 6. The Code

This is the **actual, verbatim** code from `SOLUTION-BFS.py` in this folder. Note the comment at the top — writing BFS with a real `Queue` class (like the one from folder 6) is technically the better solution; the list version below is the simplified one used in the course:

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
    
   
    # YOU CAN ALSO WRITE BFS WITH A QUEUE INSTEAD OF LIST
    # (TECHNICALLY THIS IS A BETTER SOLUTION)
    #
    # def BFS(self):
    #     current_node = self.root
    #     queue = Queue()
    #     results = []
    #     queue.put(current_node)

    #     while not queue.empty():
    #         current_node = queue.get()
    #         results.append(current_node.value)
    #         if current_node.left is not None:
    #             queue.put(current_node.left)
    #         if current_node.right is not None:
    #             queue.put(current_node.right)
    #     return results
                
    
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




my_tree = BinarySearchTree()
my_tree.insert(47)
my_tree.insert(21)
my_tree.insert(76)
my_tree.insert(18)
my_tree.insert(27)
my_tree.insert(52)
my_tree.insert(82)

print(my_tree.BFS())



"""
    EXPECTED OUTPUT:
    ----------------
    [47, 21, 76, 18, 27, 52, 82]

 """
```

### Line-by-line walkthrough of `BFS()`:

```
    queue.append(current_node)      <- root enters the queue (back)

    while len(queue) > 0:           <- keep going until nothing left to visit
        current_node = queue.pop(0) <- DEQUEUE from the FRONT (FIFO!)
        results.append(...)         <- VISIT: record the value
        if left  exists: enqueue it <- children wait their turn at the back
        if right exists: enqueue it
```

> **One line does all the magic:** `queue.pop(0)` removes from the **front** while `append` adds to the **back**. That single FIFO decision is what turns "dive deep" into "level by level".

---

## 7. Big O Analysis

| Complexity | Value | Why |
|:---|:---|:---|
| **Time** | `O(n)` | Every node is enqueued once, dequeued once, and visited once |
| **Space** | `O(w)` | The queue holds at most **one full level** of the tree at a time, where `w` = the **maximum width** of the tree |

### Why space is `O(w)` — and why that can be bad:

```
        A PERFECT BINARY TREE — every level DOUBLES:

        Level 0:                        o                    width 1
        Level 1:                o               o            width 2
        Level 2:            o       o       o       o        width 4
        Level 3:          o   o   o   o   o   o   o   o      width 8
                            \______________________/
                              the BOTTOM level alone
                              holds about  n / 2  nodes!
```

For a **perfect/full** tree, the bottom level contains roughly **half of all nodes** (`≈ n/2`). Since BFS must hold that entire level in the queue before moving on, the **worst-case space is effectively `O(n)`** for a wide tree.

```
        +-----------------------+---------------------------+
        |                       |  SPACE NEEDED             |
        +-----------------------+---------------------------+
        |  BFS (queue)          |  O(w) — up to ~n/2        |
        |                       |  (BAD for wide trees)     |
        +-----------------------+---------------------------+
        |  DFS (call stack)     |  O(h) — just the height   |
        |                       |  (BAD for deep trees)     |
        +-----------------------+---------------------------+

        BFS trades memory for breadth; DFS trades it for depth.
```

---

## 8. BFS vs DFS — Quick Comparison

| | **BFS** | **DFS** |
|:---|:---|:---|
| **Visit order** | Level by level, left to right | Down a branch to the leaf, then backtrack |
| **Data structure** | Queue (FIFO) | Call stack via recursion (LIFO) |
| **Time** | `O(n)` | `O(n)` |
| **Space** | `O(w)` — max width | `O(h)` — tree height |
| **Best when tree is...** | Deep and narrow | Wide and short |
| **Classic use** | Shortest path, level-order, "closest to root" | Sorted BST output (In-Order), serialization (Pre-Order), deletion (Post-Order) |

---

**Next Step:** Now let's look at the other side of traversal — Depth-First Search (DFS) and its three variants: Pre-Order, In-Order, and Post-Order!
