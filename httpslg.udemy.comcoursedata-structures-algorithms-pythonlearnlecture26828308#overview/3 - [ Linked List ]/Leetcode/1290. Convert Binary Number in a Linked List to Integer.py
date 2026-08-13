# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def getDecimalValue(self, head: Optional[ListNode]) -> int:
        current = head
        total = 0 if head.val == 0 else 1
        while current :
            if current.next.val == 1:
                total = total * 2 + 1
            else:
                total = total * 2
            current = current.next
        return total
