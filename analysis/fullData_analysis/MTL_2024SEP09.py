import numpy as np
import pandas as pd
import os
import tkinter as tk
from tkinter import filedialog
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.models import Model


# __________________A. SETUP__________________
np.set_printoptions(suppress=True) # suppress scientific notation
# a. Get the desired directory to load/save the data
root = tk.Tk()
root.withdraw() # we don't want a full GUI, so keep the root window from appearing
directory = filedialog.askdirectory()

# b. params
n_features_in = 7  # input
n_features_out = 3  # output
norm = 0 # normalization?

# _______________________B. LOAD DATA _________________
# input data:
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
SF_rows = np.where(feedbackCond_file.cond == 1)[0]
TF_rows = np.where(feedbackCond_file.cond == 2)[0]
NF_rows = np.where(feedbackCond_file.cond == 0)[0]

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


# ______________________ MTL ______________________________________

# input layer
input_layer = Input(shape=(5,))

# shared hidden layers (these layers will be shared by all tasks)
shared = Dense(64, activation='relu')(input_layer)
shared = Dense(32, activation='relu')(shared)

# task 1 output
output_1 = Dense(1, activation='linear', name='task_1_output')(shared)

# task 2 output
output_2 = Dense(1, activation='linear', name='task_2_output')(shared)

# tsk 3 output
output_3 = Dense(1, activation='linear', name='task_3_output')(shared)

# defining the model with one input and three outputs (multi-task)
model = Model(inputs=input_layer, outputs=[output_1, output_2, output_3])

#compile the model (TODO: look at loss functions)
model.compile(optimizer='adam', 
              loss={'task_1_output': 'mse', 'task_2_output': 'mse', 'task_3_output': 'mse'},
              metrics={'task_1_output': ['mae'], 'task_2_output': ['mae'], 'task_3_output': ['mae']})


# split test-train
# randomly choose 2 indices from each group for the test set
SF_test = np.random.choice(SF_rows, size=2, replace=False)
TF_test = np.random.choice(TF_rows, size=2, replace=False)
NF_test = np.random.choice(NF_rows, size=2, replace=False)

# remaining indices are for the training set
SF_train = np.setdiff1d(SF_rows, SF_test)
TF_train = np.setdiff1d(TF_rows, TF_test)
NF_train = np.setdiff1d(NF_rows, NF_test)

# combine the indices for the training and test sets
train_indices = np.concatenate([SF_train, TF_train, NF_train])
test_indices = np.concatenate([SF_test, TF_test, NF_test])

# split the data based on the computed indices
X_train = X[train_indices]
Y_train = Y[train_indices]
X_test = X[test_indices]
Y_test = Y[test_indices]


# fit the model
model.fit(X_train, {'task_1_output': Y_train[:, 0], 
              'task_2_output': Y_train[:, 1], 
              'task_3_output': Y_train[:, 2]}, 
          epochs=50, batch_size=8)

# summary of the model
model.summary()

# output of test set:
results = model.evaluate(X_test, 
                         {'task_1_output': Y_test[:, 0], 
                          'task_2_output': Y_test[:, 1], 
                          'task_3_output': Y_test[:, 2]})

# first item is the overall loss, and then each task's loss and MAE
print(f"overall loss: {results[0]}")
print(f"task 1 loss: {results[1]}")
print(f"task 2 loss: {results[2]}")
print(f"task 3 loss: {results[3]}")
print(f"task 1 MAE: {results[4]}")
print(f"task 2 MAE: {results[5]}")
print(f"task 3 MAE: {results[6]}")

print(f"outputs mean: {np.mean(Y, axis=0)}")
print(f"outputs std: {np.std(Y, axis=0)}")