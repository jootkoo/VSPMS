#key value pairs
#avg o(1) worst case (collisions) o(n)
class HashMap:
    def __init__(self, capacity):
        self.capacity = capacity
        self.size =  0
        self.buckets = [[] for _ in range(capacity)] # the buckets is lists x amount of capacity

    def __len__(self):
        return self.size

    def __contains__(self, key):
        index = self._hash_function(key) #the index is the broken down number from the hash func with the true key value as its peramter (this is the location of where it can be)
        buckets = self.buckets[index] #then that index is the paremeter for the bucket
         
        for k, v in buckets: #looks through the buckets for the correct key in the within the corresponding index
            if k == key: #compares the buckets within the index then compares the original key, this is needed because 2 keys can have the same index 
                return True
        return False
    
    def put(self, key, value): #operation that inpfuts a new key and value
        index = self._hash_function(key) 
        buckets = self.buckets[index]

        for i, (k,v) in enumerate(buckets): #if element not in bucket update it if not create it
            if k == key:
                buckets[i] = (k, v) #item is updated if key exists
                break
        else:
            buckets.append((key, value)) #this else statement is only accessed if we leave if statement w/o breaking
            self.size += 1 #update size



    def get(self, key): #same as contains func
        index = self._hash_function(key) 
        buckets = self.buckets[index] 
         
        for k, v in buckets: 
            if k == key: 
                return v 
        raise KeyError('Key not Found')

    def remove(self, key): #same as get but delete item if found
        index = self._hash_function(key) 
        buckets = self.buckets[index] 
         
        for i, (k, v) in enumerate(buckets): #i so we can pick which bucket we want to delete
            if k == key: 
                del buckets[i]
                self.size -= 1
                break
        else:
            raise KeyError('Key not Found')

    def keys(self):
        return [k for bucket in self.buckets for k, _ in bucket] #goes through all the buckets retrieves key value pairs to give all keys 

    def values(self):
        return [v for bucket in self.buckets for _, v in bucket] #same idea but values

    def items(self):
        return [(k,v) for bucket in self.buckets for k, v in bucket] #returns both

    #linear on key length
    def _hash_function(self, key): #helper funciton within the class (private cause of the _ in the front) to place position 
        # So what this funciton does is that it breaks down the key into a number so it can be placed accordingly (numerically based on its end value)
        # differnt letter combos can result as the same index giving multiple keys the same index
        key_string = str(key) #this converts the key into a string so the fucntion can process each character
        hash_result = 0 # This stores the hash value in which it gets broken down with the ascii 

        for c in key_string: #for every character in the key string the hash result is the result * 31 + the ascii code of the char 
            #the * 31 allows each value to be distinct other wise "ab" and "ba" could be the same 
            hash_result = (hash_result * 31 + ord(c)) % self.capacity # then modulo by self capacity so we dont ever get the capacity or larger, always a number between capacity, 0 and capacity -1
            # Modulo % gives you the remainder after division.
        return hash_result
