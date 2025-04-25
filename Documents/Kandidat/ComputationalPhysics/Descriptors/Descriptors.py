from scipy.spatial.distance import pdist, squareform
import numpy as np
import matplotlib.pyplot as plt

class DistanceMoments():
    
    def __init__(self, color='C4'):
        self.xwidth = 1
        self.color = color
        self.bin_centers = range(2)
    
    def descriptor(self,pos):
        all_distances = pdist(pos)
        mean = np.mean(all_distances)
        std = np.std(all_distances)
        return np.array([mean,std])
    
    def draw(self,pos,ax):
        vector = self.descriptor(pos)
        ax.bar(self.bin_centers,vector,width=0.8 * self.xwidth,color=self.color)
        ax.xaxis.set_major_locator(plt.MultipleLocator(1.0))
        ax.set_ylim([0,2.3])
        xticklabels = ['$\mu$','$\sigma$']
        ax.set_xticks(range(len(xticklabels)))
        ax.set_xticklabels(xticklabels)
        ax.set_title(self.__class__.__name__)

class ExtremeNeighborCount():
    
    def __init__(self, color='C5'):
        self.xwidth = 1
        self.color = color
        self.bin_centers = range(2)
    
    def descriptor(self,pos):
        threshold = np.std(pdist(pos)) * 2 ** (1/6) * 1.2
        connectivity_matrix = (squareform(pdist(pos)) < threshold).astype(int)
        np.fill_diagonal(connectivity_matrix, 0)
        neighbors = np.sum(connectivity_matrix, axis=1)
        Nlowest = np.min(neighbors)
        Nhighest = np.max(neighbors)
        return np.array([Nlowest,Nhighest])

    def draw(self,pos,ax):
        vector = self.descriptor(pos)
        ax.bar(self.bin_centers,vector,width=0.8 * self.xwidth,color=self.color)
        ax.xaxis.set_major_locator(plt.MultipleLocator(1.0))
        ax.set_ylim([0,7])
        xticklabels = ['$N_{lowest}$','$N_{highest}$']
        ax.set_xticks(range(len(xticklabels)))
        ax.set_xticklabels(xticklabels)
        ax.set_title(self.__class__.__name__)

class CoulumbMatrixSpectrum():

    def __init__(self, color='C4'):
        self.xwidth = 1
        self.color = color

    def descriptor(self,pos):
        YOUR CODE

    def draw(self,pos,ax):
        vector = self.descriptor(pos)
        N = len(vector)
        xcenters = np.linspace(0,N-1,N) * self.xwidth
        ax.bar(xcenters,vector,width=0.8 * self.xwidth,color=self.color)
        ax.xaxis.set_major_locator(plt.MultipleLocator(1.0))
        ax.set_ylim([-2,8])
        ax.set_title(self.__class__.__name__)

