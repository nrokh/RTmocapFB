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

# 1. load meta data
root = tk.Tk()
root.withdraw() 
directory = filedialog.askdirectory()

# a. load feature array
inputFeatures_csv_file = os.path.normpath(os.path.join(directory, 'pKAM_features.csv'))
inputFeatures = pd.read_csv(inputFeatures_csv_file)
print(inputFeatures.head()) #speed, height, weight, bFPA, tFPA

# b. load feedback condition ID (1:SF, 2:TF, 0:NF)
feedbackCond_csv_file = os.path.normpath(os.path.join(directory, 'feedbackGroups.csv'))
feedbackCond_file = pd.read_csv(feedbackCond_csv_file)

# 2. compute static alignment for each sub
for subject in range(1,37):
    if subject == 14 or subject == 15:
        continue
    print('----------------Starting analysis for subject ' + str(subject) + '--------------------')
    if feedbackCond_file.cond[subject-1] == 1:
        print('----------------CONDITION: SCALED FEEDBACK------------')
    elif feedbackCond_file.cond[subject-1] == 2:
        print('----------------CONDITION: TRINARY FEEDBACK------------')
    elif feedbackCond_file.cond[subject-1] == 0:
        print('----------------CONDITION: NO FEEDBACK------------')

    # a. open subject static file and tFPAs
    if subject < 10: 
        static_csv_file = os.path.normpath(os.path.join(directory, 's0' + str(subject)  + '\\s0' + str(subject) + '_static.csv'))
        staticDF = pd.read_csv(static_csv_file, skiprows=4)

        tFPA_NF_file = os.path.normpath(os.path.join(directory, 's0' + str(subject)  + '\\tFPA_NF.csv'))
        tFPA_NF = pd.read_csv(tFPA_NF_file)
        tFPA_RT4_file = os.path.normpath(os.path.join(directory, 's0' + str(subject)  + '\\tFPA_RT4.csv'))
        tFPA_RT4 = pd.read_csv(tFPA_RT4_file)
        tFPA_RET_file = os.path.normpath(os.path.join(directory, 's0' + str(subject)  + '\\tFPA_RET.csv'))
        tFPA_RET = pd.read_csv(tFPA_RET_file)
        

    else: 
        static_csv_file = os.path.normpath(os.path.join(directory, 's' + str(subject)  + '\\s' + str(subject) + '_static.csv'))
        staticDF = pd.read_csv(static_csv_file, skiprows=4)

        tFPA_NF_file = os.path.normpath(os.path.join(directory, 's' + str(subject)  + '\\tFPA_NF.csv'))
        tFPA_NF = pd.read_csv(tFPA_NF_file)
        tFPA_RT4_file = os.path.normpath(os.path.join(directory, 's' + str(subject)  + '\\tFPA_RT4.csv'))
        tFPA_RT4 = pd.read_csv(tFPA_RT4_file)
        tFPA_RET_file = os.path.normpath(os.path.join(directory, 's' + str(subject)  + '\\tFPA_RET.csv'))
        tFPA_RET = pd.read_csv(tFPA_RET_file)

    # b. compute right leg AJC, KJC, HJC
    MANK = np.mean(staticDF.iloc[:,11:14], axis=0)
    LANK = np.mean(staticDF.iloc[:,53:56], axis=0)
    AJCy = (MANK.iloc[1]+LANK.iloc[1])/2 # y = mediolateral
    AJCz = (MANK.iloc[2]+LANK.iloc[2])/2 # z = vertical
    
    MKNE = np.mean(staticDF.iloc[:,5:8], axis=0)
    LKNE = np.mean(staticDF.iloc[:,47:50], axis=0)
    KJCy = (MKNE.iloc[1] + LKNE.iloc[1])/2
    KJCz = (MKNE.iloc[2] + LKNE.iloc[2])/2

    # Harrington's regression equations for HJC:
    RASI = np.mean(staticDF.iloc[:,17:20], axis=0)
    LASI = np.mean(staticDF.iloc[:,14:17], axis=0)
    pelvisCentery = (RASI.iloc[1]+LASI.iloc[1])/2
    pelvisCenterz = (RASI.iloc[2]+LASI.iloc[2])/2
    ASIS_distance = np.sqrt( (RASI.iloc[1]-LASI.iloc[1])**2 + (RASI.iloc[2]-LASI.iloc[2])**2 )
    HJCy = pelvisCentery + 0.33*ASIS_distance + 7.3
    HJCz = pelvisCenterz - 0.30*ASIS_distance - 10.9

    # c. compute static knee alignment
    A = np.sqrt( (HJCy - KJCy)**2 + (HJCz - KJCz)**2 )
    B = np.sqrt( (AJCy - KJCy)**2 + (AJCz - KJCz)**2 )
    C = np.sqrt( (HJCy - AJCy)**2 + (HJCz - AJCz)**2 )

    # cosine law: 
    # TODO: check if it's 180-alignment or alignemnt-180
    alignment = 180 - np.rad2deg(np.arccos( (B**2 + A**2 - C**2)/(2*A*B) ))

    # d. store alignment; add to feature array (manually)
    store_staticAlignment[subject-1] = alignment


# 3. compute rKAM at each step

    # a. normalize features
    
    # b. for all steps in NF, RT4, RET, find rKAM

    # c. store subject rKAMs



# 4. visualize

# a. 