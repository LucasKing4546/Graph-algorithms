from graph import *
from pqdict import pqdict
import math
import time

def dijkstra(g: 'Graph', v1):
    # O((V + E) * log V)
    pq_pop_count = 0
    pq_push_count = 0

    visited = set()
    parent = {vertex: None for vertex in g.get_vertices()}
    distance = {vertex: float('inf') for vertex in g.get_vertices()}

    neighbours = g._Graph__outbound_neighbours

    if v1 not in g.get_vertices():
        raise ValueError("Vertex not in graph")

    distance[v1] = 0
    queue = pqdict({v1: 0})

    while queue:
        current_vertex = queue.pop()
        pq_pop_count += 1

        if current_vertex in visited:
            continue
        else:
            visited.add(current_vertex)

            for neighbour in neighbours[current_vertex]:

                new_distance = distance[current_vertex] + g.get_weight((current_vertex, neighbour))

                if neighbour not in visited and new_distance < distance[neighbour]:
                    queue[neighbour] = new_distance
                    pq_push_count += 1
                    parent[neighbour] = current_vertex
                    distance[neighbour] = new_distance

    return parent, distance, pq_push_count, pq_pop_count

def A_star(g : 'Graph', start, goal, filename):
    # Worst case: O((V + E) * log V)
    # Best case: O(E)
    pq_pop_count = 0
    pq_push_count = 0

    def heuristic(v):
        x1, y1 = g.get_coordinates(v, filename)
        x2, y2 = g.get_coordinates(goal, filename)
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    if start not in g.get_vertices() or goal not in g.get_vertices():
        raise ValueError("Start or goal vertex not in graph")

    g_score = {vertex: float('inf') for vertex in g.get_vertices()}
    g_score[start] = 0

    parent = {vertex: None for vertex in g.get_vertices()}

    queue = pqdict({start: heuristic(start)})

    neighbours = g._Graph__outbound_neighbours

    while queue:
        current = queue.pop()
        pq_pop_count += 1
        if current == goal:
            return parent, g_score, pq_push_count, pq_pop_count

        for neighbour in neighbours.get(current, []):
            new_distance = g_score[current] + g.get_weight((current, neighbour))
            if new_distance < g_score[neighbour]:
                parent[neighbour] = current
                g_score[neighbour] = new_distance
                f_score = new_distance + heuristic(neighbour)
                queue[neighbour] = f_score
                pq_push_count += 1

    return [], g_score, pq_push_count, pq_pop_count

def reconstruct_path(parent, goal):
    # O(V)
    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = parent[current]
    path.reverse()
    return path


def test_algorithms(graph_file, start, goal, coordinates_file):
    g = Graph.create_from_file(graph_file)
    print(g.return_edges())
    print(
        f"Loaded graph with {g.get_v()} vertices and {g.get_e()} edges."
    )

    g.reset_cost()

    start_time = time.perf_counter()
    parent_dij, distance_dij, pq_push, pq_pop = dijkstra(g, start)
    dij_time = (time.perf_counter() - start_time) * 1000  # in ms
    dij_cost = distance_dij.get(goal, float('inf'))
    dij_path = reconstruct_path(parent_dij, goal)
    dij_cost_calls = g.get_cost()

    g.reset_cost()

    start_time = time.perf_counter()
    parent_A_star, distance_A_star, A_pq_push, A_pq_pop = A_star(g, start, goal, coordinates_file)
    A_star_time = (time.perf_counter() - start_time) * 1000  # in ms
    A_star_cost = distance_A_star.get(goal, float('inf'))
    A_star_path = reconstruct_path(parent_A_star, goal)
    A_star_cost_calls = g.get_cost()

    # Print the outputs in the requested format.
    print(f"Minimum cost walk from {start} to {goal}:")
    print(f"Dijkstra: time: {dij_time:.2f}ms, cost: {dij_cost}, path: {', '.join(dij_path)}")
    print(f"A*: time: {A_star_time:.2f}ms, cost: {A_star_cost}, path: {', '.join(A_star_path)}")

    print("\nComparison:")
    print(f"            g.cost   PQ.push   PQ.pop")
    print(f"Dijkstra {dij_cost_calls:8} {pq_push:8} {pq_pop:8}")
    print(f"A*       {A_star_cost_calls:8} {A_pq_push:8} {A_pq_pop:8}")


if __name__ == '__main__':
    graph_file = "A3_v10000_e40000_positives_7.txt"
    start_vertex = input("Enter the start vertex: ")
    goal_vertex = input("Enter the goal vertex: ")
    coordinates_file = "A3_v10000_e40000_positives_7_vertex_positions.txt"

    test_algorithms(graph_file, start_vertex, goal_vertex, coordinates_file)