import numpy as np

from FunctionClass import Function
from OptimizeClass import Optimize
from PlottingClass import Plotting

def shouldTerminate(x, sample, eps):

    for i in range(len(sample)):
        if abs(x - sample[i]) < eps:
            return True

    return False

def runExperiment(n, iters):

    results = []

    for i in range(n):

        func = Function(n_params = 20, bounds = (0, 1000))
        true_min = func.true_min_location

        opt = Optimize(func)

        for j in range(iters):

            opt.aquisition_update(2)

            print("Iteration: ", j)
            print("True Min: ", true_min)
            print("Current Sample: ", opt.sample[-1])
            print("Distance: ", abs(true_min - opt.sample[-1]))

            if shouldTerminate(true_min, opt.sample, 0.01):
                results.append(j)
                break

    plot = Plotting(opt)

    plot.plot_function()
    plot.plot_samples()
    plot.plot_gaussian(alpha = 0.2)

    plot.show()

    return results

results = runExperiment(1, 100)

print(results)




