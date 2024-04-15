import scipy.io
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import filedialog


# note: this is very very ugly code that requires manual file naming


setPairings = scipy.io.loadmat('setPairings2.mat') # [duration1, duration 2, 1=Left 0=Right] TODO: double check L/R with switch down

subResponses = scipy.io.loadmat('C:/Users/rokhmanova/Documents/__CODE_local/RTmocapFB/analysis/pilotData_analysis/FPA_analysis/s04/s04_VBTest_responses.mat') #todo: make this nicer using tk

print(subResponses.keys()) # if you're getting a key error check to make sure that subresponses key is correct in row 20 below

setPairings_df = pd.DataFrame(data = setPairings['setPairings2']) 
subResponses_df = pd.DataFrame(data = subResponses['GG_s04_VBTESTResponses']) 

print(subResponses_df[3][0])


# get errors
errorResponses = []

for i in range(60):
    if subResponses_df[i][0] == 0: # for s03 this formatting is: subResponses_df.iloc[i,0]
        print(setPairings_df.iloc[i,:])
        errorResponses.append(setPairings_df.iloc[i,:])
     
errorResponses = pd.DataFrame(errorResponses)


rightSideErrors = errorResponses[errorResponses.iloc[:,2]==0] # right side errors

# loop through right side errors and track which ones were wrong
start60R = start150R = start240R = start420R = start510R = start600R = 3.0
for i in range(len(rightSideErrors)):
    if rightSideErrors.iloc[i,0] == 60 or rightSideErrors.iloc[i,1] == 60:
        print('60')
        start60R = start60R - 1
    elif rightSideErrors.iloc[i,0] == 150 or rightSideErrors.iloc[i,1] == 150:
        print('150')
        start150R = start150R - 1
    elif rightSideErrors.iloc[i,0] == 240 or rightSideErrors.iloc[i,1] == 240:
        print('240')
        start240R = start240R - 1
    elif rightSideErrors.iloc[i,0] == 420 or rightSideErrors.iloc[i,1] == 420:
        print('420')
        start420R = start420R-1
    elif rightSideErrors.iloc[i,0] == 510 or rightSideErrors.iloc[i,1] == 510:
        print('510')
        start510R = start510R -1
    elif rightSideErrors.iloc[i,0] == 600 or rightSideErrors.iloc[i,1] == 600:
        print('600')
        start600R = start600R-1

leftSideErrors = errorResponses[errorResponses.iloc[:,2]==1] # left side errors

# loop through right side errors and track which ones were wrong
start60L = start150L = start240L = start420L = start510L = start600L = 3.0
for i in range(len(leftSideErrors)):
    if leftSideErrors.iloc[i,0] == 60 or leftSideErrors.iloc[i,1] == 60:
        print('60')
        start60L = start60L - 1
    elif leftSideErrors.iloc[i,0] == 150 or leftSideErrors.iloc[i,1] == 150:
        print('150')
        start150L = start150L - 1
    elif leftSideErrors.iloc[i,0] == 240 or leftSideErrors.iloc[i,1] == 240:
        print('240')
        start240L = start240L- 1
    elif leftSideErrors.iloc[i,0] == 420 or leftSideErrors.iloc[i,1] == 420:
        print('420')
        start420L = start420L-1
    elif leftSideErrors.iloc[i,0] == 510 or leftSideErrors.iloc[i,1] == 510:
        print('510')
        start510L = start510L-1
    elif leftSideErrors.iloc[i,0] == 600 or leftSideErrors.iloc[i,1] == 600:
        print('600')
        start600L = start600L-1



# make a plot:
x = np.array([60, 150, 240, 420, 510, 600])
y_L = 100*np.array([start60L, start150L, start240L, start420L, start510L, start600L])/3
y_R = 100*np.array([start60R, start150R, start240R, start420R, start510R, start600R])/3
plt.plot(x,y_L, '-o', label = 'Left')
plt.plot(x,y_R, '--*', label = 'Right')
plt.ylim([0, 110])
plt.vlines(x=330, ymin = 0, ymax = 110, colors = 'k', linestyles = '--')
plt.legend()
plt.xlabel('Duration (ms)')
plt.ylabel('% Correct Responses')
plt.show()




