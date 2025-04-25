import numpy as np
import matplotlib.pyplot as plt

class HarmonicOscillator:

    def __init__(self, k, kT, xs, samples_drawn=100000):
        self.k = k
        self.kT = kT
        self.xs = xs
        self.samples_drawn = samples_drawn

    def setTemperature(self, T):
        self.kT = kT

    def potential(self, x):
        return 0.5 * self.k * x**2
    
    def probabilityDistribution(self, x):
        return np.sqrt(self.k / (2*np.pi * self.kT)) * np.exp(-self.k*x**2 / (2 * self.kT))

    def sample(self, samples_drawn, ho):
        xmax = ho.probabilityDistribution(0)
        x = np.random.uniform(-2, 2, samples_drawn)
        p = np.random.uniform(0, 1, samples_drawn)
        sample = [i for i, j in zip(x, p) if j * xmax <= ho.probabilityDistribution(i)]
        return np.array(sample)

    def MCThermalAverage(self, rounded=True):
        sample = self.sample(self.samples_drawn, self)
        thermalAverage = np.mean(self.potential(sample))
        # print(f"Monte Carlo Thermal Average: {thermalAverage}")

        if rounded:
            return round(np.mean(self.potential(sample)), 2)
        else:
            return np.mean(self.potential(sample))

    def heatCapacityNumerical(self, dT=0.5):

        kT = self.kT

        E1 = self.MCThermalAverage(rounded=False)
        
        T2 = self.kT + dT
        self.setTemperature(T2)
        E2 = self.MCThermalAverage(rounded=False)

        self.setTemperature(kT)
        print(self.kT)

        return (E2 - E1) / dT

    def __str__(self):
        return f"Harmonic Oscillator with k = {self.k} and T = {self.T}"


samples_drawn = 10000
kT = 0.1
k = 1
xs = np.linspace(-2, 2, 100)
ho = HarmonicOscillator(k, kT, xs)
samples = ho.sample(samples_drawn, ho)

print(samples)

fig, ax = plt.subplots(1, 2)
ax = ax.ravel()
ax[0].set_xlim(-2, 2)
ax[0].plot(xs, ho.potential(xs))
ax[0].plot(xs, ho.probabilityDistribution(xs))
ax[0].hist(samples, bins=25, density=True)
ax[0].text(0.1, 0.9, f"Monte Carlo Thermal Average: {ho.MCThermalAverage()}", transform=ax[0].transAxes)
ax[0].text(0.1, 0.8, f"Heat Capacity (Numerical): {ho.heatCapacityNumerical()}", transform=ax[0].transAxes)

kTs = np.linspace(0.01, 0.5, 100)
hos = [HarmonicOscillator(k, kT, xs) for kT in kTs]

cvs_numerical = [ho.heatCapacityNumerical() for ho in hos]
ax[1].plot(kTs, cvs_numerical)

plt.show()
