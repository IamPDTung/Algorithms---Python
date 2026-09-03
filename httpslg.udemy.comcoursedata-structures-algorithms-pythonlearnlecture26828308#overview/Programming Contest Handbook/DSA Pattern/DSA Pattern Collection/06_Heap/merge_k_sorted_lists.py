"""
Merge K Sorted Lists
Merge k sorted linked lists into one sorted linked list.

Idea: push (value, list_index, node) of each current head into a min-heap.
Pop the smallest, append to result, then push the next node of that list.

Time: O(n log k), n = total nodes
Space: O(k)
"""

import heapq


class ListNode:
    def __init__(self, val=0, nxt=None):
        self.val = val
        self.next = nxt

    def __lt__(self, other):   # make ListNode heap-comparable
        return self.val < other.val


def merge_k_lists(lists):
    heap = []
    for i, head in enumerate(lists):
        if head:
            heapq.heappush(heap, (head.val, i, head))

    dummy = ListNode()
    tail = dummy
    while heap:
        val, i, node = heapq.heappop(heap)
        tail.next = node
        tail = tail.next
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))

    return dummy.next


def to_list(head):
    result = []
    while head:
        result.append(head.val)
        head = head.next
    return result


if __name__ == "__main__":
    a = ListNode(1, ListNode(4, ListNode(5)))
    b = ListNode(1, ListNode(3, ListNode(4)))
    c = ListNode(2, ListNode(6))
    merged = merge_k_lists([a, b, c])
    print(to_list(merged))  # [1, 1, 2, 3, 4, 4, 5, 6]
