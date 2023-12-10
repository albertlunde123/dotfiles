2mport numpy as np
# from agox import AGOX
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

from ase.calculators.emt import EMT
from ase.constraints import FixedPlane

from random import seed
import os 



def get_next_iter(dir_pat):
    path = os.getcwd() + dir_pat
    j = 0
    for file in os.listdir(path):
        if file.endswith(".db"):
            # get number in filename
            file = file.split(".")
            file = file[0].split("b")
            if int(file[1]) > j:
                j = int(file[1])
    j += 1
    return j

# print(get_next_iter("/aqui_relax/"))

for _ in range(1):

    # j = get_next_iter("/aqui_relax/")
    j = 0
    run_seed = seed(j)  

    # print("Iteration: ", j)

    calc = EMT()

    template = Atoms("", cell = np.eye(3) * 20)
    confinement_cell = np.eye(3) * 15
    confinement_cell[2, 2] = 0

    confinement_corner = np.array([2.5, 2.5, 10])
    environment = Environment(
        template = template,
        symbols = "Au10",
        confinement_cell = confinement_cell,
        confinement_corner = confinement_corner,
    )

    # I add an additional constraint to keep the atoms confined

    fixed_plane = [FixedPlane(i, [0, 0, 1]) for i in environment.get_missing_indices()]
    constraints = environment.get_constraints() + fixed_plane

    # Path for storage
    
    db_path = "aqui_relax/db{}.db".format(int(j))
    database = Database(filename = db_path, order = 6)

    # Search settings.
    # start by sampling some candidates, we do 16

    descriptor = Fingerprint(environment=environment)
    beta = 0.01
    k0 = C(beta, (beta, beta)) * RBF()
    k1 = C(1 - beta, (1 - beta, 1 - beta)) * RBF()
    kernel = C(5000, (1, 1e5)) * (k0 + k1) + Noise(0.01, (0.01, 0.01))
    model = GPR(descriptor=descriptor, kernel=kernel, database=database, prior=Repulsive())

    sample_size = 16
    sampler = KMeansSampler(
        descriptor=descriptor, database=database, sample_size=sample_size
    )

    rattle_generator = RattleGenerator(**environment.get_confinement())
    random_generator = RandomGenerator(**environment.get_confinement())

    generators = [random_generator, rattle_generator]
    num_candidates = {0: [10, 0], 2: [0, 10]}

    collector = ParallelCollector(
        generators = generators,
        sampler = sampler, 
        environment = environment,
        num_candidates = num_candidates,
        order = 2,
    )
    
    acquisitor = LowerConfidenceBoundAcquisitor(model=model, kappa=2, order=4)

    # In this example, we relax in LCB.

    relaxer = ParallelRelaxPostprocess(
        model = acquisitor.get_acquisition_calculator(),
        constraints = constraints,
        optimizer_run_kwargs = {"steps": 100},
        start_relax = 5,
        order = 3,
    )

    evaluator = LocalOptimizationEvaluator(
        calc,
        gets = {"get_key": "prioritized_candidates"},
        optimizer_kwargs={"logfile": None},
        optimizer_run_kwargs={"fmax": 0.025, "steps": 1},
        constraints=constraints,
        store_trajectory=True,
        order=5,
        )

    agox = AGOX(collector, relaxer, acquisitor, evaluator, database, seed = run_seed)
    agox.run(N_iterations = 100)
