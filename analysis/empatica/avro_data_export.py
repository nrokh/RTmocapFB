from avro.datafile import DataFileReader
from avro.io import DatumReader
import json
import csv
import os
import matplotlib.pyplot as plt
import numpy as np
# import keyboard
import tkinter as tk
from tkinter import filedialog
import pandas as pd
import random


####################################### FUNCTIONS ########################################

def fix_time(time):
    hour_chng = int(time.split(':')[0])-2 #convert to UTC time from CET
    time = str(hour_chng) + ':' + time.split(':')[1]
    if len(time) == 4:
        time = '0' + time
    return time

def combine_processed_biomarkers(input_directory, output_directory, subject_name, day):
    csv_data_path = os.path.join(input_directory, day, subject_name, 'digital_biomarkers','aggregated_per_minute')
    # moved files that have "_sleep-detection", "_eda", "_prv", "_step-counts" to the output directory + a new folder "processed_biomarkers"... create this folder if it doesnt exist
    biomarker_filepath = os.path.join(output_directory, subject_name,'processed_biomarkers')
    os.makedirs(biomarker_filepath, exist_ok=True)
    timestamp_ms = []
    timestamp_iso = []
    data_bm = []
    missing_data = []
    file_order = []
    data_name = []

    for file in os.listdir(csv_data_path):
        if '_sleep-detection' in file or '_eda' in file or '_prv' in file or '_step-counts' in file or '_pulse-rate' in file: #add the biomarkers of interest here
            # read the first colm from each of the files and make sure they are exactly the same
            with open(os.path.join(csv_data_path, file), 'r') as f:
                reader = csv.reader(f)
                data = list(reader)
                file_timestamp = [data[i][0] for i in range(1, len(data))]
                file_timestamp_iso = [data[i][1] for i in range(1, len(data))]
                file_data = [data[i][3] for i in range(1, len(data))]
                file_missing_data = [data[i][4] for i in range(1, len(data))]
                
                file_order.append(file)
                data_name.append(file.split('_')[2].split('.')[0])
                timestamp_ms.append(file_timestamp)
                timestamp_iso.append(file_timestamp_iso)
                data_bm.append(file_data) #add label for each appended data
                missing_data.append(file_missing_data)

    # check if the timestamp_ms are the same
    if len(set([tuple(i) for i in timestamp_ms])) == 1:
        print('Timestamps are the same')
        df = pd.DataFrame(list(zip(timestamp_ms[0], timestamp_iso[0], data_bm[0], data_bm[1], data_bm[2], data_bm[3], data_bm[4], missing_data[0])), columns =['timestamp_ms', 'timestamp_iso', data_name[0], data_name[1], data_name[2], data_name[3], data_name[4], 'missing_data'])
        #TODO: make this ^^ changeable to any number of files/ biomarkers
        #check if os.path.join(biomarker_filepath, 'biomarkers_combined.csv') exists, if it does, append to it
        if os.path.exists(os.path.join(biomarker_filepath, 'biomarkers_combined.csv')):
            df.to_csv(os.path.join(biomarker_filepath, 'biomarkers_combined.csv'), mode='a', header=False, index=False)
        else:
            df.to_csv(os.path.join(biomarker_filepath, 'biomarkers_combined.csv'), index=False)
    else:
        print('ERROR: Timestamps are not the same... saving to separate files')
        for i in range(len(file_order)):
            data_name = file_order[i].split('_')[2].split('.')[0]
            df = pd.DataFrame(list(zip(timestamp_ms[i], timestamp_iso[i], data_bm[i], missing_data[i])), columns =['timestamp_ms', 'timestamp_iso', data_name, 'missing_data'])
            if os.path.exists(biomarker_filepath, file_order[i]):
                df.to_csv(os.path.join(biomarker_filepath, file_order[i]), mode='a', header=False, index=False)
            else:
                df.to_csv(os.path.join(biomarker_filepath, file_order[i]), index=False)
        return
    # return df

def parse_subject_data(combined_bm_data, startday, starttime, endday, endtime):

    start_index = 0
    end_index = 0
    for i in range(len(combined_bm_data)):
        if combined_bm_data['timestamp_iso'][i] == startday + 'T' + starttime + ':00Z':
            start_index = i
        elif combined_bm_data['timestamp_iso'][i] == endday + 'T' + endtime + ':00Z':
            end_index = i
        
    if start_index == 0 or end_index == 0:
        print('ERROR: Start or End index not found')
        return
    
    trunc_data = combined_bm_data[start_index:end_index]

    # remove missing data (when the missing_data column has a nan value)
    trunc_data_correct_wear = trunc_data[trunc_data['missing_data'].isna() == True]
    return trunc_data_correct_wear
            
def step_segmentation(trunc_bm_data):
    regular_step_sections = []
    random_segs = []
    step_segment_count = 0
    frame_count = 0
    while frame_count < int(len(trunc_bm_data)-4):
        if int(trunc_bm_data['step-counts'].values[frame_count]) > 0:
            step_group = [trunc_bm_data['step-counts'].values[frame_count], trunc_bm_data['step-counts'].values[frame_count+1], trunc_bm_data['step-counts'].values[frame_count+2], trunc_bm_data['step-counts'].values[frame_count+3], trunc_bm_data['step-counts'].values[frame_count+4]]
            hr_group = [trunc_bm_data['pulse-rate'].values[frame_count], trunc_bm_data['pulse-rate'].values[frame_count+1], trunc_bm_data['pulse-rate'].values[frame_count+2], trunc_bm_data['pulse-rate'].values[frame_count+3], trunc_bm_data['pulse-rate'].values[frame_count+4]]
            eda_group = [trunc_bm_data['eda'].values[frame_count], trunc_bm_data['eda'].values[frame_count+1], trunc_bm_data['eda'].values[frame_count+2], trunc_bm_data['eda'].values[frame_count+3], trunc_bm_data['eda'].values[frame_count+4]]
            step_sum = int(sum(step_group))
            range_step = int(max(step_group) - min(step_group))
            range_hr = int(max(hr_group) - min(hr_group))
            range_eda = max(eda_group) - min(eda_group)   

            if step_sum > 300 and step_sum < 500 and range_step < 100 and range_hr < 60 and max(hr_group) < 150 and range_eda < 0.2 and max(eda_group) < 1.0: #TODO: validate using this criteria to find the 5-min walking trials
                regular_step_sections.append([trunc_bm_data['timestamp_iso'].values[frame_count], frame_count, trunc_bm_data['timestamp_iso'].values[frame_count+4], frame_count+4, step_sum, np.mean(eda_group), np.mean(hr_group)])
                frame_count += 4
                step_segment_count += 1
        frame_count += 1

    if step_segment_count == 0:
        print('No step segments found')
        return
    
    eda_mean = np.mean([segs[5] for segs in regular_step_sections])
    eda_std = np.std([segs[5] for segs in regular_step_sections]) 
    for segs in regular_step_sections:
        if segs[5] > eda_mean + 3*eda_std or segs[5] < eda_mean - 3*eda_std:
            regular_step_sections.remove(segs)
            step_segment_count -= 1

    #pick 5 random segments to plot
    if step_segment_count > 5:
        random_segs = random.sample(regular_step_sections, 5)
    else:
        random_segs = regular_step_sections
        print('Less than 5 segments found, plotting all segments...')
        
    return regular_step_sections, random_segs, step_segment_count

def lab_step_segmentation(trunc_bm_data, subject_empatica_data):
    lab_step_sections = []
    frame_count = 0
    if subject_empatica_data.iloc[16] == 'N':
        print('No lab data for this subject')
    else:
        test_day = subject_empatica_data.iloc[6]
        baseline = test_day + 'T' + fix_time(subject_empatica_data.iloc[8]) + ':00Z'
        toein_1 = test_day + 'T' + fix_time(subject_empatica_data.iloc[9]) + ':00Z'
        toein_2 = test_day + 'T' + fix_time(subject_empatica_data.iloc[10]) + ':00Z'
        toein_3 = test_day + 'T' + fix_time(subject_empatica_data.iloc[11]) + ':00Z'
        toein_4 = test_day + 'T' + fix_time(subject_empatica_data.iloc[12]) + ':00Z'
        retention = test_day + 'T' + fix_time(subject_empatica_data.iloc[13]) + ':00Z'
        while frame_count < int(len(trunc_bm_data)-4):
            if trunc_bm_data['timestamp_iso'].values[frame_count] == baseline:
                lab_step_sections.append([trunc_bm_data['timestamp_iso'].values[frame_count], frame_count, trunc_bm_data['timestamp_iso'].values[frame_count+4], frame_count+4, 'baseline'])
                frame_count += 4
            elif trunc_bm_data['timestamp_iso'].values[frame_count] == toein_1:
                lab_step_sections.append([trunc_bm_data['timestamp_iso'].values[frame_count], frame_count, trunc_bm_data['timestamp_iso'].values[frame_count+4], frame_count+4, 'toein'])
                frame_count += 4
            elif trunc_bm_data['timestamp_iso'].values[frame_count] == toein_2:
                lab_step_sections.append([trunc_bm_data['timestamp_iso'].values[frame_count], frame_count, trunc_bm_data['timestamp_iso'].values[frame_count+4], frame_count+4, 'toein'])
                frame_count += 4
            elif trunc_bm_data['timestamp_iso'].values[frame_count] == toein_3:
                lab_step_sections.append([trunc_bm_data['timestamp_iso'].values[frame_count], frame_count, trunc_bm_data['timestamp_iso'].values[frame_count+4], frame_count+4, 'toein'])
                frame_count += 4
            elif trunc_bm_data['timestamp_iso'].values[frame_count] == toein_4:
                lab_step_sections.append([trunc_bm_data['timestamp_iso'].values[frame_count], frame_count, trunc_bm_data['timestamp_iso'].values[frame_count+4], frame_count+4, 'toein'])
                frame_count += 4
            elif trunc_bm_data['timestamp_iso'].values[frame_count] == retention:
                lab_step_sections.append([trunc_bm_data['timestamp_iso'].values[frame_count], frame_count, trunc_bm_data['timestamp_iso'].values[frame_count+4], frame_count+4, 'retention'])
                frame_count += 4
            else:
                frame_count += 1

        if len(lab_step_sections) == 0:
            print('WARNING - No lab step sections found, data is not segmented correctly')

    return lab_step_sections

def plot_pulse_eda(trunc_bm_data, sample_step_segs, output_directory, subject_name):

    copts = ['#46B1C9', '#034732', '#DD6031', '#E4CA04', '#820263']
    lopts = ['-', '--','-.',':',(5, (10, 3))]
    opts_n = 0
    fig = plt.gcf()
    (ax1, ax2) = fig.subplots(2)
    #make full screen 
    fig.set_size_inches(18.5, 10.5)
    fig.subplots_adjust(top=1, bottom=0.05, left=0.05, right=0.95, hspace=0.5, wspace=0.5)
    plt.subplots_adjust(hspace=0.35, wspace=0.2)
    ax2.set_xlabel('Time')
    ax1.set_ylabel('Pulse Rate')
    ax2.set_ylabel('EDA')
    ax1.set_ylim([0, 150])
    ax2.set_ylim([0, 1])

    for seg in sample_step_segs:
        # if opts_n < len(copts):
        ax1.plot(((trunc_bm_data['timestamp_ms'].values[seg[1]:seg[3]+1] - trunc_bm_data['timestamp_ms'].values[seg[1]])*1e-3)/60, trunc_bm_data['pulse-rate'].values[seg[1]:seg[3]+1], color = copts[opts_n], linestyle = lopts[opts_n], label = trunc_bm_data['timestamp_iso'].values[seg[1]].split('T')[0] + ' @ ' + trunc_bm_data['timestamp_iso'].values[seg[1]].split('T')[1].split('Z')[0])
        ax2.plot(((trunc_bm_data['timestamp_ms'].values[seg[1]:seg[3]+1] - trunc_bm_data['timestamp_ms'].values[seg[1]])*1e-3)/60, trunc_bm_data['eda'].values[seg[1]:seg[3]+1], color = copts[opts_n], linestyle = lopts[opts_n])
        opts_n += 1
            
    ax1.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=6)
    ax2.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=6)
    
    #save the plot and data to a file
    plt.savefig(os.path.join(output_directory, subject_name, 'pulse_eda_plot.pdf'), format='pdf', bbox_inches='tight')
    plt.show()

def plot_boxplot(trunc_bm_data, sample_step_segs, lab_step_segs, output_directory, subject_name):
    box_plot_data = [] #pulse rate, eda, lab or not
    for seg in sample_step_segs:
        box_plot_data.append([trunc_bm_data['pulse-rate'].values[seg[1]:seg[3]+1], trunc_bm_data['eda'].values[seg[1]:seg[3]+1], 'outside_lab'])   
    for seg in lab_step_segs:
        box_plot_data.append([trunc_bm_data['pulse-rate'].values[seg[1]:seg[3]+1], trunc_bm_data['eda'].values[seg[1]:seg[3]+1], seg[4]])

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xticklabels(['Outside Lab', 'Toe-in'])
    ax.set_ylabel('Pulse Rate & EDA')
    ax.set_xlabel('Walking Trials') 
    
    ax.boxplot([box_plot_data[i][0] for i in range(len(box_plot_data))], positions = [i for i in range(len(box_plot_data))])
    plt.savefig(os.path.join(output_directory, subject_name, 'pulse_eda_boxplot.pdf'), format='pdf', bbox_inches='tight')

def sleep_detection(trunc_bm_data):
    # based on https://www.tandfonline.com/doi/full/10.1080/07420528.2020.1835942
    sleep_cycle = []
    sleep_minutes = 0 
    sleep_full_wake = 0 #0
    sleep_count = 0 #101
    sleep_wake = 0 #102
    sleep_intrpt = 0 #300

    sleep_start_flag = 0
    sleep_block_count = 0

    for frame_count in range(len(trunc_bm_data)):
        frame_hour = trunc_bm_data['timestamp_iso'].values[frame_count].split('T')[1].split(':')[0]
        if int(frame_hour) > 18 or int(frame_hour) < 11: #check that the time is between 6pm and 11am and not a midday nap
            #NOTE: we are defining a sleep block as 1 hr or more of sleep
            if trunc_bm_data['sleep-detection'].values[frame_count] > 100 and sleep_start_flag == 0 and sleep_block_count == 0:
                potential_sleep_start = frame_count
                sleep_block_count += 1
            elif trunc_bm_data['sleep-detection'].values[frame_count] > 100 and sleep_start_flag == 0 and sleep_block_count < 60 and sleep_block_count > 0:
                sleep_block_count += 1
            elif trunc_bm_data['sleep-detection'].values[frame_count] > 100 and sleep_start_flag == 0 and sleep_block_count == 60:
                sleep_start_flag = 1
                start_frame = potential_sleep_start
            elif trunc_bm_data['sleep-detection'].values[frame_count] > 100 and sleep_start_flag == 1:
                end_frame = frame_count
            else:
                sleep_block_count = 0
                potential_sleep_start = 0

    for sframe_count in range(start_frame,end_frame):
        sleep_cycle.append([trunc_bm_data['timestamp_iso'].values[sframe_count],trunc_bm_data['sleep-detection'].values[sframe_count]])
        sleep_minutes += 1
        if trunc_bm_data['sleep-detection'].values[sframe_count] == 101: #sleep
            sleep_count += 1 
        elif trunc_bm_data['sleep-detection'].values[sframe_count] == 102: #wake, but still asleep
            sleep_wake += 1
        elif trunc_bm_data['sleep-detection'].values[sframe_count] == 300: #awake, but for long period
            sleep_intrpt += 1
        elif trunc_bm_data['sleep-detection'].values[sframe_count] == 0: #fully awake during the night
            sleep_full_wake += 1

    sleep_qual = sleep_count/sleep_minutes
    sleep_hours = sleep_minutes/60
    return sleep_cycle, sleep_qual, sleep_hours, sleep_count, sleep_wake, sleep_intrpt, sleep_full_wake

###################################### MAIN ########################################
####### Retrieve and combine biomarker data for each day #######
# # comment out if you already made the combined files and are doing other processing 
# in_root = tk.Tk()
# in_root.withdraw() 
# print('Select the input directory....')
# input_directory = filedialog.askdirectory()

# out_root = tk.Tk()
# out_root.withdraw() 
# print('Select the output directory....')
# output_directory = filedialog.askdirectory()

# #ask if you want to process data for all subjects or just one
# all_subjects = input('Do you want to process data for all subjects? (y/n): ')
# if all_subjects == 'y':
#     for day in ['day_1', 'day_2']:
#         check_this = os.listdir(os.path.join(input_directory, day))
#         for subject_name in os.listdir(os.path.join(input_directory, day)):
            
#             combine_processed_biomarkers(input_directory, output_directory, subject_name, day)
            
                    
#             print('Finished processing combined file for subject: ', subject_name, ' for day: ', day)
#             print('----------------------------------------')
# else:
#     subject_name = input('Enter the subject you want to process: ')
#     for day in ['day_1', 'day_2']:
#         combine_processed_biomarkers(input_directory, output_directory, subject_name, day)
#         print('Finished processing combined file for subject: ', subject_name, ' for day: ', day)
#         print('----------------------------------------')

####### Truncate the combined biomarker data for each subject #######
# comment out the directory retrieval code below if you are running the combined files code from above
out_root = tk.Tk()
out_root.withdraw() 
print('Select the output directory....')
output_directory = filedialog.askdirectory()

all_subjects_flag = input('Do you want to process data for all subjects? (y/n): ')
if all_subjects_flag == 'y':
    subject_process_list = os.listdir(output_directory)
else:
    subject_process_list = [input('Enter the subject you want to process: ')]

for subject_name in subject_process_list:
    subject_number = subject_name.split('-')[0]
    empatica_data = pd.read_csv('C:\\Users\\vsun\\Documents\\Code\\RTmocapFB\\analysis\\empatica\\emaptica_watch_phone_tracksheet.csv')

    for i in range(len(empatica_data)):
        if str(empatica_data['Subject (Empatica 1-1-#)'][i]) == subject_number:
            subject_empatica_data = empatica_data.iloc[i]
            startday = empatica_data['Day 1'][i]
            starttime = fix_time(empatica_data['Time Start'][i])
            endday = empatica_data['Day 2'][i]
            endtime = fix_time(empatica_data['Time End'][i])
            break

    # open the combined file for the subject and load it into a pandas dataframe, then trucate the data for plotting
    combined_bm_data = pd.read_csv(os.path.join(output_directory, subject_name, 'processed_biomarkers', 'biomarkers_combined.csv'))
    trunc_bm_data = parse_subject_data(combined_bm_data, startday, starttime, endday, endtime)   
    print('Finished truncated file for subject: ', subject_name)

    # find sections of step data where the subject takes 350-450 steps in a five minute window, average the biomarker data
    all_step_segs, sample_segs, step_seg_count = step_segmentation(trunc_bm_data)
    print('Finished step segmentation for subject: ', subject_name)

    # plot the pulse rate and eda for each of the ten 5-min walking trials
    plot_pulse_eda(trunc_bm_data, sample_segs, output_directory, subject_name)
    print('Finished plotting pulse and eda for subject (outside the lab): ', subject_name)

    #get the step data for the lab walking trials
    lab_step_segs = lab_step_segmentation(trunc_bm_data, subject_empatica_data)
    print('Finished lab step segmentation for subject: ', subject_name)

    # plot box plots for the walking trials outside of the lab, the walking trials in the lab, and the retention trial 
    # plot_boxplot(trunc_bm_data, sample_segs, output_directory, subject_name)

    # look at sleep detection data and find how long the participant slept for
    sleep_cycle, sleep_qual, sleep_hours, sleep_count, sleep_wake, sleep_intrpt, sleep_full_wake = sleep_detection(trunc_bm_data)    
    print('Finished sleep detection for subject: ', subject_name, ' ... hours asleep: ', round(sleep_hours,2), 'hrs & quality: ', round(sleep_qual,2))


    # segment the data from the walking trials when they are in the lab (baseline, 4 training sessions, retention)
    # TODO: change this to the tagged data right now I am just using the times from the protocol sheet
     

    
    
    

# print('----------------------------------------')
# print('Finished processing all subjects for both days')

#TODO: deal with the raw data files, combine them and save them in the same output directory, use the tags to help with processing the data