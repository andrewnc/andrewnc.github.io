# trees.py
import random
import numpy as np
import time
from matplotlib import pyplot as plt

class SinglyLinkedListNode(object):
    """Simple singly linked list node."""
    def __init__(self, data):
        self.value, self.next = data, None

class SinglyLinkedList(object):
    """A very simple singly linked list with a head and a tail."""
    def __init__(self):
        self.head, self.tail = None, None
    def __str__(self):
        go = True
        current = self.head
        li = []
        if self.head == None:
            return "[]"
        while go:
            li.append(current.value)
            if current is self.tail:
                go = False
            else:
                current = current.next
        return str(li)
    def append(self, data):
        """Add a Node containing 'data' to the end of the list."""
        n = SinglyLinkedListNode(data)
        if self.head is None:
            self.head, self.tail = n, n
        else:
            self.tail.next = n
            self.tail = n

def iterative_search(linkedlist, data):
    """Search 'linkedlist' iteratively for a node containing 'data'.
    If there is no such node in the list, or if the list is empty,
    raise a ValueError.

    Inputs:
        linkedlist (SinglyLinkedList): a linked list.
        data: the data to search for in the list.

    Returns:
        The node in 'linkedlist' containing 'data'.
    """
    current = linkedlist.head
    while current is not None:
        if current.value == data:
            return current
        current = current.next
    raise ValueError(str(data) + " is not in the list.")

def recursive_search(linkedlist, data):
    """Search 'linkedlist' recursively for a node containing 'data'.
    If there is no such node in the list, or if the list is empty,
    raise a ValueError.

    Inputs:
        linkedlist (SinglyLinkedList): a linked list object.
        data: the data to search for in the list.

    Returns:
        The node in 'linkedlist' containing 'data'.
    """
    if linkedlist.head is None:
        raise ValueError("cannot find value in empty list")
    def recursive(node, data):
        if node.value == data:
            return node
        else:
            if node.next is None:
                raise ValueError("value not found")
            else:
                return recursive(node.next, data)

    return recursive(linkedlist.head, data)



class BSTNode(object):
    """A Node class for Binary Search Trees. Contains some data, a
    reference to the parent node, and references to two child nodes.
    """
    def __init__(self, data):
        """Construct a new node and set the data attribute. The other
        attributes will be set when the node is added to a tree.
        """
        self.value = data
        self.prev = None        # A reference to this node's parent node.
        self.left = None        # self.left.value < self.value
        self.right = None       # self.value < self.right.value


class BST(object):
    """Binary Search Tree data structure class.
    The 'root' attribute references the first node in the tree.
    """
    def __init__(self):
        """Initialize the root attribute."""
        self.root = None

    def find(self, data):
        """Return the node containing 'data'. If there is no such node
        in the tree, or if the tree is empty, raise a ValueError.
        """

        # Define a recursive function to traverse the tree.
        def _step(current):
            """Recursively step through the tree until the node containing
            'data' is found. If there is no such node, raise a Value Error.
            """
            if current is None:                     # Base case 1: dead end.
                raise ValueError(str(data) + " is not in the tree.")
            if data == current.value:               # Base case 2: data found!
                return current
            if data < current.value:                # Step to the left.
                return _step(current.left)
            else:                                   # Step to the right.
                return _step(current.right)

        # Start the recursion on the root of the tree.
        return _step(self.root)

    def insert(self, data):
        """Insert a new node containing 'data' at the appropriate location.
        Do not allow for duplicates in the tree: if there is already a node
        containing 'data' in the tree, raise a ValueError.

        Example:
            >>> b = BST()       |   >>> b.insert(1)     |       (4)
            >>> b.insert(4)     |   >>> print(b)        |       / \
            >>> b.insert(3)     |   [4]                 |     (3) (6)
            >>> b.insert(6)     |   [3, 6]              |     /   / \
            >>> b.insert(5)     |   [1, 5, 7]           |   (1) (5) (7)
            >>> b.insert(7)     |   [8]                 |             \
            >>> b.insert(8)     |                       |             (8)
        """
        if self.root is None:
            self.root = BSTNode(data)
            return self.root
        current = self.root
        def _step(current):
            if current.value == data:
                raise ValueError("no duplicates allowed!")
            if data < current.value and current.left is not None:
                return _step(current.left)
            elif data < current.value and current.left is None:
                current.left = BSTNode(data)
                current.left.prev = current
                return current.left
            if data > current.value and current.right is not None:
                return _step(current.right)
            elif data > current.value and current.right is None:
                current.right = BSTNode(data)
                current.right.prev = current
                return current.right
        return _step(current)

    def find_and_remove_inorder_successor(self, target):
        """This fuction will find and remove the inorder successor and return the value"""

        def _step(current):
            if current.left is None:
                switch = current.value
                self.remove(current.value)
                return switch
            else:
                return _step(current.left)

        return _step(target.right)

    def remove(self, data):
        """Remove the node containing 'data'. Consider several cases:
            1. The tree is empty
            2. The target is the root:
                a. The root is a leaf node, hence the only node in the tree
                b. The root has one child
                c. The root has two children
            3. The target is not the root:
                a. The target is a leaf node
                b. The target has one child
                c. The target has two children
            If the tree is empty, or if there is no node containing 'data',
            raise a ValueError.

        Examples:
            >>> print(b)        |   >>> b.remove(1)     |   [5]
            [4]                 |   >>> b.remove(7)     |   [3, 8]
            [3, 6]              |   >>> b.remove(6)     |
            [1, 5, 7]           |   >>> b.remove(4)     |
            [8]                 |   >>> print(b)        |
        """

        


        target = self.find(data)

        if self.root is None:
            raise ValueError("Cannot remove from empty tree")

        # if the value to remove is the root
        if target == self.root:
            # if there are no children, remove the root
            if target.right is None and target.left is None:
                self.root = None
            # if there is one child, remove the root and reset the root to be the child
            if target.right is None and target.left is not None:
                self.root.left.prev = None
                self.root = self.root.left

            if target.right is not None and target.left is None:
                self.root.right.prev = None
                self.root = self.root.right

            if target.right is not None and target.left is not None:
                # find successor and set the successor as the root of the tree
                switch = self.find_and_remove_inorder_successor(target)
                target.value = switch
        else:
            # the target is a leaf node
            if target.right is None and target.left is None:
                
                if target.prev.left == target:
                    target.prev.left = None
                    target.prev = None

                elif target.prev.right == target:
                    target.prev.right = None
                    target.prev = None

            # the target has a left child
            if target.left is not None and target.right is None:
                if target.prev.left == target:
                    target.left.prev = target.prev
                    target.prev.left = target.left
                    target.prev = None
                    target.left = None

                elif target.prev.right == target:
                    target.left.prev = target.prev
                    target.prev.right = target.left
                    target.prev = None
                    target.left = None

            # the target has a right child
            if target.left is None and target.right is not None:
                if target.prev.left == target:
                    target.right.prev = target.prev
                    target.prev.left = target.right
                    target.right = None
                    target.prev = None

                elif target.prev.right == target:
                    target.right.prev = target.prev
                    target.prev.right = target.right
                    target.right = None
                    target.prev = None

            # target has two leaf nodes
            if target.left is not None and target.right is not None:
                switch = self.find_and_remove_inorder_successor(target)
                target.value = switch

                


            
    def __str__(self):
        """String representation: a hierarchical view of the BST.
        Do not modify this method, but use it often to test this class.
        (this method uses a depth-first search; can you explain how?)

        Example:  (3)
                  / \     '[3]          The nodes of the BST are printed out
                (2) (5)    [2, 5]       by depth levels. The edges and empty
                /   / \    [1, 4, 6]'   nodes are not printed.
              (1) (4) (6)
        """

        if self.root is None:
            return "[]"
        str_tree = [list() for i in xrange(_height(self.root) + 1)]
        visited = set()

        def _visit(current, depth):
            """Add the data contained in 'current' to its proper depth level
            list and mark as visited. Continue recusively until all nodes have
            been visited.
            """
            str_tree[depth].append(current.value)
            visited.add(current)
            if current.left and current.left not in visited:
                _visit(current.left, depth+1)
            if current.right and current.right not in visited:
                _visit(current.right, depth+1)

        _visit(self.root, 0)
        out = ""
        for level in str_tree:
            if level != list():
                out += str(level) + "\n"
            else:
                break
        return out


class AVL(BST):
    """AVL Binary Search Tree data structure class. Inherits from the BST
    class. Includes methods for rebalancing upon insertion.
    """
    def _checkBalance(self, n):
        return abs(_height(n.left) - _height(n.right)) >= 2

    def _rotateLeftLeft(self, n):
        temp = n.left
        n.left = temp.right
        if temp.right:
            temp.right.prev = n
        temp.right = n
        temp.prev = n.prev
        n.prev = temp
        if temp.prev:
            if temp.prev.value > temp.value:
                temp.prev.left = temp
            else:
                temp.prev.right = temp
        if n == self.root:
            self.root = temp
        return temp

    def _rotateRightRight(self, n):
        temp = n.right
        n.right = temp.left
        if temp.left:
            temp.left.prev = n
        temp.left = n
        temp.prev = n.prev
        n.prev = temp
        if temp.prev:
            if temp.prev.value > temp.value:
                temp.prev.left = temp
            else:
                temp.prev.right = temp
        if n == self.root:
            self.root = temp
        return temp

    def _rotateLeftRight(self, n):
        temp1 = n.left
        temp2 = temp1.right
        temp1.right = temp2.left
        if temp2.left:
            temp2.left.prev = temp1
        temp2.prev = n
        temp2.left = temp1
        temp1.prev = temp2
        n.left = temp2
        return self._rotateLeftLeft(n)

    def _rotateRightLeft(self, n):
        temp1 = n.right
        temp2 = temp1.left
        temp1.left = temp2.right
        if temp2.right:
            temp2.right.prev = temp1
        temp2.prev = n
        temp2.right = temp1
        temp1.prev = temp2
        n.right = temp2
        return self._rotateRightRight(n)

    def _rebalance(self,n):
        """Rebalance the subtree starting at the node 'n'."""
        if self._checkBalance(n):
            if _height(n.left) > _height(n.right):
                if _height(n.left.left) > _height(n.left.right):
                    n = self._rotateLeftLeft(n)
                else:
                    n = self._rotateLeftRight(n)
            else:
                if _height(n.right.right) > _height(n.right.left):
                    n = self._rotateRightRight(n)
                else:
                    n = self._rotateRightLeft(n)
        return n

    def insert(self, data):
        """Insert a node containing 'data' into the tree, then rebalance."""
        BST.insert(self, data)
        n = self.find(data)
        while n:
            n = self._rebalance(n)
            n = n.prev

    def remove(*args, **kwargs):
        """Disable remove() to keep the tree in balance."""
        raise NotImplementedError("remove() has been disabled for this class.")

def _height(current):
    """Calculate the height of a given node by descending recursively until
    there are no further child nodes. Return the number of children in the
    longest chain down.

    This is a helper function for the AVL class and BST.__str__().
    Abandon hope all ye who modify this function.

                                node | height
    Example:  (c)                  a | 0
              / \                  b | 1
            (b) (f)                c | 3
            /   / \                d | 1
          (a) (d) (g)              e | 0
                \                  f | 2
                (e)                g | 0
    """
    if current is None:
        return -1
    return 1 + max(_height(current.right), _height(current.left))


def compare_build_times():
    """Compare the build and search speeds of the SinglyLinkedList, BST, and
    AVL classes. For search times, use iterative_search(), BST.find(), and
    AVL.find() to search for 5 random elements in each structure. Plot the
    number of elements in the structure versus the build and search times.
    Use log scales if appropriate.
    """
    N = [100,500,1000,1500]
    file = open("english.txt", "r")
    words = []
    to_push = []
    to_search = []
    linked_list_creation_times = []
    BST_creation_times = []
    AVL_creation_times = []
    linked_list_search_times = []
    BST_search_times = []
    AVL_search_times = []

    for line in file:
        words.append(line.strip())
    file.close()

    for n in N:
        to_push = random.sample(words, n)

        s = SinglyLinkedList()
        b = BST()
        a = AVL()
        start = time.time()
        for word in to_push:
            s.append(word)
        linked_list_creation_times.append(time.time() - start)

        start = time.time()
        for word in to_push:
            b.insert(word)
        BST_creation_times.append(time.time()-start)

        start = time.time()
        for word in to_push:
            a.insert(word)
        AVL_creation_times.append(time.time()-start)

        to_search = random.sample(to_push, 5)

        start = time.time()
        for word in to_search:
            iterative_search(s,word)
        linked_list_search_times.append(time.time()-start)

        start = time.time()
        for word in to_search:
            b.find(word)
        BST_search_times.append(time.time()-start)

        start = time.time()
        for word in to_search:
            a.find(word)
        AVL_search_times.append(time.time()-start)

    plt.subplot(121)
    plt.loglog(N, linked_list_creation_times, lw=2, ms=15, label="linked-list")
    plt.loglog(N, BST_creation_times, lw=2, ms=15, label="BST")
    plt.loglog(N, AVL_creation_times, lw=2, ms=15, label="AVL")

    plt.title("Build times")
    plt.legend(loc = "upper left")

    plt.subplot(122)
    plt.loglog(N, linked_list_search_times, lw=2, ms=15, label="linked-list")
    plt.loglog(N, BST_search_times, lw=2, ms=15, label="BST")
    plt.loglog(N, AVL_search_times, lw=2, ms=15, label="AVL")

    plt.title("Search times")

    plt.show()



        






if __name__ == "__main__":
    b = BST()
    for i in [1,2,3,4,5,6]:
        b.insert(i)

    b.remove(1)
    print b




