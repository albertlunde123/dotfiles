from GPR import GPR
from ConfigurationSpace import ConfigurationSpace
import EnergyCalcAndStorage as ECAS
import AtomicVisualiztion as AV
import matplotlib.pyplot as plt
import sqlite3  
import numpy as np

conn = sqlite3.connect('Data/10Conf.db')
Points, Energies = ECAS.fetch_raw_configurations(conn)

print(Points[0], Energies[0])
print(ECAS.calculate_energy(Points[0]))

print(Points[1])

Energies = np.array(Energies)

i = np.argmin(Energies)
Model = GPR(Points, Energies)
Model.fit()

CS = ConfigurationSpace(10)

def descent(point, energy):
    
    cur = 10000000

    while True:

        test_points = CS.sample_near_point(point)

        if test_points is None:
            print("No new point found")
            break
        
        test_energies = [ECAS.calculate_energy(p) for p in test_points]
        # test_energies = [Model.predict(p.reshape(1, -1))[0] for p in test_points]
        min_energy = float(min(test_energies))

        print(min_energy)

        if min_energy < cur:
            point = test_points[test_energies.index(min_energy)]
            cur = min_energy
        
        else:
            print('Energy minimum found')
            break

    return point, cur

minEnergies = []
for p, e in zip(Points, Energies):
    minEnergies.append(descent(p, e))
    
minEnergies = np.array(minEnergies)
minOfMin = np.argmin(minEnergies[:, 1])

fig, ax = plt.subplots()

atomVis = AV.AtomVisu(minEnergies[minOfMin, 0], ax)

plt.show()
