import numpy as np
from agox import AGOX
from agox.acquisitors import LowerConfidenceBoundAcquisitor
from agox.models.GPR import GPR
from agox.models.descriptors.fingerprint import Fingerprint
from agox.models.GPR.kernels import RBF, Constant as C, Noise
from agox.models.GPR.priors import Repulsive
from agox.environments import Environment
from agox.databases import Database
from ase import Atoms


template = Atoms("", cell=np.eye(3) * 20)
confinement_cell = np.eye(3) * 15
confinement_cell[2, 2] = 0  # Zero height of confinement cell for the third dimension.
confinement_corner = np.array([2.5, 2.5, 10])
environment = Environment(
    template=template,
    symbols="Au10",
    confinement_cell=confinement_cell,
    confinement_corner=confinement_corner,
)

db_path = "test.db"
database = Database(filename=db_path, order=6)

descriptor = Fingerprint(environment=environment)
beta = 0.01
k0 = C(beta, (beta, beta)) * RBF()
k1 = C(1 - beta, (1 - beta, 1 - beta)) * RBF()
kernel = C(5000, (1, 1e5)) * (k0 + k1) + Noise(0.01, (0.01, 0.01))
model = GPR(descriptor=descriptor, kernel=kernel, database=database, prior=Repulsive())

lcba = LowerConfidenceBoundAcquisitor(model=model, kappa=2, order=4)
