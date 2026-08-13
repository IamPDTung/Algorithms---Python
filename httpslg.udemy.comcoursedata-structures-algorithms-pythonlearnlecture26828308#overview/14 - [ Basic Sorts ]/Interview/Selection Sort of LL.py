# Selection Sort of LL ( ** Interview Question)
# Assignment:

# Write a selection_sort() method in the LinkedList class that will sort the elements of a linked list in ascending order using the selection sort algorithm. The method should update the head and tail pointers of the linked list to reflect the new order of the nodes in the list. You can assume that the input linked list will contain only integers. You should not use any additional data structures to sort the linked list.



# Note:

# This Linked List does not have a tail pointer, which will make the method more straightforward to implement since you will not need to reassign the tail at the end.



# Input:

# The LinkedList object containing a linked list with unsorted elements (self).



# Output:

# None. The method sorts the linked list in place.



# Method Description:

# If the length of the linked list is less than 2, the method returns and the list is assumed to be already sorted.

# The selection sort algorithm works by repeatedly finding the smallest element in the unsorted part of the list and swapping it with the first element in the unsorted part of the list.

# The method starts with the entire linked list being the unsorted part of the list.

# For each pass through the unsorted part of the list, the method iterates through each element to find the smallest element in the unsorted part of the list. Once the smallest element is found, it is swapped with the first element in the unsorted part of the list.

# After each pass, the smallest element in the unsorted part of the list will be at the beginning of the unsorted part of the list.

# The method continues iterating through the unsorted part of the list until the entire list is sorted.

# After the linked list is fully sorted, the head and tail pointers of the linked list are updated to reflect the new order of the nodes in the list.



# Constraints:

# The linked list can contain duplicates.

# The method should be implemented in the LinkedList class.

# The method should not use any additional data structures to sort the linked list.

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class LinkedList:
    def __init__(self, value):
        new_node = Node(value)
        self.head = new_node
        self.length = 1

    def print_list(self):
        temp = self.head
        values = []
        while temp is not None:
            values.append(str(temp.value))
            temp = temp.next
        if values:
            print(" -> ".join(values))
        else:
            print("empty")

    def append(self, value):
        new_node = Node(value)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node
        self.length += 1


    def selection_sort(self):
        #   +===================================================+
        #   |               WRITE YOUR CODE HERE                |
        #   | Description:                                      |
        #   | - Sorts the linked list in ascending order        |
        #   |   using the selection sort algorithm.             |
        #   |                                                   |
        #   | Note:                                             |
        #   | - This linked list does not have a tail pointer.  |
        #   |                                                   |
        #   | How it works:                                     |
        #   | - Outer loop starts at the head of the list.      |
        #   | - For each node, it searches the rest of the list |
        #   |   to find the node with the smallest value.       |
        #   | - If a smaller node is found, their values are    |
        #   |   swapped (not the nodes themselves).             |
        #   | - Moves to the next node and repeats the process. |
        #   +===================================================+






# Test Cases:
# -----------------------------------

# Test 1: Empty list
print("Test 1: Empty list")
ll1 = LinkedList(5)
ll1.head = None
ll1.length = 0
ll1.selection_sort()
ll1.print_list()  # Should print: empty
print("-" * 30)

# Test 2: Single element
print("Test 2: Single element")
ll2 = LinkedList(5)
ll2.selection_sort()
ll2.print_list()  # Should print: 5
print("-" * 30)

# Test 3: Already sorted list
print("Test 3: Already sorted list")
ll3 = LinkedList(1)
ll3.append(2)
ll3.append(3)
ll3.selection_sort()
ll3.print_list()  # Should print: 1 -> 2 -> 3
print("-" * 30)

# Test 4: Reverse order
print("Test 4: Reverse order")
ll4 = LinkedList(3)
ll4.append(2)
ll4.append(1)
ll4.selection_sort()
ll4.print_list()  # Should print: 1 -> 2 -> 3
print("-" * 30)

# Test 5: Random order
print("Test 5: Random order")
ll5 = LinkedList(2)
ll5.append(1)
ll5.append(3)
ll5.selection_sort()
ll5.print_list()  # Should print: 1 -> 2 -> 3
print("-" * 30)

# Test 6: List with duplicates
print("Test 6: List with duplicates")
ll6 = LinkedList(3)
ll6.append(2)
ll6.append(2)
ll6.append(1)
ll6.append(3)
ll6.selection_sort()
ll6.print_list()  # Should print: 1 -> 2 -> 2 -> 3 -> 3
print("-" * 30)
