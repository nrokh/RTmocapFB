import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import filedialog
import math

# FUNCTIONS
# compute FPA 
def computeFPA(toe_x, toe_y, heel_x, heel_y):
    footVec = (toe_x - heel_x, toe_y - heel_y)
    FPA = -math.degrees(math.atan(footVec[1] / footVec[0]))

    return FPA


# 1. Load data
# a. Get the desired directory to save the data
root = tk.Tk()
root.withdraw() # we don't want a full GUI, so keep the root window from appearing
directory = filedialog.askdirectory()

# store error at each angle for each sub
total_error_allsubs = np.empty([18,1])#([-5, 10, -10, -15, 5, 15, 15, -15, 10, -5, 5, -10, 10, -5, 15, -15, 5, -10], size = (18,1)) 
total_error_allsubs[:,0] = [-5, 10, -10, -15, 5, 15, 15, -15, 10, -5, 5, -10, 10, -5, 15, -15, 5, -10]

# b. load subject data
for subject in range(2,5):
     
    # c. make empty stores for each of four possible errors:
    toein_medial_error = np.empty([18,1])#([], size = (18,1))
    toein_lateral_error = np.empty([18,1])
    toeout_medial_error = np.empty([18,1])
    toeout_lateral_error = np.empty([18,1])
    total_error = np.empty([18,1])


    proprio_csv_file = os.path.normpath(os.path.join(directory, 's0' + str(subject)  + '\\s0' + str(subject) + '_proprioception.csv'))
    proprio_df = pd.read_csv(proprio_csv_file)

    # 2. Loop through each tested degree
    for deg in range(0,18):

        # a. compute FPA
        FPA_proprio = computeFPA(proprio_df['RTOE proprio x-'][deg], proprio_df['RTOE proprio y-'][deg], proprio_df['RHEE proprio x-'][deg], proprio_df['RHEE proprio y-'][deg])
        FPA_manual = computeFPA(proprio_df['RTOE manual x-'][deg], proprio_df['RTOE manual y-'][deg], proprio_df['RHEE manual x-'][deg], proprio_df['RHEE manual y-'][deg])
    
        FPA_deg_error = FPA_manual - FPA_proprio 
        # b. check if it's a toe-in or toe-out test
        if proprio_df['deg test'][deg] < 0: # toe-in
            if FPA_deg_error < 0: # overshoot toe-in
                toein_medial_error = np.append(toein_medial_error, FPA_deg_error)

            else: # undershoot toe-in
                toein_lateral_error = np.append(toein_lateral_error, FPA_deg_error)

        else: # toe-out
            if FPA_deg_error < 0: # overshoot toe-out
                toeout_lateral_error = np.append(toeout_lateral_error, FPA_deg_error)

            else: # undershoot toe-out
                toeout_medial_error = np.append(toeout_medial_error, FPA_deg_error)

        total_error[deg] = FPA_deg_error 
        

    # 3. output 4 MAE (SD)s for the 4 conds:
    print('MAE (SD) for s' + str(subject) + ': Toe-in (overshoot) = ' + str(np.mean(np.abs(toein_medial_error))) + '(' + str(np.std(np.abs(toein_medial_error))) + ')')
    print('MAE (SD) for s' + str(subject) + ': Toe-in (undershoot) = '+ str(np.mean(np.abs(toein_lateral_error))) + '(' + str(np.std(np.abs(toein_lateral_error))) + ')')
    print('MAE (SD) for s' + str(subject) + ': Toe-out (overshoot) = '+ str(np.mean(np.abs(toeout_lateral_error))) + '(' + str(np.std(np.abs(toeout_lateral_error))) + ')')
    print('MAE (SD) for s' + str(subject) + ': Toe-out (undershoot) = '+ str(np.mean(np.abs(toeout_medial_error))) + '(' + str(np.std(np.abs(toeout_medial_error))) + ')')

    print('Total MSE: ' + str(np.mean(total_error)) + '(' + str(np.std(total_error)) + ')')

    # 4. append to all sub error
    total_error_allsubs = np.concatenate((total_error_allsubs, total_error), axis=1)

# 5. plot error over angles
print(total_error_allsubs)
x = total_error_allsubs[:,0]
y = total_error_allsubs[:,1:4]
plt.plot(x,y,'o')
plt.show()