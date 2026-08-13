# DLL: Palindrome Checker ( ** Interview Question)
# Write a method to determine whether a given doubly linked list reads the same forwards and backwards.

# For example, if the list contains the values [1, 2, 3, 2, 1], then the method should return True, since the list is a palindrome.

# If the list contains the values [1, 2, 3, 4, 5], then the method should return False, since the list is not a palindrome.

# Method name:
# is_palindrome

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None


class DoublyLinkedList:
    def __init__(self, value):
        new_node = Node(value)
        self.head = new_node
        self.tail = new_node
        self.length = 1

    def print_list(self):
        temp = self.head
        while temp is not None:
            print(temp.value)
            temp = temp.next

    def append(self, value):
        new_node = Node(value)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
        self.length += 1
        return True

    def is_palindrome(self):
        result = True
        rightNode = self.tail
        leftNode = self.head
        for _ in range(self.length):
            if leftNode.value != rightNode.value:
                result = False
            leftNode = leftNode.next
            rightNode = rightNode.prev
        return result
    # WRITE IS_PALINDROME METHOD HERE #
    #                                 #
    #                                 #
    #                                 #
    #                                 #
    ###################################




my_dll_1 = DoublyLinkedList(1)
my_dll_1.append(2)
my_dll_1.append(3)
my_dll_1.append(2)
my_dll_1.append(1)

print('my_dll_1 is_palindrome:')
print( my_dll_1.is_palindrome() )


my_dll_2 = DoublyLinkedList(1)
my_dll_2.append(2)
my_dll_2.append(3)

print('\nmy_dll_2 is_palindrome:')
print( my_dll_2.is_palindrome() )



"""
    EXPECTED OUTPUT:
    ----------------
    my_dll_1 is_palindrome:
    True

    my_dll_2 is_palindrome:
    False

"""
