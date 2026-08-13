# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def partition(self, head: Optional[ListNode], x: int) -> Optional[ListNode]:
        dummy1, dummy2 = ListNode(0), ListNode(0)
        prev1, prev2 = dummy1, dummy2
        while head is not None:
            if head.val < x:
                prev1.next = head
                prev1 = prev1.next
            else:
                prev2.next = head
                prev2 = prev2.next
            head = head.next

        prev1.next = dummy2.next
        prev2.next = None

        return dummy1.next
