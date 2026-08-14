
---

# Classes

## 1. Why Model Things with Classes?

**A class** is a programmer-defined type that describes both the data an object carries and the operations that can be performed on that data. Instead of treating every value as an unrelated primitive, we can model a useful thing as one coherent unit.

An object created from a class is called an **instance**. The class is the plan; the instance is a concrete value built from that plan. A program can create many instances from one class, and each instance can hold different state.

This is the first important object-oriented idea:

1. Define a reusable design once.
2. Create as many independent objects as the problem needs.
3. Let each object expose behavior through methods.

For example, a delivery system might need thousands of `Package` objects. Each package can have a tracking number and a destination, while all packages can share methods such as `mark_delivered()`.

```
                    CLASS: reusable design
                 +---------------------------+
                 | Package                   |
                 | data: tracking_id         |
                 | data: destination         |
                 | behavior: mark_delivered  |
                 +-------------+-------------+
                               |
                 +-------------+-------------+
                 |                             |
                 v                             v
        +------------------+          +------------------+
        | object/instance  |          | object/instance  |
        | tracking_id=101  |          | tracking_id=102  |
        | destination=NY   |          | destination=LA   |
        +------------------+          +------------------+
```

---

## 2. Why Were Custom Types Created?

Python already provides built-in types such as `int`, `str`, `list`, `dict`, and `set`. These types are general-purpose, but a real problem often has a more specific concept than any one built-in type can express.

Suppose a program stores a cookie as a color string. A string can hold the color, but it does not explain that the color belongs to a cookie or provide cookie-specific operations. A custom type can group related state and behavior:

* **Meaning:** `Cookie('green')` communicates more than an unlabelled string.
* **Organization:** attributes and methods for one concept live together.
* **Reuse:** one definition can create many objects.
* **Encapsulation:** callers use a small public interface instead of knowing every storage detail.
* **Invariants:** methods can enforce valid transitions, such as refusing an invalid color.
* **Composition:** objects can contain or refer to other objects, which is essential for data structures.

Without custom types, a program tends to pass several parallel variables around. Parallel variables are easy to mismatch:

```
     WITHOUT A CUSTOM TYPE                  WITH A CUSTOM TYPE
     ----------------------                 -----------------
     cookie_color = 'green'                 cookie = Cookie('green')
     cookie_size = 8                        cookie.color
     cookie_batch = 3                        cookie.get_color()
     # Which variables belong together?     # One object owns its state

     Parallel data can drift apart.         State and behavior travel together.
```

---

## 3. Class, Object, Attribute, and Method

These four terms form the vocabulary used throughout data structures.

1. **Class:** the definition or template. `Cookie` is a class.
2. **Object:** a concrete value created from a class. `cookie_one` refers to one `Cookie` object.
3. **Instance:** another name for an object created from a particular class.
4. **Attribute:** data stored on an object, accessed with dot notation. `cookie_one.color` is an attribute.
5. **Method:** a function defined inside a class. `cookie_one.get_color()` is a method call.
6. **State:** the current values of an object's attributes.
7. **Behavior:** the work exposed by the object's methods.

The dot separates the object from the member being accessed. A method call also supplies the object as its first argument internally; that is why methods are written with `self`.

```
     cookie_one = Cookie('green')
     |             |       |
     |             |       +-- constructor argument
     |             +---------- class being instantiated
     +------------------------ variable name bound to the object

     cookie_one.color          -> attribute/state
     cookie_one.get_color()    -> method/behavior
     Cookie                    -> class/type
     cookie_one                 -> object/instance
```

---

## 4. The Cookie-Cutter Analogy

The `Cookie` example uses a physical cookie cutter as an analogy for a class.

* The cutter describes a shape but is not an edible cookie.
* Pressing the cutter into dough creates a new cookie.
* Every cookie has the same general shape, but each can have a different color or decoration.
* Changing one baked cookie does not change the other baked cookies.

The class is the cutter. Calling `Cookie(...)` creates an instance. The constructor argument chooses the initial state of that particular instance.

```
       COOKIE CLASS / CUTTER
       +-------------------+
       | shape + rules     |
       | __init__          |
       | get_color         |
       | set_color         |
       +---------+---------+
                 |
       create    |    create
                 v
       +----------------+       +----------------+
       | cookie_one     |       | cookie_two     |
       | color=green    |       | color=blue     |
       +----------------+       +----------------+
          independent              independent
          instance                 instance
```

---

## 5. The Constructor and `self`

The method named `__init__` is the initializer commonly called the **constructor** in introductory Python lessons. It runs automatically when an instance is created.

In the source code, `__init__(self, color)` receives two conceptual pieces of information:

* `self` is the newly created instance.
* `color` is the value supplied by the caller.

The statement `self.color = color` creates or updates an attribute on that specific instance. The name on the left belongs to the object; the name on the right is the local parameter.

```
     Cookie('green')
          |
          | Python creates an object and calls __init__
          v
     __init__(self=<new object>, color='green')
          |
          | self.color = color
          v
     +-------------------+
     | new Cookie object  |
     | color: 'green'     |
     +-------------------+
```

When `cookie_one.get_color()` is written, Python supplies `cookie_one` as `self`. When `cookie_one.set_color('yellow')` is written, the method receives the same instance as `self` and `'yellow'` as `color`.

---

## 6. Creating Multiple Independent Instances

The source creates two objects from the same class:

```python
cookie_one = Cookie('green')
cookie_two = Cookie('blue')
```

Both objects have the same available methods, but their `color` attributes are initialized separately. The variable names are also separate references.

```
     cookie_one --------------------+
                                    v
                            +----------------+
                            | Cookie object A|
                            | color='green'  |
                            +----------------+

     cookie_two --------------------+
                                    v
                            +----------------+
                            | Cookie object B|
                            | color='blue'   |
                            +----------------+

     Same class definition, two different objects, two different states.
```

The two print calls read different values because each constructor call initializes independent state. This pattern scales to queues, trees, and graphs containing many objects.

---

## 7. Changing Attributes Through Methods

`get_color` reads the current state and returns it. `set_color` changes the current state by assigning a new value to `self.color`.

The call below changes only `cookie_one`:

```python
cookie_one.set_color('yellow')
```

The object referenced by `cookie_two` is not passed to that call, so its state remains `'blue'`.

```
     BEFORE SETTER CALL
     cookie_one -> [ Cookie | color='green' ]
     cookie_two -> [ Cookie | color='blue'  ]

     cookie_one.set_color('yellow')
                  |
                  | updates self.color on object one only
                  v

     AFTER SETTER CALL
     cookie_one -> [ Cookie | color='yellow' ]
     cookie_two -> [ Cookie | color='blue'   ]
```

A method is a controlled operation on an object's state. In this small example the setter does no validation, but a richer class could check that the new color is allowed or record a change.

---

## 8. Object and Memory Diagrams

A useful diagram separates **names**, **objects**, and the class definition. A name points to an object; the object stores instance attributes. The class supplies the shared structure and method definitions.

The diagram is conceptual. CPython has additional implementation details, but this model correctly explains the behavior in the lesson.

```
     CLASS OBJECT
     +--------------------------------+
     | Cookie                         |
     | __init__, get_color,           |
     | set_color method definitions   |
     +----------------+---------------+
                      | instances follow this class
          +-----------+-----------+
          |                       |
          v                       v
     +-------------+         +-------------+
     | object A    |         | object B    |
     | color=green |         | color=blue  |
     +-------------+         +-------------+
          ^                       ^
          |                       |
     cookie_one               cookie_two
```

When `cookie_one` changes, only object A's attribute storage changes. A method lookup can use the class definition, while `self` makes the method operate on whichever instance made the call. The source uses instance attributes created with `self.color`.

---

## 9. The Actual `Cookie.py` Code

The following is the complete source file used in the lesson. It is intentionally small so that the class mechanics are visible without unrelated application code.

```python
class Cookie:
    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def set_color(self, color):
        self.color = color


cookie_one = Cookie('green')
cookie_two = Cookie('blue')

print('Cookie one is', cookie_one.get_color())
print('Cookie two is', cookie_two.get_color())

cookie_one.set_color('yellow')

print('\nCookie one is now', cookie_one.get_color())
print('Cookie two is still', cookie_two.get_color())
```

### Behavior

The class definition initializes an instance, `get_color` reads it, and `set_color` replaces it. Two constructor calls create independent instances, so the final output is `yellow` for the first cookie and still `blue` for the second.

```
     Cookie('green') -> get_color() -> green
     Cookie('blue')  -> get_color() -> blue
     set_color on first object -> yellow
     first reads yellow; second still reads blue
```

The blank line in the final two print statements comes from `\n` inside the string. The important result is the independence of the two object states.

---

## 10. Classes as the Foundation of Data Structures

### Node

A **Node** usually stores a value and one or more references to other nodes. The reference is what turns separate objects into a chain or a branching structure.

```
     +-----------+      +-----------+      +-----------+
     | Node      |      | Node      |      | Node      |
     | value: 10 | next|-> value:20 | next|-> value:30 |
     +-----------+      +-----------+      +-----------+
                                              next -> None
```

### LinkedList

A **LinkedList** class commonly stores `head`, perhaps `tail`, and a `length`. Its methods implement append, prepend, search, and removal by changing node references.

```
     LinkedList object
     +---------------------------+
     | head ---------------------|----> Node(10) -> Node(20) -> None
     | tail ---------------------|--------------------^        |
     | length: 2                 |                             |
     +---------------------------+                             +-- end
```

### Tree

A tree node can hold `left` and `right` references. A `Tree` class can hold the root and expose insertion or traversal methods.

```
                         Tree.root
                             |
                         +---v---+
                         |   8   |
                         +---+---+
                       left     right
                        /          \
                   +---v---+    +---v---+
                   |   3   |    |  10   |
                   +-------+    +-------+
```

### Graph

A graph can use vertex objects with a collection of neighboring references, or a graph class can map a value to a list of adjacent values. Classes give those relationships a home and define traversal methods such as BFS and DFS.

```
     Graph.vertices
       A --------> B
       |           |
       v           v
       C --------> D

      Arrows are stored references/edges owned by the graph or vertices.
```

---

## 11. Real Problems Solved by Classes

| Problem | Class-based solution | Benefit |
|:---|:---|:---|
| Many records have the same shape | Define one class and create instances | Reuse and consistent fields |
| State and operations are scattered | Put attributes and methods together | Clear ownership |
| A value has valid transitions | Validate updates inside methods | Protect invariants |
| Items must connect to one another | Store object references such as `next` | Natural linked structures |
| A program must model real entities | Use domain-specific types | Code mirrors the problem |

```
     REAL PROBLEM                 CLASS RESPONSIBILITY
     --------------------------   --------------------------
     package has a destination    Package.destination
     package can be delivered     Package.mark_delivered()
     node has a successor         Node.next
     list has a first node        LinkedList.head
     tree can be searched         Tree.search()
```

---

## 12. Big O Analysis for the Cookie Class

The methods in `Cookie` read or assign one attribute. Assuming attribute access and assignment are constant-time operations, each individual operation is `O(1)`.

| Operation | Time | Extra Space | Reason |
|:---|:---:|:---:|:---|
| Define the class | `O(1)` setup conceptually | `O(1)` code object setup | The definition is written once |
| Construct one `Cookie` | `O(1)` | `O(1)` instance state | One fixed attribute is assigned |
| `get_color()` | `O(1)` | `O(1)` | One attribute lookup and return |
| `set_color(color)` | `O(1)` | `O(1)` | One attribute assignment |
| Construct `n` cookies | `O(n)` | `O(n)` | One constant-size instance per cookie |
| Read or update all `n` cookies | `O(n)` | `O(1)` auxiliary space | Visit each instance once |

```
     ONE INSTANCE:                    n INSTANCES:
     construct -> O(1)                construct each -> n * O(1) = O(n)
     read color  -> O(1)                storage       -> n * O(1) = O(n)
     update      -> O(1)
```

---

## 13. Summary and Mental Checklist

The core relationships are:

1. A **class** defines a custom type.
2. Calling the class creates an **object/instance**.
3. An **attribute** stores object state.
4. A **method** implements object behavior.
5. `self` identifies the instance receiving the method call.
6. `__init__` initializes each new instance.
7. Separate constructor calls create independent instance state.
8. Classes let data structures store links between meaningful objects.

```
     CLASS
       |
       | call with arguments
       v
     INSTANCE
       |
       +--> attributes = state
       +--> methods    = behavior
       +--> references = connections to other objects
       |
       v
     larger structures: LinkedList, Tree, Graph
```

Before writing a class, ask:

| Question | What to identify |
|:---|:---|
| What is one object? | The unit that should have an identity |
| What state belongs to it? | Attributes initialized by `__init__` |
| What can it do? | Methods and their inputs/outputs |
| What must always be true? | Invariants enforced by the interface |
| Does it connect to others? | References such as `next`, `left`, or neighbors |
| What is the cost? | Time and space for each operation |

---

**Next Step:** Use the same class-and-instance model to study Python references and pointers, then connect `Node` objects into linked lists, trees, and graphs.
