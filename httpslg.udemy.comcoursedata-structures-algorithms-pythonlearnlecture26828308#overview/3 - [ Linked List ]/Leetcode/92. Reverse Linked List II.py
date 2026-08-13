
from typing import Optional


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def build_list(arr):
    dummy = ListNode()
    curr = dummy
    for x in arr:
        curr.next = ListNode(x)
        curr = curr.next
    return dummy.next


def to_list(head):
    res = []
    while head:
        res.append(head.val)
        head = head.next
    return res


test_cases = [
    ([1, 2, 3, 4, 5], 2, 4),
    ([1, 2, 3, 4, 5], 1, 5),
    ([1, 2, 3, 4, 5], 1, 3),
    ([1, 2, 3, 4, 5], 3, 5),
    ([1, 2], 1, 2),
    ([1], 1, 1),
    ([1, 2, 3, 4, 5], 3, 3),
    ([1, 2, 3], 1, 2),
    ([1, 2, 3], 2, 3),
    ([1, 2, 3, 4], 2, 3),
    ([1, 2, 3, 4, 5, 6], 3, 4),
    ([1, 2, 3, 4, 5, 6], 2, 5),
    ([1, 2, 3, 4, 5, 6, 7], 4, 4),
    ([1, 2, 3, 4, 5, 6, 7], 1, 6),
    ([1, 2, 3, 4, 5, 6, 7], 2, 7),
]

class Solution:
    def reverseBetween(self, head: Optional[ListNode], left: int, right: int) -> Optional[ListNode]:
        dummy = ListNode(0, head)
        prev = dummy
        for _ in range(left - 1):
            prev = prev.next
        current = prev.next
        move = current.next
        for _ in range(right - left):
            nxt = move.next
            current.next = nxt
            move.next = prev.next
            prev.next = move
            move = nxt
        return dummy.next

solution = Solution()

for i, (arr, left, right) in enumerate(test_cases, 1):
    head = build_list(arr)
    result = solution.reverseBetween(head, left, right)

    print(f"Case {i}")
    print(f"Input : head={arr}, left={left}, right={right}")
    print(f"Output: {to_list(result)}")
    print("-" * 50)
