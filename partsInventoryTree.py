#O(H) run time complexity (h is height of tree), O(logn)
#depends on how well you organize
class Node:
    def __init__(self, key):
        self.left = None
        self.right = None #child nodes
        self.parent = None 
        self.key = key
        self.value = None

    def __repr__(self):
        return f"({self.key}, {self.value})"

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def __contains__(self, key):
        current_node = self.root

        while current_node is not None:
            if key < current_node.key:
                current_node = current_node.left
            elif key > current_node.key:
                current_node = current_node.right
            else:
                return True # element contains
        return False
    def __iter__(self):
        yield from self._in_order_traversal(self.root)

    def __repr__(self):
        return str(list(self._in_order_traversal(self.root)))

    def insert(self, key, value):
        if self.root is None:
            self.root = Node(key) #if empty value 
            self.root.value = value
        else:
            current_node = self.root #
            while True: #iterate
                if key < current_node.key: #if key is less than node
                    if current_node.left is None: #place the node at the position to the left if space is empty
                        current_node.left = Node(key)
                        current_node.left.value = value
                        current_node.left.parent = current_node #create new parent 
                        break
                    else: #otherwise if theres already a node there move to the left
                        current_node = current_node.left
                elif key > current_node.key: #if key is greater than node
                    if current_node.right is None: #place the node at the position to the left if space is empty
                        current_node.right = Node(key)
                        current_node.right.value = value
                        current_node.right.parent = current_node #create new parent 
                        break
                    else: #otherwise move to the right
                        current_node = current_node.right
                else: #key is found, update value 
                    current_node.value = value
                    break
    def search(self, key):
        current_node = self.root #start from root
        while True: #iterating but returns when found key or ended up at none
            if current_node is None or current_node.key == key:
                return current_node
            elif key < current_node.key:
                if current_node.left is None:
                    return None
                else:
                    current_node = current_node.left

            else: #if key is larger than current node
                if current_node.right is None:
                    return None
                else:
                    current_node = current_node.right


    def delete(self, key):
        node = self.search(key)

        if node is None:
            raise KeyError('Node with this key does not exist')
        self._delete(node)


    def traverse(self, order):
        if order == 'inorder':
            yield from self._in_order_traversal(self.root) #start from the root
        elif order == 'preorder':
            yield from self._pre_order_traversal(self.root) #start from the root
        elif order == 'postorder':
            yield from self._post_order_traversal(self.root) #start from the root
        else:
            raise ValueError("Unknown error")


    def _delete(self, node):
        #node is leaf node
        if node.left is None and node.right is None: #checks if leaf
            if node.parent is None: 
                self.root = None
            else: #find out if parent's right child or left child 
                if node.parent.right == node:  #if parents right child
                    node.parent.right = None  #delete node
                else:
                    node.parent.left = None #if left
                node.parent = None  #remove reference to parent 

        #node has exactly one child node
        elif node.left is None or node.right is None: 
            child_node = node.left if node.left is not None else node.right #child node picked based on which one is filled

            if node.parent is None: #checks if root node since root doesnt have parent 
                child_node.parent = None #if root is deleted the child points to nothing 
                self.root = child_node #child becomes the root
            else:
                if node.parent.right == node: #if parent node on the right is the element being removed
                    node.parent.right = child_node #child takes its position
                else:
                    node.parent.left = child_node
                child_node.parent = node.parent #child node becomes the parent now
            node.parent = node.left = node.right = None #node is removed

        #node has two child nodes
        else:
            successor = self._successor(node) #use sucessor helper to find replacement

            node.key = successor.key #new node values come from successor
            node.value = successor.value

            self._delete(successor)


    def _successor(self, node): #second largest value to fill posiiton 
        if node is None:
            raise ValueError('Cannot find Successor of None')
        if node.right is None:
            return None
        else:
            current_node = node.right #right is the bigger element
            while current_node.left is not None: #while loop iterates down the tree until it reaches the end to find successor
                current_node = current_node.left
            return current_node

    def _predecessor(self, node): #same as sucessor but left to right
        if node is None:
            raise ValueError('Cannot find Predecessor of None')
        if node.left is None:
            return None
        else:
            current_node = node.left
            while current_node.right is not None:
                current_node = current_node.right
            return current_node
    #generate
    #yield produces one result from the function without ending the function permanently 
    def _in_order_traversal(self,node): #left parent then right 
        if node is not None: 
            yield from self._in_order_traversal(node.left) #left all the way to the bottom
            yield (node.key, node.value) 
            yield from self._in_order_traversal(node.right)

    def _pre_order_traversal(self, node): #root first left then right 
        if node is not None:
            yield (node.key, node.value)  
            yield from self._pre_order_traversal(node.left) #left
            yield from self._pre_order_traversal(node.right) #right
    def _post_order_traversal(self, node): #left right then parent then root at the end
        if node is not None:
            yield from self._post_order_traversal(node.left) 
            yield from self._post_order_traversal(node.right)
            yield (node.key, node.value)  

