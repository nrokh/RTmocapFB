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
        if '_sleep-detection' in file or '_eda' in file or '_prv' in file or '_step-counts' in file or '_pulse-rate' in file:
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


    
    
# ## Copy subject name from Avro files
# # subject_name = '0-3YK3K152DD'
# # subject_name = '1-3YK3K152DD'
# # subject_name = '2-3YK3K152XT'

## Define the location of the Avro file and output folder.
in_root = tk.Tk()
in_root.withdraw() 
print('Select the input directory....')
input_directory = filedialog.askdirectory()

out_root = tk.Tk()
out_root.withdraw() 
print('Select the output directory....')
output_directory = filedialog.askdirectory()

## Get data for each day
for day in ['day_1', 'day_2']:
    check_this = os.listdir(os.path.join(input_directory, day))
    for subject_name in os.listdir(os.path.join(input_directory, day)):
        
        combine_processed_biomarkers(input_directory, output_directory, subject_name, day)
        
        print('----------------------------------------')
        print('Finished processing subject: ', subject_name, ' for day: ', day)
        print('----------------------------------------')
        




# # copy the file to the biomarker_filepath
            # os.rename(os.path.join(csv_data_path, file), os.path.join(biomarker_filepath, file))
            # print('Moved file: ', file, ' to ', biomarker_filepath)