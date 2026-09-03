"""
Course Schedule
There are numCourses courses labeled 0..numCourses-1. prerequisites[i] = [a, b]
means you must take course b before course a. Return True if you can finish all
courses (i.e. the prerequisite graph is a DAG - no cycle).

Idea: build adjacency list, compute indegrees, run Kahn's topological sort.
If processed count == numCourses, no cycle.

Time: O(V + E)
Space: O(V + E)
"""

from collections import defaultdict, deque


def can_finish(num_courses, prerequisites):
    graph = defaultdict(list)
    indegree = [0] * num_courses
    for a, b in prerequisites:
        graph[b].append(a)
        indegree[a] += 1

    q = deque([i for i in range(num_courses) if indegree[i] == 0])
    processed = 0
    while q:
        node = q.popleft()
        processed += 1
        for neighbor in graph[node]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                q.append(neighbor)

    return processed == num_courses


if __name__ == "__main__":
    print(can_finish(2, [[1, 0]]))            # True
    print(can_finish(2, [[1, 0], [0, 1]]))    # False (cycle)
