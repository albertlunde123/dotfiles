from Descriptors.PCA import PCA
from Molecule.Molecule import Molecule
import numpy as np
import matplotlib.pyplot as plt

# Rotating a molecule using PCA

# Load data
data = np.loadtxt('../lj10clusters.txt')
positions = data.reshape(-1, data.shape[1]//2,2)[10]

# Perform PCA
pca = PCA(positions.reshape(positions.shape[0], -1))
pca.fit()
rotated = pca.transform(20).reshape(-1,2)

# Plot
fig, ax = plt.subplots(1,2, figsize=(10,5))
mol1 = Molecule(positions)
mol2 = Molecule(rotated)
mol1.draw(ax[0])
mol2.draw(ax[1])
ax[0].set_title('Original')
ax[1].set_title('Rotated')
ax[0].set_xlim(-5,5)
ax[0].set_ylim(-5,5)
ax[1].set_xlim(-5,5)
ax[1].set_ylim(-5,5)
ax[0].set_aspect('equal')
ax[1].set_aspect('equal')
plt.show()
