import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import filedialog
import math
import seaborn as sns

def computeVibration(FPA, targetFPA, band):
    if FPA < targetFPA - band:
        duration = (targetFPA - FPA)*50 - 90
        duration = -duration
        if duration > 600:
            duration = -600

    elif FPA > targetFPA + band:
                    duration = (FPA - targetFPA)*50 - 90
                    if duration > 600:
                        duration = -600
    else:
        duration = 0
    return duration

# 1. Load data
# a. Get the desired directory to save the data
root = tk.Tk()
root.withdraw() # we don't want a full GUI, so keep the root window from appearing
directory = filedialog.askdirectory()

# 2. load a scaled subject's data (ix = 2 or 3)
subject = 3

baseline_csv_file = os.path.normpath(os.path.join(directory, 's0' + str(subject)  + '\\s0' + str(subject) + '_baselinemeanFPA.csv'))
baselineFPA = pd.read_csv(baseline_csv_file)

toein1_csv_file = os.path.normpath(os.path.join(directory, 's0' + str(subject)  + '\\s0' + str(subject) + '_meanFPA1.csv'))
toein1FPA = pd.read_csv(toein1_csv_file)

toein2_csv_file = os.path.normpath(os.path.join(directory, 's0' + str(subject)  + '\\s0' + str(subject) + '_meanFPA2.csv'))
toein2FPA = pd.read_csv(toein2_csv_file)

toein3_csv_file = os.path.normpath(os.path.join(directory, 's0' + str(subject)  + '\\s0' + str(subject) + '_meanFPA3.csv'))
toein3FPA = pd.read_csv(toein3_csv_file)

toein4_csv_file = os.path.normpath(os.path.join(directory, 's0' + str(subject)  + '\\s0' + str(subject) + '_meanFPA4.csv'))
toein4FPA = pd.read_csv(toein4_csv_file)

# 3. compute bFPA
bFPA_deg = np.mean(baselineFPA.iloc[:,2])

print('bfpa = ' + str(bFPA_deg))

# 4. for each step, compute duration of vibration; TODO: split by over/undercorrection
store_duration = np.zeros((len(toein1FPA)+len(toein2FPA)+len(toein3FPA)+len(toein4FPA), 1))
j = 0
for i in range(len(toein1FPA)):
    duration = computeVibration(toein1FPA.iloc[i,2], bFPA_deg-10, 3.0)
    store_duration[j] = duration
    j = j+1

for i in range(len(toein2FPA)):
    duration = computeVibration(toein2FPA.iloc[i,2], bFPA_deg-10, 3.0)
    store_duration[j] = duration
    j = j+1

for i in range(len(toein3FPA)):
    duration = computeVibration(toein3FPA.iloc[i,2], bFPA_deg-10, 3.0)
    store_duration[j] = duration
    j = j+1

for i in range(len(toein4FPA)):
    duration = computeVibration(toein4FPA.iloc[i,2], bFPA_deg-10, 3.0)
    store_duration[j] = duration
    j = j+1

# 5. compute percent of steps below 330ms
sum_low = sum(1 for i in store_duration if i<330 and i>0)
sum_NZ = sum(1 for i in store_duration if i > 0)
print('Of ' + str(sum_NZ) + ' steps that triggered feedback, ' + str(sum_low) + ' were below 330ms')

# 6. show distribution of durations 
# sns.set_theme()
# sns.displot(store_duration, binwidth=10)
# plt.xlim(30,600)
# plt.ylim([0,50])
# plt.title('Mean duration: ' + str(np.mean(sum_NZ)) + 'ms')
# plt.show()

# 7. create double hist plot
x = np.squeeze(store_duration)
y_pd = pd.concat([toein1FPA, toein2FPA, toein3FPA, toein4FPA])
y = np.squeeze(y_pd.iloc[:,2])



# Create a figure with three axes
fig, axes = plt.subplots(2, 2, figsize=(12, 12), gridspec_kw={'width_ratios': [1, 1]})

# Access the Axes objects from the axes array
ax1 = axes[0, 0]  # Top left subplot
ax2 = axes[0, 1]  # Top right subplot
ax3 = axes[1, 0]  # Bottom left subplot

# Scatter plot in the middle
scatter = sns.scatterplot(x=x, y=y, ax=ax2)
ax2.set_xlabel('duration')
ax2.set_ylabel('FPA')

# Histogram for varX
hist_ax1 = sns.histplot(x, ax=ax1, kde=False)
ax1.set_xlabel('duration')
ax1.set_title('Distribution of duration')
ax1.set_ylim(ymin=0, ymax=50)

# Histogram for varY
hist_ax3 = sns.histplot(y, ax=ax3, kde=False)
ax3.set_xlabel('FPA')
ax3.set_title('Distribution of FPA')

# Adjust spacing between subplots
fig.subplots_adjust(wspace=0.3, hspace=0.3)

# save and Show the plot

plt.rc("svg", fonttype="none")
plt.savefig('analysis/pilotData_analysis/FPA_analysis/pilot_distFPAdur.svg')

plt.show()