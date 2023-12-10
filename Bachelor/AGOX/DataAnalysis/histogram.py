import pickle
import numpy as np
import matplotlib.pyplot as plt

def get_the_pickle_files(path):
    paths = []
    paths.append(path + "best_energies.pckl")
    paths.append(path + "best_structure.pckl")
    paths.append(path + "energies.pckl")
    paths.append(path + "names.pckl")
    paths.append(path + "order.pckl")
    return paths



# Ok, lets just give it a try.

def get_best_energy(data):

    min_energy = 100

    for i in range(len(data)):
        if min(data[i]) < min_energy:
            min_energy = min(data[i])

    return min_energy

def count_iters_to_best_energy(data, min_energy = None):

    if min_energy == None:
        min_energy = get_best_energy(data)
    iters = []

    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j] - min_energy < 0.5:
                iters.append(j)
                break

    for i in range(len(data) - len(iters)):
        iters.append("nope")

    return iters

def success_rate(data):

    min_energy = get_best_energy(data)
    iters = count_iters_to_best_energy(data)

    success = 0

    for i in range(len(data)):
        if iters[i] != "nope":
            success += 1

    return success / len(data)

def plot_cumulative_histogram(data, bins=range(0, 101, 10), ax=None, min_energy = None):

    if min_energy == None:
        min_energy = get_best_energy(data)

    iters = count_iters_to_best_energy(data, min_energy)
    numeric_data = [x for x in iters if x != "nope"]
    
    num_sucesses = len(numeric_data)
    num_attempts = len(data)

    bins = range(0, 101, 10)

    hist, _ = np.histogram(numeric_data, bins=bins)
    cum_hist = np.cumsum(hist)
    success_rate = cum_hist / num_attempts

    ax.plot(bins[:-1], success_rate, drawstyle='steps-post')
    ax.set_ylim(0, 1)

fig, ax = plt.subplots()

# Load the data

paths = ["../MyScripts/EI_relax/BA_data/",
         "../MyScripts/aqui_relax/BA_data/",
         "../MyScripts/pure_energy/BA_data/"]
paths = [get_the_pickle_files(path) for path in paths]

min_energy = min([get_best_energy(pickle.load(open(path[0], 'rb'))) for path in paths])

for path in paths:
    with open(path[0], 'rb') as f:
        data = pickle.load(f)
        plot_cumulative_histogram(data, ax=ax, min_energy = min_energy)

# plot_cumulative_histogram(data, ax=ax)
plt.show()
