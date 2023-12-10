import numpy as np
import matplotlib.pyplot as plt
from ase import Atoms
import ConfigurationSpace
import GPR
import EnergyCalcAndStorage as ECAS

class AtomVisu:
    def __init__(self, coordinates, ax):
        self.coordinates = coordinates
        self.ax = ax

        ax.set_xlim(-1.36, 17 + 1.36)
        ax.set_ylim(-1.36, 17 + 1.36)
        ax.set_aspect('equal')

        self.plot()
        # self.show()

    def plot(self):

        # if self.coordinates.shape[1] == 2:
        #     x = self.coordinates[:,0]
        #     y = self.coordinates[:,1]
        # else:
        x = self.coordinates[::2]
        y = self.coordinates[1::2]

        for i,j in zip(x,y):
            circle = plt.Circle((i,j), 
                                1.36,
                                edgecolor='black',
                                facecolor='gold',
                                linewidth=1.0)

            self.ax.add_artist(circle)

    def show(self):
        plt.show()

