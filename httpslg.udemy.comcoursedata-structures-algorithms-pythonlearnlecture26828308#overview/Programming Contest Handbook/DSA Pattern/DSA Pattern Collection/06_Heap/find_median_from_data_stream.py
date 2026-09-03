"""
Find Median from Data Stream
Design a data structure that supports adding integers and finding the median of
all added so far.

Idea: two heaps. A max-heap (stored negated) for the smaller half, a min-heap
for the larger half. Keep sizes balanced (max_heap >= min_heap).

addNum: O(log n), findMedian: O(1)
Space: O(n)
"""

import heapq


class MedianFinder:
    def __init__(self):
        self.small = []   # max-heap (negated values) - smaller half
        self.large = []   # min-heap - larger half

    def add_num(self, num):
        heapq.heappush(self.small, -num)
        heapq.heappush(self.large, -heapq.heappop(self.small))
        if len(self.large) > len(self.small):
            heapq.heappush(self.small, -heapq.heappop(self.large))

    def find_median(self):
        if len(self.small) > len(self.large):
            return float(-self.small[0])
        return (-self.small[0] + self.large[0]) / 2.0


if __name__ == "__main__":
    mf = MedianFinder()
    for x in [5, 15, 1, 3]:
        mf.add_num(x)
        print(mf.find_median())
    # 5.0, 10.0, 5.0, 4.0
