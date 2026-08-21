# Segment Tree Basics and Visualization

## 1. Goal

A segment tree is a binary tree whose leaves are the elements of an array
and whose internal nodes store the aggregate (sum, min, max, ...) over their
interval of indices. Because every internal node remembers the aggregate of
its whole interval, both an interval query and a point update finish in
`O(log N)` instead of `O(N)`.

Why was it born? A plain array gives `O(1)` reads, but a range query such
as `sum(l..r)` scans `O(N)` elements and a point update is `O(1)`. That is
fine for static data, but many problems mix interval queries with dynamic
point updates: e.g. online judge problems that ask for "sum of a range,
then change one element, then query again, ...". Doing each range query by
scanning costs `O(N)`, and `M` queries cost `O(N*M)`, which is too slow for
large inputs. The segment tree trades `O(N)` build time and `O(N)` memory
so that every query and every update is `O(log N)`.

The implementation in `SegmentTreeBasics.py` provides:

- `SegmentTree`: a sum-aggregate tree with point update and range query.
- `LazySegmentTree`: range add + range sum with lazy propagation, so a
  whole range can be updated in `O(log N)`.
- `draw()`: an ASCII rendering of the tree with intervals for learning.
- Randomized cross-checks that compare the trees against a plain reference
  list.

Source references:

- [Segment Tree Basics and Visualization](https://labuladong.online/en/algo/data-structure-basic/segment-tree-basic/)

## 2. Application scenarios: why arrays and prefix-suffix arrays fail

Static data can be served by simpler tools. For a fixed array, the prefix
sum array answers `sum(l..r)` in `O(1)`:

```text
values:     [1, 3, 5, 7, 9, 11]
prefix:     [1, 4, 9, 16, 25, 36]

sum(2..4) = prefix[4] - prefix[1] = 25 - 4 = 21     O(1)
```

But the moment an element changes, every prefix sum after it must be
recomputed, which costs `O(N)` per update:

```text
update index 3:  5 -> 8

values:     [1, 3, 5, 8, 9, 11]
prefix:     [1, 4, 9, 17, 26, 37]
                        ^--- must touch indices 3, 4, 5   O(N)
```

The selection-sort trick uses only prefix and suffix *minimums*, which are
also static. It cannot answer "minimum over the arbitrary range [l, r]"
after updates:

```text
selection sort:
  find min of [0..N-1]  -> prefix/suffix min works
  find min of [1..N-1]  -> suffix min still works
  find min of [2..N-1]  -> still a suffix ... always the suffix!

arbitrary range [l, r] after updates:
  sum/min over [l, r] where l and r are arbitrary -> prefix array useless
  an update at any index invalidates the whole prefix array -> O(N) fix
```

So the scenario that demands a segment tree is: interval queries over
*arbitrary* ranges (not just prefixes or suffixes) interleaved with dynamic
point or range updates. Both must be fast.

## 3. Core API

`SegmentTree` (sum aggregate, point update):

```python
tree = SegmentTree(values)

tree.query(l, r)        # inclusive sum over [l, r]     O(log N)
tree.update(i, v)       # values[i] = v                 O(log N)
tree.to_list()          # copy of the underlying values O(N)
tree.size()             # number of elements            O(1)
tree.draw()             # ASCII rendering               O(N)
```

`LazySegmentTree` (range add, range sum):

```python
tree = LazySegmentTree(values)

tree.range_add(l, r, delta)  # values[i] += delta for l<=i<=r   O(log N)
tree.range_sum(l, r)         # inclusive sum over [l, r]         O(log N)
tree.point_get(i)            # current value at index i          O(log N)
```

## 4. Core principle: leaves are elements, internal nodes are intervals

For `values = [1, 3, 5, 7, 9, 11]` the segment tree looks like this. Every
node is labeled with its interval `[l, r]` and its stored sum:

```text
                 [0,5]=36
                /         \
          [0,2]=9          [3,5]=27
          /     \          /      \
     [0,1]=4   [2,2]=5  [3,4]=16  [5,5]=11
     /     \             /     \
 [0,0]=1 [1,1]=3    [3,3]=7  [4,4]=9

interval [0,5]  covers everything   sum = 1+3+5+7+9+11 = 36
interval [3,5]  covers 7, 9, 11     sum = 27
interval [3,4]  covers 7, 9         sum = 16
leaf    [0,0]  element 1
```

The two invariant rules:

```text
1. A leaf holds exactly one element:  tree[leaf] = values[i]
2. An internal node is the merge of its children:
   tree[node] = tree[left_child] + tree[right_child]
```

The same shape works for min/max/gcd aggregates: only the merge operation
changes.

## 5. Building the tree

Build recursively: split the interval at `mid`, build the two children,
then merge. The tree is stored in a flat array of size `4*N` with the heap
layout: the children of `node` are `2*node` and `2*node+1`, root at `1`.

```python
def _build(node, start, end):
    if start == end:
        tree[node] = values[start]      # leaf: one element
        return
    mid = (start + end) // 2
    _build(2 * node, start, mid)        # left half
    _build(2 * node + 1, mid + 1, end)  # right half
    tree[node] = tree[2 * node] + tree[2 * node + 1]  # merge
```

The recursion for `[1, 3, 5, 7, 9, 11]`:

```text
_build(1, 0, 5)            interval [0,5]
 |-- _build(2, 0, 2)       interval [0,2]
 |    |-- _build(4, 0, 1)  interval [0,1]
 |    |    |-- _build(8, 0, 0)   -> tree[8] = 1
 |    |    |-- _build(9, 1, 1)   -> tree[9] = 3
 |    |    `-- tree[4] = 1 + 3 = 4
 |    |-- _build(5, 2, 2)  -> tree[5] = 5
 |    `-- tree[2] = 4 + 5 = 9
 |-- _build(3, 3, 5)       interval [3,5]
 |    |-- _build(6, 3, 4)  interval [3,4]
 |    |    |-- _build(12, 3, 3)  -> tree[12] = 7
 |    |    |-- _build(13, 4, 4)  -> tree[13] = 9
 |    |    `-- tree[6] = 7 + 9 = 16
 |    |-- _build(7, 5, 5)  -> tree[7] = 11
 |    `-- tree[3] = 16 + 11 = 27
 `-- tree[1] = 9 + 27 = 36

node indices follow the heap layout: 1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 13
```

Build cost: `O(N)` nodes visited, each doing `O(1)` work.

## 6. Query: why O(log N)

A range query descends from the root. At each node there are three cases:

```text
case 1  no overlap:   right < start or end < left    -> return 0
case 2  full overlap: left <= start and end <= right -> return tree[node]
case 3  partial:      descend into both children and add the results
```

Query `[2, 4]` on `[1, 3, 5, 7, 9, 11]` (expected `5+7+9 = 21`). The
covered nodes are marked with `[*]`:

```text
                 [0,5]=36
                /         \
          [0,2]=9         [3,5]=27
          /     \          /      \
     [0,1]=4   [2,2]=5* [3,4]=16* [5,5]=11
     /     \             /     \
 [0,0]=1 [1,1]=3    [3,3]=7  [4,4]=9

[0,5]  partial  -> descend
[0,2]  partial  -> descend
[0,1]  no overlap with [2,4]  -> return 0
[2,2]  full overlap          -> return 5      [*]
[3,5]  partial  -> descend
[3,4]  full overlap          -> return 16     [*]
[5,5]  no overlap with [2,4] -> return 0

answer = 5 + 16 = 21        only 2 full nodes visited
```

More sample ranges on the same tree:

```text
query [0, 5]:
                 [0,5]=36*   full overlap -> answer 36
   visited nodes: 1

query [3, 3]:
   [0,5] partial -> [3,5] partial -> [3,4] partial -> [3,3]* -> answer 7
   visited nodes: 4 along one path

query [1, 3]:
                 [0,5]=36
                /         \
          [0,2]=9         [3,5]=27
          /     \          /      \
     [0,1]=4   [2,2]=5* [3,4]=16* [5,5]=11
     /     \
 [0,0]=1 [1,1]=3*

   [0,1] partial -> [1,1] full -> 3
   [2,2] full -> 5
   [3,4] partial -> [3,3] full -> 7
   answer = 3 + 5 + 7 = 15

query [0, 2]:
   [0,2] full overlap -> return 9
   visited nodes: 1
```

Why only `O(log N)` nodes? At each level the query visits at most two
"boundary" nodes plus the full nodes between them, and a full node stops
the recursion immediately. The interval splits in half at every level, so
there are `log2(N)` levels:

```text
level 0   [0,5]                     1 node
level 1   [0,2] [3,5]               2 boundary nodes
level 2   [0,1] [2,2] [3,4] [5,5]   <= 2 boundary + full nodes
level 3   leaves                     only the needed full leaves

total visited nodes per level: <= 4   ->   O(log N) nodes in total
```

## 7. Point update: why O(log N)

A point update touches exactly one leaf and then recomputes every ancestor
on the path back to the root. The path from the leaf to the root has
`log2(N) + 1` nodes.

Update `update(3, 8)` on `[1, 3, 5, 7, 9, 11]`. The path is marked with
arrows:

```text
before update:

                 [0,5]=36
                /         \
          [0,2]=9         [3,5]=27
          /     \          /      \
     [0,1]=4   [2,2]=5  [3,4]=16  [5,5]=11
     /     \             /     \
 [0,0]=1 [1,1]=3    [3,3]=7  [4,4]=9

after update(3, 8):

                 [0,5]=37
                    ^
          [0,2]=9  |   [3,5]=28
                    ^
     [0,1]=4  |  [2,2]=5 | [3,4]=17  [5,5]=11
                          ^
 [0,0]=1 [1,1]=3    [3,3]=8*  [4,4]=9
                       ^--- the only leaf that changed

only the path nodes are recomputed:
   [3,3]: 7 -> 8
   [3,4]: 16 -> 8 + 9 = 17
   [3,5]: 27 -> 17 + 11 = 28
   [0,5]: 36 -> 9 + 28 = 37
```

The recursive descent to the leaf, drawn as the path:

```text
_update(1, 0, 5, index=3)
  | 3 > mid=2 -> go right
  +-- _update(3, 3, 5, index=3)
       | 3 <= mid=4 -> go left
       +-- _update(6, 3, 4, index=3)
            | 3 <= mid=3 -> go left
            +-- _update(12, 3, 3, index=3)   leaf: tree[12] = 8
            +-- recompute tree[6] = 8 + 9 = 17
       +-- recompute tree[3] = 17 + 11 = 28
  +-- recompute tree[1] = 9 + 28 = 37

path length: 4 nodes = log2(6) + 1  ->  O(log N)
```

## 8. Lazy propagation: range update in O(log N)

A naive range add would visit every leaf in the range, costing `O(N)`.
Lazy propagation fixes this: when a node's interval is fully covered, we do
not descend at all. We update the node's sum, park the delta in a `lazy`
tag, and leave the children untouched. The tag is pushed down only when a
later operation actually needs the children.

```python
def _update_range(node, start, end, left, right, delta):
    if right < start or end < left:
        return
    if left <= start and end <= right:      # full cover: lazy park
        tree[node] += delta * (end - start + 1)
        lazy[node] += delta
        return
    _push(node, start, end)                  # push before descending
    mid = (start + end) // 2
    _update_range(2 * node, start, mid, left, right, delta)
    _update_range(2 * node + 1, mid + 1, end, left, right, delta)
    tree[node] = tree[2 * node] + tree[2 * node + 1]

def _push(node, start, end):
    if lazy[node] == 0 or start == end:
        return
    delta = lazy[node]
    mid = (start + end) // 2
    tree[2 * node] += delta * (mid - start + 1)
    tree[2 * node + 1] += delta * (end - mid)
    lazy[2 * node] += delta
    lazy[2 * node + 1] += delta
    lazy[node] = 0                            # tag cleared
```

`range_add(1, 4, 10)` on `[1, 3, 5, 7, 9, 11]` should add 10 to indices
1..4, producing `[1, 13, 15, 17, 19, 11]`. Only two nodes are fully
covered, so only they are touched:

```text
                 [0,5]=36
                /         \
          [0,2]=9         [3,5]=27
          /     \          /      \
     [0,1]=4   [2,2]=5  [3,4]=16  [5,5]=11
     /     \             /     \
 [0,0]=1 [1,1]=3    [3,3]=7  [4,4]=9

step 1: [0,1] is partial for [1,4] -> descend to [1,1]
        [1,1] full cover -> tree[1,1] = 3 + 10 = 13, lazy[1,1] += 10
step 2: [2,2] full cover -> tree[2,2] = 5 + 10 = 15, lazy[2,2] += 10
step 3: [3,4] full cover -> tree[3,4] = 16 + 20 = 36, lazy[3,4] += 10
        (10 for each of the 2 elements -> +20)
step 4: recompute ancestors: [0,2] = 4 + 15 = 19, [0,5] = 19 + 47 = 66

after the update (lazy tags shown in brackets):

                 [0,5]=66
                /         \
          [0,2]=19        [3,5]=47
          /     \          /      \
     [0,1]=4   [2,2]=15* [3,4]=36* [5,5]=11
     /     \    lazy+10   lazy+10
 [0,0]=1 [1,1]=13*
         lazy+10

children of the lazy nodes were NOT visited: that is the saving
```

Now a later query forces the push. `range_sum(2, 3)` descends through
`[0,5]` -> `[0,2]` -> `[2,2]` (full, returns 15) and `[3,5]` -> `[3,4]`
(partial, must push first):

```text
range_sum(2, 3):
                 [0,5]=66
                /         \
          [0,2]=19        [3,5]=47
          /     \          /      \
     [0,1]=4   [2,2]=15* [3,4]=36  [5,5]=11
                          |   \-- partial: push lazy before descending
                          |       [3,3] = 7+10 = 17, lazy+10
                          |       [4,4] = 9+10 = 19, lazy+10
                          `-- [3,4] lazy cleared -> 0
answer = 15 + 17 = 32     (= 5+10 + 7+10)

the push happened on demand, only along the query path
```

A push, drawn step by step:

```text
before _push(node=[3,4], start=3, end=4):
   tree[3,4] = 36,  lazy[3,4] = 10
   tree[3,3] = 7    lazy[3,3] = 0
   tree[4,4] = 9    lazy[4,4] = 0

after _push:
   delta = 10
   tree[3,3] += 10*1 -> 17   lazy[3,3] += 10
   tree[4,4] += 10*1 -> 19   lazy[4,4] += 10
   lazy[3,4] = 0
```

Lazy cost summary: a range add parks a tag at `O(log N)` boundary nodes
instead of touching `O(N)` leaves, and each tag is pushed exactly once,
when a later query/update needs the children.

## 9. Dynamic segment tree for huge or sparse ranges

When the index range is huge (e.g. `[0, 10^9]`) but few elements are
actually touched, building `4*N` nodes is impossible. The dynamic segment
tree allocates nodes only when they are needed: children are created
on demand and are absent when the interval was never visited.

```text
static tree, N = 10^9:    4*10^9 array slots -> out of memory

dynamic tree (sparse):    only visited intervals exist as real nodes

                       [0,10^9]          created on first query
                      /         \
                [0,5*10^8]    [5*10^8+1,10^9]   created on demand
                /     \
          [0,2.5e8]  [2.5e8+1,5e8]
                       /      \
                 [..]   [..]  ... nodes only where operations land

memory used: O(k * log U), k = number of distinct touched positions
```

The recursion is identical; only the storage changes: instead of
`self.tree[node]`, children are held in two pointers that start as `None`
and are allocated inside the recursive call when a partial visit needs
them.

## 10. Complexity summary

| Operation | Static array | Prefix sums | Segment tree | Lazy segment tree |
|:---|:---:|:---:|:---:|:---:|
| Build | `O(N)` | `O(N)` | `O(N)` | `O(N)` |
| Point update | `O(1)` | `O(N)` | `O(log N)` | `O(log N)` |
| Range sum `[l,r]` | `O(N)` scan | `O(1)` (static) | `O(log N)` | `O(log N)` |
| Range add `[l,r]` | `O(N)` | `O(N)` | `O(N)` naive | `O(log N)` lazy |
| Memory | `O(N)` | `O(N)` | `O(4N)` | `O(4N)` |

Why the height is `O(log N)`: the interval halves at every level, so the
number of levels is `log2(N)`:

```text
level 0   [0, N-1]                     size N
level 1   [0, N/2-1] [N/2, N-1]        size N/2
level 2   four intervals of size N/4
level 3   eight intervals of size N/8
  ...
level k   intervals of size N / 2^k
  ...
level log2(N)   leaves of size 1

stop when N / 2^k = 1  ->  k = log2(N) levels
```

## 11. Demo walkthrough

Run:

```text
python SegmentTreeBasics.py
```

First the basic tree is built from `[1, 3, 5, 7, 9, 11]` and its ASCII
rendering is printed. Then the deterministic checks:

```text
query(0,5) = 36       full range
query(2,4) = 21       5 + 7 + 9
query(0,0) = 1        single element
query(3,3) = 7        single element
query(1,3) = 15       3 + 5 + 7
update(3, 8)          values become [1, 3, 5, 8, 9, 11]
query(2,4) = 22       5 + 8 + 9
query(0,5) = 37       new total
```

Then 200 randomized operations on a 30-element array compare `query` with
`sum(reference[l:r+1])` of a reference list; all must match.

The lazy tree starts from the same values:

```text
range_add(1, 4, 10)   values become [1, 13, 15, 17, 19, 11]
range_sum(0,5) = 76
range_sum(2,3) = 32   15 + 17
range_sum(0,0) = 1
range_add(0, 0, 5)    values become [6, 13, 15, 17, 19, 11]
range_sum(0,2) = 34   6 + 13 + 15
```

Again 200 randomized range adds and range sums are cross-checked against a
reference list, and the whole demo ends with `All assertions passed.`

## 12. Limitations and summary

Limitations:

- The static tree needs `O(4N)` memory even when many nodes are never
  useful; the dynamic variant fixes that for sparse/huge ranges.
- Only one aggregate per tree; combining sum and min in one tree requires
  storing both per node (or a custom merge struct).
- Recursive implementations can hit recursion depth limits for extreme
  sizes; iterative versions exist but are harder to read.
- Lazy tags only work for aggregates that can absorb a range operation
  (sum += delta*len, min/max need careful handling; max with range add
  needs more bookkeeping).

Summary:

```text
plain array      range query O(N), point update O(1)
prefix sums      range query O(1), point update O(N)
segment tree     range query O(log N), point update O(log N)
lazy seg tree    range query O(log N), range update O(log N)
```

The segment tree is the canonical answer whenever the workload is a mix of
interval queries and updates on a dynamic array. Its only real costs are
`O(N)` build time and `O(4N)` memory, and the lazy trick extends it to
range updates at the same logarithmic cost.

## 13. Sources

- [Segment Tree Basics and Visualization](https://labuladong.online/en/algo/data-structure-basic/segment-tree-basic/)