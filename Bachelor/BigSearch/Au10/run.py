import ConfigurationSpace as CS
import EnergyCalcAndStorage as ECAS
import GPR as GPR
import sqlite3
import numpy as np
import random

conn = sqlite3.connect('Data/Au10.db')
points, energies = ECAS.fetch_raw_configurations(conn)


confSpace = CS.ConfigurationSpace(20)
Model = GPR.GPR(configuration_space = confSpace, 
                conn = conn)

min_point = points[np.argmin(energies)]

Model.fit()
# print(Model.points)

class GlobalSearch:
    def __init__(self, confSpace, Model, ECAS):
        self.confSpace = confSpace
        self.Model = Model
        self.ECAS = ECAS
        self.evaluatedPoints = []

    def addPoint(self, point):
        self.evaluatedPoints.append(point)

    def optimizePoint(self, method, p = None, e = None):
        if p is None:
            p, e = Model.randomPEFromData()
        self.addPoint(p)
        return method(p, e)

GS = GlobalSearch(confSpace, Model, ECAS)

for i in range(100):
    print(GS.optimizePoint(Model.expectedImprovementDescent, min_point, min(energies)))

# for i in range(100):
#     GS.optimizePoint(Model.expectedImprovementDescent)









