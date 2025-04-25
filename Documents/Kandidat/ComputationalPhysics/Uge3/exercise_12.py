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

Atoms = np.array([[-1.5, 1.5], [-1, 0], [1, 0]])
lj = LennardJones()
print(lj.energy(Atoms))

def lj_contour(ax):
    xs = np.linspace(-2, 2, 100)
    ys = np.linspace(-2, 2, 100)
    X, Y = np.meshgrid(xs, ys)
    print(Y)
    Z = np.zeros(X.shape)
    for i, x in enumerate(xs):
        for j, y in enumerate(ys):
            Z[i, j] = lj.energy(np.array([[x, y], [-1, 0], [1, 0]]))
    ax.contourf(X, Y, Z.T, np.linspace(-15.75, 0, 100), cmap='OrRd')
    ax.axis('equal')
    # plt.show()
    return

def MonteCarloOptimization(Atoms, lj, N=1000, T=0.0001):
    
    positions = []
    p0 = Atoms[0]

    for i in range(N):
        p_new = p0 + np.random.normal(0, 1, size=2)
        E0 = lj.energy([p0, Atoms[1], Atoms[2]])
        E_new = lj.energy([p_new, Atoms[1], Atoms[2]])
        dE = E_new - E0
        if np.random.uniform(0, 1) < np.exp(-dE/T):
            p0 = p_new
        positions.append(p0)

    return np.array(positions)

fig, ax = plt.subplots()
lj_contour(ax)
positions = MonteCarloOptimization(Atoms, lj)
ax.plot(positions[:, 0], positions[:, 1], 'yo-')
plt.show()



