class NeighbourIterator:
    def __init__(self, graph, vertex):
        # Theta(1)
        self.__graph = graph
        self.__currentPositions = 0
        self.__vertex = vertex

    def valid(self):
        # Theta(1)
        return self.__currentPositions < self.__graph.size_of_outbound_neighbours(self.__vertex)

    def next(self):
        # Theta(1)
        if not self.valid():
            raise ValueError("No more neighbours")
        self.__currentPositions += 1

    def getCurrentPosition(self):
        # Theta(1)
        if not self.valid():
            raise ValueError("No more neighbours")
        return list(self.__graph._Graph__outbound_neighbours[self.__vertex])[self.__currentPositions]

class InboundNeighbourIterator:
    def __init__(self, graph, vertex):
        # Theta(1)
        self.__graph = graph
        self.__currentPositions = 0
        self.__vertex = vertex

    def valid(self):
        # Theta(1)
        return self.__currentPositions < self.__graph.size_of_inbound_neighbours(self.__vertex)

    def next(self):
        # Theta(1)
        if not self.valid():
            raise ValueError("No more neighbours")
        self.__currentPositions += 1

    def getCurrentPosition(self):
        # Theta(1)
        if not self.valid():
            raise ValueError("No more neighbours")
        return list(self.__graph._Graph__inbound_neighbours[self.__vertex])[self.__currentPositions]


class BFS:
    def __init__(self, graph, vertex):
        self.__neighbours = graph._Graph__outbound_neighbours
        self.__visited = set()
        self.__queue = [(vertex, 0)]
        self.__visited.add(vertex)
        self.__current_vertex = vertex

    def __iter__(self):
        return self

    def __next__(self):
        if not self.__queue:
            raise StopIteration
        self.__current_vertex = self.__queue.pop(0)
        for neighbour in self.__neighbours[self.__current_vertex[0]]:
            if neighbour not in self.__visited:
                self.__visited.add(neighbour)
                self.__queue.append((neighbour, self.__current_vertex[1] + 1))
        return self.__current_vertex

    def get_path_length(self):
        return self.__current_vertex[1]

class DFS:
    def __init__(self, graph, vertex):
        self.__neighbours = graph._Graph__outbound_neighbours
        self.__visited = set()
        self.__stack = [(vertex, 0)]
        self.__visited.add(vertex)
        self.__current_vertex = vertex

    def __iter__(self):
        return self

    def get_path_length(self):
        return self.__current_vertex[1]

    def __next__(self):
        if not self.__stack:
            raise StopIteration
        self.__current_vertex = self.__stack.pop()
        for neighbour in self.__neighbours[self.__current_vertex[0]]:
            if neighbour not in self.__visited:
                self.__visited.add(neighbour)
                self.__stack.append((neighbour , self.__current_vertex[1] + 1))
                #print("Stack:" + str(self.__stack))
                #print()
        return self.__current_vertex
