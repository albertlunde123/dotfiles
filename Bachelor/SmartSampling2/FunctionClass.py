import random as rnd
import numpy as np

class Function:
    def __init__(self, bounds=(0, 100), n_params=10, lambda_func=None):
        self.bounds = bounds
        self.lambda_func = lambda_func
        if lambda_func is not None:
            self.evaluate = lambda x: self.lambda_func(x)
        self.parameters = self._generate_random_parameters(n_params)
        # Adding a "delta-like" term with a distinct minimum
        self.sharp_params = [rnd.uniform(bounds[0]+10, bounds[1]-10), rnd.uniform(2, 3)]
        self.true_min_value, self.true_min_location = self._find_true_min()

    def _generate_random_parameters(self, n):
        # Restricting the frequency of the sine term based on bounds
        max_frequency = 1 / (self.bounds[1] - self.bounds[0])
        return [[rnd.random()*0.7, rnd.uniform(0.1, 30*max_frequency), rnd.random()*20] for _ in range(n)]

    def get_bounds(self):
        return self.bounds

    def evaluate(self, x):
        sine_sum = sum(a * np.sin(x * p + d) for a, p, d in self.parameters)+1
        mu, sigma = self.sharp_params
        sharp_term = np.exp(-(x - mu)**2 / sigma**2)*2
        return sine_sum - sharp_term

    def _find_true_min(self, n_points=1000):
        lower, upper = self.bounds
        x_values = np.linspace(lower, upper, n_points)
        y_values = [self.evaluate(x) for x in x_values]
        min_value = min(y_values)
        min_location = x_values[y_values.index(min_value)]
        return min_value, min_location

    def initial_sample(self, n_points):
        lower, upper = self.bounds
        x_sample = [rnd.uniform(lower, upper) for _ in range(n_points)]
        x_sample.append(lower)
        x_sample.append(upper)
        y_sample = [self.evaluate(x) for x in x_sample]
        return x_sample, y_sample
