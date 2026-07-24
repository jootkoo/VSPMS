
#nodes represented in a adjacentcy list
class Graph:
    def __init__(self, directed=False):
        self.directed = directed
        self.adj_list = dict()

    def __repr__(self):
        graph_srt = ""
        for node, neighbors in self.adj_list.items(): #illustrates each nodes neighbors
            graph_srt += f"{node} -> {neighbors}\n"
        return graph_srt

    def add_node(self, node):
        if node not in self.adj_list:
            self.adj_list[node] = set() #create 'node' if not exist
        else:
            raise ValueError("Node exists already")

    def remove_node(self, node):
        if node not in self.adj_list:
            raise ValueError("Node does not exist")

        for neighbors in self.adj_list.values(): #for every set of neighbors if this node occurs there remove it
            neighbors.discard(node)
        del self.adj_list[node]


    def add_edge(self, from_node, to_node, weight = None):
        if from_node not in self.adj_list: #allow edges be created for nodes that dont exist yet 
            self.add_node(from_node)

        if to_node not in self.adj_list: #allow edges be created for nodes that dont exist yet 
            self.add_node(to_node)

        if weight is None: 
            self.adj_list[from_node].add(to_node) #if a directed graph , for weighted graph you append the weight too
            if not self.directed:
                self.adj_list[to_node].add(from_node)
        else:
            self.adj_list[from_node].add((to_node, weight)) #weighted
            if not self.directed:
                self.adj_list[to_node].add((from_node, weight))




    def remove_edge(self, from_node, to_node):
        if from_node in self.adj_list:
            if to_node in self.adj_list[from_node]:
                self.adj_list[from_node].remove(to_node)
            else:
                raise ValueError('Edge does not exist')

            if not self.directed: #if remove an edge need to remove both entrys unless directed graph
                if from_node in self.adj_list[to_node]:
                    self.adj_list[to_node].remove(from_node)
        else:
            raise ValueError('Edge does not exist')

    def get_neighbors(self, node):
        return self.adj_list.get(node, set()) #empty set by default if not exist

    def has_node(self, node):
        return node in self.adj_list

    def has_edge(self, from_node, to_node):
        if from_node in self.adj_list:
            return to_node in self.adj_list[from_node]
        return False

    def get_nodes(self):
        return list(self.adj_list.keys())

    def get_edges(self):
        edges = []
        for from_node, neighbors in self.adj_list.items():
            for to_node in neighbors:
                edges.append(from_node, to_node)

    def bfs(self, start): #breadth first search 
        visited = set()
        queue = [start]
        order = []

        while queue: #while elements still in queue, get next element to be proccessed in FIFO way
            node = queue.pop(0) #get ffirst element
            if node not in visited: #if not already proccessed
                visited.add(node) #add to visisted
                order.append(node)
                neighbors = self.get_neighbors(node) #get neighbors
                for neighbor in neighbors:
                    if isinstance(neighbor, tuple): #this means if weighted connection 
                        neighbor = neighbor[0]
                    if neighbor not in visited:
                        queue.append(neighbor)
        return order


    def dfs(self, start): #depth first search (stack)
        visited = set()
        stack = [start]
        order = []

        while stack: #while elements still in queue, get next element to be proccessed in FIFO way
            node = stack.pop() #last element 
            if node not in visited: #if not already proccessed
                visited.add(node) #add to visisted
                order.append(node)
                neighbors = self.get_neighbors(node) #get neighbors
                for neighbor in sorted(neighbors, reverse=True):
                    if isinstance(neighbor, tuple): #this means if weighted connection 
                        neighbor = neighbor[0]
                    if neighbor not in visited:
                        stack.append(neighbor)
        return order

