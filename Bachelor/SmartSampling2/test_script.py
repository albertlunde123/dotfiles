import numpy as np

from FunctionClass import Function
from OptimizeClass import Optimize
from PlottingClass import Plotting

# Initialize a function object
function_obj = Function(bounds=(0, 100 * np.pi), n_params=10)

# Initialize a GaussianProcessRegressor optimizer object
optimizer = Optimize(function_obj)

# Run optimization
optimizer.run(n_iterations=10, method='complex', k = 2, epsilon = 0.1)
print(len(optimizer.guesses))

plotter = Plotting(optimizer, rows=1, cols=2)
ax = plotter.ax_arr.ravel()
# Plot function and samples on the first subplot
plotter.plot_guess_progress(ax[0])
plotter.plot_function(ax[1])
plotter.plot_gaussian(ax[1])
plotter.plot_min(ax[1])
plotter.plot_guess(ax[1])

# Add grid and labels
# plotter.set_labels("iters", "dist")

# Show the plot
plotter.show()
