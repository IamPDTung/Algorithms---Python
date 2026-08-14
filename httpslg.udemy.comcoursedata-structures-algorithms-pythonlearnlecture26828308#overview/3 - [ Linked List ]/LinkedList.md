
---

# Linked List

## 1. What is a Linked List?

A **Linked List** is a **linear data structure** made of **Nodes**, where each node stores two things:

* a **value** — the data the node holds
* a **next** pointer — a reference to the **next node** in the chain

The list itself keeps track of two special pointers plus a counter:

* **head** — points to the FIRST node
* **tail** — points to the LAST node
* **length** — how many nodes are in the list

The last node's `next` is **None**, which marks the end of the chain.

### Key Idea:
> A linked list is a treasure hunt: every node contains a clue (its `next`
> pointer) telling you where to find the following node in memory.

### The KEY Difference vs a Python List:
> A Python list has **indexes** (0, 1, 2, ...). A linked list has **NO index**.
> The only way to reach a node is to start at `head` and follow the pointers.

### Anatomy of a Node and a List:

```
    ONE NODE:

        +---------+--------+
        |  value  |  next  | -----> points to the next node (or None)
        +---------+--------+


    A LINKED LIST with values 1 -> 2 -> 3 -> 4:

       head                                                    tail
         |                                                       |
         v                                                       v
       +---+---+      +---+---+      +---+---+      +---+--------+
       | 1 | * | ---> | 2 | * | ---> | 3 | * | ---> | 4 | None |
       +---+---+      +---+---+      +---+---+      +---+--------+
         ^
         |
       NO INDEX! To reach the node with 3, you must walk
       head -> 1 -> 2 -> 3, one pointer at a time.
```

---

## 2. Why Were Linked Lists Created?

Python lists (dynamic arrays) store their elements in **one contiguous block of memory**. That design gives fast indexing, but it has a painful cost: **inserting or removing at the front forces every other element to shift one slot**.

```
    PYTHON LIST - contiguous memory block:

       Index:     0        1        2        3
               +--------+--------+--------+--------+
     Values:   |   11   |   3    |   23   |   7    |
               +--------+--------+--------+--------+
     Address:    100      104      108      112     <- one solid block


     insert(0, 99)  =>  EVERY element must move one slot to the right:

               +--------+--------+--------+--------+--------+
               |   99   |   11   |   3    |   23   |   7    |
               +--------+--------+--------+--------+--------+
                          \_______ ALL SHIFTED _______/  =>  O(n)


    LINKED LIST - nodes scattered anywhere in memory:

       +-------+        +-------+        +-------+
       | 11|*  | -----> | 3 |*  | -----> | 23|*  | -----> None
       +-------+        +-------+        +-------+
       addr 100         addr 372         addr 215


     prepend(99)  =>  create one node, rewire ONE pointer:

       +-------+        +-------+        +-------+        +-------+
       | 99|*  | -----> | 11|*  | -----> | 3 |*  | -----> | 23|*  | -> None
       +-------+        +-------+        +-------+        +-------+
       addr 517         (nothing else moves!)              =>  O(1)
```

### Summary:

| Operation at the FRONT | Python List | Linked List |
|:---|:---|:---|
| Insert at front | `O(n)` — shift everything | **`O(1)`** — rewire one pointer |
| Remove from front | `O(n)` — shift everything | **`O(1)`** — move `head` |
| Needs contiguous memory? | Yes | **No** — nodes live anywhere |

---

## 3. What Problems Does a Linked List Solve?

* **Dynamic size** — grows and shrinks node by node; no resizing, no copying.
* **Frequent insertions/removals at the front** — `O(1)` instead of `O(n)`.
* **No contiguous memory needed** — nodes can be scattered across the heap.
* **Foundation for other data structures**:

```
    +-----------------------------------------------------------+
    |             LINKED LISTS ARE THE BASE OF:                 |
    +-----------------------------------------------------------+
    |   STACK       -> push/pop = prepend / pop_first   (O(1))  |
    |   QUEUE       -> enqueue = append, dequeue = pop_first    |
    |   GRAPH       -> adjacency lists store neighbors          |
    |   HASH TABLE  -> chaining: buckets are linked lists       |
    |   DOUBLY LL   -> adds a "prev" pointer (next topic)       |
    +-----------------------------------------------------------+
```

### Classic Interview Problems (solved in the `Leetcode/` folder):

```
    +------------------------------------------------+--------------+
    |  PROBLEM                                       | KEY TECHNIQUE|
    +------------------------------------------------+--------------+
    |  141. Linked List Cycle                        | Fast/slow ptr|
    |  206. Reverse Linked List                      | 3-ptr flip   |
    |  876. Middle of the Linked List                | Fast/slow ptr|
    |  19. Remove Nth Node From End of List          | Two pointers |
    |  24. Swap Nodes in Pairs                       | Ptr rewiring |
    |  83. Remove Duplicates from Sorted List        | Single pass  |
    |  86. Partition List                            | Two lists    |
    |  92. Reverse Linked List II                    | Sublist flip |
    |  1290. Convert Binary Number in a LL to Int    | Single pass  |
    +------------------------------------------------+--------------+
```

---

## 4. Building a Node and the Constructor

Each **Node** is just an object with `value` and `next`. The **LinkedList** constructor creates the very first node and points both `head` and `tail` at it.

### The Code (SOLUTION-LL-Constructor.py):

```python
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        

class LinkedList:
    def __init__(self, value):
        new_node = Node(value)
        self.head = new_node
        self.tail = new_node
        self.length = 1
```

### What `LinkedList(4)` builds in memory:

```
       head
         |
         v
       +---+--------+
       | 4 | None |      <- one node: head and tail BOTH point to it
       +---+--------+
         ^
         |
       tail          length = 1
```

---

## 5. Append — O(1)

**Goal:** add a new node at the END of the list. Thanks to the `tail` pointer, this is a constant-time operation.

```
    BEFORE append(2) on a list containing [1]:

       head
         |
         v
       +---+--------+
       | 1 | None |
       +---+--------+
         ^
        tail

    STEP 1: self.tail.next = new_node   -> wire the old tail to the new node

       +---+---+      +---+--------+
       | 1 | * | ---> | 2 | None |
       +---+---+      +---+--------+
         ^               ^
       head           new_node     (tail still points at 1!)

    STEP 2: self.tail = new_node        -> move tail to the new last node

       +---+---+      +---+--------+
       | 1 | * | ---> | 2 | None |
       +---+---+      +---+--------+
         ^               ^
       head             tail         length = 2
```

**Edge case:** if the list is empty, `head` and `tail` both point at the new node.

### The Code (SOLUTION-LL-Append.py):

```python
    def append(self, value):
        new_node = Node(value)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.length += 1
```

---

## 6. Pop — O(n)

**Goal:** remove the LAST node and return it. The problem: in a singly linked list there is no way to go backwards, so to find the node **before** `tail` we must walk all the way from `head`.

```
    BEFORE pop() on [1 -> 2 -> 3]:

       head                              tail
         |                                 |
         v                                 v
       [ 1 | * ] ---> [ 2 | * ] ---> [ 3 | None ]

    STEP 1: walk temp (and pre chasing behind) until temp is LAST

       [ 1 | * ] ---> [ 2 | * ] ---> [ 3 | None ]
                         ^              ^
                        pre            temp

    STEP 2: self.tail = pre          -> the node before becomes the new tail
    STEP 3: self.tail.next = None    -> cut the last node off the chain

       [ 1 | * ] ---> [ 2 | None ]      [ 3 | None ]
                         ^                 ^
                        tail              temp -> RETURNED

                        length = 2
```

**Edge cases:** empty list -> return `None`; if the list becomes empty after the pop, reset `head = None` and `tail = None`.

### The Code (SOLUTION-LL-Pop.py):

```python
    def pop(self):
        if self.length == 0:
            return None
        temp = self.head
        pre = self.head
        while(temp.next):
            pre = temp
            temp = temp.next
        self.tail = pre
        self.tail.next = None
        self.length -= 1
        if self.length == 0:
            self.head = None
            self.tail = None
        return temp
```

> This walk from `head` is exactly why `pop()` is **O(n)** — and why Doubly Linked Lists (next topic) exist.

---

## 7. Prepend — O(1)

**Goal:** add a new node at the FRONT of the list. This is where linked lists shine — no shifting, just two pointer moves.

```
    BEFORE prepend(0) on [1 -> 2]:

       head
         |
         v
       [ 1 | * ] ---> [ 2 | None ]

    STEP 1: new_node.next = self.head   -> new node points at the old head

       [ 0 | * ] ---+
                    |
                    v
       head ---> [ 1 | * ] ---> [ 2 | None ]

    STEP 2: self.head = new_node        -> head moves to the new node

       head
         |
         v
       [ 0 | * ] ---> [ 1 | * ] ---> [ 2 | None ]
                                         ^
                                        tail     length = 3
```

### The Code (SOLUTION-LL-Prepend.py):

```python
    def prepend(self, value):
        new_node = Node(value)
        if self.length == 0:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head = new_node
        self.length += 1
        return True
```

---

## 8. Pop First — O(1)

**Goal:** remove the FIRST node and return it. Just move `head` one step forward — the opposite of `pop()`, and it costs **O(1)**.

```
    BEFORE pop_first() on [1 -> 2 -> 3]:

       head
         |
         v
       [ 1 | * ] ---> [ 2 | * ] ---> [ 3 | None ]

    STEP 1: temp = self.head             -> remember the node to remove
    STEP 2: self.head = self.head.next   -> head slides one step right

       [ 1 | * ] ---> [ 2 | * ] ---> [ 3 | None ]
          ^              ^
         temp           head

    STEP 3: temp.next = None             -> fully detach the old head

       [ 1 | None ]     [ 2 | * ] ---> [ 3 | None ]
           ^               ^
        RETURNED          head          tail
```

**Edge case:** if the list becomes empty, also set `tail = None`.

### The Code (SOLUTION-LL-Pop_First.py):

```python
    def pop_first(self):
        if self.length == 0:
            return None
        temp = self.head
        self.head = self.head.next
        temp.next = None
        self.length -= 1
        if self.length == 0:
            self.tail = None
        return temp
```

---

## 9. Get & Set — O(n)

**Goal:** read (or update) the node at a given position. Since there is **no index**, `get` must start at `head` and follow `next` exactly `index` times.

```
    get(2) on [11 -> 3 -> 23 -> 7]:

       head
         |
         v
       [ 11 | * ] ---> [ 3 | * ] ---> [ 23 | * ] ---> [ 7 | None ]
          ^                ^              ^
        step 0           step 1         step 2  -> RETURN this node
       (temp = head)   (1st move)     (2nd move)
```

### The Code (SOLUTION-LL-Get.py):

```python
    def get(self, index):
        if index < 0 or index >= self.length:
            return None
        temp = self.head
        for _ in range(index):
            temp = temp.next
        return temp
```

`set_value` simply reuses `get`: if the node exists, overwrite its `value`.

### The Code (SOLUTION-LL-Set.py):

```python
    def set_value(self, index, value):
        temp = self.get(index)
        if temp:
            temp.value = value
            return True
        return False
```

---

## 10. Insert — O(n)

**Goal:** insert a new node at a given index. Ends are delegated: index `0` -> `prepend`, index `length` -> `append`. In the middle, two pointers get rewired.

```
    insert(1, 99) on [1 -> 2 -> 3]:

    STEP 1: temp = get(index - 1)   -> the node BEFORE the insertion point

       temp
         |
         v
       [1] ---> [2] ---> [3] ---> None

    STEP 2: new_node.next = temp.next   -> [99] points at [2]
            (BOTH [1] and [99] now point at [2])

       [1] ---> [2] ---> [3] ---> None
                 ^
                 |
               [99]  (new_node)

    STEP 3: temp.next = new_node        -> [1] points at [99]

       [1] ---> [99] ---> [2] ---> [3] ---> None
```

### The Code (SOLUTION-LL-Insert.py):

```python
    def insert(self, index, value):
        if index < 0 or index > self.length:
            return False
        if index == 0:
            return self.prepend(value)
        if index == self.length:
            return self.append(value)
        new_node = Node(value)
        temp = self.get(index - 1)
        new_node.next = temp.next
        temp.next = new_node
        self.length += 1   
        return True  
```

---

## 11. Remove — O(n)

**Goal:** remove the node at a given index and return it. Ends are delegated: index `0` -> `pop_first`, index `length - 1` -> `pop`. In the middle, we jump over the target.

```
    remove(1) on [1 -> 2 -> 3]:

    STEP 1: pre  = get(index - 1)   -> node before the target
            temp = pre.next         -> the target node itself

       [1] ---> [2] ---> [3] ---> None
        ^         ^
       pre       temp

    STEP 2: pre.next = temp.next    -> arrow JUMPS OVER the target

       [1] ---+         +---> [3] ---> None
              |         |
              +---------+      [2] bypassed

    STEP 3: temp.next = None        -> detach and return it

       [1] ---> [3] ---> None       [2 | None] -> RETURNED
```

### The Code (SOLUTION-LL-Remove.py):

```python
    def remove(self, index):
        if index < 0 or index >= self.length:
            return None
        if index == 0:
            return self.pop_first()
        if index == self.length - 1:
            return self.pop()
        pre = self.get(index - 1)
        temp = pre.next
        pre.next = temp.next
        temp.next = None
        self.length -= 1
        return temp
```

---

## 12. Reverse — O(n)

**Goal:** flip the whole list in place. The classic interview answer uses **three pointers**: `before`, `temp` (current), and `after`.

```
    reverse() on [1 -> 2 -> 3]:

    STEP 0: swap head and tail;  before = None;  temp = old head

       tail                              head
         |                                 |
         v                                 v
       [1] ---> [2] ---> [3] ---> None
        ^
      temp     before = None

    THE LOOP (repeat length times):
        after     = temp.next     # 1. remember the rest of the chain
        temp.next = before        # 2. FLIP the current pointer
        before    = temp          # 3. slide before one step right
        temp      = after         # 4. slide temp   one step right

    PASS 1:  None <--- [1]    [2] ---> [3] ---> None
                        ^       ^
                     before   temp

    PASS 2:  None <--- [1] <--- [2]    [3] ---> None
                                 ^       ^
                              before   temp

    PASS 3:  None <--- [1] <--- [2] <--- [3]
                                          ^
                                       before (temp = None, loop ends)

    FINAL:   head ---> [3] ---> [2] ---> [1] ---> None
             tail still points at [1]. Done!
```

### The Code (SOLUTION-LL-Reverse.py):

```python
    def reverse(self):
        temp = self.head
        self.head = self.tail
        self.tail = temp
        after = temp.next
        before = None
        for _ in range(self.length):
            after = temp.next
            temp.next = before
            before = temp
            temp = after
```

---

## 13. Big O Summary

| Method | Time | Why |
|:---|:---|:---|
| `append(value)` | **`O(1)`** | `tail` gives direct access — rewire one pointer |
| `pop()` | **`O(n)`** | must walk from `head` to find the node BEFORE `tail` |
| `prepend(value)` | **`O(1)`** | only `head` is rewired |
| `pop_first()` | **`O(1)`** | only `head` moves |
| `get(index)` | **`O(n)`** | no index — traverse from `head` |
| `set_value(index, value)` | **`O(n)`** | uses `get` first |
| `insert(index, value)` | **`O(n)`** | uses `get(index - 1)` first |
| `remove(index)` | **`O(n)`** | uses `get(index - 1)` first |
| `reverse()` | **`O(n)`** | one pass; every pointer flipped once |

| Lookup | Time |
|:---|:---|
| By value | `O(n)` — linear scan |
| By index | `O(n)` — no direct indexing |

---

## 14. Linked List vs Python List

```
    +---------------------------+------------------+-------------------+
    |  OPERATION                |  LINKED LIST     |  PYTHON LIST      |
    +---------------------------+------------------+-------------------+
    |  Lookup by index          |  O(n)            |  O(1)   <-- WINS  |
    |  Append (at end)          |  O(1)            |  O(1) amortized   |
    |  Pop (at end)             |  O(n)            |  O(1)   <-- WINS  |
    |  Prepend (at front)       |  O(1) <-- WINS   |  O(n)             |
    |  Pop first (at front)     |  O(1) <-- WINS   |  O(n)             |
    |  Insert/Remove in middle  |  O(n)            |  O(n)             |
    |  Memory layout            |  Scattered       |  Contiguous       |
    |  Extra memory per item    |  One next pointer|  None             |
    +---------------------------+------------------+-------------------+
```

### The Rule of Thumb:
> Need fast **indexing** and **end** operations? Use a **Python list**.
> Need fast **front** insertions/removals and a **dynamic size**? Use a **linked list**.

| Criteria | Linked List | Python List |
|:---|:---|:---|
| Indexing | `O(n)` | `O(1)` |
| Append / Pop at end | `O(1)` / `O(n)` | `O(1)` / `O(1)` |
| Insert / Remove at front | `O(1)` / `O(1)` | `O(n)` / `O(n)` |
| Memory | Scattered + extra pointer per node | Contiguous block |
| Cache friendliness | Poor | Excellent |

---

**Next Step:** Now let's upgrade the Linked List with a second pointer — the **Doubly Linked List** — and turn `pop()` from O(n) into O(1)!
