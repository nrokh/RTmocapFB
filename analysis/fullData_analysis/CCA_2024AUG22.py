import numpy as np
from sklearn.cross_decomposition import CCA
import matplotlib.pyplot as plt

# set up
n_features_in = 3  # input
n_features_out = 2  # output

# load inputs:
# a. resp (36x6; probably want RT4 resp)
# b. proprio
# c. bFPA

# assemble inputs into single numpy array:
#X = np.random.rand(1000, n_features_in) # 1000x3

# outputs:
#Y = np.dot(X, np.random.rand(n_features_1, n_features_2)) + np.random.normal(0, 0.1, (n_samples, n_features_2)) # 1000x2

# run cca:
n_components = min(n_features_in, n_features_out)
cca = CCA(n_components=n_components)
X_c, Y_c = cca.fit_transform(X, Y)

# print canonical correlations
print("Canonical correlations:", cca.score(X, Y))
# this represents the strength of the relationship between the two sets of variables in the canonical variate space

# plot the first two canonical variates (the first are usually the strongest)
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
# each column = the x loadings for each variate;
# first column (first variate) shows the strength of contributions of each input feature to that variate