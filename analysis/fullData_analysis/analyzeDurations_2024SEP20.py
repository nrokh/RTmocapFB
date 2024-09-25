import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
import os

np.set_printoptions(suppress=True) # suppress scientific notation
# a. Get the desired directory to load/save the data
root = tk.Tk()
root.withdraw() # we don't want a full GUI, so keep the root window from appearing
directory = filedialog.askdirectory()


# b. load feedback condition ID (1:SF, 2:TF, 0:NF)
feedbackCond_csv_file = os.path.normpath(os.path.join(directory, 'feedbackGroups.csv'))
feedbackCond_file = pd.read_csv(feedbackCond_csv_file)

# 2. compute static alignment for each sub
for subject in range(1,2):#37):

    print('----------------Starting analysis for subject ' + str(subject) + '--------------------')
    if feedbackCond_file.cond[subject-1] == 1:
        print('----------------CONDITION: SCALED FEEDBACK------------')
    elif feedbackCond_file.cond[subject-1] == 2:
        print('----------------CONDITION: TRINARY FEEDBACK------------')
    elif feedbackCond_file.cond[subject-1] == 0:
        print('----------------CONDITION: NO FEEDBACK------------')

    # a. open subject static file and tFPAs
    if subject < 10: 
        tFPA_RT1_file = os.path.normpath(os.path.join(directory, 's0' + str(subject)  + '\\tFPA_RT1.csv'))
        tFPA_RT1 = pd.read_csv(tFPA_RT1_file)

        tFPA_RT4_file = os.path.normpath(os.path.join(directory, 's0' + str(subject)  + '\\tFPA_RT4.csv'))
        tFPA_RT4 = pd.read_csv(tFPA_RT4_file)
        

    else: 
        tFPA_RT1_file = os.path.normpath(os.path.join(directory, 's' + str(subject)  + '\\tFPA_RT1.csv'))
        tFPA_RT1 = pd.read_csv(tFPA_RT1_file)

        tFPA_RT4_file = os.path.normpath(os.path.join(directory, 's' + str(subject)  + '\\tFPA_RT4.csv'))
        tFPA_RT4 = pd.read_csv(tFPA_RT4_file)

    # b. compute durations

    print(tFPA_RT1)


# 3. compute durations
# 4. save durations to two big arrays
# 5. end loop; plot histograms 