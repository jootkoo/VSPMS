class Vehicle:
    def __init__(self, vin, make, model, year):
        self.vin = vin
        self.make = make
        self.model = model
        self.year = year

#linkedlist node
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.previous = None #doubly lined list

# Linked list: Maintain a repair workflow where steps can be inserted or removed
class dLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def __repr__(self):
        #this will display and print values within the node like a helper, stays the same as linkedlist
        if self.head is None:
            return "[]"
        else:
            last = self.head #points to head 
            return_string = f"[{last.value}"
            while last.next: #loop as long as there is a next value
                last = last.next #iterates
                return_string += f",[{last.value}]" #adds the value
            return_string += f"]" #closes bracket when done 
        return return_string #returns 
        
    def __contains__(self, value): #contains O(N) , stays the same as linked list 
        last = self.head #points to the head
        while last is not None: #checks if the value im looking for is not empty
            if last.value == value:
                return True
            last = last.next #go to the next element
        return False #if never found


    def __len__(self): 
        return self.size

    def insert(self, value, index): #if empty
        if index == 0:
            self.head =Node(value) #head takes the value
            self.tail = self.head #head and tail same value since one element (prepend func)
        else:
            if self.head is None:  #index doesnt exist
                raise ValueError("Index does not exist")
            else:
                last = self.head #temp pointer 

                for i in range(index-1): #goes to spot 1 spot before it wants to be inserted
                    if last.next is None: #if the pointer next to the head is empty
                        raise ValueError("Index does not exist")
                    last = last.next #pointer is changed from the head to the desired position (the insertion will happen in front of this element)
                new_node = Node(value) #value initalized
                new_node.next = last.next #takes the spot infront of the old head (inserted in between)
                if last.next is not None:
                    last.next.previous = new_node #lets previous value point at new node
                last.next = new_node #lets the value before the new value point to value that is inserted (the new node)
            self.size += 1
    def append(self, value):
        if self.head is None: #if list is empty
            self.head = Node(value) 
            self.tail = self.head
        else:
            last_node = Node(value)
            last_node.previous = self.tail #new val is set to the end node which was the tail
            self.tail.next = last_node #old tail points forward to new node
            self.tail = last_node #new node becomes the tail 
        self.size += 1
    def delete(self, value): #delete by value
        last = self.head #temporary pointer 
        if last is not None: #if not empty
            if last.value == value: #if value found 
                self.head = last.next #removes the head node by making the second node the new head
            else:
                while last.next: #loop to iterate through list
                    if last.next.value == value: #if the value of the next element is the value 
                        if last.next.next is not None: #if the space infront of the value that is trying to be deleted is not empty
                            last.next.next.previous = last #backpointer gets redirected as well, temp head pointer
                        last.next = last.next.next #value points to the next next value (ultimately removing the element by taking its pointer)
                        break
                    last = last.next #otherwise stay put point to next val 
        self.size -= 1

    def pop(self):
        if self.head is None:
            raise ValueError("Index out of bounds")
        else:
            last = self.head #pointer
            for i in range(index-1): #place before the position 
                if last.next is None: #next value is none, not enough elements 
                    raise ValueError("Index out of bounds")
                last = last.next 

            if last.next is None:
                raise ValueError("Index out of bounds")
            else:
                if last.next.next is not None:  
                    last.next.next.previous = last #previous pointer is changed as well
                last.next = last.next.next #points to the value ahead
        self.size -= 1
if __name__ == '__main__':
    repairWorkflowLog = dLinkedList()

    vehicle1 = Vehicle(
        "1FTFW1E50MFA12345",
        "Ford",
        "F-150",
        2021
    )

    def repairWorkflow():
        log = []
        print("REPAIR WORKFLOW")
        month = int(input("Enter month :"))
        if (month > 12) or (month < 1):
            month = int(input("Invalid input, Please input valid month :"))
        log.append(month)
        day = int(input("Enter day :"))
        if (day > 31) or (day< 1):
            day = int(input("Invalid input, Please input valid day :"))
        log.append(day)
        year = int(input("Enter year :"))
        if (year < 1):
            year = int(input("Invalid input, Please input valid year :"))
        log.append(year)
        repair = str(input("Enter in repair to be logged :"))
        log.append(repair)
        return log




    current_log = repairWorkflow()
    repairWorkflowLog.append(current_log)

    print(repairWorkflowLog)



    print(vehicle1.model)
