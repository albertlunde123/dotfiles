import random as rnd
import numpy as np
import os
import pandas as pd
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C
import matplotlib.pyplot as plt
from multiprocessing import Pool
import time

class Function:
    def __init__(self,
                 bounds = (0 , 100 * np.pi),
                 n_params = 20):
        self.bounds = bounds
        self.parameters = self.generate_random_parameters(n_params)
        self.true_min_value, self.true_min_location = self.find_true_min(1000)

    def generate_random_parameters(self, n):
        params = []
        for i in range(n):
            amplitude = rnd.random()
            phase = rnd.random() * 0.5
            distance = rnd.random()
            params.append([amplitude, phase, distance])
        return params

    def evaluate(self, x):
        y = 0
        for a, p, d in self.parameters:
            y += a * np.sin(x * p) + d
        return y

    def find_true_min(self, n = 1000):
        lower, upper = self.bounds
        x_values = np.linspace(lower, upper, n)
        y_values = [self.evaluate(x) for x in x_values]
        true_minimum_value = np.min(y_values)
        true_minimum_location = x_values[np.argmin(y_values)]
        return true_minimum_value, true_minimum_location

    def get_bounds(self):
        return self.bounds

    def initial_sample(self, n_points):
        lower, upper = self.bounds
        sample_points = [rnd.uniform(lower, upper) for _ in range(n_points)] 
        function_values = [self.evaluate(x) for x in sample_points]
        return sample_points, function_values

class Optimize:
    def __init__(self, function_obj, gp = None, n_initial_points = 5, run_id = None, method = None, kappa = None):
        self.function_obj = function_obj

        if gp == None:
            kernel = C(1.0, (1e-4, 1e3)) * RBF(10, (1e-3, 1e2))
            gp = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=15)

        self.gp = gp
        self.run_id = run_id
        self.y_pred = None
        self.sigma = None
        self.method = method
        self.kappa = kappa
        self.lower_bound, self.upper_bound = self.function_obj.get_bounds()
        self.ts = np.linspace(self.lower_bound,
                              self.upper_bound,
                              1000).reshape(-1, 1)
        self.methods = ["bayesian", 
                        "aquisition",
                        "random",
                        "complex"]

        self.sample, self.values = self.function_obj.initial_sample(n_initial_points)   
        self.initial_sample = self.sample.copy()
        self.initial_values = self.values.copy()
        self.fit_gp()
        self.update_gp_predictions()
        self.average_variance = np.mean(self.sigma)
        self.guesses = []
        self.guesses_location = []
        self.cur = 0

    def fit_gp(self):
        x = np.array(self.sample).reshape(-1, 1)
        y = np.array(self.values).reshape(-1, 1)
        self.gp.fit(x, y)
    
    def update_gp_predictions(self):
        self.y_pred, self.sigma = self.gp.predict(self.ts, return_std = True)
        # print("Time taken for update_gp_predictions: {} seconds".format(time.time() - start_time))

    def bayesian_update(self):
        self.update_gp_predictions()

        guess = np.min(self.y_pred)
        guess_location = self.ts[np.argmin(self.y_pred)][0]
        self.guesses_location.append(guess_index)
        self.guesses.append(guess)

        max_var_index = np.argmax(self.sigma)
        new_sample = self.ts[max_var_index][0]
        new_value = self.function_obj.evaluate(new_sample)

        self.sample.append(new_sample)
        self.values.append(new_value)
        self.fit_gp()
        # print("Time taken for bayesian_update: {} seconds".format(time.time() - start_time))

    def aquisition_update(self, kappa):
        self.update_gp_predictions()

        guess = np.min(self.y_pred)
        guess_location = self.ts[np.argmin(self.y_pred)][0]
        self.guesses_location.append(guess_location)
        self.guesses.append(guess)

        aquisition = -(self.y_pred - kappa * self.sigma)
        max_aquisition_index = np.argmax(aquisition)

        new_sample = self.ts[max_aquisition_index][0]
        new_value = self.function_obj.evaluate(new_sample)

        self.sample.append(new_sample)
        self.values.append(new_value)
        self.fit_gp()

    def random_update(self):
        self.update_gp_predictions()

        guess = np.min(self.y_pred)
        guess_location = self.ts[np.argmin(self.y_pred)][0]
        self.guesses_location.append(guess_location)
        self.guesses.append(guess)

        new_sample = rnd.uniform(self.lower_bound, self.upper_bound)
        new_value = self.function_obj.evaluate(new_sample)

        self.sample.append(new_sample)
        self.values.append(new_value)
        self.fit_gp()

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


    def reset(self):
        self.sample = self.initial_sample.copy()
        self.values = self.initial_values.copy()
        self.fit_gp()
        self.guesses.clear()


    def run(self,
            n_iterations = 5,
            method = 'bayesian',
            kappa = None,
            data_storage = None,
            epsilon = None,
            k = None):

        self.reset()

        if method == 'bayesian':
            update_method = self.bayesian_update
            self.method = 'bayesian'

        elif method == 'random':
            update_method = self.random_update
            self.method = 'random'

        elif method == 'complex':
            def update_method():
                self.complex_update(epsilon = epsilon, k = k)
            self.method = 'complex'

        else:
            def update_method():
                self.aquisition_update(kappa)
            self.method = 'aquisition'
            self.kappa = kappa

        for _ in range(n_iterations):
            update_method()

        final_result = {
            'run_id': self.run_id,
            'best_guess': self.guesses,
            'sample': self.sample,
            'values': self.values
        }

        if data_storage is not None:
            data_storage.store_run(self.run_id,
                                   method,
                                   kappa,
                                   self.guesses[-1],
                                   self.function_obj.true_min_value)

        return final_result

class Plotting:
    def __init__(self, optimizer, colors = ["#24283b",
                                            "#c0caf5",
                                            "#9ece6a",
                                            "#f7768e"],
                 fig = None, ax = None):
        self.optimizer = optimizer
        self.ts = optimizer.ts
        self.foreground = colors[1]
        self.background = colors[0]
        self.highlight = colors[2]
        self.highlight2 = colors[3]
        if fig is None and ax is None:
            self.fig, self.ax = plt.subplots()
        else:
            self.fig = fig
            self.ax = ax
        self.style_fig()
        self.style_ax()

    def style_fig(self):
        self.fig.set_facecolor(self.background)
    
    def style_ax(self):
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['bottom'].set_visible(False)
        self.ax.spines['left'].set_visible(False)
        self.ax.tick_params(axis='x', colors=self.highlight)
        self.ax.tick_params(axis='y', colors=self.highlight)
        self.ax.set_facecolor(self.background)
        self.ax.grid(color=self.highlight, linestyle='-', linewidth=0.25, alpha=0.5)

    def plot_function(self):
        # get values to be plotted
        function_obj = self.optimizer.function_obj
        true_values = [function_obj.evaluate(t) for t in self.ts]
        sample = self.optimizer.sample
        sample_values = self.optimizer.values

        self.ax.plot(self.ts,
                true_values,
                color = self.foreground)

        self.ax.scatter(sample,
                   sample_values,
                   color = self.highlight2)

        self.ax.set_xlabel("x", color = self.highlight)
        self.ax.set_ylabel("y", color = self.highlight)

    def plot_gauss(self):
        y_pred = self.optimizer.y_pred
        sigma = self.optimizer.sigma

        self.ax.plot(self.ts,
                     y_pred,
                     color = self.highlight)
        self.ax.fill(np.concatenate([self.ts, self.ts[::-1]]),
                     np.concatenate([y_pred - 1.9600 * sigma,
                                     (y_pred + 1.9600 * sigma)[::-1]]),
                     alpha = .5,
                     fc = self.highlight)

    def plot_guess_progression(self):

        gx = self.optimizer.guesses_index
        guess = [np.array([i, j]) for i,j in zip(]


        guess_x = np.array(self.optimizer.guesses_index
        guess_y = self.optimizer.guesses
        
        true_x = self.optimizer.function_obj.true_min_index
        true_y = self.optimizer.function_obj.true_min_value
        
        
        distance = np.abs(true_min - guesses)/true_min
        iterations = np.arange(len(guesses))

        def build_label(method, kappa):
            if method == 'bayesian':
                return 'Bayesian'
            elif method == 'random':
                return 'Random'
            elif method == 'complex':
                return 'Complex'
            else:
                return 'Aquisition, kappa = {}'.format(kappa)
    
        self.ax.plot(iterations,
                     distance,
                     linewidth = 2,
                     marker = 'o',
                     # color = self.foreground,
                     # markerfacecolor = self.highlight2,
                     label = build_label(self.optimizer.method, self.optimizer.kappa))

        self.ax.set_xlabel("Iteration", color = self.highlight)
        self.ax.set_ylabel("Relative Error", color = self.highlight)

    def show_plot(self):
        plt.show()

class DataStorage:
    def __init__(self):
        # Initialize an empty DataFrame
        self.df = pd.DataFrame(columns=['Run_ID',
                                        'Method',
                                        'Best_Guess', 
                                        'True_Min',
                                        'Relative_Error'])
        
    def store_run(self, run_id, method, kappa, best_guess, true_min):
        relative_error = np.abs((best_guess - true_min) / true_min)
        self.df = self.df.append({
            'Run_ID': run_id,
            'Method': method,
            'Kappa': kappa,
            'Best_Guess': best_guess,
            'True_Min': true_min,
            'Relative_Error': relative_error
        }, ignore_index=True)
        
    def save_to_csv(self, filename):
        if os.path.exists(filename):
            existing_df = pd.read_csv(filename)
            combined_df = pd.concat([existing_df, self.df])
            combined_df.to_csv(filename, index=False)
        else:
            self.df.to_csv(filename, index=False)
