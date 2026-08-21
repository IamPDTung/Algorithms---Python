# Trie, Digital Tree, Prefix Tree Basics and Visualization

## 1. Goal

A Trie — also known as a digital tree, a prefix tree, or a dictionary tree
— is an N-ary tree in which every edge is labeled with one character and
every node holds an optional value. A node whose value is not None marks
the end of a stored key, and the path from the root down to that node
spells out the key itself. Looking up, inserting, and deleting a key of
length L each walk exactly L edges, so every operation is O(L) no matter
how many keys the tree holds.

The trie was born because the classic structures fail on strings with
shared prefixes. A HashMap stores every key in full: for "apple", "app" and
"appl" the prefix "app" is kept three times, wasting memory. And neither a
HashMap nor a TreeMap can answer prefix questions such as "list every key
starting with th" or wildcard patterns like "t.e" — both would have to scan
every single key. The trie solves both problems at once: shared prefixes
live in shared nodes, and the tree shape itself can be walked to enumerate
or match keys by prefix.

Source references:

- [Trie, Digital Tree, Prefix Tree Basics and Visualization](https://labuladong.online/en/algo/data-structure-basic/trie-map-basic/)

The implementation in `TrieBasics.py` provides:

- A `TrieNode` class holding a `children` dict and an optional `val`.
- A generic `TrieMap` with `put`, `get`, `remove`, `contains_key`, `keys`,
  `shortest_prefix_of`, `longest_prefix_of`, `has_key_with_prefix`,
  `keys_with_prefix`, `has_key_with_pattern` and `keys_with_pattern`.
- A `TrieSet` wrapper around a `TrieMap` that exposes the same prefix and
  wildcard APIs as a set.
- A `node_count` helper for the memory comparison and a depth-line ASCII
  renderer used by the demo.

The three keys "apple", "app" and "appl" share the path `a -> p -> p`, and
the nodes at "app", "appl" and "apple" each carry a filled marker saying "a
key ends here":

```text
   (root)
     |
     a
     |
     p
     |
     p@           end of key "app"
     |
     l@           end of key "appl"
     |
     e@           end of key "apple"

   @ = this node's val is not None (a stored key ends here)
   every edge is one character, so the path to any node spells a word
```

## 2. Use case: saving storage space

A HashMap stores the full key string at every entry. The three keys
"apple", "app" and "appl" carry 12 characters in total, and the prefix
"app" is written three times:

```text
   HashMap with three keys:

   "apple" -> a p p l e         5 characters
   "app"   -> a p p             3 characters
   "appl"  -> a p p l           4 characters
                                 ---------
                                 12 characters stored, "app" repeated 3x

   Trie with the same three keys:

   (root) --a--> --p--> --p--> --l--> --e-->    end of "apple"
                              |      |
                        end of "app"  end of "appl"

   only 5 character nodes exist: a, p, p, l, e
   the prefix "app" is written once and shared by all three keys
```

A tree with thousands of phone numbers, domain names, or English words
keeps this sharing for every common prefix, so total storage is
proportional to the sum of key lengths minus everything shared — often a
large saving. In the demo, `node_count()` returns 6 for these three keys
(root plus `a p p l e`): 5 character nodes where the HashMap needed 12
characters.

## 3. Use case: prefix operations

Four prefix APIs are the reason a trie is more than a string set. They all
work by walking down to a node and inspecting the subtree below it. Assume
the trie holds "that", "the", "them" and "apple".

`shortest_prefix_of(s)` returns the shortest stored key that is a prefix
of `s`. Walk `s` one character at a time and stop at the first node whose
value is not None:

```text
   shortest_prefix_of("themxyz")

   walk s = t h e m x y z
             | | | |
   (root) --t--> --h--> --e--> --m--> --x--> (no child, stop)

   "the"  ends at the 3rd node  -> value found, return "the"
   "them" ends at the 4th node  -> not reached, we already stopped
   result: "the"
```

`longest_prefix_of(s)` returns the longest such prefix. The same walk
keeps a running candidate and updates it whenever a valued node is passed:

```text
   longest_prefix_of("themxyz")

   (root) --t--> --h--> --e--> --m--> --x--> (no child, stop)
                        |        |
                      "the"    "them"
                      found    found, longer -> overwrite

   result: "them"
```

`has_key_with_prefix(prefix)` only asks whether the node reached by
`prefix` exists:

```text
   has_key_with_prefix("tha")        has_key_with_prefix("thz")

   (root) --t--> --h--> --a-->      (root) --t--> --h--> --z--> ???
                          |                                  |
                     "that" exists               no "z" child
                     result: True                result: False
```

`keys_with_prefix(prefix)` collects every key in that subtree — exactly
what an autocomplete drop-down shows while the user types:

```text
   autocomplete: the user has typed "th"

        keyboard:  t h
                     |
                     v
   (root) --t--> --h--> subtree
                         |-- "that"     (suggestion 1)
                         |-- "the"      (suggestion 2)
                         |-- "them"     (suggestion 3)

   answer: keys_with_prefix("th") -> ["that", "the", "them"]
   cost: O(L) to reach the "th" node plus O(K) to collect the K matches
```

## 4. Use case: wildcard support

A pattern string may contain '.', which matches any single character. The
search is the same trie walk, but at a '.' the walk branches to every
child instead of following one fixed character:

```text
   pattern "t.e"   (t, any, e)

   (root) --t--> --h--> --e-->    "the"  matched, value found -> True
                     \--a--> ...  dead end, no "e" child below

   pattern "t.x"   (t, any, x)

   (root) --t--> --h--> --x--> ???     no "x" child under "h"
                   \--a--> --x--> ???  no "x" child under "a"
   result: False
```

`keys_with_pattern` collects every matching key in lexicographic order:

```text
   pattern "t..t"   (t, any, any, t)

   (root) --t--> --h--> --a--> --t-->    "that"  matched
                   \--e--> --m--> ???    "them" fails at the last char

   pattern ".pp."   (any, p, p, any)

   (root) --a--> --p--> --p--> --l-->    "appl"  matched
   result: ["appl"]
```

A wildcard search is only as expensive as the nodes it actually visits: a
'.' at a wide node fans out, but branches that fail a fixed character die
immediately.

## 5. Use case: in-order key traversal

The children of every node live in a dict keyed by character. If children
are walked in sorted character order, keys are emitted in lexicographic
order — the trie behaves like a sorted map, not like a HashMap whose
iteration order is arbitrary:

```text
   trie holding "app", "appl", "apple", "that", "the", "them"

   (root)
     |-- a -- p -- p -- l -- e         end of "apple"
                        |    |
                     "app"  "appl"
     |-- t -- h -- a -- t              end of "that"
                   |
                   e -- m
             end of "the"  end of "them"

   visit children in sorted order (a before t):

   "app" < "appl" < "apple" < "that" < "the" < "them"
```

A sorted walk is what makes ordered reports and autocomplete easy: the
classic HashMap needs a full sort pass over all keys, the trie emits them
already sorted.

## 6. Basic structure

A trie node is just a dictionary of children plus one optional value:

```python
class TrieNode(Generic[V]):
    def __init__(self) -> None:
        self.children: Dict[str, TrieNode[V]] = {}
        self.val: Optional[V] = None
```

The edge label is the dict key, and `val` is None unless this node is the
end of a stored key:

```text
   TrieNode at the path "app"            TrieNode at the path "appl"
   +---------------------------------+   +---------------------------------+
   | children: Dict[str, TrieNode]   |   | children: Dict[str, TrieNode]   |
   |   "l" -> TrieNode("appl")       |   |   "e" -> TrieNode("apple")      |
   | val: 2  <- not None: key "app"  |   | val: 3  <- not None: key "appl" |
   +---------------------------------+   +---------------------------------+
```

`TrieMap` keeps a root node plus a size counter. The children of the root
are the first characters of every stored key, so the branching factor of a
node is at most the size of the character alphabet:

```text
   TrieMap
   +-------------------------------------+
   | root: TrieNode                      |
   |   children: { "a": node_a,          |   first letters of keys
   |                "t": node_t }        |
   |   val: None                         |   root never ends a key
   | size: 6                             |   number of stored keys
   +-------------------------------------+
```

`TrieSet` is a thin wrapper that stores a non-None sentinel as the value
of every key — None already means "not the end of a key" inside a node:

```text
   TrieMap (values of any type)          TrieSet (values are the sentinel)

   +----------------------------+        +----------------------------+
   | "app"  -> 2                |        | "cat" -> True (sentinel)   |
   | "the"  -> 2                |        | "car" -> True (sentinel)   |
   | "them" -> 3                |        | "dog" -> True (sentinel)   |
   +----------------------------+        +----------------------------+
   put / get / remove / keys             add / remove / contains
   prefix + wildcard APIs                prefix + wildcard APIs
```

## 7. TrieMap API

All operations take O(L) time, where L is the length of the key, prefix,
or pattern involved, plus the time to collect results:

```python
class TrieMap(Generic[V]):
    def put(self, key: str, value: V) -> Optional[V]       # O(L), returns previous value
    def get(self, key: str) -> Optional[V]                 # O(L), None if absent
    def remove(self, key: str) -> Optional[V]              # O(L), prunes dead nodes
    def contains_key(self, key: str) -> bool               # O(L)
    def keys(self) -> List[str]                            # O(N), lexicographic
    def is_empty(self) -> bool                             # O(1)
    def node_count(self) -> int                            # O(N), memory demos
    def shortest_prefix_of(self, s: str) -> Optional[str]  # O(L)
    def longest_prefix_of(self, s: str) -> Optional[str]   # O(L)
    def has_key_with_prefix(self, prefix: str) -> bool     # O(L)
    def keys_with_prefix(self, prefix: str) -> List[str]   # O(L + K)
    def has_key_with_pattern(self, pattern: str) -> bool   # O(visited nodes)
    def keys_with_pattern(self, pattern: str) -> List[str] # O(visited nodes + K)
```

`keys_with_prefix` and `keys_with_pattern` pay `K` for the keys they
collect; the wildcard pair also pays for every node the walk visits, which
is bounded by the subtree size.

Three contracts the demo relies on, stated explicitly:

```text
   keys()                 -> sorted, shorter keys first ("app" < "appl")
   keys_with_prefix(p)    -> sorted, only keys starting with p
   remove(k)              -> prunes nodes with no val and no children
```

## 8. Insert and delete algorithms

Insertion walks the key character by character, creating any node that is
missing, and finally sets the value on the last node:

```text
   put("apple", 1), starting from an empty trie

   step 1   (root) --a-->                        create "a"
   step 2   (root) --a--> --p-->                 create "p"
   step 3   (root) --a--> --p--> --p-->          create "p"
   step 4   (root) --a--> --p--> --p--> --l-->   create "l"
   step 5   (root) --a--> --p--> --p--> --l--> --e-->   create "e"
   step 6   val of the final node := 1           "apple" is now a key

   inserting "appl" next reuses the nodes a, p, p and l;
   only the value of node "l" needs to be set
```

Deletion works bottom-up: clear the value of the final node, then prune
nodes that become useless. A node is removed only when it has no value and
no children left:

```text
   remove("apple") from a trie holding "appl" (val 3) and "apple" (val 1)

   before:
   (root) --a--> --p--> --p--> --l--> --e-->   val = 1  ("apple")
                                |
                              val = 3          ("appl")

   step 1   clear val at node "e", remember 1 (the returned value)
   step 2   node "e" has no children and no val  -> prune "e"
   step 3   node "l" still holds val = 3         -> keep "l"
   step 4   nodes "a", "p", "p" lead to a live key -> keep them

   after:
   (root) --a--> --p--> --p--> --l-->   val = 3  ("appl")

   "appl" survived because its own node still carries a value;
   the shared prefix nodes were kept because they lead to it
```

## 9. Complexity

Let L be the length of the key or prefix, K the number of keys returned by
a collection operation, and N the total number of trie nodes.

| Operation | Time | Notes |
|:---|:---:|:---|
| put / get / contains_key | `O(L)` | one node per character |
| remove | `O(L)` | plus pruning on the way back |
| shortest / longest_prefix_of | `O(L)` | single walk, no branching |
| has_key_with_prefix | `O(L)` | just reach the node |
| keys_with_prefix | `O(L + K)` | walk plus collect the subtree |
| has_key_with_pattern | `O(visited)` | wildcard fans out at '.', bounded by the subtree |
| keys_with_pattern | `O(visited + K)` | same walk, collecting matches |
| keys | `O(N)` | full traversal, output already sorted |
| Space | `O(N)` | one node per distinct prefix |

`N` stays close to the number of characters actually stored because shared
prefixes share nodes: three keys whose HashMap copies total 12 characters
need only 5 character nodes plus the root. The price is a dictionary object
per node, which makes the trie heavier than a flat list for tiny key sets.

## 10. Demo walkthrough

Run:

```text
python TrieBasics.py
```

The demo builds one `TrieMap` and runs five deterministic parts:

```text
   Part A   put "apple", "app", "appl"
            -> 3 keys, node_count = 6 (root + a p p l e)
            -> HashMap would store 12 characters, trie stores 5
   Part B   put "that", "the", "them", "apple"
            -> shortest_prefix_of("themxyz") = "the"
            -> longest_prefix_of("themxyz")  = "them"
            -> has_key_with_prefix("tha") = True, ("thz") = False
            -> keys_with_prefix("th") = ["that", "the", "them"]
   Part C   wildcard checks on the same trie
            -> has_key_with_pattern("t.e") = True, ("t.x") = False
            -> keys_with_pattern("t..t") = ["that"]
            -> keys_with_pattern(".pp.") = ["appl"]
   Part D   remove("app"), then remove("apple")
            -> "appl" survives, keys stay sorted, missing key returns None
   Part E   a TrieSet with "cat", "car", "dog"
            -> contains("cat") = True, contains("cow") = False
            -> keys() = ["car", "cat", "dog"]
            -> keys_with_prefix("ca") = ["car", "cat"]
```

The final printout renders the small apple-family trie one line per depth,
with a `#` marker on nodes that end a key:

```text
   depth 0: (root)
   depth 1: a
   depth 2: p
   depth 3: p#
   depth 4: l#
   depth 5: e#
   lexicographic keys: ['app', 'appl', 'apple']
```

Every expectation is enforced with `assert`, so a passing run is also a
passing test.

## 11. Limitations and summary

What a trie cannot do, and what to keep in mind:

- Keys are strings. A `TrieMap` cannot directly store integer keys the way
  a TreeMap can; numbers must be serialized to strings first.
- Wildcard support is limited to the single-character '.'. There is no
  anchoring, repetition, or alternation — a full regex engine is far
  beyond a trie.
- Every node owns a dict. The per-node overhead is real, so a trie can be
  bigger than a packed array for short, unrelated keys.
- Prefix methods only answer prefix questions. Suffix queries need a
  reversed trie; substring queries need a suffix tree or similar.

Summary of the whole picture:

```text
   problem                      HashMap / TreeMap          Trie
   store "app"+"appl"+"apple"   12 characters              5 nodes, shared "app"
   all keys starting with "th"  scan every key             O(L + K) subtree walk
   pattern "t.e"                regex over all keys        trie walk with '.'
   keys in sorted order         sort all keys              already sorted walk
```

The trie is the natural shape behind autocomplete, spell checkers, IP
routing tables, and the typeahead search of large dictionaries — whenever
the keys are strings, the work is about prefixes, and shared prefixes
should cost nothing.

Sources:

- [Trie, Digital Tree, Prefix Tree Basics and Visualization](https://labuladong.online/en/algo/data-structure-basic/trie-map-basic/)
- [208. Implement Trie (Prefix Tree)](https://leetcode.com/problems/implement-trie-prefix-tree/)
- [211. Design Add and Search Words Data Structure](https://leetcode.com/problems/design-add-and-search-words-data-structure/)