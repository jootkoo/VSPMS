#stack

#lifo push pop peek (constnat time besides printing content)

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class Stack:
    def __init__(self):
        self.top = None
        self.size = 0 
    
    def __len__(self): #constant O(1)
        return self.size
    def __repr__(self):
        items = [] #create list
        current_item = self.top  #the current item is the top of the stack 

        while current_item is not None: #iterate through the stack 
            items.append(str(current_item.value)) #append each item to the list
            current_item = current_item.next
        return ', '.join(items)

    def push(self, value): #constant  
        new_node = Node(value) #set value
        new_node.next = self.top #new node pointer set to the top
        self.top = new_node #top is the new node

        self.size +=1 

    def pop(self):
        if self.top is None: #when the value you are trying to pop that is not there
            raise ValueError("Stack is empty")

        pop_value = self.top.value #pop value is the top value on the stack 
        self.top = self.top.next #the top value moves to the next value which is the value under it 

        self.size -=1  #size decreases
        return pop_value #return pop value 
    def peek(self):
        if self.top is None:
            raise ValueError("Stack is Empty")
        return self.top.value 

    def is_empty(self):
        return self.top is None