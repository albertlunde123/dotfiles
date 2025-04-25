import numpy as np
import matplotlib.pyplot as plt

def potential(x ,k):
    return 0.5 * k * x**2

def probabilityDistribution(x, k, T):
    return np.sqrt(k / (2*np.pi * T)) * np.exp(-k*x**2 / (2 * T))

def metropolisMonteCarloSampling(x0, k, T, N, D):
    # N is the number of samples
    # D is the proposal distribution
    # x0 is the initial state
    samples = []
    pD = lambda x: probabilityDistribution(x, k, T)
    for _ in range(N):
        x = x0 + D()
        if np.random.rand() <= min([1, pD(x) / pD(x0)]):
            x0 = x
        samples.append(x0)
    return samples

kT = 0.1
k = 1
x0 = 0
xs = np.linspace(-2, 2, 100)

# We try a normal distribution as the proposal distribution

D = lambda: 0.1 * np.random.normal(0, 1)

fig, ax = plt.subplots(2, 2, figsize=(10, 5))
ax = ax.flatten()

fig.suptitle('Metropolis MC - Normal Distribution Proposal')
for i, N in enumerate([100, 1000, 10000, 100000]):
    ax[i].hist(metropolisMonteCarloSampling(x0, k, kT, N, D), bins=25, density=True, alpha=0.5)
    ax[i].plot(xs, potential(xs, k), label='Potential')
    ax[i].plot(xs, probabilityDistribution(xs, k, kT))
    ax[i].set_title(f'N = {N}')

# plt.legend()
plt.savefig('normalDistribution.png')

# We try a uniform distribution as the proposal distribution

D = lambda: 4 * np.random.rand() - 2

fig, ax = plt.subplots(2, 2, figsize=(10, 5))
fig.suptitle('Metropolis MC - Uniform Distribution Proposal')
ax = ax.flatten()

for i, N in enumerate([100, 1000, 10000, 100000]):
    ax[i].hist(metropolisMonteCarloSampling(x0, k, kT, N, D), bins=25, density=True, alpha=0.5)
    ax[i].plot(xs, potential(xs, k), label='Potential')
    ax[i].plot(xs, probabilityDistribution(xs, k, kT))
    ax[i].set_title(f'N = {N}')

# plt.legend()
plt.savefig('uniformDistribution.png')
plt.show()
