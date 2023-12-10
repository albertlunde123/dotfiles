import numpy as np

from FunctionClass import Function
from OptimizeClass import Optimize
from PlottingClass import Plotting

# import gaussian function

from scipy.stats import norm

colors = ["white", "green", "orange", "black", "purple", "yellow", "orange", "purple", "pink", "brown", "gray", "cyan"]

# Initialize a function object



f = lambda x: (np.sin(x)*0.5) * np.exp(-x/6)

function_obj = Function(bounds=(0, 3 * np.pi), n_params=1, lambda_func=f)

opt_obj = Optimize(function_obj)
opt_obj.set_sample([0, 0.0094, 1.0, 5, 8, 9.41, opt_obj.ts[-1]])
opt_obj.fit_and_update_gp()

plot_obj = Plotting(opt_obj, 1, 1, colors = colors)
# ax = plot_obj.ax_arr.ravel()
# for a in ax:
#     a.set_ylim(-1, 0.5)

# plot_obj.plot_function(color = 3)
plot_obj.plot_gaussian(0.2, 1)
plot_obj.plot_expected_improvement()
plot_obj.plot_samples()
plot_obj.set_labels("x", "y", "")
plot_obj.disable_borders()

opt_obj.expected_improvement_update()

# plot_obj.plot_function(ax = ax[1])
# plot_obj.plot_gaussian(0, 1, ax = ax[1])
# plot_obj.plot_expected_improvement(ax = ax[1])
# # plot_obj.plot_bayesian(ax = ax[1])
# plot_obj.plot_samples(ax = ax[1])
# plot_obj.set_labels("x", "y", "", ax = ax[1])


# plot_obj.show()
plot_obj.save("../Rapport/figures/EI/EI_example.png")
