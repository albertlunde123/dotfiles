from pyDOE import lhs
import numpy as np
import EnergyCalcAndStorage as ECAS
import ConfigurationSpace as CS
import sqlite3

# Create database connection
conn = sqlite3.connect('Au10.db')
CS = CS.ConfigurationSpace(20)
print(CS.bounds)

# Generate initial sample

def generateSample(CS, n, conn):

    sampleSize = 1000000
    X = lhs(n, samples=sampleSize) * CS.calc_bounds(10)

    k = 0

    for p in X:
        if CS.check_non_overlapping(p):
            p = np.array(p).reshape(10, 2)
            k += 1
            print(k)
            ECAS.store_energy(p, conn)
        if k == 50:
            break

generateSample(CS, 20, conn)




