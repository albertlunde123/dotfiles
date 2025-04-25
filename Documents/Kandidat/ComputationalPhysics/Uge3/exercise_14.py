# Description: This file contains the implementation of the Lennard-Jones potential

import numpy as np
from scipy.spatial.distance import pdist
from scipy import optimize
import matplotlib.pyplot as plt

class LennardJones():
    def __init__(self,eps0=5,sigma=2**(-1/6)):
        self.eps0 = eps0
        self.sigma = sigma
        
    def _V(self,r):
        return 4 * self.eps0 * ( (self.sigma/r)**12 - (self.sigma/r)**6 )

    def _dV_dr(self, r):
        return 4 * self.eps0 * ( -12 * self.sigma**12 / r**13 + 6 * self.sigma**6 / r**7 )

    def energy(self, pos):
        return np.sum(self._V(pdist(pos)))
    
    def forces(self, pos):
        diff = pos[np.newaxis, :, :] - pos[:, np.newaxis, :]
        r = np.sqrt(np.sum(diff**2, axis=-1))
        np.fill_diagonal(r, np.inf)
        force_magnitude = self._dV_dr(r)
        forces = np.sum(force_magnitude[..., np.newaxis] * diff / \
                        r[..., np.newaxis], axis=1)
        return forces

def lj_contour(ax):
    xs = np.linspace(-2, 2, 100)
    ys = np.linspace(-2, 2, 100)
    X, Y = np.meshgrid(xs, ys)
    Z = np.zeros(X.shape)
    for i, x in enumerate(xs):
        for j, y in enumerate(ys):
            Z[i, j] = lj.energy(np.array([[x, y], [-1, 0], [1, 0]]))
    ax.contourf(X, Y, Z.T, np.linspace(-15.75, 0, 100), cmap='OrRd')
    ax.axis('equal')
    return

def line_search(atoms):
    lj = LennardJones()
    force = lj.forces(atoms)
    force[1:] = 0
    fd = force / np.linalg.norm(force)
    print(force)
    
    def E(alpha):
        return lj.energy(atoms + alpha * fd)

    # Find the alpha that minimizes E(alpha)
    alpha = optimize.fmin(E, 0)

    return atoms + alpha * fd


def optimizer(atoms):
    pos = [atoms[0]]
    lj = LennardJones()
    atom = atoms.copy()
    for i in range(1000):
        atom = line_search(atom)
        pos.append(atom[0])
    return pos

def plot_atoms(atoms, ax):
    for p in atoms[1:]:
        circle = plt.Circle(p, 0.1, color='blue')
        ax.add_artist(circle)
    circle = plt.Circle(atoms[0], 0.1, color='red')
    ax.add_artist(circle)
    return



Atoms = np.array([[-1.5, 1.5], [-1, 0], [1, 0]])
lj = LennardJones()
fig, ax = plt.subplots()
plot_atoms(Atoms, ax)

ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_aspect('equal')


lj_contour(ax)

pos = optimizer(Atoms)
pos = np.array(pos)
for i, p in enumerate(pos):
    ax.plot(p[0], p[1], 'o', color='black', alpha=i/len(pos))
ax.plot(pos[:, 0], pos[:, 1], 'o-', color='black')
plt.show()

