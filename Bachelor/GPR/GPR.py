import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal

X = np.linspace(0, 10, 100)

def kernel(x1, x2):
    return np.exp(-0.5 * (x1 - x2)**2)  

# def kernel(x1, x2):
#     if x1 == x2:
#         return 1
#     return 0.1

def cov_matrix(X, Y,  kernel):
    C = np.zeros((len(X), len(Y)))
    for i in range(len(X)):
        for j in range(len(Y)):
            C[i, j] = kernel(X[i], Y[j])
    return C

X = np.linspace(0, 10, 5)
y = np.sin(X)

CX = cov_matrix(X, X, kernel)
inv_CX = np.linalg.inv(CX)

XX = np.linspace(0, 10, 100)
CXX = cov_matrix(XX, XX, kernel)
CXX_X = cov_matrix(XX, X, kernel)
mu = np.dot(np.dot(CXX_X, inv_CX), y)
sigma = CXX - np.dot(np.dot(CXX_X, inv_CX), CXX_X.T)
sample = multivariate_normal.rvs(mu, sigma, 1)
plt.plot(XX, mu, 'g-')

for i in XX:
    CXX_i = cov_matrix([i], [i], kernel)
    CXX_X_i = cov_matrix([i], X, kernel)
    mu_i = np.dot(np.dot(CXX_X_i, inv_CX), y)
    sigma_i = CXX_i - np.dot(np.dot(CXX_X_i, inv_CX), CXX_X_i.T)
    sample_i = multivariate_normal.rvs(mu_i, sigma_i, 1)
    plt.scatter(i, mu_i, c='b', s=10)

plt.plot(X, y, 'ro')
plt.plot(XX, np.sin(XX), 'r-')
# plt.plot(XX, sample.T, 'b-')
plt.fill_between(XX, mu - 2 * np.sqrt(np.diag(sigma)), mu + 2 * np.sqrt(np.diag(sigma)), color='g', alpha=0.2)
plt.show()







