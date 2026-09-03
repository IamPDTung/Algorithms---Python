"""
Gas Station
There are n gas stations along a circular route. gas[i] = gas at station i,
cost[i] = gas needed to travel from i to i+1. Return the starting station index
such that you can travel the whole circle once, or -1.

Idea: if total gas < total cost, impossible. Otherwise the answer is the index
right after the point where the running balance reaches its minimum (equivalently:
restart the start candidate whenever the balance goes negative).

Time: O(n)
Space: O(1)
"""


def can_complete_circuit(gas, cost):
    total = 0
    current = 0
    start = 0
    for i in range(len(gas)):
        total += gas[i] - cost[i]
        current += gas[i] - cost[i]
        if current < 0:
            start = i + 1
            current = 0
    return start if total >= 0 else -1


if __name__ == "__main__":
    print(can_complete_circuit([1, 2, 3, 4, 5], [3, 4, 5, 1, 2]))  # 3
    print(can_complete_circuit([2, 3, 4], [3, 4, 3]))             # -1
