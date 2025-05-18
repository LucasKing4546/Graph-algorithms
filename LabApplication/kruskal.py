from graph import *
from collections import deque


# Average case: O(V + E)
def tree_height(tree, root):
    if not root:
        return 0

    queue = deque([(root, 1)])
    visited = {root}
    max_height = 1

    while queue:
        vertex, level = queue.popleft()
        max_height = max(max_height, level)

        neighbors = tree.neighbors(vertex) # using neighbour iterator
        while neighbors.valid():
            neighbor = neighbors.getCurrentPosition()
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, level + 1))
            neighbors.next()

    return max_height


# Average case: O(F/2)
def find_tree(forest, vertex):
    for tree in forest:
        if vertex in tree:
            return tree
    return None

# Average case: O(|set1| + |set2| + |forest|)
def make_union(set1, set2, forest):
    union = set1.union(set2)
    new_forest = {s for s in forest if s != set1 and s!= set2}
    new_forest.add(frozenset(union))
    return new_forest


# Average case: O(E log E + E * V)
def kruskal(g: Graph):
    t = Graph()
    sorted_edges = sorted(g.get_edges().items(), key=lambda x: (x[1], x[0]))
    forest = set()
    for vertex in g.get_vertices():
        t.add_vertex(vertex)
        component = set()
        component.add(vertex)
        forest.add(frozenset(component))

    i = 0

    while t.get_e() < g.get_v()-1:
        ((v1,v2), weight) = sorted_edges[i]
        tree_of_v1 = find_tree(forest, v1)
        tree_of_v2 = find_tree(forest, v2)
        if tree_of_v1 != tree_of_v2:
            t.add_edge((v1, v2), weight)
            forest = make_union(tree_of_v1, tree_of_v2, forest)
        i = i + 1
        if i > len(sorted_edges):
            raise Exception("g is disconnected")

    return t


if __name__ == "__main__":
    graph_file = "A4_1.txt"
    g = Graph.create_from_file(graph_file)
    t = kruskal(g)
    print(t)
    print("Tree height: ", tree_height(t, next(iter(t.get_edges()))[0]))