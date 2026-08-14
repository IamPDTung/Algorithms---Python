
---

# Stack

A **Stack** is a linear data structure that follows **LIFO (Last In, First Out)**. The newest item is the first item removed. A stack has one active end called the **top**. Both insertion and removal happen at that end.

## 1. LIFO and the Top

Think of plates: the top plate is added and removed first.

| Term | Meaning |
|:---|:---|
| **Top** | Reference to the most recently added node |
| **Push** | Add one item to the top |
| **Pop** | Remove and return the top item |
| **Height** | Number of items in the stack |
| **LIFO** | Last item in is the first item out |

```text
                 TOP
                  |
             [newest]  <- out first
             [older]
             [oldest]  <- out last
                  |
               BOTTOM
```

If values `A`, `B`, and `C` are pushed in that order, the removal order is `C`, `B`, `A`.

---

## 2. Node-Based Representation

The core implementation uses a singly linked list. Each **Node** stores a value and `next`; the stack stores `top` and `height`. The first node is top, and `None` marks the bottom.

```text
       stack.top
           |
     [3] ---> [2] ---> [1] ---> None
      newest     older      oldest
     height = 3
```

| Invariant | Why it matters |
|:---|:---|
| `top` points to the newest node | `push` and `pop` can start immediately |
| The last node has `next == None` | It marks the bottom of the list |
| `height` equals the number of nodes | Empty checks and size tracking are constant time |
| An empty stack has `top == None` | There is no node to remove |

Only `top` and at most one `next` pointer change; no elements shift.

---

## 3. Why the Linked-List Head Is the Top

The singly linked-list head is immediately reachable. Head insertion/removal changes one pointer; using the tail for `pop` requires finding its predecessor, so it is `O(n)`.

```text
     HEAD AS TOP: top ---> [new] ---> [old] ---> None
     TAIL AS TOP: head ---> [1] ---> [2] ---> [3] ---> None
                           walk to predecessor: O(n)
```

The pointer rule is therefore simple: **the linked-list head is the stack top**.

Push links the new node to the old top, moves `top`, and increments `height`. Pop saves the top, advances `top`, detaches the saved node, and decrements `height`.

```text
     push: top -> [2] -> [1]       top -> [4] -> [2] -> [1]
     pop:  temp=[4] -> [2] -> [1]   top -> [2] -> [1]
```

---

## 4. Constructor

The constructor creates one `Node`, assigns it to `top`, and sets `height` to `1`; `Stack(4)` is not empty.

```text
     Stack(4): top ---> [4] ---> None
     height = 1
```

Repository solution, unchanged:

```python
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        

class Stack:
    def __init__(self, value):
        new_node = Node(value)
        self.top = new_node
        self.height = 1



my_stack = Stack(4)

print('Top:', my_stack.top.value)
print('Height:', my_stack.height)


"""
    EXPECTED OUTPUT:
    ----------------
    Top: 4
    Height: 1

"""
```

Complexity: `O(1)` time and `O(1)` auxiliary space.

---

## 5. Push

`push` links the new node to the old top before moving `top`, preserving every older node.

```text
     State 0: top -> [2] -> [1] -> None, height = 2
     State 1: new_node -> [3] -> None
     State 2: new_node -> [3] -> [2] -> [1] -> None
     State 3: top -> [3] -> [2] -> [1] -> None, height = 3

     empty push(9): top -> [9] -> None, height 0 -> 1
```

The repository solution is reproduced verbatim:

```python
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        

class Stack:
    def __init__(self, value):
        new_node = Node(value)
        self.top = new_node
        self.height = 1

    def print_stack(self):
        temp = self.top
        while temp is not None:
            print(temp.value)
            temp = temp.next

    def push(self, value):
        new_node = Node(value)
        if self.height == 0:
            self.top = new_node
        else:
            new_node.next = self.top
            self.top = new_node
        self.height += 1
 



my_stack = Stack(2)

print('Stack before push(1):')
my_stack.print_stack()

my_stack.push(1)

print('\nStack after push(1):')
my_stack.print_stack()



"""
    EXPECTED OUTPUT:
    ----------------
    Stack before push(1):
    2

    Stack after push(1):
    1
    2   

"""
```

---

## 6. Pop and the Empty Edge Case

`pop` saves the top, advances `top`, detaches the saved node, and decrements `height`. It checks empty state first and returns `None` without dereferencing.

```text
     State 0: top -> [1] -> [2] -> [3] -> None, temp = [1]
     State 1: top -> [2] -> [3] -> None
     State 2: returned temp = [1] -> None, height = 2

     empty pop: top -> None, height = 0, result = None
```

The repository solution is reproduced verbatim:

```python
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        

class Stack:
    def __init__(self, value):
        new_node = Node(value)
        self.top = new_node
        self.height = 1

    def print_stack(self):
        temp = self.top
        while temp is not None:
            print(temp.value)
            temp = temp.next

    def push(self, value):
        new_node = Node(value)
        if self.height == 0:
            self.top = new_node
        else:
            new_node.next = self.top
            self.top = new_node
        self.height += 1
        return True

    def pop(self):
        if self.height == 0:
            return None
        temp = self.top
        self.top = self.top.next
        temp.next = None
        self.height -= 1
        return temp
    

    

my_stack = Stack(4)
my_stack.push(3)
my_stack.push(2)
my_stack.push(1)

print('Stack before pop():')
my_stack.print_stack()

print('\nPopped node:')
print(my_stack.pop().value)

print('\nStack after pop():')
my_stack.print_stack()



"""
    EXPECTED OUTPUT:
    ----------------
    Stack before pop():
    1
    2
    3
    4

    Popped node:
    1

    Stack after pop():
    2
    3
    4

"""
```

---

## 7. Operation Complexity

Because `top` is the linked-list head, top operations avoid traversal.

```text
     top ---> [A] ---> [B] ---> [C] ---> None
              ^ push/pop end
```

| Operation | Time | Extra space | Reason |
|:---|:---:|:---:|:---|
| Constructor | `O(1)` | `O(1)` | Create one node and two references |
| `push` | `O(1)` | `O(1)` | Change one `next` link and `top` |
| `pop` | `O(1)` | `O(1)` | Advance `top` and detach one node |
| `peek` | `O(1)` | `O(1)` | Read `top.value` |
| `is_empty` | `O(1)` | `O(1)` | Check `height` or `top` |
| `print_stack` | `O(n)` | `O(1)` | Visit every node |

The stack itself uses `O(n)` memory for `n` nodes; the space column is temporary work.

---

## 8. Call Stack, Undo, and Browser Back

The **call stack** stores active function frames: a call pushes a frame and a return pops it. Recursion adds frames until a base case returns. Too much recursion can overflow this finite stack.

An editor pushes each completed state, so undo pops the newest edit. A second stack can hold redo states. Browser Back uses the same idea: navigation pushes pages, Back pops the current page, and a forward stack can preserve it.

```text
     call stack:       undo stack:       browser history:
     TOP               TOP              TOP
      |                 |                |
     [first()]         [delete C]       [docs]
     [main()]          [type B]         [search]
                       [type A]         [home]
     return pops       undo pops        Back pops docs
```

Visiting a new browser page after Back normally clears forward history because the new page creates a different future branch.

---

## 9. Interview Algorithms

### Balanced Parentheses

`Parentheses Balanced.py` scans left to right: push openings, pop for closings, reject a close with no matching opening, and require an empty stack at the end.

```text
     input: (()())
     stack: ( -> (( -> ( -> (( -> ( -> []
     final empty stack => balanced
```

The empty string is balanced; `(()`, `())`, and `)(` are not. The reference implementation is:

```python
def is_balanced_parentheses(parentheses):
    stack = []
    for character in parentheses:
        if character == '(':
            stack.append(character)
        elif not stack:
            return False
        else:
            stack.pop()
    return len(stack) == 0
```

Complexity: `O(n)` time and `O(n)` worst-case space.

### Reverse a String

`Reverse String.py` pushes each input character, then pops into the result; the first pop is the original last character.

```text
     push: h e l l o       top -> [o] -> [l] -> [l] -> [e] -> [h]
     pop:  o l l e h       output = "olleh"
```

```python
def reverse_string(string):
    stack = []
    for character in string:
        stack.append(character)

    reversed_string = ''
    while stack:
        reversed_string += stack.pop()
    return reversed_string
```

Complexity: `O(n)` time and `O(n)` auxiliary space; the stack exposes LIFO directly.

### Sort a Stack

`Sort Stack.py` asks for ascending order with the lowest value at the top, using one additional stack. It behaves like insertion sort.

```text
     pop temp; move larger sorted values back; push temp
     sorted top: [1] -> [2] -> [3] -> [4] -> [5]
     transfer sorted_stack back to input stack
```

Move larger sorted values back before pushing `temp`, then transfer the result. Complexity: `O(n^2)` time and `O(n)` extra space.

```python
def sort_stack(stack):
    sorted_stack = Stack()
    while not stack.is_empty():
        temp = stack.pop()
        while (not sorted_stack.is_empty()
               and sorted_stack.peek() > temp):
            stack.push(sorted_stack.pop())
        sorted_stack.push(temp)

    while not sorted_stack.is_empty():
        stack.push(sorted_stack.pop())
```

The repository file is a prompt scaffold; the function above expresses its stated algorithm without altering that source.

---

## 10. Interview Files and Comparisons

The Stack `Interview` directory contains these problem names:

| File | Main idea |
|:---|:---|
| `Implement Stack Using a List.py` | Store stack values in an empty Python list |
| `Parentheses Balanced.py` | Use LIFO matching to validate parentheses |
| `Reverse String.py` | Use pushes and pops to reverse characters |
| `Sort Stack.py` | Sort with one additional stack |

The first file is a constructor exercise; the other three include scaffolding and tests. Completed linked-list code is in the three `SOLUTION-Stack-*.py` files under `Core`.

### Linked-List Stack vs Python-List Stack

Both implementations expose LIFO. Linked lists change the head; Python lists use `append` and `pop` at the end, amortized `O(1)`.

```text
     Linked list stack                 Python list stack

     top -> [C] -> [B] -> [A]          list: [A, B, C]
             head is top                     end is top
```

| Concern | Linked-list stack | Python-list stack |
|:---|:---|:---|
| Top operation | Head pointer | List end |
| `push` | `O(1)` worst case | Amortized `O(1)` |
| `pop` | `O(1)` worst case | Amortized `O(1)` |
| Random access | Not natural | `O(1)` by index, but not stack behavior |
| Per-item overhead | Node object and pointer | List storage overhead |
| Empty representation | `top is None`, `height == 0` | `len(stack_list) == 0` |
| Best teaching value | Pointer manipulation | Simple production code |

Interview files use `stack_list[-1]` as top; core files demonstrate linked-list pointer mechanics.

### Stack Checklist

If a problem says “last action,” “most recent,” “nested,” or “undo,” test for LIFO.

Before implementing a linked-list stack, verify:

1. `top` points to the newest node and new nodes link before it moves.
2. `pop` checks empty state before dereferencing.
3. `height` changes once per successful operation.
4. A returned node is detached.

**Next Step:** Continue with queues to study the FIFO order, the `first` and `last` pointers, and how enqueue and dequeue stay `O(1)` in a linked-list implementation.
