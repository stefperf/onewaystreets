# solving Riddler Classic @ https://fivethirtyeight.com/features/can-you-navigate-the-one-way-streets/


import itertools
from fractions import Fraction


def get_edges(n):
    """
    get the list of edges for a square grid graph of given side size
    :param n: side size as number of vertices
    :return: list of edges as tuples (vertex0, vertex1)
    """
    res = []
    # add horizontal edges
    for y in range(n):
        base = y * n
        for x in range(n - 1):
            res.append((base + x, base + x + 1))
    # add vertical edges
    for x in range(n):
        for y in range(n - 1):
            res.append((x + y * n, x + (y + 1) * n))
    return res


def build_directed_graph(n_vertices, directed_edges):
    """
    build a directed graph
    :param n_vertices: number of vertices
    :param directed_edges: list of tuples (vertex0, vertex1) representing directed edges
    :return: directed graph as a list of vertices reachable from each vertex
    """
    graph = [[] for _ in range(n_vertices)]
    for (v0, v1) in sorted(directed_edges):
        graph[v0].append(v1)
    return graph


def can_reach(directed_graph, v0, v1):
    """
    True iff vertex v1 can be reached from vertex v0
    :param directed_graph: list of vertices reachable from each vertex
    :param v0: start vertex
    :param v1: end vertex
    :return: boolean
    """
    reachable_vertices = set(directed_graph[v0])
    newly_added = reachable_vertices.copy()
    while True:
        if v1 in reachable_vertices:
            return True
        next_vertices = set()
        for v in newly_added:
            for w in directed_graph[v]:
                if w not in reachable_vertices:
                    reachable_vertices.add(w)
                    next_vertices.add(w)
        if not next_vertices:
            return False
        newly_added = next_vertices


def reach_prob(n):
    """
    calculate the probability that the bottom right corner can be reached from the top left corner
    in a square street grid where every connection between two crossroads is a one-way street in a random direction
    :param n: side of the square as number of nodes
    :return: probability as an exact fraction
    """
    n_vertices = n ** 2
    edges = get_edges(n)
    n_edges = len(edges)
    v0, v1 = 0, n_vertices - 1
    n_successes, n_graphs = 0, 0
    for directions in itertools.product((0, 1), repeat=n_edges):
        directed_edges = [(edge[direction], edge[(1 + direction) % 2]) for edge, direction in zip(edges, directions)]
        graph = build_directed_graph(n_vertices, directed_edges)
        success = can_reach(graph, v0, v1)
        if success:
            n_successes += 1
        n_graphs += 1
    return Fraction(n_successes, n_graphs)


for n_blocks in range(1, 4):
    n = n_blocks + 1
    print(f'With a square grid of {n_blocks} x {n_blocks} blocks, ' +
          f'there exists at least one path with probability {reach_prob(n)}.')
