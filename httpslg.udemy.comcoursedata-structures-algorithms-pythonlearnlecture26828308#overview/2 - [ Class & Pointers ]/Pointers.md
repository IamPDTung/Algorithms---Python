
---

# Pointers

## 1. References in Python

In many data-structures lessons, the word **pointer** means a value that lets one variable or object reach another object. Python does not expose C-style pointer arithmetic or an explicit dereference operator. Instead, Python variables are **names bound to objects**, and those bindings behave like references.

The practical model is:

1. An object lives somewhere in memory.
2. A name refers to that object.
3. Assignment changes which object a name refers to.
4. Mutation changes the contents of a mutable object itself.

This distinction explains why `dict2 = dict1` can make a change visible through both names, while `num2 = 22` does not change `num1`.

```
     name                     object in memory
     +---------+              +----------------+
     | variable| ------------> | value/state    |
     +---------+              +----------------+

     Two names may point to one object:

     name_a ------------------+
                              v
                         +------------+
     name_b ---------------->| object   |
                         +------------+
```

Here “points” describes reachability; Python code cannot add `1` to an address, manually free an object, or dereference an address as an integer.
---

## 2. Why Shared References Matter

Connected data structures need objects to refer to other objects. A linked list is not merely a row of independent values; each node must know which node comes next. A tree node must reach its children. A graph vertex must reach neighboring vertices.

If every connection copied the entire target object, a small update could require copying a large structure and would destroy the meaning of identity. A shared reference stores one relationship to the existing object instead.

```
     Linked list connection

     head
      |
      v
     +---------+       +---------+       +---------+
     | value=10| next->| value=20| next->| value=30|
     +---------+       +---------+       +---------+
                                              next -> None

     The arrows are references stored in the nodes.
     The nodes remain separate objects with stable identities.
```

Shared references let algorithms change links, represent graph edges without copying vertices, and let several owners observe one mutable record. The responsibility is that mutation through either alias is visible through the other.

---

## 3. Assignment, Binding, and Rebinding

An assignment statement such as `num2 = num1` evaluates the right-hand side and binds the left-hand name to the same object. It does not ask the object to clone itself.

The later statement `num2 = 22` is **rebinding**. It points `num2` at another integer object. It does not edit the integer object that `num1` originally reached.

```
     After num1 = 11

     num1 ---------------------> [ integer 11 ]

     After num2 = num1

     num1 ---------------------> [ integer 11 ] <---------------- num2

     After num2 = 22

     num1 ---------------------> [ integer 11 ]
     num2 ---------------------> [ integer 22 ]
```

A name can be rebound without changing an object; changing an object requires a supported mutation such as assigning a dictionary key or appending to a list. Python passes object references by assignment, so a caller can observe mutation but not rebinding of a local parameter.

---

## 4. The Integer Example: Immutable Objects

The first half of `Pointers.py` uses integers. Integers are **immutable**: once an object represents `11`, Python does not change it into `22`; `num2 = 22` binds `num2` to another integer object.

Before the update, both names reach the same integer object in the conceptual model. Consequently, the two `id()` calls print the same identity at that moment.

```
     BEFORE num2 = 22:  num1 ----+
                                  v
                              [ int: 11 ]
                                  ^
                          num2 ----+

     AFTER num2 = 22:   num1 -> [ int: 11 ]
                        num2 -> [ int: 22 ]
     The assignment changed the num2 arrow, not int:11.
```

The exact addresses are implementation-dependent; the stable lesson is the identity relationship at each stage.

---

## 5. `id()` as an Identity Proof

Python's built-in `id(object)` returns an integer identifying that object during its lifetime. In CPython it is commonly related to the memory address, but code should use it as an identity diagnostic, not as a portable address for pointer arithmetic.

The source prints identities before and after each assignment:

```
     BEFORE INTEGER REBINDING
     num1 value = 11       num1 id = X
     num2 value = 11       num2 id = X
                                      ^ same object

     AFTER INTEGER REBINDING
     num1 value = 11       num1 id = X
     num2 value = 22       num2 id = Y
                                      ^ usually X != Y
```

`id()` proves aliasing when two names return the same identity at the same time. It does not prove that two objects have equal contents. Conversely, two equal immutable values may be distinct objects, although Python implementations can reuse or intern some values.

For everyday checks, use `is` for the same-object question and sentinels such as `None`; use `==` for equal contents. Two equal immutable values can still be distinct objects.

---

## 6. The Dictionary Example: Aliasing and Mutation

The second half creates one dictionary and binds two names to it. `dict1` and `dict2` are **aliases**, or names for the same object. Dictionaries are mutable, so `dict2['value'] = 22` changes the dictionary rather than rebinding `dict2`.

```
     BEFORE: dict1 ---+
                      v
                 [ {'value': 11} ]
                      ^
              dict2 --+

     AFTER:  dict1 ---+
                      v
                 [ {'value': 22} ]
                      ^
              dict2 --+
     id(dict1) == id(dict2); the object was mutated.
```

This behavior is intentional and useful when several parts of a program must share one mutable record. It is also a common source of bugs when a programmer expected `dict2 = dict1` to make an independent copy.

---

## 7. Rebinding Versus Mutation

The two operations look similar in code but have different effects.

| Operation | What changes? | What aliases observe? |
|:---|:---|:---|
| `name = other` | The name's binding | Only the rebinding name points elsewhere |
| `name[key] = value` | A mutable object's contents | Every alias sees the mutation |
| `name = name + [value]` | Usually creates a new list and rebinds | Other aliases keep the old list |

Compare these two list operations:

```python
items_a = [1, 2]
items_b = items_a
items_b.append(3)

items_c = [1, 2]
items_d = items_c
items_d = items_d + [3]
```

In the first pair, both names see `[1, 2, 3]`. In the second pair, `items_d` points to a new list while `items_c` still points to `[1, 2]`.

```
     MUTATION: append                 REBINDING: + creates a list
     a ----+                           c -----> [1, 2]
           v                           d -----> [1, 2, 3]
       [1, 2, 3]                       (old and new objects differ)
     b ----+
```

When debugging a reference problem, first ask: “Did the statement modify the object, or did it only change a name?” That question usually reveals why another variable did or did not change.

---

## 8. Memory Diagrams Before and After Dictionary Mutation

A step-by-step diagram makes the `Pointers.py` output predictable. The before state is the alias created by `dict2 = dict1`; the after state follows `dict2['value'] = 22`.

```
     BEFORE MUTATION                    AFTER MUTATION
     dict1 ---+                         dict1 ---+
              v                                  v
         +-------------+                    +-------------+
         | D: value=11 |                    | D: value=22 |
         +-------------+                    +-------------+
              ^                                  ^
     dict2 ---+                         dict2 ---+

     id(dict1) == id(dict2) in both states; only D's contents changed.
```

The dictionary's identity stays constant while its contents change. This is the exact pattern used when a node stores a reference to a mutable neighboring object: the link remains, while the reachable object's state may change.

---

## 9. Connecting Nodes with `next`

A linked list uses the same reference behavior with class instances. `next` is an attribute whose value is either another `Node` object or `None`.

```python
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


first = Node(10)
second = Node(20)
first.next = second
```

The assignment `first.next = second` does not copy `second`. It stores a reference to the existing object inside `first`.

```
     first ------------------+
                              v
     +----------------+   +----------------+
     | Node A          |   | Node B          |
     | value: 10       |   | value: 20       |
     | next -----------|-->| next: None      |
     +----------------+   +----------------+
                              ^
     second ------------------+
```

Now `first.next` and `second` reach the same node. Updating `second.value` is visible when walking from `first` because traversal reaches that same object.

This is the essential bridge from variables and dictionaries to linked lists, trees, and graphs. A connection is an attribute containing a reference.

---

## 10. The Actual `Pointers.py` Code

The following is the complete source file used in the lesson. It demonstrates integer rebinding first, then dictionary aliasing and mutation.

```python
num1 = 11

num2 = num1

print("Before num2 value is updated:")
print("num1 =", num1)
print("num2 =", num2)

print("\nnum1 points to:", id(num1))
print("num2 points to:", id(num2)) 

num2 = 22 

print("\nAfter num2 value is updated:")
print("num1 =", num1)
print("num2 =", num2) 

print("\nnum1 points to:", id(num1))
print("num2 points to:", id(num2))


#####################################


dict1 = {
         'value': 11
        }

dict2 = dict1 

print("\n\nBefore value is updated:")
print("dict1 =", dict1)
print("dict2 =", dict2)

print("\ndict1 points to:", id(dict1))
print("dict2 points to:", id(dict2)) 

dict2['value'] = 22

print("\nAfter value is updated:")
print("dict1 =", dict1)
print("dict2 =", dict2) 

print("\ndict1 points to:", id(dict1))
print("dict2 points to:", id(dict2))

```

### What the Program Demonstrates

The integer phase prints `11` and `22` after rebinding only `num2`. The dictionary phase creates an alias, mutates one shared object, and prints `{'value': 22}` through both names.

```
     integer:   num1 -> 11       num2 -> 22  (after rebinding)
     dictionary: dict1 --+        dict2 --+   (after mutation)
                          v                v
                         {'value': 22}
```

The numeric identities printed by `id()` can differ between runs. Their equality or inequality within each stage is the useful observation.

---

## 11. Common Reference Pitfalls

### Accidental aliasing

Writing `backup = current` does not make a backup of a mutable object. It creates another name for the same object. Use an intentional shallow or deep copy when independent state is required, and understand what nested objects remain shared.

```
     backup = current       # two names, one mutable object
     backup['x'] = 9         # current sees the change too
```

Use an intentional shallow or deep copy for independent state; a shallow copy can still share nested values. A mutable default argument is also shared across calls, so use `None` as a sentinel and create a fresh object inside the function.

### Losing the head of a list

Rebinding the only variable that reaches a linked-list head can make the rest of the structure inaccessible. Keep a stable `head` reference while moving a temporary cursor.

```
     safe traversal:
     head -> Node(10) -> Node(20) -> None
     current ---------> Node(10)
     current = current.next      # head still reaches the list
```

### Cycles and infinite traversal

If a `next` reference points backward, a traversal without a visited set or cycle check may never reach `None`.

```
     Node A -> Node B -> Node C
        ^                   |
        +-------------------+
     A cycle: no natural None endpoint
```

### Equality and local parameters

Two dictionaries can have equal contents but different identities: use `==` for contents and `is` for identity. A function can mutate a received list, but rebinding its local parameter does not rebind the caller's name.

---

## 12. Practical Use Cases

References appear in nearly every nontrivial data structure and many application designs.

| Use case | Reference relationship | Typical operation |
|:---|:---|:---|
| Linked list | Node -> next Node | Insert, remove, traverse |
| Binary tree | Node -> left/right child | Search, insert, recurse |
| Graph | Vertex -> neighboring vertices | BFS, DFS, shortest paths |
| Shared cache | Many names -> one dictionary | Read or update one cache |
| Object composition | Order -> Customer, items | Coordinate related state |

```
     APPLICATION OBJECTS
     +---------+       +---------+       +---------+
     | Order   |------>| Customer|       | Product |
     +----+----+       +---------+       +----^----+
          |                                  |
          +----------------------------------+
                    references express relationships
```

When a relationship has identity and can change independently, a reference is usually a better model than copying the entire value. When independent snapshots are required, copy deliberately instead.

---

## 13. Big O Analysis of Reference Operations

A reference assignment usually changes one binding or one pointer-like field, so it is `O(1)` time and `O(1)` auxiliary space. The referenced structure is not traversed or copied by that assignment.

| Operation | Time | Extra Space | Explanation |
|:---|:---:|:---:|:---|
| `name = other` | `O(1)` | `O(1)` | Rebind one name |
| `node.next = other` | `O(1)` | `O(1)` | Store one reference |
| `dict2 = dict1` | `O(1)` | `O(1)` | Create an alias, no copy |
| `dict2['value'] = 22` | Average `O(1)` | `O(1)` | Hash-table key update |
| `id(object)` | `O(1)` | `O(1)` | Query identity metadata |
| Traverse `n` linked nodes | `O(n)` | `O(1)` | Follow one reference per node |
| Copy a structure with `n` elements | At least `O(n)` | `O(n)` | Each element/reference must be visited |

The constant-time cost of connecting two nodes is why linked-list insertion can be efficient when the insertion position is already known. Finding that position may still cost `O(n)`.

```
     connect two known nodes:       O(1)
     first -> second

     find the kth node first:       O(n)
     then connect at that position: O(1)
     total:                         O(n)
```

---

## 14. Summary Tables and Mental Checklist

### Integer Versus Dictionary

| Feature | Integer `11` | Dictionary `{'value': 11}` |
|:---|:---|:---|
| Mutable? | No, immutable | Yes, mutable |
| `b = a` | Both names initially share the object | Both names alias the dictionary |
| `b = new_value` | Rebinds `b`; `a` is unchanged | Rebinds `b` if it is an assignment |
| `b['value'] = new_value` | Not applicable | Mutates the shared object |
| Other aliases see mutation? | No integer mutation exists | Yes |

### Questions to Ask While Debugging

1. How many objects exist?
2. Which names or attributes reach each object?
3. Is the type mutable or immutable?
4. Did the statement rebind a name or mutate an object?
5. Should this relationship be shared or copied?
6. Can a traversal reach `None`, or can it cycle?
7. What is the time and space cost of following the references?

```
     reference debugging loop
     [names] --> [objects] --> [mutable state]
        |             |               |
        |             |               +-- did contents change?
        |             +------------------ same id / same object?
        +-------------------------------- did a name rebind?
```

The central rule is simple:

> Assignment changes a binding. Mutation changes a mutable object. Aliases observe the same mutation.

That rule explains the full `Pointers.py` example and prepares us to implement connected structures safely.

---

**Next Step:** Define a `Node` class with a `next` reference, then implement linked-list insertion and deletion while drawing the arrows before and after every mutation.
