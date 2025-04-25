# import Molecule as mlc
from ..classes.molecule import Molecule
import numpy as np
import matplotlib.pyplot as plt

pos_flat = np.loadtxt('../lj10clusters.txt')
pos = pos_flat.reshape(-1,pos_flat.shape[1]//2,2)

dm = desc.DistanceMoments()

mean_std= np.array([dm.descriptor(p) for p in pos])


fig, ax = plt.subplots()
ax.plot(mean_std[0, :], mean_std[1, :], 'o')
plt.show()
