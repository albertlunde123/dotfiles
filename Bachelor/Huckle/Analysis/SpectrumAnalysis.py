import numpy as np
import sympy as sp
import networkx as nx
import matplotlib.pyplot as plt
import random as rd
import random_configuration as rc

A = sp.Matrix([[0, 1, 0, 0, 1],
               [1, 0, 1, 0, 0],
               [0, 1, 0, 1, 0],
               [0, 0, 1, 0, 1],
               [1, 0, 0, 1, 0]])

B = sp.Matrix([[0, 1, 0, 1, 0],
               [1, 0, 1, 0, 0],
               [0, 1, 0, 1, 0],
               [1, 0, 1, 0, 1],
               [0, 0, 0, 1, 0]])

G1 = rc.make_graph(A)
G2 = rc.make_graph(B)

print(rc.calc_energy(A))
print(rc.calc_energy(B))

def power_norm(A, k):
    A = A**k
    A = sum(A)
    return A ** (1/k)

# print(max(A.eigenvals().keys()))
# print(power_norm(A, 100))

# plt.show()


