import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

survey_data = pd.read_csv('C:/Users/vsun/Documents/Code/RTmocapFB/analysis/fullData_analysis/survey_analysis/parsed_survey_data.csv')

# Exclude subject 9 from the analysis
survey_data_filtered = survey_data[survey_data['subject'] != 'S09']

# plot borg_RPE_ret vs pulse_rate_mean for filtered data
plt.figure()
plt.scatter(survey_data_filtered['pulse_rate_mean'], survey_data_filtered['Borg_RPE_ret'])
plt.ylabel('Borg RPE')
plt.xlabel('Pulse Rate')
plt.title('Borg RPE vs Pulse Rate (excluding subject 9)')
plt.show()

# Plot pulse rate by feedback condition
def plot_pulse_rate_by_condition(ax, data, column, title):
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

# Create a figure and axis for the plot
fig, ax = plt.subplots()
plot_pulse_rate_by_condition(ax, survey_data_filtered, 'pulse_rate_mean', 'Pulse Rate by Feedback Condition (excluding subject 9)')
plt.ylim(50, 200)
plt.show()



