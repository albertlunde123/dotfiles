from multiprocessing import Pool
from smartSampling import Function, Optimize, DataStorage
import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C

def run_optimization(run_id, data_storage, kappa=4):
    bounds = (0, 100 * np.pi)
    n_params = 20
    kernel = C(1.0, (1e-4, 1e3)) * RBF(10, (1e-3, 1e2))
    gp = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=10)

    function_obj = Function(bounds, n_params)
    optimizer = Optimize(function_obj, gp, run_id=run_id)
    
    result = optimizer.run(n_iterations = 20, method='random', kappa=kappa, data_storage=data_storage)
    return result

for i in range(100):
    print(i)
    data_storage = DataStorage()
    run_optimization(1, data_storage, 6)
    data_storage.save_to_csv('random_20_1.csv')

# with Pool(4) as pool:
#     results = pool.starmap(run_optimization,
#                            [(i, data_storage, 4) for i in range(25)])


