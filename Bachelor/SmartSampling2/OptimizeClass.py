import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C
from scipy.stats import norm

class Optimize:
    def __init__(self, function_obj, gp=None, n_initial_points=1, run_id=None, method=None, kappa=None):
        self.setup_initial_state(function_obj, gp, n_initial_points, run_id, method, kappa)
        self.fit_and_update_gp()
        self.guesses = []
        self.guesses_location = []
        self.cur = 0

    def setup_initial_state(self, function_obj, gp, n_initial_points, run_id, method, kappa):
        self.function_obj = function_obj
        self.kernel = C(1, (1e-4, 1e3)) * RBF(2, (1e-3, 1e2))
        self.gp = gp or GaussianProcessRegressor(kernel=self.kernel, alpha =1e-5, n_restarts_optimizer=50)
        # self.gp = gp or GaussianProcessRegressor(kernel=C(1.0, (1e-4, 1e3)) * RBF(10, (1e-3, 1e2)), n_restarts_optimizer=15)
        self.run_id, self.method, self.kappa = run_id, method, kappa
        self.lower_bound, self.upper_bound = self.function_obj.get_bounds()
        self.ts = np.linspace(self.lower_bound, self.upper_bound, 1000).reshape(-1, 1)
        self.sample, self.values = self.function_obj.initial_sample(n_initial_points)
        self.initial_sample, self.initial_values = self.sample.copy(), self.values.copy()

    def set_sample(self, sample):
        self.sample = [float(x) for x in sample]
        self.values = [self.function_obj.evaluate(x) for x in self.sample]


    def reset(self):
        self.sample, self.values = self.initial_sample.copy(), self.initial_values.copy()
        self.fit_and_update_gp()
        self.guesses = []
        self.guesses_location = []
        self.cur = 0

    def fit_and_update_gp(self):
        self.fit_gp()
        self.update_gp_predictions()

    def fit_gp(self):
        # print("Sample shape:", np.shape(self.sample))
        # print(self.sample)
        # print(self.values)
        self.gp.fit(np.array(self.sample).reshape(-1, 1), np.array(self.values).reshape(-1, 1))

    def update_gp_predictions(self):
        self.y_pred, self.sigma = self.gp.predict(self.ts, return_std=True)

    def update_guesses(self, guess, guess_location):
        self.guesses.append(guess)
        self.guesses_location.append(guess_location)

    def update_samples(self, new_sample, new_value):
        self.sample.append(float(new_sample))
        self.values.append(float(new_value))
        self.fit_and_update_gp()

    def random_update(self): 
        new_sample = np.random.uniform(self.lower_bound, self.upper_bound)
        new_value = self.function_obj.evaluate(new_sample)
        self.update_guesses(new_value, new_sample)
        self.update_samples(new_sample, new_value)

    def bayesian_update(self):
        guess, guess_location = np.min(self.y_pred), self.ts[np.argmin(self.y_pred)][0]
        new_sample = self.ts[np.argmax(self.sigma)][0]
        new_value = self.function_obj.evaluate(new_sample)
        self.update_guesses(guess, guess_location)
        self.update_samples(new_sample, new_value)

    def aquisition_update(self, kappa):
        aquisition = -(self.y_pred - kappa * self.sigma)
        max_aquisition_index = np.argmax(aquisition)
        new_sample, new_value = self.ts[max_aquisition_index][0], self.function_obj.evaluate(self.ts[max_aquisition_index][0])
        guess, guess_location = np.min(self.y_pred), self.ts[np.argmin(self.y_pred)][0]
        self.update_guesses(guess, guess_location)
        self.update_samples(new_sample, new_value)

    def complex_update(self, epsilon, k):

        self.update_gp_predictions()

        mean_var = np.mean(self.sigma)

        if self.cur == 0:
            print("bayesian")
            if self.average_variance < mean_var * k:
                self.bayesian_update()
            else:
                self.average_variance = mean_var
                self.cur = 1
                self.aquisition_update(0)
        else:
            print("aquisition")
            self.aquisition_update(0)
            if np.abs(self.guesses[-1] - self.guesses[-2]) < epsilon:
                self.cur = 0
                self.average_variance = np.mean(self.sigma)
            self.bayesian_update()


    def expected_improvement_update(self):
        # print("EI NEW ITERATION")
        y_min = min(self.values)  # Currently best sampled point

        # Initialize variables to store maximum EI and corresponding x
        max_ei = -1
        x_next = None

        for x in self.ts:  # Assuming self.ts is your search space
            x = x.reshape(1, -1)  # Make sure x is 2D
            mu, sigma = self.gp.predict(x, return_std=True)

            if sigma != 0:  # To avoid division by zero
                z = (y_min - mu - 0.2) / sigma
                ei = (y_min - mu - 0.2) * norm.cdf(z) + sigma * norm.pdf(z)

            else:
                ei = 0

            # if x in self.sample:
            #     # To avoid evaluating at the same point twice
            #     ei = 0

            if ei > max_ei:
                max_ei = ei
                x_next = x
        
        # print("X_NEXT:", x_next)
        y_next = self.function_obj.evaluate(x_next[0])  # Evaluate the function at the next point

        self.update_guesses(y_next, x_next) 
        self.update_samples(x_next, y_next)# Update guesses (your existing method)

    def run(self,
            n_iterations=5,
            method='bayesian',
            kappa=None, 
            data_storage=None, 
            epsilon=None, 
            k=None):

        self.reset()

        update_methods = {
            'bayesian': self.bayesian_update,
            'random': self.random_update,
            'aquisition': lambda: self.aquisition_update(kappa),
            'complex': lambda: self.complex_update(epsilon=epsilon, k=k),
            'expected_improvement': self.expected_improvement_update
        }

        if method not in update_methods:
            raise ValueError(f"Invalid method: {method}. Valid methods are {list(update_methods.keys())}.")

        self.method = method
        self.kappa = kappa

        update_method = update_methods[method]

        for _ in range(n_iterations):
            update_method()

        if data_storage is not None:
            data_storage.store_run(self.run_id, method, kappa, self.guesses[-1], self.function_obj.true_min_value)

        return {
            'run_id': self.run_id,
            'best_guess': self.guesses,
            'sample': self.sample,
            'values': self.values
        }

