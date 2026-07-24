class Mazesolver :
    def __init__(self,start:tuple[int,int], end:tuple[int,int],queue):
        self.start = start
        self.end = end 
        self.queue = []
        self.visited = set()
        self.parent = {}

    def solve(self,maze): 
        """ implemnt  a BFS algo 
        """
        self.queue = deque()
        self.queue.append(self.start)

        self.visited.add(self.start)
        
        
