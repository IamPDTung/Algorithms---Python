"""
Merge Intervals
Given an array of intervals where intervals[i] = [start, end], merge all
overlapping intervals and return an array of the non-overlapping intervals.

Idea: sort by start. If the next interval overlaps the current merged interval,
extend it; otherwise push the current and start a new one.

Time: O(n log n)
Space: O(n) for output
"""


def merge(intervals):
    intervals.sort(key=lambda x: x[0])
    result = []
    for start, end in intervals:
        if result and start <= result[-1][1]:
            result[-1][1] = max(result[-1][1], end)
        else:
            result.append([start, end])
    return result


if __name__ == "__main__":
    print(merge([[1, 3], [2, 6], [8, 10], [15, 18]]))  # [[1,6],[8,10],[15,18]]
    print(merge([[1, 4], [4, 5]]))                     # [[1,5]]
