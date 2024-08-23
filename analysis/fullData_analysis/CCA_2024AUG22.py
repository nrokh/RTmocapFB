import numpy as np
from sklearn.cross_decomposition import CCA
import matplotlib.pyplot as plt

# generate random data
np.random.seed(42)
n_samples = 1000
n_features_1 = 4  # input
n_features_2 = 3  # output

# inputs:
X = np.random.rand(n_samples, n_features_1)

# outputs:
Y = np.dot(X, np.random.rand(n_features_1, n_features_2)) + np.random.normal(0, 0.1, (n_samples, n_features_2))

# run cca:
n_components = min(n_features_1, n_features_2)
cca = CCA(n_components=n_components)
X_c, Y_c = cca.fit_transform(X, Y)

# print canonical correlations
print("Canonical correlations:", cca.score(X, Y))

# plot the first two canonical variates
plt.figure(figsize=(10, 6))
plt.scatter(X_c[:, 0], Y_c[:, 0], alpha=0.7)
plt.title("First Canonical Variate")
plt.xlabel("X canonical variate 1")
plt.ylabel("Y canonical variate 1")
plt.grid(True)
plt.show()

# print feature loadings
print("\nX loadings:")
print(cca.x_loadings_)
print("\nY loadings:")
print(cca.y_loadings_)