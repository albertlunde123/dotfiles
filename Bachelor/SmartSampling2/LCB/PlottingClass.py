import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm


class Plotting:
    def __init__(self, optimizer, rows=1, cols=1, colors=None):
        self.optimizer = optimizer
        self.ts = optimizer.ts


        self.colors = colors if colors else ["#24283b",
                                             "#c0caf5",
                                             "#9ece6a",
                                             "#f7768e",
                                             "#e0af68"]
        # plt.rcParams['font.family'] = 'serif'
        plt.rcParams['font.weight'] = 'bold'
        # plt.rcParams['font.size'] = 20
        plt.rcParams['text.color'] = self.colors[1]
        plt.rcParams['text.usetex'] = True

        self.fig, self.ax_arr = plt.subplots(rows, cols)
        self._set_defaults()

    # DATA ANALYSIS METHODS

    def get_fig(self):
        return self.fig

    def distance_to_optimum(self):
        dist = []
        gy = self.optimizer.guesses
        gx = self.optimizer.guesses_location
        x = [self.optimizer.function_obj.true_min_location for _ in range(len(gx))]
        y = [self.optimizer.function_obj.true_min_value for _ in range(len(gy))]
        for i in range(len(gx)):
            dist.append(np.linalg.norm(np.array([gx[i], gy[i]]) - np.array([x[i], y[i]])))
        return dist


    # PLOTTING METHODS
    def _set_defaults(self):
        self.fig.set_facecolor(self.colors[0])
        
        if isinstance(self.ax_arr, np.ndarray):
            for ax in np.ravel(self.ax_arr):
                self._style_ax(ax)
        else:
            self._style_ax(self.ax_arr)

    def disable_borders(self, ax = None):
        ax = ax if ax else self._get_default_ax()
        
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.tick_params(axis='x', colors="white")
        ax.tick_params(axis='y', colors="white")
        ax.yaxis.label.set_color("white")
        ax.xaxis.label.set_color("white")


    def _style_ax(self, ax):
        ax.spines['top'].set_color(self.colors[1])
        ax.spines['right'].set_color(self.colors[1])
        ax.spines['bottom'].set_color(self.colors[1])
        ax.spines['left'].set_color(self.colors[1])
        # ax.spines['top'].set_visible(False)
        # ax.spines['right'].set_visible(False)
        # ax.spines['bottom'].set_visible(False)
        # ax.spines['left'].set_visible(False)
        ax.tick_params(axis='x', colors=self.colors[1])
        ax.tick_params(axis='y', colors=self.colors[1])
        ax.yaxis.label.set_color(self.colors[1])
        ax.xaxis.label.set_color(self.colors[1])
        ax.title.set_color(self.colors[1])
        ax.set_facecolor(self.colors[0])

    def _get_default_ax(self):
        if isinstance(self.ax_arr, np.ndarray):
            return self.ax_arr[0, 0]
        else:
            return self.ax_arr

    def set_labels(self, x_label, y_label, title, ax = None):
        ax = ax if ax else self._get_default_ax()
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.set_title(title)

    def plot_function(self, ax = None, linestyle = '--', linewidth = 1, color = 1):
        ax = ax if ax else self._get_default_ax()
        function_obj = self.optimizer.function_obj
        true_values = [function_obj.evaluate(t) for t in self.ts]
        ax.plot(self.ts,
                true_values,
                linestyle='--',
                linewidth=1,
                color=self.colors[1])

    def plot_samples(self, ax = None):
        ax = ax if ax else self._get_default_ax()
        sample = self.optimizer.sample
        values = self.optimizer.values
        ax.plot(sample,
                values,
                marker='o',
                markersize=5,
                linewidth=0,
                color=self.colors[3])

    def plot_gaussian(self, alpha = 0.5, i = 2, ax = None, border = False):
        ax = ax if ax else self._get_default_ax()
        y_pred = self.optimizer.y_pred
        sigma = self.optimizer.sigma
        ax.plot(self.ts, y_pred, color=self.colors[i])
        ax.fill_between(self.ts.flatten(), y_pred - 1.9600 * sigma, y_pred + 1.9600 * sigma, alpha=alpha, color=self.colors[i])
        if border:
            ax.plot(self.ts, y_pred - 1.9600 * sigma, color=self.colors[i], linewidth=0.5)
            ax.plot(self.ts, y_pred + 1.9600 * sigma, color=self.colors[i], linewidth=0.5)

    def plot_guess_progress(self, ax = None, color = 3):
        ax = ax if ax else self._get_default_ax()
        dist = self.distance_to_optimum()
        iters = [i+1 for i in range(len(dist))]
        ax.set_ylim([0, max(dist) + 0.1])
        ax.plot(iters,
                dist,
                linestyle='--',
                marker='o',
                markersize=7,
                markerfacecolor=self.colors[color],
                color=self.colors[color])

    def plot_guess(self, ax = None):
        ax = ax if ax else self._get_default_ax()
        guesses = self.optimizer.guesses[-1]
        guesses_location = self.optimizer.guesses_location[-1]
        ax.scatter(guesses_location, guesses, color=self.colors[3]) 

    def plot_min(self, ax = None):
        ax = ax if ax else self._get_default_ax()
        true_min_location = self.optimizer.function_obj.true_min_location
        true_min_value = self.optimizer.function_obj.true_min_value
        ax.scatter(true_min_location, true_min_value, color=self.colors[2])

    def plot_aquisition(self, kappa = 2, ax = None):
        ax = ax if ax else self._get_default_ax()
        aquisition = self.optimizer.y_pred - kappa * self.optimizer.sigma
        min_aquisition = np.min(aquisition)
        min_aquisition_location = self.ts[np.argmin(aquisition)]
        ax.plot(self.ts,
                aquisition,
                color=self.colors[4],
                linestyle='--')
        ax.plot(min_aquisition_location,
                min_aquisition,
                marker='o',
                markersize=7,
                markerfacecolor=self.colors[4],
                color=self.colors[4],
                linewidth=0)

    def plot_expected_improvement(self, ax = None, delta = 0.2, sig = None):
        ax = ax if ax else self._get_default_ax()
        # Extract needed information from the Optimize object
        gp = self.optimizer.gp
        y_min = min(self.optimizer.values)
        true_min = self.optimizer.function_obj.true_min_value 
        ts = self.optimizer.ts  # Assuming this is your search space

        # Initialize variables to store EI values
        EI_values = []

        # Calculate Expected Improvement for each point in the search space
        i = -1
        for x in ts:
            i += 1
            x = x.reshape(1, -1)  # Make sure x is 2D

            if sig is None:
                sigma = gp.predict(x, return_std=True)[1]
            else:
                sigma = sig[i]

            mu = gp.predict(x, return_std=True)[0]

            if sigma > 1e-15:  # To avoid division by zero
                z = (y_min - mu - delta) / sigma
                ei = (y_min - mu - delta) * norm.cdf(z) + sigma * norm.pdf(z)
            else:
                ei = 0

            EI_values.append(ei)
        
        max_EI = np.max(EI_values)
        for i in range(len(EI_values)):
            EI_values[i] = (EI_values[i]/max_EI-1-np.abs(true_min))*2 - 3

        
        # ax.text(0.5,
        #         np.max(EI_values),
        #         'Expected Improvement',
        #         color = "black")
        
        # ax.plot(ts,
        #         [np.max(EI_values) + 0.1] * len(ts),
        #         linestyle='-',
        #         linewidth=0.5,
                # color="black")

        # Plot EI values
        ax.plot(ts,
                 EI_values,
                 linestyle='-',
                 linewidth=0.5,
                 color=self.colors[4],
                 label='Expected Improvement')

        ax.plot(ts,
                (y_min - delta)*np.ones(len(ts)),
                linestyle='-',
                linewidth=2,
                color=self.colors[4],
                label='True Minimum')

        ax.fill_between(ts.flatten(),
                        np.array(EI_values).flatten(),
                        np.min(EI_values),
                        color=self.colors[4],
                        alpha=0.5)


    def plot_bayesian(self, ax = None, scale = 1):
        ax = ax if ax else self._get_default_ax()
        max_variance = np.max(self.optimizer.sigma)
        max_variance_location = self.ts[np.argmax(self.optimizer.sigma)]
        ax.plot(self.ts,
                self.optimizer.sigma*scale,
                color=self.colors[4],
                linestyle='--')
        ax.plot(max_variance_location,
                max_variance*scale,
                marker='o',
                markersize=7,
                markerfacecolor=self.colors[4],
                color=self.colors[4],
                linewidth=0)

    def show(self):
        plt.show()

    def tight(self):
        plt.tight_layout()

    def save(self, path):
        plt.savefig(path)

