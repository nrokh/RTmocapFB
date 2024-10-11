import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import pandas as pd
import seaborn as sns
import ptitprince as pt

###################### Load Data ###################### 
sub_ID = pd.read_excel('analysis/fullData_analysis/survey_analysis/all_survey_results.xlsx', sheet_name='All', usecols='B')
fb_group = pd.read_excel('analysis/fullData_analysis/survey_analysis/all_survey_results.xlsx', sheet_name='All', usecols='C')
tlx = pd.read_excel('analysis/fullData_analysis/survey_analysis/all_survey_results.xlsx', sheet_name='TLX')
ocean = pd.read_excel('analysis/fullData_analysis/survey_analysis/all_survey_results.xlsx', sheet_name='OCEAN')
tam = pd.read_excel('analysis/fullData_analysis/survey_analysis/all_survey_results.xlsx', sheet_name='TAM')
open_ended = pd.read_excel('analysis/fullData_analysis/survey_analysis/all_survey_results.xlsx', sheet_name='Open')
switch = pd.read_excel('analysis/fullData_analysis/survey_analysis/all_survey_results.xlsx', sheet_name='Switch')
borg = pd.read_excel('analysis/fullData_analysis/survey_analysis/all_survey_results.xlsx', sheet_name='Borg')

###################### Borg ###################### 
for col in borg.columns:
    borg[col] = borg[col].apply(lambda x: x.split(':')[0] if isinstance(x, str) and ':' in x else x)
borg = borg.apply(pd.to_numeric)
borg['Borg_RPE_mean'] = round(borg.mean(axis=1), 1)
borg['Borg_RPE_ret'] = borg.iloc[:, 6]

###################### TLX Scoring ###################### 
tlx['RTLX'] = round(tlx.iloc[:, 0:6].sum(axis=1) / 6, 1) # RTLX (raw TLX)

###################### TAM Scoring ###################### 
"""
    perceived usefulness (PU) and perceived ease of use (PEOU)
    PU: 1, 2, 6, 7, 8
    PEOU: 3, 4, 5, 9, 10
    Changed 'Strongly Disagree' to 1, ..., 'Strongly Agree' to 7 and summed the scores for each trait
"""
tam = tam.replace({'Strongly disagree': 1, 'Disagree': 2, 'Somewhat disagree': 3, 'Neutral': 4, 'Somewhat agree': 5, 'Agree': 6, 'Strongly agree': 7})

tam['PU'] = tam.iloc[:, [0, 1, 5, 6, 7]].sum(axis=1)
tam['PEOU'] = tam.iloc[:, [2, 3, 4, 8, 9]].sum(axis=1)

# TAM scores as the mean
tam['PU_mean'] = tam['PU'] / 5
tam['PEOU_mean'] = tam['PEOU'] / 5

# TAM scores as a fraction of the total possible score
tam['PU_frac'] = tam['PU'] / 35
tam['PEOU_frac'] = tam['PEOU'] / 35

###################### OCEAN Scoring ###################### 
"""
    (R = reverse scored): 10R, 40R, 17R, 2R, 22R, 9R, 29R, 14R, 34R, 41R, 16R, 3R, 23R, 25R, 37R
    Extraversion: 1, 10R, 20, 30, 40R, 7, 17R, 27 
    Agreeableness: 2R, 12, 22R, 32, 42, 9R, 19, 29R, 39 
    Conscientiousness: 4, 14R, 24, 34R, 11, 21, 31, 41R  
    Neuroticism: 6, 16R, 26, 36, 3R, 13, 23R, 33 
    Openness: 8, 18, 28, 38, 5, 15, 25R, 35, 37R, 43 
    Changed 'Disagree' to 1, ..., 'Agree' to 5 and summed the scores for each trait
"""

ocean = ocean.replace({'Disagree': 1, 'Slightly disagree': 2, 'Neutral': 3, 'Slightly agree': 4, 'Agree': 5})
ocean.iloc[:, [9, 39, 16, 1, 21, 8, 28, 13, 33, 40, 15, 2, 22, 24, 36]] = 6 - ocean.iloc[:, [9, 39, 16, 1, 21, 8, 28, 13, 33, 40, 15, 2, 22, 24, 36]]

ocean['Extraversion'] = ocean.iloc[:, [0, 9, 19, 29, 39, 6, 16, 27]].sum(axis=1)
ocean['Agreeableness'] = ocean.iloc[:, [1, 11, 21, 31, 41, 8, 18, 28, 38]].sum(axis=1)
ocean['Conscientiousness'] = ocean.iloc[:, [3, 13, 23, 33, 10, 20, 30, 40]].sum(axis=1)
ocean['Neuroticism'] = ocean.iloc[:, [5, 15, 25, 35, 2, 12, 22, 32]].sum(axis=1)
ocean['Openness'] = ocean.iloc[:, [7, 17, 27, 37, 4, 14, 24, 34, 36, 42]].sum(axis=1)

# OCEAN scores as the mean 
ocean['Extraversion_mean'] = ocean['Extraversion'] / 8
ocean['Agreeableness_mean'] = ocean['Agreeableness'] / 9
ocean['Conscientiousness_mean'] = ocean['Conscientiousness'] / 8
ocean['Neuroticism_mean'] = ocean['Neuroticism'] / 8
ocean['Openness_mean'] = ocean['Openness'] / 10

# OCEAN scores as a fraction of the total possible score
ocean['Extraversion_frac'] = ocean['Extraversion'] / 40
ocean['Agreeableness_frac'] = ocean['Agreeableness'] / 45
ocean['Conscientiousness_frac'] = ocean['Conscientiousness'] / 40 
ocean['Neuroticism_frac'] = ocean['Neuroticism'] / 40 
ocean['Openness_frac'] = ocean['Openness'] / 50

###################### Switch ###################### 
""" 
    SW1 = enjoy more, SW2 = best for learning
    Trinary = 1, Scaled = 2
"""
switch['SW1'] = switch.iloc[:, 2].astype(str)
switch['SW2'] = switch.iloc[:, 4].astype(str)

# for each of the values in SW1 and SW2, check if the start of the string is 'S' or 'C' and assign a value of 2 or 1 respectively
switch['SW1'] = switch['SW1'].apply(lambda x: 2 if x[0] == 'S' else 1)
switch['SW2'] = switch['SW2'].apply(lambda x: 2 if x[0] == 'S' else 1)

###################### Saving ###################### 
# save to combined df
all_data = pd.concat([sub_ID, fb_group, tlx.iloc[:,0:6], tlx['RTLX'], tam['PU'], tam['PEOU'], ocean['Extraversion'], ocean['Agreeableness'], ocean['Conscientiousness'], ocean['Neuroticism'], ocean['Openness'], switch['SW1'], switch['SW2'], borg['Borg_RPE_mean'], borg['Borg_RPE_ret']], axis=1)
all_data.columns = ['subject','test_group','mental_demand', 'physical_demand', 'temporal_demand', 'effort', 'frustration', 'performance', 'RTLX', 'PU', 'PEOU','extraversion', 'agreeableness', 'conscientiousness', 'neuroticism', 'openness', 'switch1', 'switch2', 'Borg_RPE_mean', 'Borg_RPE_ret']
all_data['test_group'] = all_data['test_group'].map({0: 'NF', 1: 'TF', 2: 'SF'})

# save to file
all_data.to_csv('analysis/fullData_analysis/survey_analysis/parsed_survey_data.csv', index=False)
###################### Plotting ###################### 

# Plot RTLX scores by feedback condition
def plot_scores_by_condition(ax, data, column, title):
    feedback_conditions = ['Feedback', 'No Feedback']
    feedback_data = data[(data['test_group'] == 'SF') | (data['test_group'] == 'TF')][column]
    no_feedback_data = data[data['test_group'] == 'NF'][column]
    
    # Violin plot for Feedback and No Feedback
    violin_parts = ax.violinplot([feedback_data, no_feedback_data], positions=range(1, 3), showmeans=True, showextrema=True, showmedians=False)
    
    # Scatter plot for SF and TF within Feedback, and NF within No Feedback
    sf_data = data[data['test_group'] == 'SF'][column]
    tf_data = data[data['test_group'] == 'TF'][column]
    nf_data = data[data['test_group'] == 'NF'][column]
    
    ax.scatter(np.random.normal(1, 0.04, len(sf_data)), sf_data, alpha=0.3, s=50, label='SF', color='blue')
    ax.scatter(np.random.normal(1, 0.04, len(tf_data)), tf_data, alpha=0.3, s=50, label='TF', color='green')
    ax.scatter(np.random.normal(2, 0.04, len(nf_data)), nf_data, alpha=0.3, s=50, label='NF', color='red')
    
    ax.set_title(title)
    ax.set_ylabel(f'{column} Score')
    ax.set_xticks(range(1, 3))
    ax.set_xticklabels(feedback_conditions)
    ax.legend()

fig = plt.figure(figsize=(18, 12))

# Create a grid spec with 2 rows and 2 columns
gs = fig.add_gridspec(2, 2, width_ratios=[2, 1])

# Plot RTLX scores by feedback condition (taking up 2 rows, 1 column)
ax0 = fig.add_subplot(gs[:, 0])
plot_scores_by_condition(ax0, all_data, 'RTLX', 'RTLX Scores by Feedback Condition')
ax0.set_ylim(0, 100)

# Plot mental demand scores by feedback condition (top right)
ax1 = fig.add_subplot(gs[0, 1])
plot_scores_by_condition(ax1, all_data, 'mental_demand', 'Mental Demand Scores by Feedback Condition')
ax1.set_ylim(0, 100)

# Plot Borg RPE (retention) scores by feedback condition (bottom right)
ax2 = fig.add_subplot(gs[1, 1])
plot_scores_by_condition(ax2, all_data, 'Borg_RPE_ret', 'Borg RPE Scores (Retention) by Feedback Condition')
ax2.set_ylim(6, 20)

plt.tight_layout()
plt.show()


# # Plot each of the tlx subscales as 6 subplots, boxplots for each group
# fig, axes = plt.subplots(2, 3, figsize=(18, 12))
# axes = axes.flatten()
# for i, col in enumerate(all_data.columns[2:8]): 
#     sns.boxplot(x='test_group', y=col, data=all_data, ax=axes[i], palette=['#A85751', '#1B998B', '#424B54' ])
#     axes[i].set_title(f'{col} by FB Group', fontsize=16, fontweight='bold')
#     axes[i].set_ylabel(col, fontsize=14)
#     axes[i].set_xlabel('Group', fontsize=14)
#     axes[i].tick_params(axis='x', labelsize=12)
#     axes[i].tick_params(axis='y', labelsize=12)
#     axes[i].yaxis.grid(True)
#     axes[i].xaxis.grid(True)
#     axes[i].set_ylim(-10, 100)
# plt.tight_layout()
# plt.savefig('analysis/survey_analysis/tlx_scores_by_group.png')
# plt.show()


# # Plot PU and PEOU for each group
# fig, axes = plt.subplots(1, 2, figsize=(12, 6))
# sns.boxplot(x='test_group', y='PU', data=all_data, ax=axes[0], palette=['#A85751', '#1B998B', '#424B54' ])
# axes[0].set_title('Perceived Usefulness by FB Group', fontsize=16, fontweight='bold')
# axes[0].set_ylabel('Perceived Usefulness', fontsize=14)
# axes[0].set_xlabel('Group', fontsize=14)
# axes[0].tick_params(axis='x', labelsize=12)
# axes[0].tick_params(axis='y', labelsize=12)
# axes[0].yaxis.grid(True)
# axes[0].xaxis.grid(True)
# axes[0].set_ylim(0,35)

# sns.boxplot(x='test_group', y='PEOU', data=all_data, ax=axes[1], palette=['#A85751', '#1B998B', '#424B54' ])
# axes[1].set_title('Perceived Ease of Use by FB Group', fontsize=16, fontweight='bold')
# axes[1].set_ylabel('Perceived Ease of Use', fontsize=14)
# axes[1].set_xlabel('Group', fontsize=14)
# axes[1].tick_params(axis='x', labelsize=12)
# axes[1].tick_params(axis='y', labelsize=12)
# axes[1].yaxis.grid(True)
# axes[1].xaxis.grid(True)
# axes[1].set_ylim(0,35)
# plt.tight_layout()
# plt.figtext(0.5, 0.01, "*note: this is for general vibrotactile feedback", ha="center", fontsize=12, style='italic')
# plt.savefig('analysis/survey_analysis/tam_scores_by_group.png')
# plt.show()


# make a grouped bar plot of the SW1 and SW2 scores for each group, showing how many people chose each option for each group
fig, axes = plt.subplots(1, 2, figsize=(12, 6))
switch1_counts = all_data.groupby(['test_group', 'switch1']).size().unstack()
switch2_counts = all_data.groupby(['test_group', 'switch2']).size().unstack()
switch1_counts.plot(kind='bar', stacked=True, ax=axes[0], color=['#1B998B', '#A85751'])
axes[0].set_title('Enjoyed More by FB Group', fontsize=16, fontweight='bold')
axes[0].set_ylabel('Count', fontsize=14)
axes[0].set_xlabel('Group', fontsize=14)
axes[0].tick_params(axis='x', labelsize=12)
axes[0].tick_params(axis='y', labelsize=12)
axes[0].get_legend().set_visible(False)

switch2_counts.plot(kind='bar', stacked=True, ax=axes[1], color=['#1B998B', '#A85751'])
axes[1].set_title('Perceived Use for Learning by FB Group', fontsize=16, fontweight='bold')
axes[1].set_ylabel('Count', fontsize=14)
axes[1].set_xlabel('Group', fontsize=14)
axes[1].tick_params(axis='x', labelsize=12)
axes[1].tick_params(axis='y', labelsize=12)
plt.tight_layout()
legend = plt.legend( loc='upper right', labels=['TF', 'SF'])
# plt.savefig('analysis/survey_analysis/switch_scores_by_group.png')
plt.show()






