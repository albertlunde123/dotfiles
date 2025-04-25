import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist
from matplotlib import animation

class LennardJones():
    def __init__(self,eps0=5,sigma=2**(-1/6)):
        self.eps0 = eps0
        self.sigma = sigma
        
    def _V(self,r):
        return 4*self.eps0*((self.sigma/r)**12-(self.sigma/r)**6)

    def energy(self, pos):
        return np.sum(self._V(pdist(pos)))

class Particle():
    def __init__(self, pos, vel):
        self.pos = pos
        self.vel = vel
        self.personal_best = pos
        self.calc_energy = None

    def energy(self, other_atoms):
        return calc_energy(np.vstack((self.pos, other_atoms)))

    def update_personal_best(self, energy):
        if energy < self.energy(self.personal_best):
            self.personal_best = self.pos
        return

    def update_pos(self):
        self.pos += self.vel
        return
    
class Swarm():
    def __init__(self, n, w, c1, c2, calc_energy, other_atoms):
        self.n = n
        self.w = w
        self.c1 = c1
        self.c2 = c2
        self.calc_energy = calc_energy
        self.other_atoms = other_atoms
        self.particles = [Particle(np.random.rand(2)*4-2, np.random.rand(2)*0.5) for _ in range(n)]
        for p in self.particles:
            p.calc_energy = calc_energy
        self.gbest = self.particles[0].pos

    def update_positions(self):
        for p in self.particles:
            p.update_pos()
        return

    def update_velocities(self):
        for p in self.particles:
            r1 = np.random.rand()
            r2 = np.random.rand()
            p.vel = (self.w*p.vel + self.c1*r1*(p.personal_best-p.pos) + self.c2*r2*(self.gbest-p.pos))*0.2
        return

    def update_gbest(self):
        p = None
        best_energy = calc_energy(np.vstack((self.gbest, self.other_atoms)))
        for p in self.particles:
            if p.energy(self.other_atoms) < best_energy:
                self.gbest = p.pos
        return

    def update_personal_bests(self):
        for p in self.particles:
            p.update_personal_best(p.energy(self.other_atoms))
        return
    
    def update(self):
        self.update_gbest()
        self.update_velocities()
        self.update_positions()
        self.update_personal_bests()
        return
    
    def run(self, n):
        for i in range(n):
            self.update()
        return
    


Atoms = np.array([[-1, 0], [1, 0]])
calc_energy = LennardJones().energy

swarm = Swarm(10, 0.8, 3, 1, calc_energy, Atoms)


fig, ax = plt.subplots()


for atom in Atoms:
    ax.add_artist(plt.Circle(atom, 0.5, color='r'))

colors = ['b', 'g', 'y', 'c', 'm', 'k', 'w', 'r', 'pink', 'orange']

for p in swarm.particles:
    ax.add_artist(plt.Circle(p.pos, 0.05, color='b'))


def update(i):
    swarm.update()
    for p, c in zip(swarm.particles, colors):
        ax.add_artist(plt.Circle(p.pos, 0.05, color=c))
    return

ani = animation.FuncAnimation(fig, update, frames=100, repeat=False, interval=100)


# for p in swarm.particles:
#     ax.add_artist(plt.Circle(p.pos, 0.05, color='g'))


ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_aspect('equal')

plt.show()

