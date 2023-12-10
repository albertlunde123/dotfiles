import numpy as np
import matplotlib.pyplot as plt

class Molecule:
    # atoms: list of atoms positions
    # bonds: list of bonds (atom1, atom2)
    def __init__(self,  atoms, bonds, ax, **kwarg):
        self.atoms = atoms
        self.bonds = bonds
        self.ax = ax

        ax.set_aspect('equal')
        ax.set_xlim(min(atoms[:, 0]) - 1, max(atoms[:, 0]) + 1)
        ax.set_ylim(min(atoms[:, 1]) - 1, max(atoms[:, 1]) + 1)

    def draw(self):
    
        for atom in self.atoms:
            circle = plt.Circle((atom[0], atom[1]), 0.2)
            self.ax.add_artist(circle)

        for bond in bonds:
            atom1 = self.atoms[bond[0]]
            atom2 = self.atoms[bond[1]]

            # double line

            line = plt.Line2D((atom1[0], atom2[0]), (atom1[1], atom2[1]), lw=2.5, color='black')

            self.ax.add_artist(line)


    def show(self):
        plt.show()

fig, ax = plt.subplots()

atoms = np.array([[0, 0], [1, 0], [0, 1], [1, 1]])
bonds = np.array([[0, 1], [0, 2], [1, 3], [2, 3]])

mol = Molecule(atoms, bonds, ax)
mol.draw()
mol.show()


