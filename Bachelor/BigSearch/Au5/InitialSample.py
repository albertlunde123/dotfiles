from pyDOE import lhs
import numpy as np
import os
import DFT

# Create the directory for the initial sample
if not os.path.exists('initial_sample'):
    os.makedirs('initial_sample')

n = 5
n_dim = n * 2
n_sample = 1000000

# Generate the initial sample
X = lhs(n_dim, samples=n_sample) * 5

def check_overlap(p):
    for i in range(n):
        for j in range(i + 1, n):
            if np.linalg.norm(p[i] - p[j]) < 2.1:
                return True
    return False

k = 0
for i, p in enumerate(X):
    
    p = p.reshape((n, 2))

    if check_overlap(p):
        print("Overlap found")
        continue

    k += 1

    DFT.energy_calc(p)

    if k == 51:
        break


