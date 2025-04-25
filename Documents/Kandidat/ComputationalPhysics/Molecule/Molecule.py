import matplotlib.pyplot as plt
import numpy as np

class Molecule():
    def __init__(self, pos):
        self.pos = pos

    def rattle(self, sigma=0.1):
        self.pos += np.random.normal(0, sigma, self.pos.shape)
    
    def draw(self, ax, color='teal'):
        for p in self.pos:
            ax.add_artist(plt.Circle(p, 0.5,
                                     facecolor=color,
                                     edgecolor='black',
                                     lw=3,
                                     ls='-'))
