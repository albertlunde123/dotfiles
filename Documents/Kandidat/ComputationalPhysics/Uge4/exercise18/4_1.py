import Molecule as mlc
from Descriptors import DistanceMoments
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist

# class DistanceMoments():
    
#     def __init__(self, color='C4'):
#         self.xwidth = 1
#         self.color = color
#         self.bin_centers = range(2)
    
#     def descriptor(self,pos):
#         all_distances = pdist(pos)
#         mean = np.mean(all_distances)
#         std = np.std(all_distances)
#         return np.array([mean,std])
    
#     def draw(self,pos,ax):
#         vector = self.descriptor(pos)
#         ax.bar(self.bin_centers,vector,width=0.8 * self.xwidth,color=self.color)
#         ax.xaxis.set_major_locator(plt.MultipleLocator(1.0))
#         ax.set_ylim([0,2.3])
#         xticklabels = ['$\mu$','$\sigma$']
#         ax.set_xticks(range(len(xticklabels)))
        # ax.set_xticklabels(xticklabels)
        # ax.set_title(self.__class__.__name__)

dm = DistanceMoments()

pos_flat = np.loadtxt('lj10clusters.txt')
pos = pos_flat.reshape(-1,pos_flat.shape[1]//2,2)
pos = pos[:6]

fig, ax = plt.subplots(3, 4)
ax = ax.reshape(6, 2)

for i in range(6):
    mol = mlc.Molecule(pos[i])
    mol.draw(ax[i, 0])
    ax[i, 0].set_xlim([-4,4])
    ax[i,0].set_ylim([-4,4])
    ax[i, 0].set_aspect('equal')
    dm.draw(pos[i],ax[i, 1])

plt.show()


