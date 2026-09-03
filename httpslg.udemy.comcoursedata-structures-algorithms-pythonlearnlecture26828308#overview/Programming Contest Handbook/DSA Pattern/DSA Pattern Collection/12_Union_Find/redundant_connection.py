"""
Redundant Connection
In a graph that started as a tree with n nodes labeled 1..n, one extra edge was
added making it a graph with exactly one cycle. Return an edge that can be
removed so that the result is a tree again (the answer with the largest index).

Idea: union edge endpoints. The first edge whose endpoints are already connected
is the redundant edge closing the cycle.

Time: O(n * alpha(n))
Space: O(n)
"""


class DSU:
    def __init__(self, n):
        self.parent = list(range(n + 1))
        self.rank = [0] * (n + 1)

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
        return True


def find_redundant_connection(edges):
    dsu = DSU(len(edges))
    for u, v in edges:
        if not dsu.union(u, v):
            return [u, v]
    return []


if __name__ == "__main__":
    print(find_redundant_connection([[1, 2], [1, 3], [2, 3]]))  # [2, 3]
    print(find_redundant_connection([[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]]))
    # [1, 4]
