import EnergyCalcAndStorage as ECAS
import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C
from scipy.stats import norm

# conn = sqlite3.connect('Data/10Conf.db')
# points, energies = ECAS.fetch_raw_configurations(conn)

class GPR:
    def __init__(self,
                 configuration_space,
                 conn,
                 points = None,
                 energies = None,
                 gp = None):

        self.configuration_space = configuration_space
        self.conn = conn
        if points is None:
            points, energies = ECAS.fetch_raw_configurations(self.conn)

        self.points = points
        self.energies = energies
        # self.points = np.array(points).reshape(-1, 1)
        # self.energies = np.array(energies)
        self.kernel = C(1.0, (1e-3, 1e3)) * RBF(1.0, (1e-3, 1e3))
        if gp is None:
            self.gp = GaussianProcessRegressor(kernel=self.kernel, n_restarts_optimizer=9)
        else:
            self.gp = gp

    def predict(self, point):
        return self.gp.predict(point, return_std=True)

    def fit(self):
        self.gp.fit(self.points, self.energies)

    def update_points_energies(self, point, energy):

        new_point = np.array(point).reshape(1, -1)
        new_energy = np.array([energy])

        self.points = np.vstack((self.points, new_point))
        self.energies = np.append(self.energies, new_energy)

        self.gp.fit(self.points, self.energies)

    def randomPEFromData(self):
        idx = np.random.randint(0, len(self.points))
        return self.points[idx], self.energies[idx]

    def regularDescent(self, point, energy):

        # point, energy = self.randomPEFromData()

        while True:

            test_points = self.configuration_space.sample_near_point(point)
            # print("Test points: ", test_points.shape)
            if test_points is None:
                break

            test_energies = self.predict(test_points)[0]
            min_idx = np.argmin(test_energies)

            if test_energies[min_idx] < energy:
                point = test_points[min_idx]
                energy = test_energies[min_idx]

            else:
                break

        if energy < min(self.energies):
            print("New candidate found")
            print("Energy: ", energy)
            true_energy = ECAS.store_energy(point, self.conn)
            print("True energy: ", true_energy)
            self.update_points_energies(point, true_energy)

            print("Current best energy", min(self.energies))

            return point, true_energy

        else:
            print("No new candidate found")
            return point, None

    def aquisitionDescent(self, point, energy):

        while True:

            test_points = self.configuration_space.sample_near_point(point)
            if test_points is None:
                break

            test_energies, sigma = self.predict(test_points)
            aqui = test_energies - 2 * sigma

            min_idx = np.argmin(aqui)
            if aqui[min_idx] < energy:
                point = test_points[min_idx]
                energy = aqui[min_idx]

            else:
                break

        if energy < min(self.energies):
            print("New candidate found")
            print("Energy: ", energy)
            true_energy = ECAS.store_energy(point, self.conn)
            print("True energy: ", true_energy)
            self.update_points_energies(point, true_energy)

            print("Current best energy", min(self.energies))

            return point, true_energy

        else:
            print("No new candidate found")
            return point, None

    def expectedImprovementDescent(self, point, energy):

        threshold = 0
        while True:

            test_points = self.configuration_space.sample_near_point(point)
            if test_points is None:
                print("No new candidate found")
                break

            test_energies, sigma = self.predict(test_points)

            def EI(mu, sigma, f_min):
                z = (f_min - mu ) / sigma
                return (f_min - mu) * norm.cdf(z) + sigma * norm.pdf(z)

            ei = EI(test_energies, sigma, min(self.energies))
            max_idx = np.argmax(ei)

            if ei[max_idx] > threshold:
                point = test_points[max_idx]
                threshold = ei[max_idx]

            else:
                break

        if threshold > 0:
            true_energy = ECAS.store_energy(point, self.conn)
            print("True energy: ", true_energy)
            self.update_points_energies(point, true_energy)
            print("Current best energy", min(self.energies))
            return point, true_energy

        else:
            # print("No new candidate found")
            return point, None
