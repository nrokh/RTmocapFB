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

def get_processed_biomarkers(input_directory, output_directory, subject_name, day):
    csv_data_path = os.path.join(input_directory, day, subject_name, 'digital_biomarkers','aggregated_per_minute')
    # moved files that have "_sleep-detection", "_eda", "_prv", "_step-counts" to the output directory + a new folder "processed_biomarkers"... create this folder if it doesnt exist
    biomarker_filepath = os.path.join(output_directory, subject_name,'processed_biomarkers')
    os.makedirs(biomarker_filepath, exist_ok=True)
    timestamp_ms = []
    timestamp_iso = []
    data_bm = []
    missing_data = []
    file_order = []

    for file in os.listdir(csv_data_path):
        if '_sleep-detection' in file or '_eda' in file or '_prv' in file or '_step-counts' in file:
            # read the first colm from each of the files and make sure they are exactly the same
            with open(os.path.join(csv_data_path, file), 'r') as f:
                reader = csv.reader(f)
                data = list(reader)
                file_timestamp = [data[i][0] for i in range(1, len(data))]
                file_timestamp_iso = [data[i][1] for i in range(1, len(data))]
                file_data = [data[i][3] for i in range(1, len(data))]
                file_missing_data = [data[i][4] for i in range(1, len(data))]

                file_order.append(file)
                timestamp_ms.append(file_timestamp)
                timestamp_iso.append(file_timestamp_iso)
                data_bm.append(file_data) #add label for each appended data
                missing_data.append(file_missing_data)


    return biomarker_filepath

    
    
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
        
        compiled_csv_data_path = get_processed_biomarkers(input_directory, output_directory, subject_name, day)
        
        print('----------------------------------------')
        print('Finished processing subject: ', subject_name, ' for day: ', day)
        print('----------------------------------------')
        




# # copy the file to the biomarker_filepath
            # os.rename(os.path.join(csv_data_path, file), os.path.join(biomarker_filepath, file))
            # print('Moved file: ', file, ' to ', biomarker_filepath)