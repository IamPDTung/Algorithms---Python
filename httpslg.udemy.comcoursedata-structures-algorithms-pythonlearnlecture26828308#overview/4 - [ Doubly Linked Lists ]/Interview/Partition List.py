# DLL: Partition List ( ** Interview Question)
# Write a method called partition_list(self, x) that rearranges the nodes in a doubly linked list so that all nodes with a value less than a given number x come before all nodes with a value greater than or equal to x.

# You must maintain the original relative order of the nodes in each of the two partitions.

# The partitioning must be performed in-place. You cannot create new nodes (other than dummy nodes).

# Both .next and .prev pointers must be updated correctly.

# If the list is empty, nothing should happen.





# 🧪 Examples

# Example 1
# Input DLL:
# 3 <-> 8 <-> 5 <-> 10 <-> 2 <-> 1
# Partition value: x = 5
# Output DLL:
# 3 <-> 2 <-> 1 <-> 8 <-> 5 <-> 10

# Why:

# Nodes < 5: 3, 2, 1

# Nodes >= 5: 8, 5, 10

# Order of nodes is preserved in both groups

# Smaller group comes before larger/equal group



# Example 2
# Input DLL:
# 1 <-> 2 <-> 3
# Partition value: x = 5
# Output DLL:
# 1 <-> 2 <-> 3
# Why:
# All nodes are already less than x. No rearrangement needed.



# Example 3
# Input DLL:
# 7 <-> 8 <-> 9
# Partition value: x = 5
# Output DLL:
# 7 <-> 8 <-> 9
# Why:
# All nodes are >= x. Order remains the same.



# Example 4
# Input DLL:
# 1
# Partition value: x = 2
# Output DLL:
# 1
# Why:
# Single-node list. Nothing to rearrange.



# Example 5
# Input DLL:
# (empty)
# Partition value: x = 3
# Output DLL:
# (empty)
# Why:
# Empty list. Nothing to do.





# 📘 What This Exercise Is Designed to Teach

# How to traverse and reorganize nodes in a doubly linked list.

# How to use dummy nodes to simplify pointer manipulation.

# How to maintain both .next and .prev pointers correctly in DLLs.

# How to perform an in-place partition without losing any nodes.

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None


class DoublyLinkedList:
    def __init__(self, value):
        new_node = Node(value)
        self.head = new_node
        self.length = 1

    def print_list(self):
        output = []
        current_node = self.head
        while current_node is not None:
            output.append(str(current_node.value))
            current_node = current_node.next
        print(" <-> ".join(output))

    def append(self, value):
        new_node = Node(value)
        if self.head is None:
            self.head = new_node
        else:
            temp = self.head
            while temp.next is not None:
                temp = temp.next
            temp.next = new_node
            new_node.prev = temp
        self.length += 1
        return True

    def make_empty(self):
        self.head = None
        self.tail = None
        self.length = 0


    def partition_list(self, x):
        #   +===================================================+
        #   |               WRITE YOUR CODE HERE                |
        #   | Description:                                      |
        #   | - Partitions a doubly linked list around a value  |
        #   |   `x`.                                            |
        #   | - All nodes with values less than `x` come before |
        #   |   nodes with values greater than or equal to `x`. |
        #   |                                                   |
        #   | Behavior:                                         |
        #   | - Uses two dummy nodes to create two sublists:    |
        #   |   one for nodes < x, and one for nodes >= x.      |
        #   | - Each node is added to the appropriate sublist   |
        #   |   while maintaining both next and prev pointers.  |
        #   | - The sublists are then joined together.          |
        #   | - The head of the list is updated to the start of |
        #   |   the merged result.                              |
        #   +===================================================+








# -------------------------------
# Test Cases:
# -------------------------------

print("\nTest Case 1: Partition around 5")
dll1 = DoublyLinkedList(3)
dll1.append(8)
dll1.append(5)
dll1.append(10)
dll1.append(2)
dll1.append(1)
print("BEFORE: ", end="")
dll1.print_list()
dll1.partition_list(5)
print("AFTER:  ", end="")
dll1.print_list()

print("\nTest Case 2: All nodes less than x")
dll2 = DoublyLinkedList(1)
dll2.append(2)
dll2.append(3)
print("BEFORE: ", end="")
dll2.print_list()
dll2.partition_list(5)
print("AFTER:  ", end="")
dll2.print_list()

print("\nTest Case 3: All nodes greater than x")
dll3 = DoublyLinkedList(6)
dll3.append(7)
dll3.append(8)
print("BEFORE: ", end="")
dll3.print_list()
dll3.partition_list(5)
print("AFTER:  ", end="")
dll3.print_list()

print("\nTest Case 4: Empty list")
dll4 = DoublyLinkedList(1)
dll4.make_empty()
print("BEFORE: ", end="")
dll4.print_list()
dll4.partition_list(5)
print("AFTER:  ", end="")
dll4.print_list()

print("\nTest Case 5: Single node")
dll5 = DoublyLinkedList(1)
print("BEFORE: ", end="")
dll5.print_list()
dll5.partition_list(5)
print("AFTER:  ", end="")
dll5.print_list()
