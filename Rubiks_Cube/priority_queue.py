class PQNode:
        def __init__(self, node, next=None):
            self.node = node
            self.next = next

class PriorityQueue:
    def __init__(self, list=[]):
        if len(list) == 0:
            self.head = PQNode(None)
        else:
            self.head = PQNode(list.pop())

        for node in list:
            self.append(node)

        self.size = len(list)
                

    def add(self, node):
        if self.size == 0 or node.score <= self.head.node.score:
            self.head = PQNode(node, self.head)
            self.size += 1
            return
        
        current = self.head
        while current.next.node != None:
            if node.score <= current.next.node.score:
                current.next = PQNode(node, current.next)
                self.size += 1
                return
            current = current.next

        current.next = PQNode(node, current.next)
        self.size += 1
        
    def pop(self):
        smallest = self.head
        self.head = self.head.next
        self.size -= 1
        return smallest.node
    
    def print(self):
        current = self.head
        while current.node != None:
            print(f"Node value: {current.node.score}")
            current = current.next
    
if __name__=="__main__":
    pq = PriorityQueue()
    pq.add(3)
    pq.add(5)
    pq.add(1)
    pq.print()
    print(pq.pop())