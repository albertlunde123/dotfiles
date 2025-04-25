import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

def V(x):
    return (-1  -np.exp(-((x+15)/10)**2) \
              -2*np.exp(-((x-10)/10)**2) + \
                -np.exp(-((x-35)/10)**2) \
              -3*np.exp(-((x-60)/10)**2) \
                -np.exp(-((x-85)/10)**2)\
              -2*np.exp(-((x-110)/10)**2) \
              ) * \
            (1+1/5*np.cos(2*np.pi/2.5*x))

def MonteCarloOptimization(f, x0, T, steps):
    D = lambda a: min(1, np.exp(-a / T))

    energies = []
    xs = []

    x = x0
    # print(x)

    for _ in range(steps):
        if f(x) < -4.75:
            break
        x_new = x + np.random.normal(0, 1)
        # print(x_new)
        if np.random.uniform() <= D(f(x_new) - f(x)):
            x = x_new
        xs.append(x)
        energies.append(f(x))
        x0 = x

    return xs, energies

def runExperiment(V, T, steps):

    threshold = -4.75
    start_value = np.random.uniform(-10, 110)

    points, energies = MonteCarloOptimization(V, start_value, T, steps)
    t_to_fin = len(points)
    if t_to_fin == steps:
        return steps + 1
    return t_to_fin
    # for i, e in enumerate(energies):
    #     if e < threshold:
    #         return i
    # return steps + 1

def runExperiments(V, T, steps, n):

    results = []
    for _ in range(n):
        result = runExperiment(V, T, steps)
        if result < steps:
            results.append(result)
    return results

def success_curve(results, max_steps=1000):
   
    results = np.sort(results)
    indexes = np.unique(results, return_index=True)[1]
    
    x_data = results[indexes]
    y_data = [i/max_steps for i in np.append(indexes[1:], len(results))]
    return x_data, y_data
    # success_rate = []
    # steps = []
    

    # for i in indexes:
    #     success_rate.append(indexes[1][i]/len(results))
    #     steps.append(i)

    # return success_rate, steps

xs = np.linspace(-10, 110, 1000)
ys = V(xs)
x0 = 2.8
T = 2
steps = 10000

fig, ax = plt.subplots()
results = runExperiments(V, T, steps, 100)
xs, ys = success_curve(results)
ax.plot(xs, ys, 'k')

plt.show()

#####################
# 4.2
# points, energies = MonteCarloOptimization(V, x0, T, steps)

# fig, ax = plt.subplots(1, 2)
# ax = ax.ravel()

# ax[0].plot(xs, ys)
# for i, p, e in zip(range(1, 9), points, energies):
#     ax[0].plot(p, e, 'ko', alpha=i/len(points))

# ax[0].set_xlim(np.min(points)-5, np.max(points)+5)
# ax[0].set_ylim(np.min(energies)-1, np.max(energies)+1)
# steps = range(1, len(points)+1)
# ax[1].plot(points, steps, 'k')
# for i, s, e in zip(range(1, 9), points, steps):
#     ax[1].plot(s, e, 'ko', alpha=i/len(points))

# ax[1].set_xlim(np.min(points)-5, np.max(points)+5)
# plt.show()
#####################

#####################
# 4.3
# def update(i):
#     walker.set_data(points[i], energies[i])
#     return [walker]

# points, energies = MonteCarloOptimization(V, x0, T, steps)
# fig, ax = plt.subplots()

# ax.plot(xs, ys)
# walker = ax.plot(points[0], energies[0], 'ko')[0]

# anim = animation.FuncAnimation(fig,
#                                update,
#                                frames=steps,
#                                interval=100,
#                                blit=True)

# plt.show()
#####################



