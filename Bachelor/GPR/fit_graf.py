import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal

X  = np.linspace(0, 10, 200)

# construction of the GP prior

def kernel(x1, x2):
    return np.exp(-0.5 * (x1 - x2)**2)  

def cov_matrix(X, Y,  kernel):
    C = np.zeros((len(X), len(Y)))
    for i in range(len(X)):
        for j in range(len(Y)):
            C[i, j] = kernel(X[i], Y[j])
    return C

data = np.linspace(0, 10, 5)
y = np.sin(data)

def GPR_predict(prediction_point, X, y, kernel):
    C = cov_matrix(X, X, kernel)
    C_inv = np.linalg.inv(C)
    C_star = cov_matrix(X, prediction_point, kernel)
    C_star_star = cov_matrix(prediction_point, prediction_point, kernel)
    mu = C_star.T @ C_inv @ y
    sigma = C_star_star - C_star.T @ C_inv @ C_star
    return mu, sigma

mu, sigma = GPR_predict(X, data, y, kernel) 

fig, ax = plt.subplots()

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)

plt.tick_params(color = "white")
plt.xticks([])
plt.yticks([])

ax.grid(color='grey', linestyle='-', linewidth=5, alpha=0.5)

x_max, x_min = -0.5, 10.5
# y_max, y_min = np.max(samples) + 1, np.min(samples) - 0.2
# ax.set_ylim(y_min, y_max)

ax.set_xlim(x_min, x_max)

plt.rcParams.update({
    "pgf.texsystem": "pdflatex",
    "font.family": "serif",  # use serif/main font for text elements
    "text.usetex": True,     # use inline math for ticks
})


def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

# col1 and col2 should be specified in rgb
def gradient(col1, col2, width):
    colors = []

    diffs = [int((j - i)/width) for j,i in zip(col1, col2)]
    for i in range(width):
        col = [k + j*i for k,j in zip(col2, diffs)]
        colors.append(rgb_to_hex(tuple(col)))

    return colors

colors = [(151, 43, 196),
          (33, 130, 4),
          (240, 133, 2),
          (0, 0, 0)]

colors = [rgb_to_hex(colors[i]) for i in range(len(colors))]

ax.plot(X, mu, color=colors[0], linewidth=2,
        label = "GPR")
ax.fill_between(X, mu - 2*np.sqrt(np.diag(sigma)), mu + 2*np.sqrt(np.diag(sigma)), color=colors[1], alpha=0.2)
ax.plot(X, np.sin(X), color=colors[2], linewidth=2,
        label = "True function")
ax.plot(data, y, color=colors[3], marker='o', linestyle='None', markersize=8)
ax.legend(loc='upper right', frameon=True, fontsize=14)

props = dict(boxstyle = 'square, pad=0.5',
            facecolor = '#ffffff',
            edgecolor = '#000000'
)

text = r"$\Sigma(x_i, x_j) = \exp\left(\frac{\left(x_i - x_j\right)^2}{2}\right)$"
# ax.text(0.05, 0.95, text, bbox=props, transform=ax.transAxes, fontsize=14)
ax.set_title(r"Gaussian Process Regression$", fontsize=16)
# plt.show()
fig.savefig('../Rapport/figures/GPR/GP_posterior.jpg')
