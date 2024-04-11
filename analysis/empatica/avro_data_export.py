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

def get_biomarkers(input_directory, output_directory, subject_name, day):
    csv_data_path = os.path.join(input_directory, day, subject_name, 'digital_biomarkers','aggregated_per_minute')
    # moved files that have "_sleep-detection", "_eda", "_prv", "_step-counts" to the output directory + a new folder "processed_biomarkers"... create this folder if it doesnt exist
    biomarker_filepath = os.path.join(output_directory, subject_name,'processed_biomarkers')
    os.makedirs(biomarker_filepath, exist_ok=True)
    for file in os.listdir(csv_data_path):
        if '_sleep-detection' in file or '_eda' in file or '_prv' in file or '_step-counts' in file:
            with open(os.path.join(csv_data_path, file), 'r') as f:
                print('Processing file: ', file)    
                reader = csv.reader(f)
                data = list(reader)
            if os.path.exists(os.path.join(biomarker_filepath, file)):
                print('File exists, appending data...')
                with open(os.path.join(biomarker_filepath, file), 'a') as f:
                    writer = csv.writer(f)
                    writer.writerows(data)
            else:
                print('File exists, appending data...')
                with open(os.path.join(biomarker_filepath, file), 'w') as f:
                    writer = csv.writer(f)
                    writer.writerows(data)
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
        
        compiled_csv_data_path = get_biomarkers(input_directory, output_directory, subject_name, day)
        
        print('----------------------------------------')
        print('Finished processing subject: ', subject_name, ' for day: ', day)
        print('----------------------------------------')
        

