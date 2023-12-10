import numpy as np
import sympy as sp
import networkx as nx
import matplotlib.pyplot as plt
import random as rd

# Function: random_configuration

def random_adjacency_matrix(dim, bonds):

    # Create a random adjacency matrix
    A = np.zeros((dim, dim))
    for i in range(bonds):
        # Randomly choose two different indices
        j = rd.randint(0, dim-1)
        k = rd.randint(0, dim-1)
        while k == j or A[j, k] == 1:
            k = rd.randint(0, dim-1)
        # Randomly choose a bond
        A[j, k] = 1
        A[k, j] = A[j, k]
    
    return A

def make_circle_matrix(dim):

    # Create a circle adjacency matrix

    A = np.zeros((dim, dim))
    for i in range(dim):
        A[i, (i + 1) % dim] = 1
        A[(i + 1) % dim, i] = 1

    return A



def make_graph(A):
    
        # Make a graph from an adjacency matrix

        G = nx.Graph()
        rows, cols = A.shape
        for i in range(rows):
            for j in range(cols):
                if A[i, j] == 1:
                    G.add_edge(i, j)
        
        plt.figure()
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True)

        return G

def calc_energy(A):

    A = sp.Matrix(A)

    energy = 0
    # eigenvalues = sorted(list(A.eigenvals().keys()))
    eigenvalues = A.eigenvals()
    ei_list = []

    for ei, deg in eigenvalues.items():
        ei_list.extend([ei] * deg)
    # make a list of eigenvalues taking note of degeneracy
    
    eigenvalues = sorted(ei_list)

    # print(seigenvalues))

    print(eigenvalues)
    dimension = int(np.round(len(eigenvalues) / 2 + 0.01, 0))
    
    for i in range(dimension):
        k = 2
        if i == dimension - 1:
            k = 1
        energy += float(eigenvalues[i] * k)

    return np.round(energy, 2)

def check_isomorphism(A, B):
        # Check if two graphs are isomorphic
        print("hello")
        return nx.is_isomorphic(A, B)

def generate_graphs(dim, bonds, number):
    # Generate a number of random graphs
    graphs = []
    for i in range(number):
        graphs.append(make_graph(random_adjacency_matrix(dim, bonds)))
    return graphs


def remove_isomorphic(graphs):
    # Remove isomorphic graphs
    unique_graphs = []
    for graph in graphs:
        isomorphic = False
        for unique_graph in unique_graphs:
            if check_isomorphism(graph, unique_graph):
                isomorphic = True
        if not isomorphic:
            unique_graphs.append(graph)
    return unique_graphs


# graphs = generate_graphs(5, 5, 25)
# unique_graphs = remove_isomorphic(graphs)

# for i, graph in enumerate(unique_graphs):
#     make_graph(nx.adjacency_matrix(graph).toarray())
#     plt.savefig('graph{}.png'.format(i))
    

