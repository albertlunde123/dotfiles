from smartSampling import Function, Optimize, Plotting
import random as rnd
import numpy as np
import os
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C
import matplotlib.pyplot as plt

fig, ax = plt.subplots()

func = Function()

def runAllMethods(function, kappa, epsilon, k):

    optimizer = Optimize(function,
                         kappa = kappa,
                         n_initial_points=1)

    # optimizer.run(50,
    #               'complex',
    #               epsilon = epsilon,
    #               k = k)


    for method in optimizer.methods:
        print(method)
        optimizer.run(80,
                      method,
                      kappa = kappa,
                      epsilon = epsilon,
                      k = k)

        plot = Plotting(optimizer,
                        fig = fig,
                        ax = ax)

        plot.plot_guess_progression()
        plot.ax.legend()

    plt.show()

runAllMethods(func,     
              kappa = 2,
              epsilon = 0.1,
              k = 2)
