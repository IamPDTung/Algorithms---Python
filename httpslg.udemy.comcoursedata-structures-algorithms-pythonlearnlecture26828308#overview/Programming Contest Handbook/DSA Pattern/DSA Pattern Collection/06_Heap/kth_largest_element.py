"""
Kth Largest Element in Array
Find the kth largest element in an unsorted array.

Idea: maintain a min-heap of size k. After processing all numbers, the heap
contains the k largest numbers; the root is the kth largest.

Time: O(n log k)
Space: O(k)
"""

import heapq


def find_kth_largest(nums, k):
    heap = []
    for x in nums:
        if len(heap) < k:
            heapq.heappush(heap, x)
        elif x > heap[0]:
            heapq.heapreplace(heap, x)
    return heap[0]


if __name__ == "__main__":
    print(find_kth_largest([3, 2, 1, 5, 6, 4], 2))    # 5
    print(find_kth_largest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4))  # 4
