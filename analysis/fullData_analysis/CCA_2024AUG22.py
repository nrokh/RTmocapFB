import numpy as np
import pandas as pd
import os
import tkinter as tk
from tkinter import filedialog
from sklearn.cross_decomposition import CCA
import matplotlib.pyplot as plt


# a. Get the desired directory to load/save the data
root = tk.Tk()
root.withdraw() # we don't want a full GUI, so keep the root window from appearing
directory = filedialog.askdirectory()

# b. set up
n_features_in = 3  # input
n_features_out = 2  # output
norm = 1 # normalization?


# ___________________________________________________________________________________
# c. run CCA
    # i. load inputs as numpy arrays
        # 1. resp (36x6; probably want RT4 resp)
in_resp_file = os.path.normpath(os.path.join(directory, 'features\\in_resp.csv'))
in_resp = np.genfromtxt(in_resp_file, delimiter=',')

        # 2. proprio
in_proprio_file = os.path.normpath(os.path.join(directory, 'features\\in_proprio_RMSE.csv'))
in_proprio = np.genfromtxt(in_proprio_file, delimiter=',')

        # 3. bFPA
in_bFPA_file = os.path.normpath(os.path.join(directory, 'features\\in_bFPA.csv'))
in_bFPA = np.genfromtxt(in_bFPA_file, delimiter=',')

    # ii. assemble inputs into single numpy array:
X = np.stack((in_resp[1:,4], in_proprio[1:], in_bFPA[1:]), axis=1) # shape = 36x3
if norm:
        X = (X - np.mean(X, axis=0) )/np.std(X, axis=0, ddof=1)

    # iii. load outputs as numpy arrays:
out_RMSE_file = os.path.normpath(os.path.join(directory, 'features\\out_RMSE.csv'))
out_RMSE = np.genfromtxt(out_RMSE_file, delimiter=',')

    # iv. assemble outputs into single numpy array:
Y = out_RMSE[1:, [4,5]]
if norm:
        Yn = (Y - np.mean(Y, axis=0) )/np.std(Y, axis=0, ddof=1)

    # v. run cca:
n_components = min(n_features_in, n_features_out)
cca = CCA(n_components=n_components)
X_c, Y_c = cca.fit_transform(X, Y)

# d. interpretation
    # i. print canonical correlations
print("Canonical correlations:", cca.score(X, Y))
# this represents the strength of the relationship between the two sets of variables in the canonical variate space

    # ii. plot the first two canonical variates (the first are usually the strongest)
plt.figure(figsize=(10, 6))
plt.scatter(X_c[:, 0], Y_c[:, 0], alpha=0.7)
plt.title("First Canonical Variate")
plt.xlabel("X canonical variate 1")
plt.ylabel("Y canonical variate 1")
plt.grid(True)
plt.show()

    # iii. print feature loadings
print("\nX loadings:")
print(cca.x_loadings_)
print("\nY loadings:")
print(cca.y_loadings_)
# each column = the x loadings for each variate;
# first column (first variate) shows the strength of contributions of each input feature to that variate