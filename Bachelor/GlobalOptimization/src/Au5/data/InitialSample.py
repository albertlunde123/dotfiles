from pyDOE import lhs
import numpy as np
import os
import EnergyCalcAndStorage as ECAS
import ConfigurationSpace as CS
import sqlite3

conn = sqlite3.connect('10Conf.db')

bounds = CS.calc_bounds(5)

# Create the directory for the initial sample
if not os.path.exists('initial_sample'):
    os.makedirs('initial_sample')

n = 5
n_dim = n * 2
n_sample = 1000000

# Generate the initial sample
X = lhs(n_dim, samples=n_sample) * bounds

def check_overlap(p):
    for i in range(n):
        for j in range(i + 1, n):
            if np.linalg.norm(p[i] - p[j]) < 2.72:
                return True
    return False

k = 0
for i, p in enumerate(X):

    print(p)
    
    p = p.reshape((n, 2))

    if check_overlap(p):
        continue

    k += 1

    # ECAS.store_energy(p, conn)

    if k == 51:
        break


