import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import filedialog
from scipy import stats
from matplotlib.colors import to_rgba
import ptitprince as pt 
import seaborn as sns

root = tk.Tk()
root.withdraw() 
directory = filedialog.askdirectory()
subs_tot = 36

# Select the file that has all the subject folders
feedbackCond_csv_file = os.path.normpath(os.path.join(directory, 'feedbackGroups.csv'))
fb_cond = pd.read_csv(feedbackCond_csv_file).values.flatten()[:36] # 2 = SF, 1 = TF, 0 = NF

# Load VB test data from day 1, look at accuracy for each duration difference (30, 80, 240, 300 ms)
vbtest = []
duration_diff_ms = []
vibration_side = [1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 
                  0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0] # 1 = right, 0 = left
duration_pairs_ms = [[300 , 380], [300, 270], [330, 300], [300, 600], [270, 300], [60, 300], [220, 300], [300, 330], [380, 300],
                [300, 270], [300, 220], [300, 60], [330, 300], [300, 60], [300, 380], [220, 300], [300, 600], [270, 300], [600, 300],
                [270, 300], [60, 300], [300, 380], [300, 220], [300, 330], [300, 60], [600, 300], [300, 220], [380, 300], [330, 300],
                [600, 300], [300, 380], [300, 270], [330, 300], [300, 600], [270, 300], [60, 300], [220, 300], [300, 330], [380, 300],
                [300, 270], [300, 220], [300, 60], [330, 300], [300, 60], [300, 380], [220, 300], [300, 600], [270, 300], [600, 300],
                [270, 300], [60, 300], [300, 380], [300, 220], [300, 330], [300, 60], [600, 300], [300, 220], [380, 300], [330, 300], [600, 300]] # vibration pairs used in the VB test (ms)

# Calculate the difference between durations (ms
for i in range(len(duration_pairs_ms)):
    duration_diff_ms.append(abs(duration_pairs_ms[i][0] - duration_pairs_ms[i][1]))

for i in range(subs_tot):
    sub = i+1
    sub_str = str(sub).zfill(2)
    vbtest_file = os.path.normpath(os.path.join(directory, 's'+sub_str,'s'+sub_str+'_day1_vbtest.csv'))
    vbtest.append(np.genfromtxt(vbtest_file, delimiter=','))
    if sub == 4:
        vbtest[3][0] = 1 # something is weird with the first row...

# Sort the accuracy of the VB test by duration difference
duration_diff_counts = [0, 0, 0, 0]
duration_idx = [[], [], [], []]
duration_diff_map = {30: 0, 80: 1, 240: 2, 300: 3}

for i, diff in enumerate(duration_diff_ms):
    if diff in duration_diff_map:
        idx = duration_diff_map[diff]
        duration_diff_counts[idx] += 1
        duration_idx[idx].append(i)

vbtest_acc = np.zeros((subs_tot, 4))
for i in range(subs_tot):
    for j in range(4):
        idx = duration_idx[j]
        for k in idx:
            if vbtest[i][k] == 1:
                vbtest_acc[i][j] += 1
        
vbtest_acc = np.column_stack((vbtest_acc, np.sum(vbtest_acc, axis=1)))
trial_counts = np.array([len(duration_idx[j]) for j in range(4)] + [len(duration_pairs_ms)])
vbtest_acc = vbtest_acc / trial_counts # normalize by the number of trials

# Visualizing the vb accuracy data
df = pd.DataFrame(vbtest_acc, columns=['30 ms', '80 ms', '240 ms', '300 ms', 'Total'])
df['Feedback Condition'] = fb_cond
df = pd.melt(df, id_vars=['Feedback Condition'], value_vars=['30 ms', '80 ms', '240 ms', '300 ms', 'Total'], 
             var_name='Duration Difference (ms)', value_name='Accuracy')

fig, axs = plt.subplots(2, 2, figsize=(15, 10))

# Scatter plots for each feedback condition - TODO: figure out how to condense this to one subplot... currently doing in affinty designer
feedback_conditions = ['NF', 'TF', 'SF']
for i, cond in enumerate(feedback_conditions):
    ax = axs[i // 2, i % 2]
    for duration in ['30 ms', '80 ms', '240 ms', '300 ms']:
        subset = df[(df['Feedback Condition'] == i) & (df['Duration Difference (ms)'] == duration)]
        sizes = subset.groupby('Accuracy').size().reindex(subset['Accuracy']).fillna(0) * 100  # Scale factor for size
        sns.scatterplot(x='Duration Difference (ms)', y='Accuracy', data=subset, 
                        color='black', marker='o', s=sizes, ax=ax, label=duration)
    ax.set_title(f'VB Test Accuracy for {cond} Feedback Condition')
    ax.set_ylim(0.4, 1.1)  # Set y-axis limits
    ax.legend().set_visible(False)  # Turn off the legend

# Violin plot for total accuracy
ax = axs[1, 1]
sns.violinplot(x='Feedback Condition', y='Accuracy', data=df[df['Duration Difference (ms)'] == 'Total'], ax=ax, palette=['#424B54', '#1B998B', '#A85751'])
ax.set_xticklabels(['NF', 'TF', 'SF'])
ax.set_title('Total VB Test Accuracy by Feedback Condition')
ax.set_ylim(0.4, 1.1)  # Set y-axis limits

plt.tight_layout()
plt.show()

# Stats for the accuracy for VB test... do we want to include this?
nf_acc = df[(df['Feedback Condition'] == 0) & (df['Duration Difference (ms)'] == 'Total')]['Accuracy']
tf_acc = df[(df['Feedback Condition'] == 1) & (df['Duration Difference (ms)'] == 'Total')]['Accuracy']
sf_acc = df[(df['Feedback Condition'] == 2) & (df['Duration Difference (ms)'] == 'Total')]['Accuracy']

# Shapiro-Wilk test for normality
nf_shapiro = stats.shapiro(nf_acc) #p = 0.122
tf_shapiro = stats.shapiro(tf_acc) #p = 0.0135*
sf_shapiro = stats.shapiro(sf_acc) #p = 0.310
total_shapiro = stats.shapiro(df[df['Duration Difference (ms)'] == 'Total']['Accuracy']) #p = 0.183

# Bartlett's test for equal variance... p = 0.556
bartlett = stats.bartlett(nf_acc, tf_acc, sf_acc)




