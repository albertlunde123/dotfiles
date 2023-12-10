from sympy import Matrix, pretty_print
import numpy as np

class Cluster:
    def __init__(self, n, bonds, non_bonds = False):
        self.n = n
        self.bonds = bonds
        self.non_bonds = non_bonds

    def construct_matrix(self, beta = -1.0):
        self.matrix = np.zeros((self.n, self.n))
        for i in range(self.n):
            for j in range(self.n):
                if i == j:
                    self.matrix[i, j] = 0
                elif (i, j) in self.bonds:
                    self.matrix[i, j] = beta
                    self.matrix[j, i] = beta

        if self.non_bonds == True:
            self.matrix = np.zeros((self.n, self.n)) + beta
            for i in range(self.n):
                for j in range(self.n):
                    if i == j:
                        self.matrix[i, j] = 0
                    elif (i, j) in self.bonds:
                        self.matrix[i, j] = 0
                        self.matrix[j, i] = 0

                # else:
                #     self.matrix[i, j] = 0
        # convert matrix to sympy matrix
        self.matrix = Matrix(self.matrix)

    def print_matrix(self):
        pretty_print(self.matrix)

    def eigenvalues(self):
        eigenvalues = self.matrix.eigenvals()
        ei_list = []
        for key in eigenvalues:
            degen = eigenvalues[key]
            for i in range(degen):
                ei_list.append(key)
        ei_list = np.array(ei_list)

        return np.sort(ei_list)

    def calc_energy(self, plus = False):
        energy = 0
        eigenvals = self.eigenvalues()

        print(eigenvals[1])

        if plus == True:
            for i in range(self.n-1):
                if i < 2:
                    energy += eigenvals[0]
                else:
                    energy += eigenvals[1]
            return energy

        for i in range(self.n):
            if i < 3:
                energy += eigenvals[0]
            else:
                energy += eigenvals[1]
        return energy


clust = Cluster(5, [(0, 3), (0,4)],
                non_bonds = True)

clust.construct_matrix(beta = -1)
clust.print_matrix()
ei = clust.eigenvalues()
print(ei)
print(clust.calc_energy(plus = True))
