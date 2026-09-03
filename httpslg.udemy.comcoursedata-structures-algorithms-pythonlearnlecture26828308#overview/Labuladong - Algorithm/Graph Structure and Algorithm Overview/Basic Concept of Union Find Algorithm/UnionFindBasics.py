from __future__ import annotations

from typing import List, Sequence, Tuple


class UnionFindNaive:
    """Basic Union-Find with NO optimization.

    union/connected can degrade to O(V) because the tree can become a linked
    list. Shown first so you can see why the optimizations exist.
    """

    def __init__(self, n: int) -> None:
        self._parent = list(range(n))
        self._count = n

    def find(self, x: int) -> int:
        while self._parent[x] != x:
            x = self._parent[x]
        return x

    def union(self, p: int, q: int) -> bool:
        rp, rq = self.find(p), self.find(q)
        if rp == rq:
            return False
        self._parent[rp] = rq
        self._count -= 1
        return True

    def connected(self, p: int, q: int) -> bool:
        return self.find(p) == self.find(q)

    def count(self) -> int:
        return self._count


class UnionFind:
    """Union-Find with union-by-size + path compression.

    Both make the trees stay shallow, giving near-constant O(alpha(V)) time.
    """

    def __init__(self, n: int) -> None:
        self._parent = list(range(n))
        self._size = [1] * n
        self._count = n

    def find(self, x: int) -> int:
        root = x
        while self._parent[root] != root:
            root = self._parent[root]
        while self._parent[x] != x:  # path compression: flatten the path
            nxt = self._parent[x]
            self._parent[x] = root
            x = nxt
        return root

    def union(self, p: int, q: int) -> bool:
        rp, rq = self.find(p), self.find(q)
        if rp == rq:
            return False
        # union by size: hang the smaller tree under the larger one
        if self._size[rp] < self._size[rq]:
            rp, rq = rq, rp
        self._parent[rq] = rp
        self._size[rp] += self._size[rq]
        self._count -= 1
        return True

    def connected(self, p: int, q: int) -> bool:
        return self.find(p) == self.find(q)

    def count(self) -> int:
        return self._count


def friend_circles(m: Sequence[Sequence[int]]) -> int:
    """Given an adjacency matrix M of a friend network, count friend circles.

    M[i][j] == 1 means i and j are directly friends. A friend circle is a set
    of people who are all (transitively) connected. Uses Union-Find.
    """
    n = len(m)
    uf = UnionFind(n)
    for i in range(n):
        for j in range(n):
            if m[i][j] == 1:
                uf.union(i, j)
    return uf.count()


def _demo() -> None:
    print("=== Dynamic connectivity: 10 isolated nodes ===")
    uf = UnionFind(10)
    print("initial components:", uf.count(), "(each node is its own)")
    print()

    print("=== Union operations ===")
    for p, q in [(0, 1), (1, 2), (5, 6)]:
        uf.union(p, q)
        print(f"  union({p},{q}) -> components now: {uf.count()}")
    print()

    print("=== connected() queries ===")
    print("connected(0,2):", uf.connected(0, 2), "(0-1, 1-2 transitive)")
    print("connected(0,5):", uf.connected(0, 5), "(different circles)")
    print("connected(5,6):", uf.connected(5, 6))
    print()

    print("=== Why transitive connectivity matters ===")
    print("  0-1, 1-2  =>  0 and 2 are connected through 1")
    print("  connected(0,2) =", uf.connected(0, 2))
    print()

    print("=== Friend circles (LeetCode-style) ===")
    # 4 people: A-B friends, C alone, D alone -> 3 circles
    m = [
        [1, 1, 0, 0],
        [1, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ]
    print("adjacency matrix:")
    for row in m:
        print("  ", row)
    print("number of friend circles:", friend_circles(m))
    print()

    print("=== Naive vs optimized tree shape ===")
    naive = UnionFindNaive(6)
    for p, q in [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)]:
        naive.union(p, q)
    opt = UnionFind(6)
    for p, q in [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)]:
        opt.union(p, q)
    print("naive parent chain (0..5):", naive._parent, "(0->1->2->...->5 list)")
    print("opt   parent chain (0..5):", opt._parent, "(all point at one root)")
    print()

    # ---- assertions ----
    assert uf.count() == 7  # 10 - 3 successful unions
    assert uf.connected(0, 2) is True
    assert uf.connected(0, 5) is False
    assert uf.connected(5, 6) is True
    assert friend_circles(m) == 3
    assert naive._parent == [1, 2, 3, 4, 5, 5]
    assert all(p == 0 for p in opt._parent)
    print("All assertions passed.")


if __name__ == "__main__":
    _demo()
