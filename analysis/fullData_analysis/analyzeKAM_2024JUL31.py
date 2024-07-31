import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
import os

#TODO: save FPAs from analyzeFPA file

# 0. SETUP
# a. set model and normalization coefficients from Rokhmanova et al. 2022
b_weight = 0.5
scale_weight = 0.0
b_height = 0.5
scale_height = 0.0
b_speed = 0.5
scale_speed = 0.0
b_alignment = 0.5
scale_alignment = 0.0
b_bFPA = 0.5
scale_bFPA = 0.0
b_tFPA = 0.5
scale_tFPA = 0.0

# b. create arrays for storage
subs_tot = 36
store_staticAlignment = np.zeros((subs_tot,1))
store_allrKAM_NF = np.zeros((subs_tot, 80))
store_allrKAM_RT4 = np.zeros((subs_tot, 200))
store_allrKAM_RET = np.zeros((subs_tot, 200))

# 1. load feature array
# TODO: create csv file containing walking speed, height, weight, and tFPA
root = tk.Tk()
root.withdraw() 
directory = filedialog.askdirectory()

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