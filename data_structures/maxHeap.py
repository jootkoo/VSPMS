class maxHeap:
    def __init__(self):
        self.heap = []

    def __len__(self):
        return len(self.heap)
    def __repr__(self):
        return str(self.heap)

    def insert(self, key, value ):
        self.heap.append((key, value)) #append value to tree
        self.sift_up(len(self.heap)-1) #that value will then go up the tree where it needs to go, -1 since always last element

    def peek_max(self):
        if not self.heap:
            raise IndexError('Empty Heap')
        return self.heap[0]

    def extract_max(self):
        if not self.heap:
            raise IndexError('Empty Heap')
        
        max_element = self.heap[0] #grabs element
        last_element = self.heap.pop() #removes the element \ if w index need to delete
        if self.heap: #then needs to reorder
            self.heap[0] = last_element #grabs the last element in the list 
            self.sift_down(0) #sifts down to correct position 
        return max_element

    def heapify(self, elements): #takes the normal list of elements and rearranges them into the heap rules (max)
        self.heap = list(elements) #copies elements into heap

        for i in reversed(range(self._parent(len(self.heap)- 1) + 1)): #finds the last node that have children and works backwards to the root
            self.sift_down(i) 

    def _parent(self, index):
        return (index - 1) // 2 if index != 0 else None

    def _left(self, index):
        left = 2 * index + 1
        return left if left <len(self.heap) else None

    def _right(self, index):
        right = 2 * index + 2
        return right if right <len(self.heap) else None

    def sift_up(self,index): #swim
        parent_index = self._parent(index)
        while parent_index is not None and self.heap[index][0] > self.heap[parent_index][0]: #asks is the current items number larger than its parents number
            self.heap[index], self.heap[parent_index] = self.heap[parent_index], self.heap[index] #swap positions 
            index = parent_index #index moves up
            parent_index = self._parent(index) #finds new parent 

    def sift_down(self, index): #sink
        while True:
            largest = index

            left = self._left(index)
            right = self._right(index)

            if left is not None and self.heap[left][0] > self.heap[largest][0]:
                largest = left
            if right is not None and self.heap[right][0] > self.heap[largest][0]:
                largest = right
            
            if largest == index: #when in order 
                break

            self.heap[index], self.heap[largest] = self.heap[largest], self.heap[index] #swap
            index = largest
