---
# Doubly Linked List
## 1. What Is a Doubly Linked List?
A **Doubly Linked List (DLL)** is a linear data structure made from independent **nodes**. Every node stores a value and two links: `next` points forward and `prev` points backward. The list object stores `head`, `tail`, and `length`.
Unlike a Python list, a linked list has no direct array index. To reach a position, follow links from one node to another. A DLL can begin at either end because every node knows both neighbors.

```text
ONE NODE:
    +---------------------------+
    | prev | value | next        |
    +---------------------------+
      ^                  |
      |                  v
    previous node     next node
LIST [1, 2, 3]:
    head                                      tail
      |                                         |
      v                                         v
    [None | 1 | *] <--> [* | 2 | *] <--> [* | 3 | None]
    prev of head is None; next of tail is None.
```
The links are references, not copies of values. The nodes may be scattered in memory; `next` and `prev` preserve the logical order.
---
## 2. Why Was It Created?
A **Singly Linked List (SLL)** has only `next`. Its tail is easy to find when `tail` is stored, but removing the tail requires the node before it. That predecessor cannot be reached by moving backward, so SLL `pop()` walks from `head` and costs `O(n)`.
DLL adds `prev` specifically to solve that backward-traversal problem. The old tail already points to its predecessor, so DLL `pop()` can move `tail` left in `O(1)`. The extra pointer costs memory, but it removes repeated full-list walks.

```text
SLL tail removal: must search from the front
    head                                      tail
      |                                         |
      v                                         v
    [1 | *] ----> [2 | *] ----> [3 | None]
       walk ---------------------------> predecessor of tail

DLL tail removal: predecessor is already available
    head                                      tail
      |                                         |
      v                                         v
    [None|1|*] <--> [*|2|*] <--> [*|3|None]
                                  ^
                                  | tail.prev
    +----> [2]
```
| Question | SLL | DLL |
|:---|:---|:---|
| Forward traversal | `O(n)` | `O(n)` |
| Backward traversal | Not supported directly | `O(n)` from `tail` |
| Remove last with a tail pointer | `O(n)` | **`O(1)`** |
| Remove first | `O(1)` | `O(1)` |
| Extra link per node | `next` | `next` plus `prev` |
---
## 3. Problems Solved by DLLs
DLLs are useful when an item has a natural predecessor and successor and both directions matter.

* **Browser history:** the current page moves to `next` on Forward and to `prev` on Back.
* **Undo/redo:** an edit cursor moves backward through undo states and forward through redo states.
* **LRU cache:** a hash map finds a node and a DLL moves it to the front or removes it from the middle in `O(1)` once the node is known.
* **Deque (double-ended queue):** append and remove at both ends without shifting an array.
```text
                 +----------------------+
                 | current node         |
                 +----------------------+
                    ^                |
      undo / Back   |                | redo / Forward
                    |                v
             [older state] <--> [newer state]

DEQUE:       pop_first / prepend       append / pop
             <--------------------->
```
The DLL does not automatically make every lookup constant time. It makes end operations and known-node rewiring constant time. An LRU cache still needs a map from key to node; the map supplies lookup and the DLL supplies order.
---
## 4. Node, Head, Tail, and Length
The course `Node` has exactly three fields:

* `value` is the payload.
* `next` references the next node, or `None` at the tail.
* `prev` references the previous node, or `None` at the head.
The list metadata has three roles:

* `head` identifies the first node.
* `tail` identifies the last node.
* `length` records the number of nodes and lets methods validate indexes.
```text
NONEMPTY DLL:
    head                                                        tail
      |                                                           |
      v                                                           v
    [prev=None | value=A | next=*] <--> [prev=* | value=B | next=None]
                    length = 2

EMPTY STATE AFTER REMOVAL:
    head = None       tail = None       length = 0
```
The source files initialize a new node with both links set to `None`. The constructor accepts an initial value, so `DoublyLinkedList(value)` starts with one node; an empty list is reached after removing that node.
### Course source: `SOLUTION-DLL-Constructor.py`
```python
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None
        

class DoublyLinkedList:
    def __init__(self, value):
        new_node = Node(value)
        self.head = new_node
        self.tail = new_node
        self.length = 1
```
### Pointer Invariants
1. If `length == 0`, `head is None` and `tail is None`.
2. If `length > 0`, both `head` and `tail` are not `None`.
3. `head.prev is None` and `tail.next is None`.
4. For every forward link, `node.next.prev is node`.
5. For every backward link, `node.prev.next is node`.
6. `head is tail` exactly when `length == 1`.
7. Counting nodes forward from `head` and backward from `tail` both gives `length`.
After removing a node, the returned node should be detached: its `next` and `prev` are `None`. These invariants are the quickest way to detect a missed pointer assignment.
---
## 5. Construction
`DoublyLinkedList(value)` allocates one `Node`, assigns the same object to `head` and `tail`, and sets `length` to `1`. The node is both the first and last node, so its `next` and `prev` remain `None`.
```text
BEFORE construction:
    no list object

AFTER DoublyLinkedList(7):
             head, tail
                |
                v
    None <--> [prev=None | value=7 | next=None] <--> None
                length = 1
```
| Construction work | Time | Extra space |
|:---|:---:|:---:|
| Allocate the first node and metadata | `O(1)` | `O(1)` |
There is no no-argument constructor in the course implementation. Do not assume `DoublyLinkedList()` creates an empty list; the required argument is the first value.
---
## 6. Append
`append(value)` adds a node after the current `tail`. For a nonempty list, the old tail's `.next` points to the new node, the new node's `.prev` points back to the old tail, and `tail` moves. The new node's `.next` was already `None` in `Node.__init__`.
```text
BEFORE append(4):
    head                              tail
      |                                 |
      v                                 v
    [None|1|*] <--> [*|2|*] <--> [*|3|None]
AFTER append(4):
    head                                           tail
      |                                              |
      v                                              v
    [None|1|*] <--> [*|2|*] <--> [*|3|*] <--> [*|4|None]
```
Pointer updates, in source order:

1. `self.tail.next = new_node`: old tail now points forward to the new node.
2. `new_node.prev = self.tail`: new node points backward to the old tail.
3. `self.tail = new_node`: metadata identifies the new final node.
4. `self.length += 1`: count increases after the links are valid.
For an empty state, the source assigns both `self.head = new_node` and `self.tail = new_node`; no `.next` or `.prev` link needs another assignment.
### Course source: `SOLUTION-DLL-Append.py`
```python
    def append(self, value):
        new_node = Node(value)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
        self.length += 1
        return True
```
Time is `O(1)` and auxiliary space is `O(1)`. The method returns `True`.
---
## 7. Pop
`pop()` removes and returns the final node. DLL changes the operation that was slow in SLL: `temp = self.tail`, then `self.tail = self.tail.prev` reaches the predecessor directly.
```text
BEFORE pop() on [1, 2, 3]:
    head                              tail
      |                                 |
      v                                 v
    [None|1|*] <--> [*|2|*] <--> [*|3|None]
                                     ^
                                      temp
AFTER pop():
    head                       tail                 returned temp
      |                          |                         |
      v                          v                         v
    [None|1|*] <--> [*|2|None]  [None|3|None]
```
Pointer and metadata updates for a list with more than one node:

1. `temp = self.tail` saves the node to return.
2. `self.tail = self.tail.prev` moves `tail` to the predecessor.
3. `self.tail.next = None` marks the new tail and cuts the forward link.
4. `temp.prev = None` detaches the returned node backward.
5. `self.length -= 1` updates the count.
For one node, the source sets `self.head = None` and `self.tail = None`; it does not need link rewiring because both links were already `None`. For an empty list it returns `None` before reading `tail`.
### Course source: `SOLUTION-DLL-Pop.py`
```python
    def pop(self):
        if self.length == 0:
            return None
        temp = self.tail
        if self.length == 1:
            self.head = None
            self.tail = None 
        else:       
            self.tail = self.tail.prev
            self.tail.next = None
            temp.prev = None
        self.length -= 1
        return temp
```
Time is `O(1)`, auxiliary space is `O(1)`, and the return value is a detached `Node` or `None`.
---
## 8. Prepend
`prepend(value)` inserts a node before the current `head`. The old head remains the first existing node, but the new node becomes the new head.
```text
BEFORE prepend(0):
    head                              tail
      |                                 |
      v                                 v
    [None|1|*] <--> [*|2|None]
AFTER prepend(0):
    head                                           tail
      |                                              |
      v                                              v
    [None|0|*] <--> [*|1|*] <--> [*|2|None]
```
Pointer updates, in source order:

1. `new_node.next = self.head`: new node points forward to the old head.
2. `self.head.prev = new_node`: old head points backward to the new node.
3. `self.head = new_node`: metadata moves to the new first node.
4. `self.length += 1`: count increases.
`new_node.prev` remains `None` from construction. In the empty branch, `head` and `tail` both become `new_node`; the new node already has two null links.
### Course source: `SOLUTION-DLL-Prepend.py`
```python
    def prepend(self, value):
        new_node = Node(value)
        if self.length == 0:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        self.length += 1
        return True
```
Time and auxiliary space are both `O(1)`. The method returns `True`.
---
## 9. Pop First
`pop_first()` removes and returns the first node. It is the mirror of `pop()`: use `head.next`, clear the new head's `prev`, and detach the old head's `next`.
```text
BEFORE pop_first() on [1, 2, 3]:
    head                              tail
      |                                 |
      v                                 v
    [None|1|*] <--> [*|2|*] <--> [*|3|None]
      ^
     temp
AFTER pop_first():
    returned temp          head                       tail
          |                  |                          |
          v                  v                          v
    [None|1|None]  [None|2|*] <--> [*|3|None]
```
Pointer and metadata updates:

1. `temp = self.head` saves the old head.
2. `self.head = self.head.next` advances to the second node.
3. `self.head.prev = None` makes the new head's backward boundary explicit.
4. `temp.next = None` detaches the returned node forward.
5. `self.length -= 1` updates the count.
With one node, the source sets both `head` and `tail` to `None`; it does not execute the multi-node link assignments. With no nodes, it returns `None`.
### Course source: `SOLUTION-DLL-Pop_First.py`
```python
    def pop_first(self):
        if self.length == 0:
            return None
        temp = self.head
        if self.length == 1:
            self.head = None
            self.tail = None
        else:
            self.head = self.head.next
            self.head.prev = None
            temp.next = None      
        self.length -= 1
        return temp
```
Time is `O(1)` and auxiliary space is `O(1)`.
---
## 10. Get and Direction Choice
`get(index)` returns the node at a valid zero-based index. Invalid indexes (`index < 0` or `index >= length`) return `None`.
The course deliberately chooses a direction. If `index < self.length / 2`, it starts at `head` and follows `.next`. Otherwise it starts at `tail` and follows `.prev`. Because the comparison is strict, the middle index of an odd-sized list belongs to the tail branch.
```text
BEFORE get(1) or get(3):
    head                                             tail
      |                                                |
      v                                                v
    [0] <--> [1] <--> [2] <--> [3] <--> [4]
      |------ forward for small index ------>|        |
      |<------ backward for large index ------|        |

AFTER get: `temp` is [1] via next or [3] via prev; links remain unchanged.
    [0] <--> [1] <--> [2] <--> [3] <--> [4]
```
`get` does not modify any `.next` or `.prev` field. It only moves a local variable `temp`; this is a read-only traversal. Its work is `O(min(index, length - 1 - index))` under the two-direction strategy, with `O(n)` worst-case time and `O(1)` auxiliary space.
### Course source: `SOLUTION-DLL-Get.py`
```python
    def get(self, index):
        if index < 0 or index >= self.length:
            return None
        temp = self.head
        if index < self.length/2:
            for _ in range(index):
                temp = temp.next
        else:
            temp = self.tail
            for _ in range(self.length - 1, index, -1):
                temp = temp.prev  
        return temp
```
---
## 11. Set Value
The course method is named `set_value(index, value)`. It calls `get(index)`, changes only the selected node's `.value`, and returns a Boolean. An invalid index returns `False`; a valid index returns `True`.
```text
BEFORE set_value(1, 99):
    head                                      tail
      |                                         |
      v                                         v
    [None|10|*] <--> [*|20|*] <--> [*|30|None]
                             target

AFTER set_value(1, 99):
    head                                      tail
      |                                         |
      v                                         v
    [None|10|*] <--> [*|99|*] <--> [*|30|None]
    next and prev links are unchanged.
```
The only field update is `temp.value = value`. `get` performs the directional traversal, so `set_value` has `O(n)` worst-case time and `O(1)` auxiliary space. It does not create a node, change `head`, change `tail`, or change `length`.
### Course source: `SOLUTION-DLL-Set.py`
```python
    def set_value(self, index, value):
        temp = self.get(index)
        if temp:
            temp.value = value
            return True
        return False
```
---
## 12. Insert
`insert(index, value)` accepts indexes from `0` through `length`, inclusive. The source delegates `index == 0` to `prepend` and `index == length` to `append`. Only a middle insertion performs four link assignments.
```text
BEFORE insert(2, 99):
    head                              tail
      |                                 |
      v                                 v
    [None|1|*] <--> [*|2|*] <--> [*|3|None]
                    before          after

AFTER insert(2, 99):
    head                                           tail
      |                                              |
      v                                              v
    [None|1|*] <--> [*|2|*] <--> [*|99|*] <--> [*|3|None]
                                      new_node
```
For a middle insertion, the source updates every relevant link in this order:

1. `new_node.prev = before` connects the new node backward.
2. `new_node.next = after` connects the new node forward.
3. `before.next = new_node` makes the predecessor point forward to it.
4. `after.prev = new_node` makes the successor point backward to it.
5. `self.length += 1` records the extra node.
The source obtains `before` with `self.get(index - 1)` and sets `after = before.next`. For an invalid index it returns `False`; valid insertions return `True`. End delegation means an empty list accepts `insert(0, value)` through `prepend`.
### Course source: `SOLUTION-DLL-Insert.py`
```python
    def insert(self, index, value):
        if index < 0 or index > self.length:
            return False
        if index == 0:
            return self.prepend(value)
        if index == self.length:
            return self.append(value)

        new_node = Node(value)
        before = self.get(index - 1)
        after = before.next

        new_node.prev = before
        new_node.next = after
        before.next = new_node
        after.prev = new_node
        
        self.length += 1   
        return True  
```
The pointer rewiring itself is `O(1)`, but locating `before` is `O(n)` worst case. Auxiliary space is `O(1)`.
---
## 13. Remove
`remove(index)` returns and detaches the node at a valid index. It delegates the boundaries: index `0` calls `pop_first`, and index `length - 1` calls `pop`. A middle removal reconnects the two neighbors directly.
```text
BEFORE remove(2) from [1, 2, 3, 4]:
    head                                           tail
      |                                              |
      v                                              v
    [None|1|*] <--> [*|2|*] <--> [*|3|*] <--> [*|4|None]
                                    temp

AFTER remove(2):
    head                              tail             returned temp
      |                                 |                    |
      v                                 v                    v
    [None|1|*] <--> [*|2|*] <--> [*|4|None]       [None|3|None]
```
For a middle node `temp`, the source makes these exact updates:

1. `temp.next.prev = temp.prev`: successor points backward to predecessor.
2. `temp.prev.next = temp.next`: predecessor points forward to successor.
3. `temp.next = None`: detach the returned node forward.
4. `temp.prev = None`: detach the returned node backward.
5. `self.length -= 1`: decrease the count.
Invalid indexes return `None`. A one-node list reaches `pop_first` for index `0`, and an empty list fails validation before any pointer is read.
### Course source: `SOLUTION-DLL-Remove.py`
```python
    def remove(self, index):
        if index < 0 or index >= self.length:
            return None
        if index == 0:
            return self.pop_first()
        if index == self.length - 1:
            return self.pop()

        temp = self.get(index)
        
        temp.next.prev = temp.prev
        temp.prev.next = temp.next
        temp.next = None
        temp.prev = None

        self.length -= 1
        return temp
```
The source uses directional `get`, so the overall operation is `O(n)` worst case and `O(1)` auxiliary space. Given a node reference directly, the two neighbor rewires would be `O(1)`.
---
## 14. Complete Operation Complexity
```text
END OPERATIONS:
    prepend / pop_first  <==============================>  append / pop
             both sides are directly addressable by head and tail

INDEX OPERATIONS:
    head --next--> ... --next--> index
    tail --prev--> ... --prev--> index
    get chooses the shorter direction, but never gets direct indexing.
```
| Course method | Valid-result behavior | Time | Auxiliary space |
|:---|:---|:---:|:---:|
| Constructor | one node | `O(1)` | `O(1)` |
| `append(value)` | `True` | `O(1)` | `O(1)` |
| `pop()` | Node or `None` | `O(1)` | `O(1)` |
| `prepend(value)` | `True` | `O(1)` | `O(1)` |
| `pop_first()` | Node or `None` | `O(1)` | `O(1)` |
| `get(index)` | Node or `None` | `O(n)` worst case | `O(1)` |
| `set_value(index, value)` | `True` or `False` | `O(n)` worst case | `O(1)` |
| `insert(index, value)` | `True` or `False` | `O(n)` worst case | `O(1)` |
| `remove(index)` | Node or `None` | `O(n)` worst case | `O(1)` |
| `print_list()` | prints all values | `O(n)` | `O(1)` |
`get` can take `O(min(index, n - 1 - index))` link hops when `n` is the current length. Big O tables use the worst case because an index near an end can still be requested on a large list.
---
## 15. SLL Versus DLL and Memory Cost
```text
SLL NODE:                         DLL NODE:
    +-------------+               +----------------------+
    | value | next|               | prev | value | next  |
    +-------------+               +----------------------+
    one direction                 two directions, one extra reference
```
| Design choice | Singly linked list | Doubly linked list |
|:---|:---|:---|
| Node links | `value`, `next` | `value`, `next`, `prev` |
| Move forward | Yes | Yes |
| Move backward | No direct link | Yes |
| `append` with `tail` | `O(1)` | `O(1)` |
| Remove tail | `O(n)` | **`O(1)`** |
| Remove first | `O(1)` | `O(1)` |
| `get(index)` | `O(n)` from head | `O(n)` worst case, chooses an end |
| Middle removal by index | `O(n)` to locate and rewire | `O(n)` to locate, `O(1)` to rewire |
| Per-node memory | one link | two links |
For `n` nodes, the DLL has `O(n)` node storage plus `O(1)` metadata. Relative to SLL, it adds one reference field per node, so the constant memory factor is larger even though asymptotic space remains `O(n)`. The tradeoff is worthwhile when backward navigation, tail removal, or arbitrary known-node removal is frequent.
---
