#fifo
# enqueue is placing the queue in the back, dequeue is when a items time to leave it is removed from the front 

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class Queue:
    def __init__(self):
        self.front = None
        self.rear = None
        self.size = 0 

    def __len__(self):
        return self.size

    def __repr__(self): #O(N)
        items = []
        current_item = self.front
        while current_item is not None:
            items.append(str(current_item.value))
            current_item = current_item.next

        return  ', '.join(items)

    def enqueue(self, value): #O(1)
        new_node = Node(value)
        if self.rear is None: #if the back is None, meaning the front is none too 
            self.front = self.rear = new_node #new node is both the front and the back since there is only one element 
        else:
            self.rear.next = new_node #point to new node
            self.rear = new_node #make the rear value the new node
        self.size +=1
    def dequeue(self): #O(1)
        if self.front is None:
            raise IndexError("Queue is Empty")
        dequeue_value = self.front.value #dequeue value is the front of the queue
        self.front = self.front.next #reset the value, the front value becomes the one behind it

        if self.front is None: #if theres no front theres no back 
            self.rear = None

        self.size -= 1 #removed element 

        return dequeue_value

    def enqueue_front(self, value): #place element in the front instead of back
        new_node = Node(value)
        if self.front is None:
            self.front = self.rear = new_node #sets the first element if doesnt exist
        else:
            new_node.next = self.front #sets new node
            self.front = new_node
        self.size += 1 #updates size

    def dequeue_rear(self): #dequeue back element
        if self.front is None:
            raise IndexError("Queue is empty") #there is nothing to get rid of in the back

        if self.front == self.rear: #if there is only one element, making the element fron and back
            removed_value = self.rear.value
            self.front = None
            self.rear = None
            self.size -= 1
            return removed_value

        current = self.front
        while current.next != self.rear: #move pointer to rear
            current = current.next
        removed_value = self.rear.value
        self.rear = current
        self.rear.next = None
        self.size -= 1

        return removed_value


    def peek_rear(self):
        if self.rear is None:
            raise IndexError("Queue is empty")

        return self.rear.value

    def peek(self):
        if self.front is None:
            raise IndexError("Queue is Empty")

        return self.front.value

    def is_empty(self):
        return self.front is None


