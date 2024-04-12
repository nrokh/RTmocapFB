from avro.datafile import DataFileReader
from avro.io import DatumReader
import json
import csv
import os
# import matplotlib.pyplot as plt
# import pandas as pd
# import numpy as np
# import keyboard
import tkinter as tk
from tkinter import filedialog
import pandas as pd


####################################### FUNCTIONS ########################################

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

    # shave off excess data 
    start_index = 0
    end_index = 0
    for i in range(len(combined_bm_data)):
        # print(combined_bm_data['timestamp_iso'][i])
        # print(startday + 'T' + starttime + ':00Z')

        if combined_bm_data['timestamp_iso'][i] == startday + 'T' + starttime + ':00Z':
            start_index = i
        elif combined_bm_data['timestamp_iso'][i] == endday + 'T' + endtime + ':00Z':
            end_index = i
        
    if start_index == 0 or end_index == 0:
        print('ERROR: Start or End index not found')
        return
    
    trunc_data = combined_bm_data[start_index:end_index]

    # remove data missing because of device missing data (when the missing_data column has a nan value)
    trunc_data_correct_wear = trunc_data[trunc_data['missing_data'].isna() == True]
    return trunc_data_correct_wear
            

####################################### MAIN ########################################
# ## Retrieve and combine biomarker data for each day - comment out if you already made the combined files and are doing other processing
# in_root = tk.Tk()
# in_root.withdraw() 
# print('Select the input directory....')
# input_directory = filedialog.askdirectory()

# out_root = tk.Tk()
# out_root.withdraw() 
# print('Select the output directory....')
# output_directory = filedialog.askdirectory()

# for day in ['day_1', 'day_2']:
#     check_this = os.listdir(os.path.join(input_directory, day))
#     for subject_name in os.listdir(os.path.join(input_directory, day)):
        
#         combine_processed_biomarkers(input_directory, output_directory, subject_name, day)
        
                
#         print('Finished processing combined file for subject: ', subject_name, ' for day: ', day)
#         print('----------------------------------------')

## Truncate the combined biomarker data for each subject
# comment out the directory retrieval code below if you are running the combined files code from above
out_root = tk.Tk()
out_root.withdraw() 
print('Select the output directory....')
output_directory = filedialog.askdirectory()

for subject_name in os.listdir(output_directory):
    startday = input('\nwhat day did ' + subject_name + ' start the experiment? (YYYY-MM-DD):    ')
    starttime = input('what time did ' + subject_name + ' start the experiment? (HH:MM 24h format):    ')
    endday = input('what day did ' + subject_name + ' end the experiment? (YYYY-MM-DD):    ')
    endtime = input('what time did ' + subject_name + ' end the experiment? (HH:MM 24h format):    ')

    #open the combined file for the subject and load it into a pandas dataframe called combined_bm_data
    combined_bm_data = pd.read_csv(os.path.join(output_directory, subject_name, 'processed_biomarkers', 'biomarkers_combined.csv'))

    trunc_bm_data = parse_subject_data(combined_bm_data, startday, starttime, endday, endtime)   
    print('\nFinished truncated file for subject: ', subject_name)

    # find sections of step data where the subject takes 300-500 steps in a five minute window
    # save the time stamps and the step counts for these sections in a running list (so the start time stamp and the end time stamp and then the total number of steps for the 5 minute window)
    for i in range(len(trunc_bm_data)-4):
        testing = trunc_bm_data['step-counts']
        # print(testing)
        # print(testing.values[5])
        # print('\n')
        # print(trunc_bm_data['step-counts'][4])
        if int(trunc_bm_data['step-counts'].values[i]) > 0:
            step_sum = int(trunc_bm_data['step-counts'].values[i]+trunc_bm_data['step-counts'].values[i+1]+trunc_bm_data['step-counts'].values[i+2]+trunc_bm_data['step-counts'].values[i+3]+trunc_bm_data['step-counts'].values[i+4])
            if step_sum > 300 and step_sum < 500: 
                i = i+4
            print(step_sum)


# print('----------------------------------------')
# print('Finished processing all subjects for both days')

#TODO: deal with the raw data files, combine them and save them in the same output directory, use the tags to help with processing the data

## 