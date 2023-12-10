import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def getMeanStd(path):

    data = pd.read_csv(path, sep=',')
    relative_error = data['Relative_Error']
    mean_relative_error = np.mean(relative_error)
    std_relative_error = np.std(relative_error)

    return mean_relative_error, std_relative_error

paths = ['aquisition_' + i + '.csv' for i in ['2', '4', '6']]
paths.append('bayesian.csv')
paths.append('random_20.csv')
means = []
stds = []

for path in paths:
    mean, std = getMeanStd(path)
    means.append(mean)
    stds.append(std)

fig, ax = plt.subplots()

ax.errorbar([2, 4, 6, 8, 10], means, yerr=stds, fmt='o')



plt.show()

