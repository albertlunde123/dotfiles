import numpy as np

from FunctionClass import Function
from OptimizeClass import Optimize
from PlottingClass import Plotting

colors = []

# Initialize a function object

f = lambda x: np.sin(x*0.1)*np.exp(-0.01*x) + 0.3*np.cos(x*0.05)
function_obj = Function(bounds=(0, 100 * np.pi), n_params=1, lambda_func=f)

opt_obj = Optimize(function_obj)
opt_obj.set_sample([0, 200, 210, 314])
opt_obj.fit_and_update_gp()

plot_obj = Plotting(opt_obj, 1, 2)
ax = plot_obj.ax_arr.ravel()

plot_obj.plot_function(ax = ax[0])
plot_obj.plot_gaussian(0, 1, ax = ax[0])
plot_obj.plot_aquisition(2, ax = ax[0])
plot_obj.plot_samples(ax = ax[0])
plot_obj.set_labels("x", "y", "Aquisition Method: $\kappa = 2$", ax = ax[0])

opt_obj.aquisition_update(2)

plot_obj.plot_function(ax = ax[1])
plot_obj.plot_gaussian(0, 1, ax = ax[1])
plot_obj.plot_aquisition(2, ax = ax[1])
plot_obj.plot_samples(ax = ax[1])
plot_obj.set_labels("x", "y", "Aquisition Method: $\kappa = 2$", ax = ax[1])


plot_obj.show()

