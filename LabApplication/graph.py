from collections import defaultdict
from iterators import NeighbourIterator, InboundNeighbourIterator, BFS, DFS

class Graph:
    def __init__(self):
        # Theta(1)
        self.__vertices = []
        self.__edges = {}
        self.__directed = False
        self.__weighted = True
        self.__inbound_neighbours = defaultdict(set)
        self.__outbound_neighbours = defaultdict(set)
        self.__cost = 0
    def change_if_directed(self):
         # O(V + E)
        self.__directed = not self.__directed
        if not self.__directed:
            for vertex in self.__vertices:
                # Making the set of neighbours of each vertex identical in the double list of neighbours
                set_of_neighbours = self.__inbound_neighbours[vertex].union(self.__outbound_neighbours[vertex])

                self.__inbound_neighbours[vertex] = set_of_neighbours
                self.__outbound_neighbours[vertex] = set_of_neighbours

            # No duplicate edges in undirected graphs
            seen = set()
            for edge in list(self.__edges.keys()):
                normalized = tuple(sorted(edge))
                if normalized in seen:
                    del self.__edges[edge]
                else:
                    seen.add(normalized)
        else:
            # Adding the opposite edges when changing the graph to directed
            for edge in list(self.__edges.keys()):
                opposite_edge = (edge[1], edge[0])
                if opposite_edge not in self.__edges.keys():
                    self.__edges[opposite_edge] = self.__edges[edge]

    def change_if_weighted(self):
        # Theta(E)
        self.__weighted = not self.__weighted
        if not self.__weighted:
            for edge in self.__edges.keys():
                self.__edges[edge] = 1
        else:
            for edge in self.__edges.keys():
                self.__edges[edge] = 0

    def add_vertex(self, vertex: str):
        # O(v)
        if vertex in self.__vertices:
            raise ValueError("Vertex already exists")
        else:
            self.__vertices.append(vertex)

    def set_weight(self, edge, weight: int):
        # Theta(1)
        if not self.__weighted:
            raise ValueError("Graph is unweighted")
        if not edge in self.__edges:
            raise ValueError("Edge {} does not exist".format(edge))
        self.__edges[edge] = weight

    def get_edge(self, edge):
        if edge in self.__edges.keys():
            return edge
        elif (edge[1], edge[0]) in self.__edges.keys():
            return (edge[1], edge[0])
        raise ValueError("Edge {} does not exist".format(edge))

    def get_weight(self, edge):
        # Theta(1)
        if not self.__weighted:
            raise ValueError("Graph is unweighted")
        if not self.is_edge(edge[0], edge[1]):
            raise ValueError("Edge {} does not exist".format(edge))
        self.__cost += 1
        return self.__edges[self.get_edge(edge)]

    def get_cost(self):
        return self.__cost

    def reset_cost(self):
        self.__cost = 0

    def add_edge(self, edge, weight: int|None = None):
        # Theta(v)
        if edge in self.__edges.keys():
            raise ValueError("Edge already exists")

        if edge[0] in self.__vertices and edge[1] in self.__vertices:
            if not self.__directed:
                # In undirected graph, check for the opposite edge.
                opposite_edge = (edge[1], edge[0])

                if opposite_edge in self.__edges.keys():
                    raise ValueError("Edge already exists")

                self.__inbound_neighbours[edge[0]].add(edge[1])
                self.__outbound_neighbours[edge[1]].add(edge[0])

            # Add the edge.
            if weight is not None:
                self.__edges[edge] = weight
            else:
                self.__edges[edge] = 1
            # Update neighbours.
            self.__inbound_neighbours[edge[1]].add(edge[0])
            self.__outbound_neighbours[edge[0]].add(edge[1])
        else:
            raise ValueError("Vertices {} are not in the graph".format(edge))

    def remove_vertex(self, vertex: str):
        # O(v + e)
        if vertex in self.__vertices:
            self.__vertices.remove(vertex)
            if vertex in self.__inbound_neighbours.keys():
                for neighbour in self.__inbound_neighbours[vertex]:
                    self.__inbound_neighbours[neighbour].remove(vertex)
                self.__inbound_neighbours.pop(vertex)
            if vertex in self.__outbound_neighbours.keys():
                for neighbour in self.__outbound_neighbours[vertex]:
                    self.__outbound_neighbours[neighbour].remove(vertex)
                self.__outbound_neighbours.pop(vertex)

            # Create a list of edges to remove
            edges_to_remove = [edge for edge in self.__edges.keys()
                               if edge[0] == vertex or edge[1] == vertex]

            # Remove edges from the list
            for edge in edges_to_remove:
                self.__edges.pop(edge)
        else:
            raise ValueError("Vertex {} is not in the graph".format(vertex))

    def remove_edge(self, edge):
        # O(1)
        if edge in self.__edges.keys():
            self.__inbound_neighbours[edge[1]].discard(edge[0])
            self.__outbound_neighbours[edge[0]].discard(edge[1])
            if not self.__directed:
                self.__inbound_neighbours[edge[0]].discard(edge[1])
                self.__outbound_neighbours[edge[1]].discard(edge[0])
            self.__edges.pop(edge)
        else:
            raise ValueError("Edge {} is not in the graph".format(edge))

    def get_v(self):
        # Theta(1)
        return len(self.__vertices)

    def get_e(self):
        # Theta(1)
        return len(self.__edges)

    def is_edge(self, vertex1: str, vertex2: str):
        # O(e)
        if self.__directed is False:
            if (vertex1, vertex2) in self.__edges.keys() or (vertex2, vertex1) in self.__edges.keys():
                return True
        else:
            if (vertex1, vertex2) in self.__edges :
                return True
        return False

    def neighbors(self, vertex: str):
        return NeighbourIterator(self, vertex)

    def inbound_neighbours(self, vertex: str):
        return InboundNeighbourIterator(self, vertex)

    def BFS_iter(self, vertex):
        return BFS(self, vertex)

    def DFS_iter(self, vertex):
        return DFS(self, vertex)

    def get_vertices(self):
        # Theta(1)
        return self.__vertices[:]

    def get_edges(self):
        return self.__edges.copy()

    def return_edges(self):
        # Theta(e)
        s = str()
        for edge in self.__edges:
            s += str(edge[0]) + ' ' + str(edge[1]) + ' ' + str(self.__edges[edge]) + '\n'
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

    def directed(self):
        if self.__directed:
            return "directed"
        return "undirected"

    def weighted(self):
        if self.__weighted:
            return "weighted"
        return "unweighted"

    def get_coordinates(self, vertex, filename):
        with open(filename, 'r') as f:
            lines = f.readlines()
        if not lines:
            raise ValueError("File is empty or improperly formatted.")
        for line in lines[1:]:
            parts = line.split(",")
            if parts[0] == vertex:
                return float(parts[1]), float(parts[2])
        raise ValueError("Vertex {} not found in file".format(vertex))

    def count_neighbours(self, vertex):
        return len(self.__outbound_neighbours[vertex])


    def __str__(self):
        return str(f"{self.directed()} {self.weighted()} \n{self.return_edges()}{self.get_isolated_vertices()}\n")

    @classmethod
    def create_from_file(cls, filename):
        with open(filename, 'r') as f:
            lines = f.readlines()
        if not lines:
            raise ValueError("File is empty or improperly formatted.")

        header = lines[0].split()
        if len(header) != 2:
            raise ValueError("File is improperly formatted.")
        directed = True if header[1] == "directed" else False
        weighted = True if header[0] == "weighted" else False

        graph = cls()
        graph.__directed = directed
        graph.__weighted = weighted

        for line in lines[1:]:
            parts = line.split()
            if len(parts) == 1:
                graph.add_vertex(parts[0])
            elif len(parts) == 2 and weighted is False :
                v1, v2 = parts
                if v1 not in graph.get_vertices():
                    graph.add_vertex(v1)
                if v2 not in graph.get_vertices():
                    graph.add_vertex(v2)
                graph.add_edge((parts[0], parts[1]))
            elif len(parts) == 3 and weighted is True:
                v1, v2, weight_str = parts
                try:
                    weight = int(weight_str)
                except ValueError:
                    raise ValueError(f"Invalid weight '{weight_str}' for edge ({v1}, {v2}).")
                # Add vertices if not present.
                if v1 not in graph.get_vertices():
                    graph.add_vertex(v1)
                if v2 not in graph.get_vertices():
                    graph.add_vertex(v2)
                graph.add_edge((v1, v2), weight)
            else:
                raise ValueError("File is improperly formatted.")
        return graph