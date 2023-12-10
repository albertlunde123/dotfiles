from smartSampling import Function, Optimize, Plotting
import numpy as np
import matplotlib.pyplot as plt
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C

bounds = (0, 100 * np.pi)
n_params = 20
kernel = C(1.0, (1e-4, 1e3)) * RBF(10, (1e-3, 1e2))
gp = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=10)

function = Function(bounds, n_params)
optimizer = Optimize(function, gp)
# optimizer.run(70, kappa = 0)

fig, ax = plt.subplots(2, 2, figsize=(10, 10))
ax = ax.ravel()


for a, i in zip(ax, [10, 20, 40, 80]):
    optimizer.run(i, method = 'aquistion', kappa = 0)
    optimizer.sigma = optimizer.sigma * 0.5
    plot = Plotting(optimizer, fig = fig, ax = a)
    plot.plot_function()
    plot.plot_gauss()
    a.set_title('Iterations: {}'.format(i),
                color = plot.foreground,
                fontsize = 20)

# plot = Plotting(optimizer)
# # plot.plot_function()
# plot.plot_guess_progression()
# plot.plot_gauss()
plot.show_plot()

