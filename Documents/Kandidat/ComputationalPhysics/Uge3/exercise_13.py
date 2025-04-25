from scipy.spatial.distance import pdist
import numpy as np
import matplotlib.pyplot as plt

class LennardJones():
    def __init__(self,eps0=5,sigma=2**(-1/6)):
        self.eps0 = eps0
        self.sigma = sigma
        
    def _V(self,r):
        return 4*self.eps0*((self.sigma/r)**12-(self.sigma/r)**6)

    def energy(self, pos):
        return np.sum(self._V(pdist(pos)))

def generate_atoms(N=3):
    return np.random.uniform(-2, 2, size=(N, 2))

def plot_atoms(ax, Atoms, color='b'):
    for atom in Atoms[:-1]:
        circ = plt.Circle((atom[0], atom[1]), 0.5, color=color)
        ax.add_artist(circ)
    circ = plt.Circle((Atoms[-1][0], Atoms[-1][1]), 0.5, color='k')
    ax.add_artist(circ)

def MonteCarloOptimization(atoms, lj, N=1000, T=0.1):
    
    # keeping the last atom fixed
    n = len(atoms)
    print(n)

    for i in range(N):
        for j in range(n-1):
            new_atoms = atoms.copy()
            new_atoms[j] = atoms[j] + np.random.normal(0, 1, size=2)
            E0 = lj.energy(atoms)
            E_new = lj.energy(new_atoms)
            dE = E_new - E0
            if np.random.uniform(0, 1) < np.exp(-dE/T):
                atoms = new_atoms
    return atoms

fig, ax = plt.subplots(1, 2)
ax = ax.ravel()
ax[0].set_xlim(-5, 5)
ax[0].set_ylim(-5, 5)
ax[0].set_aspect('equal')
atoms = generate_atoms(N=8)
plot_atoms(ax[0], atoms)
lj = LennardJones()


ax[1].set_xlim(-5, 5)
ax[1].set_ylim(-5, 5)
ax[1].set_aspect('equal')
new_atoms = MonteCarloOptimization(atoms, lj)
plot_atoms(ax[1], new_atoms, 'r')

plt.show()
# positions = MonteCarloOptimization(Atoms, lj)
# ax.plot(positions[:, 0], positions[:, 1], 'yo-')
# plt.show()



