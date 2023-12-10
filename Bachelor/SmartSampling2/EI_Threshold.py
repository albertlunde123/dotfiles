#Illustration of expected improvement (EI)
import numpy as np

from FunctionClass import Function
from OptimizeClass import Optimize
from PlottingClass import Plotting

from scipy.stats import norm

# f = lambda x: np.sin(x + 2.5) * 10 - x + x**2/100
f = lambda x: np.sin(x) + 0.2*x

# Create function object

function_obj = Function(bounds=[2, 13], lambda_func = f)

# Create optimize object

optimize_obj = Optimize(function_obj)
optimize_obj.set_sample([2, 3.8, 6, 13])
optimize_obj.fit_and_update_gp()

# Get EI

def EI(mu, sigma, sample, eps):
    EI = np.array([])
    i = 0
    for sigma, mu in zip(sigma, mu):
        i += 1
        if sigma == 0:
            EI = np.append(EI, 0)
        else:
            z = (np.min(sample) - mu - eps)/sigma
            EI_ = (np.min(sample) - mu - eps)*norm.cdf(z) + sigma*norm.pdf(z)
            EI = np.append(EI, EI_)
    return EI

x = np.linspace(2, 13, 1000)
mu, sigma = optimize_obj.gp.predict(x.reshape(-1, 1), return_std = True)
EI = EI(mu, sigma, optimize_obj.sample, 0.2)

sigma = sigma * 0.5
EI_center, EI_sigma = mu[np.argmax(EI)], sigma[np.argmax(EI)]

gauss = lambda y: 0.3 * norm.pdf(y, loc = EI_center, scale = EI_sigma) + x[np.argmax(EI)]



def plot_EI_gaussian(point, plot_obj, k = 0.3, sig_fac = 4, b = 1):

    EI_center, EI_sigma = mu[point], sigma[point]
    gauss = lambda y: k * norm.pdf(y, loc = EI_center, scale = EI_sigma*b) + x[point]

    ys = np.linspace(EI_center - sig_fac*EI_sigma, EI_center + sig_fac*EI_sigma, 100)

    plot_obj.ax_arr.plot(gauss(ys), ys, color = 'purple', linewidth = 1)

    ys_2 = np.linspace(EI_center - sig_fac * EI_sigma, 0.143, 1000)
    x1 = x[point] * np.ones(len(ys_2))
    x2 = gauss(ys_2)

    plot_obj.ax_arr.fill_betweenx(ys_2, x1, x2, color = 'purple', alpha = 0.5, edgecolor = 'black', linewidth = 0)

# Create plotting object

colors = ['w', 'black', 'g', 'black', 'm', 'c', 'k']

plotting_obj = Plotting(optimize_obj, 1, 1, colors = colors)
plotting_obj.optimizer.sigma = plotting_obj.optimizer.sigma
plotting_obj.optimizer.sigma[370:] = plotting_obj.optimizer.sigma[370:] * 0.7
plotting_obj.plot_gaussian(alpha = 0.2, border = False)
plotting_obj.optimizer.sigma[370:] = plotting_obj.optimizer.sigma[370:] / 0.7 * 0.5

plotting_obj.plot_expected_improvement(delta = 0, sig = plotting_obj.optimizer.sigma)

plotting_obj.disable_borders()


plotting_obj.ax_arr.plot(x, [np.min(optimize_obj.values)]*len(x), color = 'orange', linewidth = 1, linestyle = '-')
plotting_obj.plot_samples()


# Add some text to the plot, ensuring that it will be rendered using LaTeX font

plotting_obj.ax_arr.text(2,
                         -2,
                         r'$\delta = 0$',
                         fontsize = 20,
                         weight = 'bold')




plotting_obj.tight()

# plotting_obj.ax_arr.set_title('Expected Improvement', fontsize = 20)
# plotting_obj.show()
plotting_obj.save("../Rapport/figures/EI/EI_Threshold1.png")
