import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import itertools
import random as rd
import math

# We make it generate a bunch of random matrices instead.

def generate_symmetric_matrices(n, num_ones, amount):
    upper_triangle_indices = [(i, j) for i in range(n) for j in range(i+1, n)]
    total_combinations = math.comb(len(upper_triangle_indices), num_ones)

    selected_indices = set()
    while len(selected_indices) < amount:
        selected_indices.add(rd.randint(0, total_combinations - 1))

    matrices = []
    for index in selected_indices:
        combo = get_combination(upper_triangle_indices, num_ones, index)
        matrix = np.zeros((n, n), dtype=int)
        for i, j in combo:
            matrix[i][j] = 1
            matrix[j][i] = 1
        if not np.any(np.all(matrix == 0, axis=0)):
            matrices.append(matrix)

    return matrices

def get_combination(iterable, r, index):
    """
    Generate the `index`-th combination of `iterable` of size `r`.
    """
    pool = tuple(iterable)
    n = len(pool)
    if r < 0 or r > n:
        raise ValueError("Invalid combination size")

    c = math.comb(n, r)
    if index < 0 or index >= c:
        raise IndexError("Combination index out of range")

    result = []
    for i in range(r, 0, -1):
        c, n, r = math.comb(n - 1, i - 1), n - 1, i - 1
        while index >= c:
            index -= c
            c, n = math.comb(n - 1, r), n - 1

        result.append(pool[-n-1])

    return result

def eigenvalues(mat):
    eigenvalues = np.linalg.eigvals(mat)
    return np.sort(eigenvalues)

def Energy(matrix):
    ei_list = eigenvalues(matrix)
    half_len = len(ei_list) // 2
    energy = 2 * np.sum(ei_list[:half_len])
    
    # If there's an odd number of eigenvalues, add the middle one once
    if len(ei_list) % 2 != 0:
        energy += ei_list[half_len]
    
    return energy

def lowest_energy(matrices):
    lowest_energy = float('inf')
    lowest_matrix = None
    for matrix in matrices:
        energy = Energy(matrix)
        if energy < lowest_energy:
            lowest_energy = energy
            lowest_matrix = matrix
    return lowest_matrix, lowest_energy

def highest_energy(matrices):
    highest_energy = -100
    highest_matrix = None
    for matrix in matrices:
        energy = Energy(matrix)
        if energy > highest_energy:
            highest_energy = energy
            highest_matrix = matrix
    return highest_matrix, highest_energy


def draw_graph(adj_matrix, energy, ax):
    G = nx.Graph()
    n = len(adj_matrix)

    # Add nodes
    for i in range(n):
        G.add_node(i)

    # Add edges based on the adjacency matrix
    for i in range(n):
        for j in range(i+1, n):
            if adj_matrix[i][j] == 1:
                G.add_edge(i, j)

    # Use a layout algorithm to position the nodes
    pos = nx.kamada_kawai_layout(G)  # Fruchterman-Reingold algorithm

    # Draw the graph
    nx.draw(G, pos, ax=ax, node_color='gold', node_size=300, edge_color='black', with_labels=False)

    # Draw custom node circles using plt.Circle
    for node, (x, y) in pos.items():
        circle = plt.Circle((x, y), 0.1, color='gold', zorder=2)
        ax.add_artist(circle)
    
    ax.set_title(f'Energy: {energy:.2f}', fontsize=16)
    ax.set_axis_off()  # Turn off the axis


def amount_to_sample(n, k):
    return math.comb(n*(n-1)//2, k) / 10


for j in range(18, 19):
    fig, ax = plt.subplots(1, 1)
    ax.set_aspect('equal')

    k = amount_to_sample(10, j)
    if k > 100000:
        k = 100000

    print(k)

    # print(k)
    
    matrices = generate_symmetric_matrices(10, j, k)
    
    print("matrices made")

    low_matrix, low_energy = lowest_energy(matrices)
    high_matrix, high_energy = highest_energy(matrices)
    draw_graph(low_matrix, low_energy, ax)
    # draw_graph(high_matrix, high_energy, ax[1])
    fig.suptitle("n_atoms = 8, n_bindings = " + str(j))
    # ("n_atoms = 7, n_bindings = " + str(j))
    fig.savefig("BestConfigurations/10_" + str(j) + ".png")

# matrices = generate_symmetric_matrices(7, 10, 1000)
# lowest_matrix, lowest_energy = lowest_energy(matrices)
# highest_matrix, highest_energy = highest_energy(matrices)

# draw_graph(lowest_matrix, lowest_energy, ax[0])
# print(lowest_matrix)
# draw_graph(highest_matrix, highest_energy, ax[1])

# plt.show()
# print(lowest_matrix, lowest_energy)
# print(highest_matrix, highest_energy)
