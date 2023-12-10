import matplotlib.animation as animation
import matplotlib.pyplot as plt

from OptimizeClass import Optimize
from PlottingClass import Plotting
from FunctionClass import Function

from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C

kernel = C(1.0, (1e-3, 1e3)) * RBF(10, (1e-3, 1e2))

class AnimationClass:
    def __init__(self, optimizer, plotter, optimizer_methods, plotter_methods):
        self.optimizer = optimizer
        self.plotter = plotter
        self.optimizer_methods = optimizer_methods
        self.plotter_methods = plotter_methods
        self.fig = self.plotter.get_fig()
        self.animation = None

    def update(self, i):
        self.plotter.ax_arr.clear()
        for method in self.optimizer_methods:
            getattr(self.optimizer, method)()
        for method in self.plotter_methods:
            getattr(self.plotter, method)()

    def animate(self, frames=100):
        # fig = plt.figure()
        self.animation = animation.FuncAnimation(self.fig, self.update, frames=frames)
        self.animation.save('animation.gif', writer='imagemagick', fps=1)

f = Function()
o = Optimize(f)
p = Plotting(o)

a = AnimationClass(o, p, ['expected_improvement_update'], ['plot_function', 'plot_gaussian', 'plot_expected_improvement'])
a.animate(40)

print(o.gp.kernel.get_params())
