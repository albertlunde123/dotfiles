import numpy as np
import matplotlib.pyplot as plt

# In this file, we will generate a random path of 100 points in 2D space

N = 100
arr = np.zeros((100, 2))

def walk(arr):
    randP = np.random.rand(N) * 2 * np.pi
    deltaP = np.array([[np.sin(p*2*np.pi), np.cos(p*2*np.pi)] for p in randP])
    return arr + deltaP

def rms(arr):
    return np.sqrt(np.mean(np.linalg.norm(arr, axis=1)**2))

dists = []
new_arr = arr.copy()

for i in range(100):
    new_arr = walk(new_arr)
    dists.append(rms(new_arr))

xs = np.stack((arr[:,0], new_arr[:,0]), axis=1)
ys = np.stack((arr[:,1], new_arr[:,1]), axis=1)

fig, ax = plt.subplots(1, 2)

for i in range(N):
    ax[0].plot(xs[i], ys[i], 'bo')

steps = np.linspace(0, 100, 100)
steps = np.log(steps)
ax[1].plot(steps, np.log(dists))
ax[1].set_xlabel('Step')
ax[1].set_ylabel('RMS distance')
# ax[1].set_xscale('log')
# ax[1].set_yscale('log')
plt.show()







