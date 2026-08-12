"""
=============================================================================
 DLL INTERVIEW QUESTION: Swap Nodes in Pairs
=============================================================================

PROBLEM
-------
Implement the swap_pairs() method, which swaps every two ADJACENT nodes of
the doubly linked list by RELINKING the nodes (not by swapping values).

If the list has an odd number of nodes, the last node stays in place.

EXAMPLES
--------
    Input : 1 <-> 2 <-> 3 <-> 4
    Output: 2 <-> 1 <-> 4 <-> 3

    Input : 1 <-> 2 <-> 3 <-> 4 <-> 5
    Output: 2 <-> 1 <-> 4 <-> 3 <-> 5

CONSTRAINTS
-----------
    * Do not swap node values -- relink the nodes themselves.
    * Must handle: empty list, single node, odd number of nodes.
    * Both .next AND .prev pointers must be correct after the swap.

HINTS (try yourself first!)
---------------------------
    1. A dummy node before the head simplifies the edge cases.
    2. For each pair (first, second): rewire the links around them,
       connect the pair to the nodes before and after it.
    3. Don't forget to update self.head when you are done.

=============================================================================
"""


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

    # ------------------------------------------------------------------
    # YOUR TASK: implement this method, then run the file to test it.
    # ------------------------------------------------------------------
    def swap_pairs(self):
        raise NotImplementedError("swap_pairs() is not implemented yet")


# ===========================================================================
# TEST RUNNER -- no need to edit below. Just run this file to check yourself.
# ===========================================================================

def build_dll(values):
    """Build a DoublyLinkedList from a list of values."""
    dll = DoublyLinkedList(0)   # placeholder node, removed below
    dll.head = None
    dll.length = 0
    for value in values:
        dll.append(value)
    return dll


def forward_values(dll):
    """Collect values by walking .next pointers."""
    values = []
    node = dll.head
    while node is not None:
        values.append(node.value)
        node = node.next
    return values


def backward_values(dll):
    """Collect values by walking .prev pointers from the last node."""
    node = dll.head
    if node is None:
        return []
    while node.next is not None:
        node = node.next
    values = []
    while node is not None:
        values.append(node.value)
        node = node.prev
    return values


TEST_CASES = [
    ("even number of nodes", [1, 2, 3, 4],    [2, 1, 4, 3]),
    ("odd number of nodes",  [1, 2, 3, 4, 5], [2, 1, 4, 3, 5]),
    ("exactly two nodes",    [1, 2],          [2, 1]),
    ("single node",          [1],             [1]),
    ("empty list",           [],              []),
]


def run_tests():
    print("=" * 72)
    print(" TESTS: Swap Nodes in Pairs")
    print("=" * 72)
    passed = skipped = 0
    for i, (name, values, expected) in enumerate(TEST_CASES, start=1):
        dll = build_dll(values)
        try:
            dll.swap_pairs()
        except NotImplementedError:
            skipped += 1
            print(f"  [SKIP] Test {i}: {name} (not implemented yet)")
            continue
        forward = forward_values(dll)
        backward = backward_values(dll)
        if forward == expected and backward == expected[::-1]:
            passed += 1
            print(f"  [PASS] Test {i}: {name}")
        else:
            print(f"  [FAIL] Test {i}: {name}")
            print(f"         input:            {values}")
            print(f"         expected forward: {expected}")
            print(f"         actual forward:   {forward}")
            print(f"         actual backward:  {backward} (expected {expected[::-1]})")
    print("-" * 72)
    print(f"  Score: {passed}/{len(TEST_CASES)}")
    if skipped:
        print("  -> Implement swap_pairs() and run this file again.")
    elif passed == len(TEST_CASES):
        print("  -> ALL TESTS PASSED. Nice work!")
    print()


if __name__ == "__main__":
    run_tests()


# ---------------------------------------------------------------------------
# SANDBOX (optional): uncomment and play around manually.
# ---------------------------------------------------------------------------
# dll = build_dll([1, 2, 3, 4, 5])
# print("before:"); dll.print_list()
# dll.swap_pairs()
# print("after: "); dll.print_list()
