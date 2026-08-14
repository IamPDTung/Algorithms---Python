
---

# Hash Table

## 1. What is a Hash Table?

A **Hash Table** is a **key/value store**. You give it a **key** (like a word or a name), and it gives you back the associated **value** — extremely fast.

The magic ingredient is the **hash function**: it takes the key and converts it into an **address (index)** of an underlying array. The key/value pair is then stored at that address.

```
    KEY                    HASH FUNCTION                 ADDRESS

    "bolts"     --->   [  __hash("bolts")  ]   --->        4
    "washers"   --->   [  __hash("washers")]   --->        4   (collision!)
    "lumber"    --->   [  __hash("lumber") ]   --->        6

    THE UNDERLYING ARRAY (data_map, size 7):

    Index:    0        1        2        3        4          5        6
            +-------+-------+-------+-------+----------+-------+----------+
            | null  | null  | null  | null  | bolts    | null  | lumber   |
            |       |       |       |       | washers  |       |          |
            +-------+-------+-------+-------+----------+-------+----------+
```

### Key Idea:
> Arrays are fast **by index** (`O(1)`). A hash table turns any **key** into an **index**, so looking up by key becomes as fast as looking up by index.

---

## 2. The Hash Function

The course hash function (from `SOLUTION-HT-Constructor.py`) loops over every letter of the key, mixes in `ord(letter) * 23`, and keeps the result inside the array with modulo `%`:

```python
    def __hash(self, key):
        my_hash = 0
        for letter in key:
            my_hash = (my_hash + ord(letter) * 23) % len(self.data_map)
        return my_hash  
```

### Properties of a Good Hash Function:

```
    +---------------------------------------------------------------+
    |                 HASH FUNCTION PROPERTIES                      |
    +---------------------------------------------------------------+
    |  1. DETERMINISTIC:                                            |
    |     same key  ==>  same address, EVERY time                   |
    |     hash("bolts") is 4 today, tomorrow, always                |
    |                                                               |
    |  2. DISTRIBUTES EVENLY:                                       |
    |     keys spread across all addresses                          |
    |     (few collisions => fast lookups)                          |
    |                                                               |
    |  3. ONE-WAY:                                                  |
    |     key -> address is easy                                    |
    |     address -> original key is (practically) impossible       |
    +---------------------------------------------------------------+
```

### Trace — hashing `"bolts"` step by step (size = 7):

```
    my_hash starts at 0. For each letter: my_hash = (my_hash + ord(letter)*23) % 7

    'b':  (0 + 98*23)  % 7 = 2254 % 7 = 0
    'o':  (0 + 111*23) % 7 = 2553 % 7 = 5
    'l':  (5 + 108*23) % 7 = 2489 % 7 = 4
    't':  (4 + 116*23) % 7 = 2672 % 7 = 5
    's':  (5 + 115*23) % 7 = 2650 % 7 = 4

    FINAL ADDRESS for "bolts"  ==>  4
```

---

## 3. Why Were Hash Tables Created?

A plain **array/list** has a split personality:

* Access **BY INDEX** is instant — `my_list[4]` is `O(1)`.
* Search **BY VALUE** is slow — "is 82 in this list?" requires checking every element: `O(n)`.

```
    LIST — access by index:             LIST — search by value (82?):

    +----+----+----+----+               +----+----+----+----+
    | 21 | 47 | 76 | 82 |               | 21 | 47 | 76 | 82 |
    +----+----+----+----+               +----+----+----+----+
              ^                           x    x    x    x
              |                           check all 4 => O(n)
    my_list[3] => O(1), instant

    HASH TABLE — lookup by KEY "washers":

    "washers" --> hash --> 4 --> jump straight to index 4 => O(1) average
```

### The Hash Table Insight:
> **Hash the key to get an index, then use the array's `O(1)` index access.** Average lookup, insert, and delete by key all become `~O(1)` — no scanning required.

---

## 4. What Problems Does a Hash Table Solve?

Hash tables are everywhere you need to **remember things by name** and retrieve them instantly:

```
    +----------------------------------------------------------+
    |              WHERE HASH TABLES ARE USED                  |
    +----------------------------------------------------------+
    |  * Dictionaries / maps (Python dict IS a hash table)     |
    |  * Caches (URL -> rendered page)                         |
    |  * Counting frequencies (word counts, vote tallies)      |
    |  * Detecting duplicates (seen this value before?)        |
    |  * Indexing database rows by ID                          |
    +----------------------------------------------------------+
```

### Classic Interview Problems (see the `Interview` folder):

| Problem | File | Core Idea |
|:---|:---|:---|
| **Two Sum** | `HT-Two Sum.py` | Store complements, find the pair in one pass |
| **Group Anagrams** | `HT-Group Anagrams.py` | Sorted word as key, list of anagrams as value |
| **First Non-Repeating Character** | `HT-First Non-Repeating Character.py` | Count char frequencies, return first with count 1 |
| **Find Duplicates** | `HT-Find Duplicates.py` | Value as key; seen before => duplicate |
| **Subarray Sum** | `HT-Subarray Sum.py` | Store prefix sums to find the target range |
| **Item In Common** | `HT-ItemInCommon1.py` / `HT-ItemInCommon2.py` | Nested loops vs hash table |

### The Classic Contrast — Item In Common:

```
    O(n^2) NESTED LOOPS (ItemInCommon1):     O(n) HASH TABLE (ItemInCommon2):

    list1 = [1, 3, 5]                        put list1 into a hash table:
    list2 = [2, 4, 5]                        {1:T, 3:T, 5:T}

    for i in list1:                          for j in list2:
        for j in list2:                          if j in table: return True
            if i == j: ...                   one pass, O(1) lookups => O(n)

    every i meets every j
    => 3 x 3 = 9 comparisons => O(n^2)
```

---

## 5. Collisions and Chaining

A **collision** happens when **two different keys hash to the same address**. It is unavoidable — there are infinitely many possible keys but only 7 addresses.

```
    COLLISION:  "bolts" and "washers" BOTH hash to address 4

    "bolts"   ---> [hash] ---+
                             +--->  4  ???
    "washers" ---> [hash] ---+
```

### Solution 1 — Chaining (the course approach):

Each address holds a **list (chain) of [key, value] pairs**. Colliding pairs are simply **appended** to the same chain:

```
    Index 4 chain after inserting "bolts" then "washers":

    4 :  [ ['bolts', 1400], ['washers', 50] ]
           \_______________/  \________________/
              first pair         appended after collision
```

### Solution 2 — Open Addressing (the alternative):

If the address is taken, **probe** for the next empty slot in the array itself (linear probing, quadratic probing, ...):

```
    "washers" wants address 4, but it is taken:

    Index:   4          5          6
           +---------+---------+---------+
           | bolts   | washers |         |   <- washers slid to next free slot
           +---------+---------+---------+
```

| Strategy | Idea | Used by |
|:---|:---|:---|
| **Chaining** | Each address stores a list of pairs | This course |
| **Open Addressing** | Find the next empty address | Many built-in dicts |

---

## 6. How It Works — Constructor & `set_item`

### The Constructor (from `SOLUTION-HT-Constructor.py`):

The underlying storage is a plain list of size 7, every slot starting as `None`:

```python
class HashTable:
    def __init__(self, size = 7):
        self.data_map = [None] * size
```

```
    data_map right after construction:

    Index:    0      1      2      3      4      5      6
            +------+------+------+------+------+------+------+
            | None | None | None | None | None | None | None |
            +------+------+------+------+------+------+------+
```

### The `set_item` Method (from `SOLUTION-HT-Set.py`):

```python
    def set_item(self, key, value):
        index = self.__hash(key)
        if self.data_map[index] == None:
            self.data_map[index] = []
        self.data_map[index].append([key, value])
```

### Step-by-Step Trace — `set_item('bolts', 1400)`, then `'washers'`, then `'lumber'`:

```
    STEP 1: set_item('bolts', 1400)
    hash('bolts') = 4 -> slot 4 is None -> create [] -> append ['bolts', 1400]

    4 :  [ ['bolts', 1400] ]

    STEP 2: set_item('washers', 50)          <== COLLISION at address 4!
    hash('washers') = 4 -> slot 4 exists -> append ['washers', 50]

    4 :  [ ['bolts', 1400], ['washers', 50] ]

    STEP 3: set_item('lumber', 70)
    hash('lumber') = 6 -> slot 6 is None -> create [] -> append ['lumber', 70]

    6 :  [ ['lumber', 70] ]

    FINAL STATE (matches print_table() output):

    0 :  None
    1 :  None
    2 :  None
    3 :  None
    4 :  [['bolts', 1400], ['washers', 50]]
    5 :  None
    6 :  [['lumber', 70]]
```

---

## 7. How It Works — `get_item`

### The `get_item` Method (from `SOLUTION-HT-Get.py`):

```python
    def get_item(self, key):
        index = self.__hash(key)
        if self.data_map[index] is not None:
            for i in range(len(self.data_map[index])):
                if self.data_map[index][i][0] == key:
                    return self.data_map[index][i][1]
        return None
```

### Trace — `get_item('washers')` (FOUND inside a chain):

```
    hash('washers') = 4  -> jump to address 4

    Chain at 4:  [ ['bolts', 1400], ['washers', 50] ]
                      ^                 ^
                   i = 0:            i = 1:
                   'bolts' !=        'washers' ==
                   'washers'         'washers' -> return 50
```

### Trace — `get_item('lumber')` when lumber was never inserted (NOT FOUND):

```
    hash('lumber') = 6  ->  address 6 is None -> return None

    OUTPUT:   Bolts: 1400     Washers: 50     Lumber: None
```

---

## 8. How It Works — `keys`

### The `keys` Method (from `SOLUTION-HT-Keys.py`):

Walk **every address**; wherever a chain exists, walk **every pair** in it and collect the key (element `[0]` of each pair):

```python
    def keys(self):
        all_keys = []
        for i in range(len(self.data_map)):
            if self.data_map[i] is not None:
                for j in range(len(self.data_map[i])):
                    all_keys.append(self.data_map[i][j][0])
        return all_keys
```

### Trace — gathering all keys:

```
    i = 0..3:  None          -> skip
    i = 4:     chain of 2    -> append 'bolts', append 'washers'
    i = 5:     None          -> skip
    i = 6:     chain of 1    -> append 'lumber'

    all_keys = ['bolts', 'washers', 'lumber']
```

---

## 9. Big O Analysis

### Average vs Worst Case:

```
    AVERAGE CASE (good hash function):       WORST CASE (all keys collide):

    keys spread over all 7 addresses         every key lands at address 0

    0 : [k1]                                 0 : [k1,k2,k3,k4,k5,k6,k7]
    1 : [k2]                                 1 : None
    2 : [k3]                                 2 : None
    ...                                      ...
    6 : [k7]                                 6 : None

    chain length ~ 1 => O(1) per lookup      chain length = n => O(n) per lookup
    (one hash + jump straight there)         (hash + walk a linked list!)
```

### Big O Table:

| Operation | Average Case | Worst Case (all collisions) |
|:---|:---|:---|
| **`set_item`** | `O(1)` | `O(n)` |
| **`get_item`** | `O(1)` | `O(n)` |
| **`keys`** | `O(n)` — must visit every pair | `O(n)` |
| **Space** | `O(n)` | `O(n)` |

> **The assumption:** the `O(1)` average depends entirely on a **good hash function** that spreads keys evenly. The modulo by the table size (plus a prime multiplier like 23) is what keeps chains short.

### Hash Table vs List:

| Operation | List (Array) | Hash Table (Average) |
|:---|:---|:---|
| **Access by index** | `O(1)` | — (keys replace indexes) |
| **Search by value/key** | `O(n)` | **`O(1)`** |
| **Insert** | `O(1)` at end | **`O(1)`** |
| **Delete by value/key** | `O(n)` | **`O(1)`** |
| **Keeps insertion order?** | Yes | No (order follows addresses) |

```
    THE TRADE-OFF:

    List:       fast by INDEX,  slow to SEARCH BY VALUE
    Hash Table: fast by KEY,    but keys must be hashable
                                and a bad hash function
                                degrades it toward O(n)
```

---

**Next Step:** Now let's practice with the interview problems in the `Interview` folder — Two Sum, Group Anagrams, First Non-Repeating Character, Find Duplicates, Subarray Sum, and Item In Common!
