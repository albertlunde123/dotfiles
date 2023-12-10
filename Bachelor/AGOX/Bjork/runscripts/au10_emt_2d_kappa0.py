import matplotlib

matplotlib.use("Agg")

import numpy as np
from agox import AGOX
from agox.databases import Database
from agox.environments import Environment
from agox.evaluators import LocalOptimizationEvaluator
from agox.generators import RandomGenerator, RattleGenerator
from agox.samplers import KMeansSampler
from agox.collectors import ParallelCollector
from agox.acquisitors import EIAcquisitor
from agox.acquisitors import LowerConfidenceBoundAcquisitor
from agox.postprocessors import ParallelRelaxPostprocess
from ase import Atoms

from agox.models.descriptors.fingerprint import Fingerprint
from agox.models.GPR.kernels import RBF, Constant as C, Noise
from agox.models.GPR import GPR
from agox.models.GPR.priors import Repulsive

# Using argparse if e.g. using array-jobs on Slurm to do several independent searches.
from argparse import ArgumentParser
parser = ArgumentParser()
parser.add_argument('-i', '--run_idx', type=int, default=0)
args = parser.parse_args()

run_idx = args.run_idx
from random import seed
seed(run_idx)
np.random.seed(run_idx)
database_index = args.run_idx

for i in range(20):

    ##############################################################################
    # Calculator
    ##############################################################################

    from ase.calculators.emt import EMT

    calc = EMT()

    ##############################################################################
    # System & general settings:
    ##############################################################################

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

    # We add an additional constraint from ASE to keep atoms confined to 2D during
    # relaxations.
    # The box constraint will keep them in the specified cell in the other dimensions.
    from ase.constraints import FixedPlane

    fixed_plane = [FixedPlane(i, [0, 0, 1]) for i in environment.get_missing_indices()]
    constraints = environment.get_constraints() + fixed_plane

    # Database
    db_path = "kappa0/db{}.db".format(i)  # From input argument!
    database = Database(filename=db_path, order=6)

    # print(database.get_all_candidates())

    ##############################################################################
    # Search Settings:
    ##############################################################################

    # Setup a ML model.
    descriptor = Fingerprint(environment=environment)
    beta = 0.01
    k0 = C(beta, (beta, beta)) * RBF()
    k1 = C(1 - beta, (1 - beta, 1 - beta)) * RBF()
    kernel = C(5000, (1, 1e5)) * (k0 + k1) + Noise(0.01, (0.01, 0.01))
    model = GPR(descriptor=descriptor, kernel=kernel, database=database, prior=Repulsive())

    # Sampler to choose candidates to modify using the generators.
    sample_size = 10
    sampler = KMeansSampler(
        descriptor=descriptor, database=database, sample_size=sample_size
    )


    # Generators to produce candidates structures
    rattle_generator = RattleGenerator(**environment.get_confinement())
    random_generator = RandomGenerator(**environment.get_confinement())

    # Dict specificies how many candidates are created with and the dict-keys are iterations.
    generators = [random_generator, rattle_generator]
    num_candidates = {0: [10, 0], 2: [0, 10]}

    # Collector creates a number of structures in each iteration. 
    collector = ParallelCollector(
        generators=generators,
        sampler=sampler,
        environment=environment,
        num_candidates=num_candidates,
        order=2,
    )

    # Acquisitor to choose a candidate to evaluate in the real potential.
    acquisitor = EIAcquisitor(model=model, database=database, order=4)
    acquisitor2 = LowerConfidenceBoundAcquisitor(model=model, kappa=2, order=4)
    # acquisitor = LowerConfidenceBoundAcquisitor(model=model, kappa=0, order=4)

    relaxer = ParallelRelaxPostprocess(
         model=acquisitor2.get_acquisition_calculator(),
         constraints=constraints,
         optimizer_run_kwargs={"steps": 100},
         start_relax=5,
         order=3,
     )

    # Evaluator to evaluate the candidates in the real potential.
    evaluator = LocalOptimizationEvaluator(
         calc,
         gets={"get_key": "prioritized_candidates"},
         optimizer_kwargs={"logfile": None},
         optimizer_run_kwargs={"fmax": 0.025, "steps": 1},
         constraints=constraints,
         store_trajectory=True,
         order=5,
     )

    ##############################################################################
    # Let get the show running!
    ##############################################################################

    # The oder of things here does not matter. But it can be simpler to understand
    # what the expected behaviour is if they are put in order.

    agox = AGOX(collector, acquisitor, evaluator, database, seed=run_idx)

    agox.run(N_iterations=100)

    # print(database.candidate_energies)
