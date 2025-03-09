from collections import defaultdict


class Graph:
    def __init__(self):
        # Theta(1)
        self.__vertices = []
        self.__edges = []
        self.__inbound_neighbours = defaultdict(list)
        self.__outbound_neighbours = defaultdict(list)


    def add_vertex(self, vertex: int):
        # O(n)
        if vertex in self.__vertices:
            raise ValueError("Vertex already exists")
        else:
            self.__vertices.append(vertex)

    def add_edge(self, edge: tuple[int, int]):
        if edge[0] in self.__vertices and edge[1] in self.__vertices:
            self.__edges.append(edge)
            self.__inbound_neighbours[edge[1]].append(edge[0])
            self.__outbound_neighbours[edge[0]].append(edge[1])
        else:
            raise ValueError("Vertex {} is not in the graph".format(edge[0]))

    def remove_vertex(self, vertex: int):
        # O(v + e^2)
        if vertex in self.__vertices:
            self.__vertices.remove(vertex)
            if vertex in self.__inbound_neighbours.keys():
                self.__inbound_neighbours.pop(vertex)
            if vertex in self.__outbound_neighbours.keys():
                self.__outbound_neighbours.pop(vertex)
            for edge in self.__edges:
                if edge[0] == vertex or edge[1] == vertex:
                    self.__edges.remove(edge)
        else:
            raise ValueError("Vertex {} is not in the graph".format(vertex))

    def remove_edge(self, edge: tuple[int, int]):
        # O(e)
        if edge in self.__edges:
            if edge[1] in self.__inbound_neighbours.keys():
                self.__inbound_neighbours[edge[1]].remove(edge[0])
            if edge[0] in self.__outbound_neighbours.keys():
                self.__outbound_neighbours[edge[0]].remove(edge[1])
            self.__edges.remove(edge)
        else:
            raise ValueError("Edge {} is not in the graph".format(edge))

    def get_v(self):
        # Theta(1)
        return len(self.__vertices)

    def get_e(self):
        # Theta(1)
        return len(self.__edges)

    def is_edge(self, vertex1: int, vertex2: int):
        # O(e)
        if (vertex1, vertex2) in self.__edges:
            return True
        return False

    def neighbors(self, vertex: int):
        '''
        neighbors = []
        if index is None:
             neighbors= self.__outbound_neighbours[vertex][:]
        else:
            for i in range(index):
                neighbors.append(self.__outbound_neighbours[vertex][i])
        return neighbors
        '''
        return NeighbourIterator(self, vertex)

    def inbound_neighbours(self, vertex: int):
        '''
        neighbors = []
        if index is None:
            neighbors = self.__inbound_neighbours[vertex][:]
        else:
            for i in range(index):
                neighbors.append(self.__inbound_neighbours[vertex][i])
        return neighbors
        '''
        return InboundNeighbourIterator(self, vertex)

    def get_vertices(self):
        # Theta(1)
        return self.__vertices[:]

    def return_edges(self):
        # Theta(e)
        s = str()
        for edge in self.__edges:
            s += str(edge[0]) + ' ' + str(edge[1]) + '\n'
        return s

    def get_isolated_vertices(self):
        # Theta(v)
        s = str()
        for vertex in self.__vertices:
            if len(self.__inbound_neighbours[vertex]) == 0 and len(self.__outbound_neighbours[vertex]) == 0:
                s += str(vertex) + '\n'
        return s

    def size_of_outbound_neighbours(self, vertex):
        # Theta(1)
        return len(self.__outbound_neighbours[vertex])

    def size_of_inbound_neighbours(self, vertex):
        # Theta(1)
        return len(self.__inbound_neighbours[vertex])

    def __str__(self):
        return str(f"directed unweighted \n{self.return_edges()}{self.get_isolated_vertices()}\n")

class NeighbourIterator:
    def __init__(self, graph: Graph, vertex):
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
        return self.__graph._Graph__outbound_neighbours[self.__vertex][self.__currentPositions]

class InboundNeighbourIterator:
    def __init__(self, graph: Graph, vertex):
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
        return self.__graph._Graph__inbound_neighbours[self.__vertex][self.__currentPositions]

if __name__ == "__main__":
    g = Graph()
    for i in range(8):
        g.add_vertex(i+1)

    g.add_edge((1, 2))
    g.add_edge((2, 1))
    g.add_edge((3, 4))
    g.add_edge((4, 5))
    g.add_edge((5, 2))
    g.remove_vertex(6)
    g.remove_edge((2,1))
    print(g)
    try:
        print(g.get_vertices())
        print(g.get_v())
        print(g.get_e())
        print(g.is_edge(1, 2))
        print(g.is_edge(2, 1))
        i = g.neighbors(4)
        print(i.getCurrentPosition())
        j = g.inbound_neighbours(2)
        print(j.getCurrentPosition())
        j.next()
        print(j.getCurrentPosition())
    except Exception as e:
        print(e)



