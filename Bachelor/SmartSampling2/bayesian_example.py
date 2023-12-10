
import numpy as np

from FunctionClass import Function
from OptimizeClass import Optimize
from PlottingClass import Plotting

colors = ["white", "black", "red", "blue", "green", "yellow", "orange", "purple", "pink", "brown", "gray", "cyan"]

# Initialize a function object

f = lambda x: np.sin(x*0.05)*np.exp(0.005*x)*0.2 + 1
function_obj = Function(bounds=(0, 100 * np.pi), n_params=1, lambda_func=f)

opt_obj = Optimize(function_obj)
opt_obj.set_sample([0, 100, 120, 314])
opt_obj.fit_and_update_gp()

plot_obj = Plotting(opt_obj, 1, 2, colors = colors)
ax = plot_obj.ax_arr.ravel()
for a in ax:
    a.set_ylim(0, 2)

plot_obj.plot_function(ax = ax[0])
plot_obj.plot_gaussian(0, 1, ax = ax[0])
plot_obj.plot_bayesian(ax = ax[0], scale = 0.3)
plot_obj.plot_samples(ax = ax[0])
plot_obj.set_labels("x", "y", "", ax = ax[0])

opt_obj.bayesian_update()

plot_obj.plot_function(ax = ax[1])
plot_obj.plot_gaussian(0, 1, ax = ax[1])
# plot_obj.plot_bayesian(ax = ax[1])
plot_obj.plot_samples(ax = ax[1])
plot_obj.set_labels("x", "y", "", ax = ax[1])
plot_obj.disable_borders()


plot_obj.show()

