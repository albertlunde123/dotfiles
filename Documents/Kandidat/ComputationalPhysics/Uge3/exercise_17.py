import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist
from scipy.optimize import fmin, minimize
from matplotlib import animation

class LennardJones():
    def __init__(self,eps0=5,sigma=2**(-1/6)):
        self.eps0 = eps0
        self.sigma = sigma
        
    def _V(self,r):
        return 4*self.eps0*((self.sigma/r)**12-(self.sigma/r)**6)

    def energy(self, pos):
        return np.sum(self._V(pdist(pos)))

    def _dV_dr(self, r):
        return 4 * self.eps0 * ( -12 * self.sigma**12 / r**13 + 6 * self.sigma**6 / r**7 )

    def forces(self, pos):
        diff = pos[np.newaxis, :, :] - pos[:, np.newaxis, :]
        r = np.sqrt(np.sum(diff**2, axis=-1))
        np.fill_diagonal(r, np.inf)
        force_magnitude = self._dV_dr(r)
        forces = np.sum(force_magnitude[..., np.newaxis] * diff / \
                        r[..., np.newaxis], axis=1)
        return forces

class Cluster():
    def __init__(self, n_particles=10, box_size=4, calc=LennardJones()):
        self.positions = np.random.rand(n_particles, 2)*box_size*2-box_size
        self.positions[0] = [0, 0]
        self.calc = calc

    def energy(self):
        return self.calc.energy(self.positions)

    def force(self):
        return self.calc.forces(self.positions)

def basinHopping(cluster):
    # We will be keeping the first atom fixed at the origin
    # so we will only be updating the positions of the other atoms
    n_particles = cluster.positions.shape[0]
    r_rnd = np.random.randn(n_particles-1, 2) * 0.1
    trial = np.copy(cluster.positions)
    trial[1:] += r_rnd
    lj = LennardJones()

    def objective(x):
        trial_positions = np.vstack((np.zeros((1, 2)), x.reshape(-1, 2)))
        return cluster.calc.energy(trial_positions)

    def objective_grad(x):
        trial_positions = np.vstack((np.zeros((1, 2)), x.reshape(-1, 2)))
        forces = cluster.calc.forces(trial_positions)
        return forces.flatten()[2:]

    # # We will now minimize the objective function

    x0 = trial[1:].flatten()
    res = minimize(objective, x0, method='L-BFGS-B')
    
    relaxed = np.vstack((np.zeros((1, 2)), res.x.reshape(-1, 2)))
    
    if lj.energy(relaxed) < lj.energy(cluster.positions):
        cluster.positions[1:] = trial[1:]
    
    # if res.success:
    #     if res.x.calc.energy(trial_positions) < cluster.calc.energy(cluster.positions):
    #         cluster.positions[1:] = res.x.reshape(-1, 2)



    return cluster



fig, ax = plt.subplots()
ax.set_xlim(-5, 5)
ax.set_ylim(-5, 5)
ax.set_aspect('equal')

Cluster = Cluster()

for p in Cluster.positions:
    ax.add_artist(plt.Circle(p, 0.5, color='b', fill=False))

for i in range(100):
    Cluster = basinHopping(Cluster)

print(Cluster.positions)

for p in Cluster.positions:
    ax.add_artist(plt.Circle(p, 0.5, color='r', fill=True))

plt.show()





