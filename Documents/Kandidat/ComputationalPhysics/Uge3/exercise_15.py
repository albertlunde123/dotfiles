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

def line_search(atoms, fix_atoms, min_force = 0.05):
    
    lj = LennardJones()

    def step(atoms, fix_atoms):
        forces = lj.forces(atoms)
        forces[fix_atoms] = 0
        forces = forces / np.linalg.norm(forces)

        E = lambda x: lj.energy(atoms + x * forces)
        alpha = optimize.fmin(E, 0)[0]
        return atoms + alpha * forces
    
    # k = 0
    # while np.linalg.norm(lj.forces(atoms)) > min_force or k > 100:
    #     k += 1
    #     atoms = step(atoms, fix_atoms)
    
    for i in range(1000):
        atoms = step(atoms, fix_atoms)
        if np.linalg.norm(lj.forces(atoms)) < min_force:
            break

    return atoms

def generate_atoms(n_atoms, box_size):
    return np.random.uniform(0, box_size, size = (n_atoms, 2))

def plot_atoms(atoms, ax, color='b', alpha=0.5, fill=False):
    for atom in atoms:
        circle = plt.Circle(atom, 0.5, color=color, alpha=alpha, fill=fill)
        ax.add_artist(circle)
    return

fig, ax = plt.subplots()
ax.set_xlim(-1, 6)
ax.set_ylim(0, 5)
ax.set_aspect('equal')
atoms = generate_atoms(10, 5)
plot_atoms(atoms, ax)
atoms = line_search(atoms, [0])
plot_atoms(atoms, ax, color='r', fill=True)

plt.show()






