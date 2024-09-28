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

# ################################################################################################################################################################

# # Load VB test data from day 1, look at accuracy for each duration difference (30, 80, 240, 300 ms)
# vbtest = []
# duration_diff_ms = []
# vibration_side = [1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 
#                   0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0] # 1 = right, 0 = left
# duration_pairs_ms = [[300 , 380], [300, 270], [330, 300], [300, 600], [270, 300], [60, 300], [220, 300], [300, 330], [380, 300],
#                 [300, 270], [300, 220], [300, 60], [330, 300], [300, 60], [300, 380], [220, 300], [300, 600], [270, 300], [600, 300],
#                 [270, 300], [60, 300], [300, 380], [300, 220], [300, 330], [300, 60], [600, 300], [300, 220], [380, 300], [330, 300],
#                 [600, 300], [300, 380], [300, 270], [330, 300], [300, 600], [270, 300], [60, 300], [220, 300], [300, 330], [380, 300],
#                 [300, 270], [300, 220], [300, 60], [330, 300], [300, 60], [300, 380], [220, 300], [300, 600], [270, 300], [600, 300],
#                 [270, 300], [60, 300], [300, 380], [300, 220], [300, 330], [300, 60], [600, 300], [300, 220], [380, 300], [330, 300], [600, 300]] # vibration pairs used in the VB test (ms)

# # Calculate the difference between durations (ms
# for i in range(len(duration_pairs_ms)):
#     duration_diff_ms.append(abs(duration_pairs_ms[i][0] - duration_pairs_ms[i][1]))

# for i in range(subs_tot):
#     sub = i+1
#     sub_str = str(sub).zfill(2)
#     vbtest_file = os.path.normpath(os.path.join(directory, 's'+sub_str,'s'+sub_str+'_day1_vbtest.csv'))
#     vbtest.append(np.genfromtxt(vbtest_file, delimiter=','))
#     if sub == 4:
#         vbtest[3][0] = 1 # something is weird with the first row...

# # Sort the accuracy of the VB test by duration difference
# duration_diff_counts = [0, 0, 0, 0]
# duration_idx = [[], [], [], []]
# duration_diff_map = {30: 0, 80: 1, 240: 2, 300: 3}

# for i, diff in enumerate(duration_diff_ms):
#     if diff in duration_diff_map:
#         idx = duration_diff_map[diff]
#         duration_diff_counts[idx] += 1
#         duration_idx[idx].append(i)

# vbtest_acc = np.zeros((subs_tot, 4))
# for i in range(subs_tot):
#     for j in range(4):
#         idx = duration_idx[j]
#         for k in idx:
#             if vbtest[i][k] == 1:
#                 vbtest_acc[i][j] += 1
        
# vbtest_acc = np.column_stack((vbtest_acc, np.sum(vbtest_acc, axis=1)))
# trial_counts = np.array([len(duration_idx[j]) for j in range(4)] + [len(duration_pairs_ms)])
# vbtest_acc = vbtest_acc / trial_counts # normalize by the number of trials

# # Visualizing the vb accuracy data
# df = pd.DataFrame(vbtest_acc, columns=['30 ms', '80 ms', '240 ms', '300 ms', 'Total'])
# df['Feedback Condition'] = fb_cond
# df = pd.melt(df, id_vars=['Feedback Condition'], value_vars=['30 ms', '80 ms', '240 ms', '300 ms', 'Total'], 
#              var_name='Duration Difference (ms)', value_name='Accuracy')

# fig, axs = plt.subplots(2, 2, figsize=(15, 10))

# # Scatter plots for each feedback condition - TODO: figure out how to condense this to one subplot... currently doing in affinity designer
# feedback_conditions = ['NF', 'TF', 'SF']
# for i, cond in enumerate(feedback_conditions):
#     ax = axs[i // 2, i % 2]
#     for duration in ['30 ms', '80 ms', '240 ms', '300 ms']:
#         subset = df[(df['Feedback Condition'] == i) & (df['Duration Difference (ms)'] == duration)]
#         sizes = subset.groupby('Accuracy').size().reindex(subset['Accuracy']).fillna(0).apply(lambda x: 40 + (x - 1) * (1500 - 40) / (12 - 1))  # Scale factor for size
#         sns.scatterplot(x='Duration Difference (ms)', y='Accuracy', data=subset, 
#                         color='black', marker='o', s=sizes, ax=ax, label=duration)
#     ax.set_title(f'VB Test Accuracy for {cond} Feedback Condition')
#     ax.set_ylim(0.4, 1.1)  # Set y-axis limits
#     ax.legend().set_visible(False)  # Turn off the legend

# # Create a legend for the sizes of the dots
# handles, labels = [], []
# for trials in range(1, 13):  # 1 to 12 trials
#     size = 40 + (trials - 1) * (1500 - 40) / (12 - 1)  # Scale factor for size
#     handles.append(plt.scatter([], [], s=size, color='black', alpha=0.6))
#     labels.append(f'{trials} trials')

# fig.legend(handles, labels, title='Dot Size (Number of Trials)', loc='upper right')

# # Violin plot for total accuracy
# ax = axs[1, 1]
# sns.violinplot(x='Feedback Condition', y='Accuracy', data=df[df['Duration Difference (ms)'] == 'Total'], ax=ax, palette=['#424B54', '#1B998B', '#A85751'])
# ax.set_xticklabels(['NF', 'TF', 'SF'])
# ax.set_title('Total VB Test Accuracy by Feedback Condition')
# ax.set_ylim(0.4, 1.1)  # Set y-axis limits

# plt.tight_layout()
# plt.show()

# # Stats for the accuracy for VB test... do we want to include this?
# nf_acc = df[(df['Feedback Condition'] == 0) & (df['Duration Difference (ms)'] == 'Total')]['Accuracy']
# tf_acc = df[(df['Feedback Condition'] == 1) & (df['Duration Difference (ms)'] == 'Total')]['Accuracy']
# sf_acc = df[(df['Feedback Condition'] == 2) & (df['Duration Difference (ms)'] == 'Total')]['Accuracy']

# # Shapiro-Wilk test for normality
# nf_shapiro = stats.shapiro(nf_acc) #p = 0.122
# tf_shapiro = stats.shapiro(tf_acc) #p = 0.0135*
# sf_shapiro = stats.shapiro(sf_acc) #p = 0.310
# total_shapiro = stats.shapiro(df[df['Duration Difference (ms)'] == 'Total']['Accuracy']) #p = 0.183

# # Bartlett's test for equal variance... p = 0.556
# bartlett = stats.bartlett(nf_acc, tf_acc, sf_acc)

################################################################################################################################################################

# Load proprioception data from Day 1 TODO: check that the in_proprio_in and in_proprio_out files are correct and not flipped
files = ['in_proprio_in.csv', 'in_proprio_out.csv', 'in_proprio_RMSE.csv']
data = {}

for file in files:
    file_path = os.path.normpath(os.path.join(directory, 'features', file))
    data[file.split('.')[0]] = np.abs(np.genfromtxt(file_path, delimiter=',')) if 'RMSE' not in file else np.genfromtxt(file_path, delimiter=',')

in_proprio_in = -data['in_proprio_in'][1:].flatten()
in_proprio_out = data['in_proprio_out'][1:].flatten()
in_proprio_RMSE = data['in_proprio_RMSE'][1:].flatten()

# Make a dataframe for the proprioception data with the feedback condition
df = pd.DataFrame({'Feedback Condition': fb_cond, 'Toe-In': in_proprio_in, 'Toe-Out': in_proprio_out, 'RMSE': in_proprio_RMSE})

# Plot the toe-in and toe-out proprioception data (make the toe-in negative) and plot as scatter plot with 0-deg error in the center of the plot, separating the toe-in and toe-out data... the y axis should be the feedback condition group and the x axis should be the proprioceptive error
fig, axs = plt.subplots(1, 2, figsize=(15, 5))

# Define a function to plot the data
def plot_proprioception_error(ax, data, title):
    feedback_conditions = ['SF', 'TF', 'NF']
    violin_parts = ax.violinplot(data, positions=range(1, 4), showmeans=True, showextrema=True, showmedians=False)
    ax.set_title(title)
    ax.set_ylabel('Proprioceptive Error (degrees)')
    ax.set_xticks(range(1, 4))
    ax.set_xticklabels(feedback_conditions)
    for i, cond_data in enumerate(data, start=1):
        ax.scatter(np.random.normal(i, 0.04, len(cond_data)), cond_data, alpha=0.3, s=15)

# Separate data for each feedback condition
data_in = [df[df['Feedback Condition'] == i]['Toe-In'] for i in range(2, -1, -1)]
data_out = [df[df['Feedback Condition'] == i]['Toe-Out'] for i in range(2, -1, -1)]

# Plot Toe-In Proprioceptive Error
plot_proprioception_error(axs[0], data_in, 'Toe-In Proprioceptive Error by Feedback Condition')

# Plot Toe-Out Proprioceptive Error
plot_proprioception_error(axs[1], data_out, 'Toe-Out Proprioceptive Error by Feedback Condition')

plt.tight_layout()
plt.show()
