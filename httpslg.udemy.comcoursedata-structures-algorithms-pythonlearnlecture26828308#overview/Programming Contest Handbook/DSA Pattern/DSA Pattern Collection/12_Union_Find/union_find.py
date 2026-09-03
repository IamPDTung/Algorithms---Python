"""
Union-Find (Disjoint Set Union) — reusable implementation.

Operations with path compression and union by rank:
  find(x)  -> O(alpha(n)) amortized ~ O(1)
  union(x, y) -> returns False if already connected, else True
"""


class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.components = n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1
        self.components -= 1
        return True

    def connected(self, x, y):
        return self.find(x) == self.find(y)


if __name__ == "__main__":
    dsu = DSU(6)
    print(dsu.union(0, 1))   # True
    print(dsu.union(2, 3))   # True
    print(dsu.union(0, 3))   # True
    print(dsu.connected(1, 2))  # True
    print(dsu.components)       # 3  ({0,1,2,3}, {4}, {5})
