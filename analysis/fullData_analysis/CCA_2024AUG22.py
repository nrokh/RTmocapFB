import numpy as np
import pandas as pd
import os
import tkinter as tk
from tkinter import filedialog
from sklearn.cross_decomposition import CCA
from sklearn.linear_model import Lasso
import matplotlib.pyplot as plt
from statsmodels.multivariate.cancorr import CanCorr
from sklearn.model_selection import KFold
from sklearn.model_selection import LeaveOneOut
from sklearn.metrics import mean_squared_error
from scipy import stats

import scipy

np.set_printoptions(suppress=True) # suppress scientific notation
# a. Get the desired directory to load/save the data
root = tk.Tk()
root.withdraw() # we don't want a full GUI, so keep the root window from appearing
directory = filedialog.askdirectory()

# b. set up
n_features_in = 7  # input
n_features_out = 3  # output
norm = 0 # normalization?


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

        # 4. vbtest # TODO: discuss whether this should be included at all
in_vbtest_file = os.path.normpath(os.path.join(directory, 'features\\in_vbtest.csv'))
in_vbtest = np.genfromtxt(in_vbtest_file, delimiter=',')

        # 5. ROM in
        # NOTE: this is saved as negative, because it's toe-in; I switch the sign when assembling the array 
in_ROM_in_file = os.path.normpath(os.path.join(directory, 'features\\in_ROM_in.csv'))
in_ROM_in = np.genfromtxt(in_ROM_in_file, delimiter=',')    

        # 6. ROM out
in_ROM_out_file = os.path.normpath(os.path.join(directory, 'features\\in_ROM_out.csv'))
in_ROM_out = np.genfromtxt(in_ROM_out_file, delimiter=',')  

        # 7. feedback condition (one-hot encoding with NF as 0)
feedbackCond_csv_file = os.path.normpath(os.path.join(directory, 'feedbackGroups.csv'))
feedbackCond_file = pd.read_csv(feedbackCond_csv_file)
in_cond_SF = np.zeros((36,))
in_cond_TF = np.zeros((36,))
for i in range(1,37):
        if feedbackCond_file.cond[i-1] == 1: # SF
                in_cond_SF[i-1] = 1
        elif feedbackCond_file.cond[i-1] == 2: # TF
                in_cond_TF[i-1] = 1

        # 7b. feedback condition (binary with NF as 0)
in_cond_fb = np.zeros((36,))
for i in range(1,37):
        if feedbackCond_file.cond[i-1] == 1 or feedbackCond_file.cond[i-1] == 2:
                in_cond_fb[i-1] = 1

        # 8. proprio in vs out
in_proprio_in_file = os.path.normpath(os.path.join(directory,'features\\in_proprio_in.csv'))
in_proprio_in = np.abs(np.genfromtxt(in_proprio_in_file, delimiter=','))
in_proprio_out_file = os.path.normpath(os.path.join(directory,'features\\in_proprio_out.csv'))
in_proprio_out = np.abs(np.genfromtxt(in_proprio_out_file, delimiter=','))

        # 9. height
in_height_file = os.path.normpath(os.path.join(directory,'features\\in_height.csv'))
in_height = np.abs(np.genfromtxt(in_height_file, delimiter=','))

        # 10. weight
in_weight_file = os.path.normpath(os.path.join(directory,'features\\in_weight.csv'))
in_weight = np.abs(np.genfromtxt(in_weight_file, delimiter=','))

        # 11. sex
in_isFemale_file = os.path.normpath(os.path.join(directory,'features\\in_isFemale.csv'))
in_isFemale = np.abs(np.genfromtxt(in_isFemale_file, delimiter=','))

    # iii. load outputs as numpy arrays:
    # 1. RMSE
out_RMSE_file = os.path.normpath(os.path.join(directory, 'features\\out_RMSE.csv'))
out_RMSE = np.genfromtxt(out_RMSE_file, delimiter=',')

        # 2. delta RMSE
out_delta_RT4 = (out_RMSE[1:,4] - out_RMSE[1:,0])/out_RMSE[1:,0]
out_delta_RET = (out_RMSE[1:,5] - out_RMSE[1:,0])/out_RMSE[1:,0]

        # 3. error ratios
out_errRatio_in_file = os.path.normpath(os.path.join(directory,'features\\out_errRatio_in.csv'))
out_errRatio_in = np.abs(np.genfromtxt(out_errRatio_in_file, delimiter=','))
out_errRatio_out_file = os.path.normpath(os.path.join(directory,'features\\out_errRatio_out.csv'))
out_errRatio_out = np.abs(np.genfromtxt(out_errRatio_out_file, delimiter=','))

        # 4. catch trial RMSE
out_cRMSE_file = os.path.normpath(os.path.join(directory, 'features\\out_cRMSE.csv'))
out_cRMSE = np.genfromtxt(out_cRMSE_file, delimiter=',')


    # ii. assemble inputs into single numpy array:
X = np.stack((in_proprio_in[1:], in_bFPA[1:], np.abs(in_ROM_in[1:])-in_bFPA[1:],  in_cond_fb, in_resp[1:,4]), axis=1) # shape = 36xN
if norm:
        X = (X - np.mean(X, axis=0) )/np.std(X, axis=0, ddof=1)

    # iv. assemble outputs into single numpy array:
Y = np.stack((out_RMSE[1:,4], out_RMSE[1:,5], out_errRatio_out[1:,5]), axis=1)
if norm:
        Y = (Y - np.mean(Y, axis=0) )/np.std(Y, axis=0, ddof=1)

# lasso regression for feature selection
X = np.stack((in_proprio_in[1:], in_proprio_out[1:], in_proprio[1:], in_bFPA[1:], 
              np.abs(in_ROM_in[1:])-in_bFPA[1:], np.abs(in_ROM_in[1:]), np.abs(in_ROM_out[1:])-in_bFPA[1:], 
              np.abs(in_ROM_out[1:]),in_vbtest[1:], in_height[1:], in_weight[1:], 
              in_isFemale[1:], in_cond_fb, in_resp[1:,4]), axis=1) # shape = 36xN
if norm:
        X = (X - np.mean(X, axis=0) )/np.std(X, axis=0, ddof=1)
Y = np.stack((out_RMSE[1:,4], out_RMSE[1:,5], out_errRatio_out[1:,5]), axis=1)
if norm:
        Y = (Y - np.mean(Y, axis=0) )/np.std(Y, axis=0, ddof=1)

lasso = Lasso(alpha=0.1)
lasso.fit(X, Y)
selected_features = np.abs(lasso.coef_) > 0
print("Selected features:", selected_features)

# CCA AFTER LASSO:
X = np.stack((in_proprio_in[1:], in_bFPA[1:], np.abs(in_ROM_in[1:])-in_bFPA[1:], in_cond_fb, in_resp[1:,4]), axis=1) # shape = 36xN
if norm:
        X = (X - np.mean(X, axis=0) )/np.std(X, axis=0, ddof=1)

Y = np.stack((out_RMSE[1:,4], out_RMSE[1:,5], out_errRatio_out[1:,5]), axis=1)
if norm:
        Y = (Y - np.mean(Y, axis=0) )/np.std(Y, axis=0, ddof=1)


# # ___________________________ CCA: ____________________
Y_pred = np.zeros_like(Y)
Y_real = np.zeros_like(Y)
loo = LeaveOneOut()

for train_index, test_index in loo.split(X):
    X_train, X_test = X[train_index], X[test_index]
    Y_train, Y_test = Y[train_index], Y[test_index]

    cca = CCA(n_components=min(X.shape[1], Y.shape[1]))
    cca.fit(X_train, Y_train)

    Y_pred[test_index] = cca.predict(X_test)
    Y_real[test_index] = Y_test

# report MSE:
mse = np.sqrt(mean_squared_error(Y_real[:,0], Y_pred[:,0]))
print("RT4 RMSE" + str(mse))
r2, p_val = stats.pearsonr(Y_real[:,0], Y_pred[:,0])
print("RT4 R2 score: " + str(np.square(r2)) + " p= " + str(p_val))

# plot pred vs real
plt.figure(figsize=(10, 6))
plt.scatter(Y_real[:,0], Y_pred[:,0])
plt.plot([min(Y_real[:,0]), max(Y_real[:,0])], [min(Y_real[:,0]), max(Y_real[:,0])], 'r--', label='perfect fit')
plt.xlabel('RMSE (real)')
plt.ylabel('RMSE (pred)')
plt.title('RT4 RMSE')
plt.legend()
plt.show()

mse = np.sqrt(mean_squared_error(Y_real[:,1], Y_pred[:,1]))
print("RET RMSE" + str(mse))
r2, p_val = stats.pearsonr(Y_real[:,1], Y_pred[:,1])
print("RET R2 score: " + str(np.square(r2)) + " p= " + str(p_val))

# plot pred vs real
plt.figure(figsize=(10, 6))
plt.scatter(Y_real[:,1], Y_pred[:,1])
plt.plot([min(Y_real[:,1]), max(Y_real[:,1])], [min(Y_real[:,1]), max(Y_real[:,1])], 'r--', label='perfect fit')
plt.xlabel('RMSE (real)')
plt.ylabel('RMSE (pred)')
plt.title('RET RMSE')
plt.legend()
plt.show()

mse = np.sqrt(mean_squared_error(Y_real[:,2], Y_pred[:,2]))
print("ERROR RATIO : " + str(mse))
r2, p_val = stats.pearsonr(Y_real[:,2], Y_pred[:,2])
print("Error ratio R2 score: " + str(np.square(r2)) + " p= " + str(p_val))

# plot pred vs real
plt.figure(figsize=(10, 6))
plt.scatter(Y_real[:,2], Y_pred[:,2])
plt.plot([min(Y_real[:,2]), max(Y_real[:,2])], [min(Y_real[:,2]), max(Y_real[:,2])], 'r--', label='perfect fit')
plt.xlabel('error ratio (real)')
plt.ylabel('error ratio (pred)')
plt.title('Error ratio RMSE')
plt.legend()
plt.show()




# cca_coeffs = []
# X_c_folds = []
# Y_c_folds = []
# n_components = min(n_features_in, n_features_out)
# n_splits = 6

# # initialize k-fold
# kf = KFold(n_splits = n_splits, shuffle=True, random_state=23) #23

# for train_index, test_index in kf.split(X):
#         print('__________ New fold: _______________')

#         X_train, X_test = X[train_index], X[test_index]
#         Y_train, Y_test = Y[train_index], Y[test_index]

#         cca = CCA(n_components=n_components)
#         X_c, Y_c = cca.fit_transform(X_train, Y_train)

#         #  canonical variates for the test sample
#         X_c_test, Y_c_test = cca.transform(X_test, Y_test)

#         # iii. print feature loadings
#         print("\nX loadings:")
#         print(cca.x_loadings_)
#         print("\nY loadings:")
#         print(cca.y_loadings_)

#         cca_model = CanCorr(X_train,Y_train)

#         #  hypothesis test
#         results = cca_model.corr_test()

#         print("\nSummary:")
#         print(results.summary())

#         # manually calculate p-values for the loadings between the original variables and the canonical variates:
#         n = X.shape[0]  # sample size

#         # get standard errors
#         se_X = np.sqrt((1 - cca.x_loadings_**2) / (n - 2))
#         se_Y = np.sqrt((1 - cca.y_loadings_**2) / (n - 2))

#         # get t-values
#         t_X = cca.x_loadings_ / se_X
#         t_Y = cca.y_loadings_ / se_Y

#         # get p-values (two-tailed test)
#         p_X = 2 * (1 - scipy.stats.t.cdf(np.abs(t_X), n-2))
#         p_Y = 2 * (1 - scipy.stats.t.cdf(np.abs(t_Y), n-2))


#         print("\nP-values for X loadings:")
#         print(str(p_X))

#         print("\nP-values for Y loadings:")
#         print(str(p_Y))

#         cca_coeffs.append(cca.score(X_test, Y_test))
#         X_c_folds.append(X_c_test)
#         Y_c_folds.append(Y_c_test)


# ##### NON-k-FOLD RESULTS:
#     # v. run cca:
# n_components = min(n_features_in, n_features_out)
# cca = CCA(n_components=n_components)
# X_c, Y_c = cca.fit_transform(X, Y)

# # d. interpretation
#     # i. print canonical correlations
# print("Canonical correlations:", cca.score(X, Y))
# # this represents the strength of the relationship between the two sets of variables in the canonical variate space

#     # iii. print feature loadings
# print("\nX loadings:")
# print(cca.x_loadings_)
# print("\nY loadings:")
# print(cca.y_loadings_)
# # each column = the x loadings for each variate;
# # first column (first variate) shows the strength of contributions of each input feature to that variate

# # run stats?
# cca_model = CanCorr(X,Y)

# # Perform the hypothesis test
# results = cca_model.corr_test()

# print("\nSummary:")
# print(results.summary())

# # manually calculate p-values for the loadings between the original variables and the canonical variates:
# n = X.shape[0]  # sample size

# # get standard errors
# se_X = np.sqrt((1 - cca.x_loadings_**2) / (n - 2))
# se_Y = np.sqrt((1 - cca.y_loadings_**2) / (n - 2))

# # get t-values
# t_X = cca.x_loadings_ / se_X
# t_Y = cca.y_loadings_ / se_Y

# # get p-values (two-tailed test)
# p_X = 2 * (1 - scipy.stats.t.cdf(np.abs(t_X), n-2))
# p_Y = 2 * (1 - scipy.stats.t.cdf(np.abs(t_Y), n-2))


# print("\nP-values for X loadings:")
# print(str(p_X))

# print("\nP-values for Y loadings:")
# print(str(p_Y))



#     # ii. plot the first two canonical variates (the first are usually the strongest)

# SF_rows = np.where(feedbackCond_file.cond == 1)[0]
# TF_rows = np.where(feedbackCond_file.cond == 2)[0]
# NF_rows = np.where(feedbackCond_file.cond == 0)[0]
# plt.figure(figsize=(6, 6))
# plt.scatter(X_c[SF_rows, 0], Y_c[SF_rows, 0], alpha=0.7, color = '#0f4c5c', label = 'SF', s = 60)
# plt.scatter(X_c[TF_rows, 0], Y_c[TF_rows, 0], alpha=0.7, color = '#5f0f40', label = 'TF', s = 60)
# plt.scatter(X_c[NF_rows, 0], Y_c[NF_rows, 0], alpha=0.7, color = '#e36414', label = 'NF', s = 60)
# plt.title("First Canonical Variate")
# plt.xlabel("X canonical variate 1")
# plt.ylabel("Y canonical variate 1")
# plt.ylim([-2.2, 2])
# plt.xlim([-2.5, 1.7])
# plt.legend()

# plt.savefig("analysis/fullData_analysis/pp_Results/CCA1.svg", format="svg")
# plt.show()

# plt.figure(figsize=(6, 6))
# plt.scatter(X_c[SF_rows, 1], Y_c[SF_rows, 1], alpha=0.7, color = '#0f4c5c', label = 'SF', s = 60)
# plt.scatter(X_c[TF_rows, 1], Y_c[TF_rows, 1], alpha=0.7, color = '#5f0f40', label = 'TF', s = 60)
# plt.scatter(X_c[NF_rows, 1], Y_c[NF_rows, 1], alpha=0.7, color = '#e36414', label = 'NF', s = 60)
# plt.xlabel('X_c2')
# plt.ylabel('Y_c2')
# plt.title("Second Canonical Variate")
# plt.xlabel("X canonical variate 2")
# plt.ylabel("Y canonical variate 2")
# plt.ylim([-2.2, 2])
# plt.xlim([-2.5, 1.7])
# plt.legend()

# plt.savefig("analysis/fullData_analysis/pp_Results/CCA2.svg", format="svg")
# plt.show()

