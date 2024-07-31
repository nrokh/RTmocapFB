import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
import os

#TODO: save tFPAs from analyzeFPA file

# 0. SETUP
# a. set model and normalization coefficients from Rokhmanova et al. 2022
offset = 0.35673

b_weight = -0.01444
mean_weight = 71.31296
std_weight = 12.59157

b_height = -0.00413
mean_height = 172.37590
std_height = 8.63829

b_speed = 0.00340
mean_speed = 1.12072
std_speed = 0.00684

b_alignment = -0.01475
mean_alignment = 1.24025
std_alignment = 3.16196

b_bFPA = -0.00492
mean_bFPA = 3.09735
std_bFPA = 4.14900

b_tFPA = 0.30261
mean_tFPA = 5.5
std_tFPA = 2.87

# b. create arrays for storage
subs_tot = 36
store_staticAlignment = np.zeros((subs_tot,1))
store_allrKAM_NF = np.zeros((subs_tot, 80))
store_allrKAM_RT4 = np.zeros((subs_tot, 200))
store_allrKAM_RET = np.zeros((subs_tot, 200))

# 1. load feature array
root = tk.Tk()
root.withdraw() 
directory = filedialog.askdirectory()

inputFeatures_csv_file = os.path.normpath(os.path.join(directory, 'pKAM_features.csv'))
inputFeatures = pd.read_csv(inputFeatures_csv_file)

# 2. compute static alignment for each sub

    # a. open subject static file

    # b. compute AJC, KJC, HJC

    # c. compute static knee alignment

    # d. store alignment

    # e. add alignment to feature array

# 3. compute rKAM at each step

    # a. for all steps in NF, RT4, RET, find rKAM

    # b. store subject rKAMs

# 4. visualize

# a. 