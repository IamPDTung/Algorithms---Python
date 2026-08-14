
---

# Queue

A **Queue** is a linear data structure that follows **FIFO (First In, First Out)**. The item that arrives first is the item removed first. A linked-list queue has two useful references: **first** points to the front, and **last** points to the rear.

## 1. FIFO, First, and Last

Think of people waiting in a line. A person joins at the back and leaves from the front. The person who has waited longest is served first.

The essential terms are:

| Term | Meaning |
|:---|:---|
| **First** | Reference to the oldest node at the front |
| **Last** | Reference to the newest node at the rear |
| **Enqueue** | Add one item at the rear |
| **Dequeue** | Remove and return one item at the front |
| **FIFO** | First item in is the first item out |
| **Length** | Number of items in the queue |

```text
     dequeue direction                         enqueue direction
            <---                                      --->

     first                                              last
       |                                                  |
       v                                                  v
     +-----+      +-----+      +-----+      +-----+
     |  A  | ---> |  B  | ---> |  C  | ---> |  D  |
     +-----+      +-----+      +-----+      +-----+
     oldest                                      newest
```

If values `A`, `B`, and `C` are enqueued in that order, the dequeue order is `A`, `B`, `C`.

---

## 2. Node-Based Representation

The core implementation uses a singly linked list. Each **Node** stores a value and a `next` pointer. The queue stores `first`, `last`, and `length` so both ends are known without scanning the list.

`first` is the head of the linked list and represents the next item to leave. `last` is the tail and represents the newest item. The last node always points to `None`.

```text
     queue.first                                  queue.last
          |                                           |
          v                                           v
     +-----------+      +-----------+      +-----------+
     | value: 1  |      | value: 2  |      | value: 3  |
     | next:  o--+----->| next:  o--+----->| next: None|
     +-----------+      +-----------+      +-----------+
        oldest                                  newest

     queue.length = 3
```

The important invariants are:

| Invariant | Why it matters |
|:---|:---|
| `first` points to the oldest node | `dequeue` can remove immediately |
| `last` points to the newest node | `enqueue` can append immediately |
| `last.next is None` | It marks the rear boundary |
| `length` equals the number of nodes | Empty and one-item cases are explicit |
| Empty queue has `first is None` and `last is None` | No endpoint points at a removed node |

The two endpoint references are what make a linked-list queue efficient at both ends.

---

## 3. Enqueue at the Last

`enqueue` uses `last` to append without traversal: link the old last, move `last`, and increment `length`.

```text
     State 0: first -> [1] -> [2] -> None, last = [2], length = 2
     State 1: new_node -> [3] -> None
     State 2: first -> [1] -> [2] -> [3] -> None
     State 3: last = [3], length = 3

     empty enqueue(9): first and last -> [9] -> None, length = 1
```

---

## 4. Dequeue at the First

`dequeue` removes the oldest node at `first` in constant time.

```text
     State 0: first -> [1] -> [2] -> [3] -> None, last = [3]
     State 1: temp = [1], first -> [2] -> [3] -> None
     State 2: returned temp = [1] -> None, length = 2

     one item: first = last = [1] -> None; after pop both are None
     empty: first = last = None, length = 0, result = None
```

When `length == 1`, resetting both `first` and `last` prevents a stale rear pointer. Empty dequeue returns `None` without dereferencing `first`.

---

## 5. Constructor

The core constructor receives an initial value, creates one node, and points both `first` and `last` to it. It sets `length` to `1`. An empty queue is represented after the final item is dequeued, or would be represented by `first = None`, `last = None`, and `length = 0` in an empty constructor design.

```text
     Queue(4)

     first --+
             +--> [4] ---> None
     last  --+
     length = 1
```

The repository solution is reproduced without changing its code:

```python
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        
class Queue:
    def __init__(self, value):
        new_node = Node(value)
        self.first = new_node
        self.last = new_node
        self.length = 1

    def print_queue(self):
        temp = self.first
        while temp is not None:
            print(temp.value)
            temp = temp.next




my_queue = Queue(4)

my_queue.print_queue()



"""
    EXPECTED OUTPUT:
    ----------------
    4

"""
```

The constructor takes `O(1)` time and uses `O(1)` auxiliary space for the new node.

---

## 6. Enqueue Implementation

The `enqueue` solution has two branches. If `first is None`, the queue is empty, so both endpoint references receive the new node. Otherwise, `last.next` receives the new node and `last` moves to it. In both branches, `length` increases by one.

```text
     Non-empty branch:

     first ---> [old first] ---> ... ---> [old last] ---> None
                                                   |
                                                   +--> new_node
     last = new_node

     Empty branch:

     first ---> new_node <--- last
```

The repository solution is reproduced verbatim:

```python
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        

class Queue:
    def __init__(self, value):
        new_node = Node(value)
        self.first = new_node
        self.last = new_node
        self.length = 1

    def print_queue(self):
        temp = self.first
        while temp is not None:
            print(temp.value)
            temp = temp.next
        
    def enqueue(self, value):
        new_node = Node(value)
        if self.first is None:
            self.first = new_node
            self.last = new_node
        else:
            self.last.next = new_node
            self.last = new_node
        self.length += 1
        



my_queue = Queue(1)

print('Queue before enqueue(2):')
my_queue.print_queue()

my_queue.enqueue(2)

print('\nQueue after enqueue(2):')
my_queue.print_queue()



"""
    EXPECTED OUTPUT:
    ----------------
    Queue before enqueue(2):
    1

    Queue after enqueue(2):
    1
    2

"""
```

---

## 7. Dequeue Implementation and Resetting Last

The `dequeue` solution checks `length == 0` first. It saves `first` in `temp`. If there is one item, both `first` and `last` become `None`. Otherwise, `first` advances to its next node and `temp.next` is detached. Finally, `length` decreases and `temp` is returned.

```text
     length > 1:                       length == 1:

     first -> [A] -> [B]               first -> [A] <- last
                |                       after pop:
                +-- temp                first -> None
     first -> [B]                       last  -> None
     last unchanged
```

The reset of `last` is not optional. Without it, an empty queue would have `first is None` but a stale rear pointer, and a later enqueue could attach to a node that is no longer in the queue.

The repository solution is reproduced verbatim:

```python
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        

class Queue:
    def __init__(self, value):
        new_node = Node(value)
        self.first = new_node
        self.last = new_node
        self.length = 1

    def print_queue(self):
        temp = self.first
        while temp is not None:
            print(temp.value)
            temp = temp.next
        
    def enqueue(self, value):
        new_node = Node(value)
        if self.first is None:
            self.first = new_node
            self.last = new_node
        else:
            self.last.next = new_node
            self.last = new_node
        self.length += 1
        return True

    def dequeue(self):
        if self.length == 0:
            return None
        temp = self.first
        if self.length == 1:
            self.first = None
            self.last = None
        else:
            self.first = self.first.next
            temp.next = None
        self.length -= 1
        return temp

 

 
my_queue = Queue(1)
my_queue.enqueue(2)

# (2) Items - Returns 2 Node
print(my_queue.dequeue().value)
# (1) Item -  Returns 1 Node
print(my_queue.dequeue().value)
# (0) Items - Returns None
print(my_queue.dequeue())



"""
    EXPECTED OUTPUT:
    ----------------
    1
    2
    None

"""
```

---

## 8. Operation Complexity

With both endpoint references, the queue never traverses the list for its primary operations.

```text
     first                              last
       |                                  |
       v                                  v
     [A] ---> [B] ---> [C] ---> [D] ---> None
       ^                                  ^
     dequeue                           enqueue
```

| Operation | Time | Extra space | Reason |
|:---|:---:|:---:|:---|
| Constructor | `O(1)` | `O(1)` | Create one node and set two endpoints |
| `enqueue` | `O(1)` | `O(1)` | Use `last.next`, then move `last` |
| `dequeue` | `O(1)` | `O(1)` | Remove `first`, with a one-item reset |
| `peek` at first | `O(1)` | `O(1)` | Read `first.value` |
| `is_empty` | `O(1)` | `O(1)` | Check `length` or `first` |
| `print_queue` | `O(n)` | `O(1)` | Visit every node |

The queue itself occupies `O(n)` memory for `n` nodes. The table's space column counts only temporary working memory.

---

## 9. Printer Queues

A printer receives jobs faster than it can print them. Each job is enqueued at the rear. The printer dequeues the oldest job, which prevents a later job from cutting in front of an earlier one.

```text
     jobs arrive: report, photo, invoice

     first                                      last
       |                                          |
       v                                          v
     [report] ---> [photo] ---> [invoice] ---> None
         |
         +-- printer dequeues this job first
```

The queue can also hold metadata such as owner, page count, priority class, or arrival time. A strict FIFO queue treats all jobs in arrival order; a priority queue is a different policy that selects by priority rather than arrival alone.

---

## 10. Schedulers and Work Queues

Operating systems, web servers, and background workers use queues to hold tasks waiting for service. A worker dequeues one task, performs it, and then takes the next one.

```text
     producers                         worker
     task A ---+                    +--------+
     task B ---+--> [A] -> [B] ---> | takes A|
     task C ---+                    +--------+

     after A completes: [B] -> [C]
```

FIFO gives predictable fairness. A scheduler may use multiple queues when it needs priorities, separate customers, or rate limits. The underlying first/last pointer mechanics remain the same for each ordinary queue.

---

## 11. Breadth-First Search

**BFS (Breadth-First Search)** explores a graph or tree layer by layer. It enqueues a starting vertex, repeatedly dequeues the next vertex, and enqueues each unvisited neighbor. FIFO order ensures all vertices at the current distance are handled before deeper vertices.

```text
     graph layers:

             A                 distance 0
            / \
           B   C               distance 1
          / \   \
         D   E   F             distance 2

     queue sequence:
     [A] -> dequeue A -> [B, C]
     dequeue B         -> [C, D, E]
     dequeue C         -> [D, E, F]
```

The usual BFS complexity is `O(V + E)` for `V` vertices and `E` edges, assuming adjacency lists. The queue can hold `O(V)` vertices in the widest layer.

---

## 12. Queue Using Stacks

The Queue `Interview` directory contains `Queue Using Stacks - Enqueue.py` and `Queue Using Stacks - Dequeue.py`. These exercises implement queue behavior with two Python lists used as stacks: `stack1` and `stack2`.

The repository's enqueue strategy keeps the front at `stack1[-1]`. To add a value at the back, it moves all values from `stack1` to `stack2`, pushes the new value onto `stack1`, then moves the old values back. The order is restored so `peek` still returns the oldest value.

```text
     enqueue 4 into queue [1, 2, 3]

     stack1 top -> [3, 2, 1]       stack2 -> []
     move       stack1 -> []       stack2 top -> [1, 2, 3]
     push 4     stack1 top -> [4]  stack2 -> [1, 2, 3]
     restore    stack1 top -> [3, 2, 1, 4]  stack2 -> []
     queue front is stack1[-1] = 1
```

The dequeue exercise removes `stack1[-1]`. If `stack1` is empty, it returns `None`. This arrangement gives `O(n)` enqueue and `O(1)` dequeue for the stated strategy. An alternative two-stack queue commonly makes each operation amortized `O(1)` by moving elements only when the output stack is empty.

The files contain prompts and scaffolding around these exact problem names; the linked-list queue solutions are the three `SOLUTION-Queue-*.py` files under `Core`.

---

## 13. Stack and Queue Comparison

Both structures restrict access to an endpoint, but they enforce opposite removal orders.

```text
     STACK: same end for both operations

     push ---> [C] [B] [A] ---> pop
                         newest leaves first

     QUEUE: different ends

     dequeue <--- [A] [B] [C] <--- enqueue
                 oldest leaves first
```

| Feature | Stack | Queue |
|:---|:---|:---|
| Ordering rule | LIFO | FIFO |
| Add operation | `push` at top | `enqueue` at last |
| Remove operation | `pop` at top | `dequeue` at first |
| Linked-list endpoints | `top` | `first` and `last` |
| Typical use | Undo, call stack, nested syntax | Printer, scheduler, BFS |
| Linked-list add/remove | `O(1)` / `O(1)` | `O(1)` / `O(1)` |
| Key empty state | `top is None` | `first is None` and `last is None` |

Choose based on which item must be served first, not based only on the names of the methods.

---

## 14. Queue Checklist

When a problem says “first waiting,” “arrival order,” “next task,” or “level by level,” test whether FIFO is the required behavior.

```text
     Does the oldest item leave first?
                    |
                 yes v
             +-------------+
             | Use a queue |
             +-------------+
                    |
       keep both endpoints consistent
          /                    \
     first = front           last = rear
     dequeue here             enqueue here
```

Before implementing a linked-list queue, verify:

1. `first` always identifies the next node to leave.
2. `last` always identifies the newest node.
3. `enqueue` handles the empty queue by setting both endpoints.
4. `dequeue` resets both endpoints when removing the last item.
5. `length` changes only after a successful operation.
6. A removed node is detached before it is returned.

**Next Step:** Practice implementing a queue from an empty state, then compare the linked-list version with the two-stack interview design and measure where each strategy spends its work.
