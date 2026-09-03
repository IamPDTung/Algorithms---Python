"""
Daily Temperatures
Given an array of daily temperatures, return an array such that answer[i] is the
number of days you have to wait until a warmer temperature.

Idea: monotonic decreasing stack of indices. When we see a warmer day, pop and
record the difference.

Time: O(n)
Space: O(n)
"""


def daily_temperatures(temperatures):
    n = len(temperatures)
    answer = [0] * n
    stack = []
    for i, t in enumerate(temperatures):
        while stack and temperatures[stack[-1]] < t:
            prev = stack.pop()
            answer[prev] = i - prev
        stack.append(i)
    return answer


if __name__ == "__main__":
    print(daily_temperatures([73, 74, 75, 71, 69, 72, 76, 73]))
    # [1, 1, 4, 2, 1, 1, 0, 0]
    print(daily_temperatures([30, 40, 50, 60]))   # [1, 1, 1, 0]
