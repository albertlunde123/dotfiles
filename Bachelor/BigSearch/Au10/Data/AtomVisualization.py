import numpy as np
import matplotlib.pyplot as plt
from ase import Atoms
import ConfigurationSpace
import GPR
import EnergyCalcAndStorage as ECAS
import sqlite3

class AtomVisu:
    def __init__(self, coordinates = None, ax = None, conn = None):
        self.coordinates = coordinates
        self.ax = ax
        self.conn = conn

        ax.set_xlim(-1.36, 11.5 + 1.36)
        ax.set_ylim(-1.36, 11.5 + 1.36)
        ax.set_aspect('equal')

        # self.plot()
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

    def get_best_config(self):
        configs, energies = ECAS.fetch_raw_configurations(self.conn)
        min_config = configs[np.argmin(energies)]

        self.coordinates = min_config

        return min_config, np.min(energies)

    def show(self):
        plt.show()

conn = sqlite3.connect('Au10.db')
fig, ax = plt.subplots()
AV = AtomVisu(ax = ax,
              conn = conn)
best_config, best_energy = AV.get_best_config()
AV.plot()
AV.show()

