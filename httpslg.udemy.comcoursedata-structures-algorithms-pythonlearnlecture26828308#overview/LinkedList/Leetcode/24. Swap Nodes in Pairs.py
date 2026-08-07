# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def swapPairs(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if head is None or head.next is None:
            return head
        dum = ListNode(0, head)
        result = head.next
        prev = dum
        while prev.next and prev.next.next:
            first = prev.next
            second = first.next
            nxt = second.next
            second.next = first
            first.next = nxt
            prev.next = second
            prev = first
        return result
