import numpy as np
from FunctionClass import Function
from OptimizeClass import Optimize
from PlottingClass import Plotting
from scipy.stats import norm

f = lambda x: np.sin(x)

fun = Function(bounds=[1, 10], lambda_func=f)
opt = Optimize(fun)
opt.set_sample([1, 2, 3, 4, 10])
opt.fit_and_update_gp()
plot = Plotting(opt)
plot.plot_function()
plot.plot_gaussian()
plot.plot_samples()
plot.disable_borders()
plot.show()
