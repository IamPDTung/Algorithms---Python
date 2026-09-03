"""
Number of Provinces
There are n cities. isConnected[i][j] = 1 if city i is directly connected to
city j. Return the total number of provinces (connected groups of cities).

Idea: union all connected pairs, then count distinct roots.

Time: O(n^2 * alpha(n))
Space: O(n)
"""


class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1


def find_circle_num(is_connected):
    n = len(is_connected)
    dsu = DSU(n)
    for i in range(n):
        for j in range(i + 1, n):
            if is_connected[i][j]:
                dsu.union(i, j)
    return len({dsu.find(i) for i in range(n)})


if __name__ == "__main__":
    print(find_circle_num([[1, 1, 0], [1, 1, 0], [0, 0, 1]]))  # 2
    print(find_circle_num([[1, 0, 0], [0, 1, 0], [0, 0, 1]]))  # 3
