from graph import *


def check_isomorphic(graph, target_graph):
    if set(graph.get_vertices()) != set(target_graph.get_vertices()):
        return False

    graph_edges = set()
    for edge in graph.get_edges():
        if not graph.is_edge(edge[0], edge[1]):
            continue
        graph_edges.add(tuple(sorted([edge[0], edge[1]])))

    target_edges = set()
    for edge in target_graph.get_edges():
        if not target_graph.is_edge(edge[0], edge[1]):
            continue
        target_edges.add(tuple(sorted([edge[0], edge[1]])))

    return graph_edges == target_edges


def get_degree_two_vertices(graph):
    result = []
    for vertex in graph.get_vertices():
        if graph.count_neighbours(vertex) == 2:
            result.append(vertex)
    return result


def get_neighbors_list(graph, vertex):
    neighbors = []
    iterator = graph.neighbors(vertex)
    while iterator.valid():
        neighbors.append(iterator.getCurrentPosition())
        iterator.next()
    return neighbors


def reducing(graph, target_graph):
    # First phase: Remove degree-2 vertices from source graph that aren't in target
    vertices_to_process = get_degree_two_vertices(graph)

    for vertex in vertices_to_process:
        if vertex not in target_graph.get_vertices():
            neighbors = get_neighbors_list(graph, vertex)

            if graph.count_neighbours(vertex) != 2:
                continue

            neighbor1, neighbor2 = neighbors

            if not graph.is_edge(neighbor1, neighbor2):
                graph.add_edge((neighbor1, neighbor2))
                graph.remove_vertex(vertex)
                print(f"Removed vertex {vertex}, added edge ({neighbor1}, {neighbor2})")

    # Second phase: Add degree-2 vertices from target graph that aren't in source
    target_vertices = get_degree_two_vertices(target_graph)

    for vertex in target_vertices:
        if vertex not in graph.get_vertices():
            neighbors = get_neighbors_list(target_graph, vertex)

            if len(neighbors) != 2:
                continue

            neighbor1, neighbor2 = neighbors

            if graph.is_edge(neighbor1, neighbor2):
                if (neighbor1, neighbor2) in graph.get_edges():
                    graph.remove_edge((neighbor1, neighbor2))
                else:
                    graph.remove_edge((neighbor2, neighbor1))

                graph.add_vertex(vertex)
                graph.add_edge((vertex, neighbor1))
                graph.add_edge((vertex, neighbor2))
                print(f"Added vertex {vertex} between {neighbor1} and {neighbor2}")


if __name__ == "__main__":
    graph_file = "A5_1.txt"
    target_file = "A5_2.txt"
    g = Graph.create_from_file(graph_file)
    target_graph = Graph.create_from_file(target_file)
    reducing(g, target_graph)
    if check_isomorphic(g, target_graph):
        print("The graphs are homeomorphic")
    else:
        print("The graphs are not homeomorphic")