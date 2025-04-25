import numpy as np
import matplotlib.pyplot as plt

class PCA():

    def __init__(self, X):
        self.X = X
        self.components = None
    
    def fit(self):
        X = self.X
        # We start by centering the data.
        self.mean = np.mean(X, axis=0)
        X_centered = X - self.mean
        # We calculate the covariance matrix.
        C = 1/(X.shape[0] - 1) * X_centered.T @ X_centered
        # We do eigenvalue decomposition.
        eigenvalues, eigenvectors = np.linalg.eig(C)
        idx = eigenvalues.argsort()[::-1]
        eigenvalues = eigenvalues[idx]
        eigenvectors = eigenvectors[:,idx]
        self.components = eigenvectors
        return
    
    def transform(self, n_components):
        return self.X @ self.components[:,:n_components]

# data = np.array([[2.5, 2.4],
#           [2.0, 1.0],
#           [2.2, 2.9],
#           [1.4, 2.2],
#           [1.1, 0.9]])

# fig, ax = plt.subplots(1, 2)
# ax[0].scatter(data[:,0], data[:,1])

# pca = PCA(data)
# pca.fit()
# rotated_data = pca.transform(data, 2)
# ax[1].scatter(rotated_data[:,0], rotated_data[:,1])

# ax[0].set_title('Original data')
# ax[1].set_title('Rotated data')
# ax[0].set_aspect('equal')
# ax[1].set_aspect('equal')

# plt.show()

# pos_flat = np.loadtxt('../lj10clusters.txt')
# positions = pos_flat.reshape(-1,pos_flat.shape[1]//2,2)
# positions = positions.reshape(positions.shape[0],-1)

# pca = PCA(n_components=2)
# print(pca.fit(positions))

