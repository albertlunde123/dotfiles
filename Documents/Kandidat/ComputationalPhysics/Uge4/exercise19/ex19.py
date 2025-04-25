from Descriptors.Descriptors import ExtremeNeighborCount
from Molecule.Molecule import Molecule
import numpy as np
import matplotlib.pyplot as plt


pos_flat = np.loadtxt('../lj10clusters.txt')
pos = pos_flat.reshape(-1,pos_flat.shape[1]//2,2)

enc = ExtremeNeighborCount()

print(enc.descriptor(pos[0]))
mol = Molecule(pos[0])

fig, ax = plt.subplots()
ax.set_aspect('equal')
ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)
mol.draw(ax)

plt.show()

