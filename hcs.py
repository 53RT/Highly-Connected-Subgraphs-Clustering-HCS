import networkx as nx
import numpy as np

"""Python implementation of basic HCS

Implementation of Highly Connected Subgraphs (HCS) clustering which is introduced by "Hartuv, E., & Shamir, R. (2000).
 A clustering algorithm based on graph connectivity. Information processing letters, 76(4-6), 175-18"
 
Based on NetworkX and Numpy

Notation:
    G = Graph
    E = Edge
    V = Vertex
    
    |V| = Number of Vertices in G
    |E| = Number of Edges in G
"""


def create_example_graph():
    """Create example graph used in the paper

    :return: NetworkX Graph
    """

    v = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'X': 9, 'Y': 10, 'Z': 11}

    adjacency = np.zeros(shape=(12, 12), dtype=np.uint8)
    adjacency[v['A'], [v['B'], v['C'], v['D']]] = 1
    adjacency[v['B'], [v['A'], v['D'], v['E'], v['Y']]] = 1
    adjacency[v['C'], [v['A'], v['D'], v['E']]] = 1
    adjacency[v['D'], [v['A'], v['B'], v['C'], v['E']]] = 1
    adjacency[v['E'], [v['B'], v['C'], v['D'], v['F']]] = 1
    adjacency[v['F'], [v['E'], v['Y'], v['G'], v['I'], v['H']]] = 1
    adjacency[v['G'], [v['Z'], v['F'], v['I'], v['H']]] = 1
    adjacency[v['H'], [v['F'], v['G'], v['I']]] = 1
    adjacency[v['I'], [v['H'], v['F'], v['G']]] = 1
    adjacency[v['X'], [v['Y'], v['Z']]] = 1
    adjacency[v['Y'], [v['B'], v['X'], v['Z'], v['F']]] = 1
    adjacency[v['Z'], [v['X'], v['Y'], v['G']]] = 1

    return nx.from_numpy_matrix(adjacency)


def highly_connected(G, E):
    """Checks if the graph G is highly connected

    Highly connected means, that splitting the graph G into subgraphs needs more than 0.5*|V| edge deletions
    This definition can be found in Section 2 of the publication.

    :param G: Graph G
    :param E: Edges needed for splitting G
    :return: True if G is highly connected, otherwise False
    """

    return len(E) > len(G.nodes) / 2


def remove_edges(G, E):
    """Removes all edges E from G

    Iterates over all edges in E and removes them from G
    :param G: Graph to remove edges from
    :param E: One or multiple Edges
    :return: Graph with edges removed
    """

    for edge in E:
        G.remove_edge(*edge)
    return G


def HCS(G):
    """Basic HCS Algorithm

    cluster labels, removed edges are stored in global variables

    :param G: Input graph
    :return: Either the input Graph if it is highly connected, otherwise a Graph composed of
    Subgraphs that build clusters
    """

    E = nx.algorithms.connectivity.cuts.minimum_edge_cut(G)

    if not highly_connected(G, E):
        G = remove_edges(G, E)
        sub_graphs = list(nx.connected_component_subgraphs(G))

        if len(sub_graphs) == 2:
            H = HCS(sub_graphs[0])
            _H = HCS(sub_graphs[1])

            G = nx.compose(H, _H)

    return G


def labelled_HCS(G):
    """
    Runs basic HCS and returns Cluster Labels


    :param G: Input graph
    :return: List of cluster assignments for the single vertices
    """

    _G = HCS(G)
    sub_graphs = nx.connected_component_subgraphs(_G)

    labels = np.zeros(shape=(len(G)), dtype=np.uint16)

    for _class, _cluster in enumerate(sub_graphs, 1):
        c = list(_cluster.nodes)
        labels[c] = _class

    return labels


if __name__ == "__main__":
    labels = labelled_HCS(create_example_graph())
    print(labels)
