import numpy as np
from scikit_learn import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C

class GPR:
    def __init__(self, kernel = C(1.0, (1e-3, 1e3)) * RBF(1.0, (1e-3, 1e3))):
        self.kernel = kernel
        self.gpr = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=9)
        self.X = None
        self.y = None

    def setX(self, X):
        assert isinstance(X, np.ndarray)
        self.X = X

    def sety(self, y):
        assert isinstance(y, np.ndarray)
        self.y = y

    def fit(self):
        self.gpr.fit(self.X, self.y)

    def predict(self, X):
        return self.gpr.predict(X, return_std=True)
