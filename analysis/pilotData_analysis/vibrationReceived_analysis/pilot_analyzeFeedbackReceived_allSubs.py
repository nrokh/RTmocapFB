import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import os
import tkinter as tk
from tkinter import filedialog
import math
import seaborn as sns
from scipy import stats

def computeVibration(FPA, targetFPA, band):
    if FPA < targetFPA - band:
        duration = (targetFPA - FPA)*50 - 90
        duration = -duration
        if duration < -600:
            duration = -600

    elif FPA > targetFPA + band:
                    duration = (FPA - targetFPA)*50 - 90
                    if duration > 600:
                        duration = 600
    else:
        duration = 0
    return duration

# 1. Load data
# a. Get the desired directory to load data
root = tk.Tk()
root.withdraw() # we don't want a full GUI, so keep the root window from appearing
directory = filedialog.askdirectory()

# 2. load all scaled subject's data

#count the number of files in the directory that start with 's' 
num_files = len([f for f in os.listdir(directory) if f.startswith('s')])
store_duration_total = []
store_toein_total = []
store_toein_total_rel = []

for subs in range(1,num_files+1):
    baseline_csv_file = os.path.normpath(os.path.join(directory, 's0' + str(subs)  + '\\s0' + str(subs) + '_baselinemeanFPA.csv'))
    baselineFPA = pd.read_csv(baseline_csv_file)

    toein1_csv_file = os.path.normpath(os.path.join(directory, 's0' + str(subs)  + '\\s0' + str(subs) + '_meanFPA1.csv'))
    toein1FPA = pd.read_csv(toein1_csv_file)

    toein2_csv_file = os.path.normpath(os.path.join(directory, 's0' + str(subs)  + '\\s0' + str(subs) + '_meanFPA2.csv'))
    toein2FPA = pd.read_csv(toein2_csv_file)

    toein3_csv_file = os.path.normpath(os.path.join(directory, 's0' + str(subs)  + '\\s0' + str(subs) + '_meanFPA3.csv'))
    toein3FPA = pd.read_csv(toein3_csv_file)

    toein4_csv_file = os.path.normpath(os.path.join(directory, 's0' + str(subs)  + '\\s0' + str(subs) + '_meanFPA4.csv'))
    toein4FPA = pd.read_csv(toein4_csv_file)

    # 3. compute bFPA
    bFPA_deg = np.mean(baselineFPA.iloc[:,2])
    target_deg = bFPA_deg-10
    print('Subject ' + str(subs) + ' bfpa = ' + str(bFPA_deg))

    # 4. for each step, compute duration of vibration
    toein_subject = pd.concat([toein1FPA, toein2FPA, toein3FPA, toein4FPA]) 

    for i in range(len(toein_subject)):
        duration = computeVibration(toein_subject.iloc[i,2], target_deg, 3.0)
        store_duration_total.append(duration)
        store_toein_total.append(toein_subject.iloc[i,2])
        store_toein_total_rel.append(toein_subject.iloc[i,2] - target_deg)


# 5. compute percent of steps below 330ms
sum_low = sum(1 for i in store_duration_total if i<330 and i>0)
sum_NZ = sum(1 for i in store_duration_total if i > 0)
print('Of ' + str(sum_NZ) + ' steps that triggered feedback, ' + str(sum_low) + ' were below 330ms')

# 6. show distribution of durations 
sns.set_theme()
plt.figure(figsize=(10, 5))

store_duration_total_abs = [abs(x) for x in store_duration_total if x != 0]

plt.subplot(1, 2, 1)
sns.histplot(store_duration_total_abs, binwidth=10)
plt.xlabel('Duration (ms)')
plt.ylabel('Count')
plt.xlim([30,600])
plt.xticks(range(0, 600, 50))
plt.ylim([0,150])
plt.title('Distribution of vibration durations for All Subjects')

plt.subplot(1, 2, 2)
sns.boxplot(store_duration_total_abs)
plt.xlabel('Duration (ms)')
plt.title('Boxplot of vibration durations for All Subjects')
plt.ylim([0,620])
#draw horizontal line at 1st quartile and half
plt.axhline(y=90, color='r', linestyle='--')
plt.axhline(y=140, color='r', linestyle='--')

# eq = sns.kdeplot(store_duration_total, clip=(90,600), bw_adjust=5)
# plt.xlim([30,600])
# plt.xlabel('Duration (ms)')
# plt.xticks(range(0, 600, 50))

# mean_without_zeros = str(round(np.mean([x for x in store_duration_total if x != 0]),2))
# plt.title('Mean duration: ' + mean_without_zeros + 'ms')

plt.rc("svg", fonttype="none")
plt.savefig('analysis/pilotData_analysis/FPA_analysis/pilot_vb_test_justification.svg')
plt.show()

# 7. create double hist plot
x = np.squeeze(store_duration_total)
y = np.squeeze(store_toein_total_rel)

# Create a figure with a custom GridSpec
fig = plt.figure(figsize=(12, 12))
gs = gridspec.GridSpec(2, 2, width_ratios=[1, 1])
plt.get_current_fig_manager().window.state('zoomed')

# Access the Axes objects from the GridSpec
ax1 = plt.subplot(gs[0, 0])  # Top left subplot
ax2 = plt.subplot(gs[0, 1])  # Top right subplot
ax3 = plt.subplot(gs[1, :])  # Bottom subplot spanning both columns

# Histogram for varX
hist_ax1 = sns.histplot(x, ax=ax1, kde=False)
ax1.set_xlabel('Duration (ms)')
ax1.set_title('Distribution of duration for All Subjects')
ax1.set_ylim(ymin=0, ymax=80)
ax1.set_xlim(xmin=-620, xmax=620)
ax1.set_xticks(range(-600, 600, 100))
ax1.text(-600, 70, '**All pilot subjects did not receive scaled feedback, \nbut this is the distribution of vibration durations that would have been received', fontsize=8)

# Scatter plot in the middle
scatter = sns.scatterplot(x=x, y=y, ax=ax2)
ax2.set_xlabel('Duration (ms)')
ax2.set_ylabel('Relative FPA (deg)')
ax2.set_xlim(xmin=-620, xmax=620)
ax2.set_xticks(range(-600, 600, 100))

# Histogram for varY
hist_ax3 = sns.histplot(y, ax=ax3, kde=False)
ax3.set_xlabel('Relative FPA (deg)')
ax3.set_title('Distribution of FPA for All Subjects')
ax3.set_xlim(xmin=-17, xmax=17)

# Adjust spacing between subplots
plt.subplots_adjust(wspace=0.3, hspace=0.3)

# save and Show the plot
plt.rc("svg", fonttype="none")
plt.savefig('analysis/pilotData_analysis/FPA_analysis/pilot_distFPAdur_totalSubs.svg')

plt.show()