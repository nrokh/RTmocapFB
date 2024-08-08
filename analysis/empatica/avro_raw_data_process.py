import avro.schema
from avro.datafile import DataFileReader
from avro.io import DatumReader
import json
import csv
import os
import shutil
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import filedialog
import pandas as pd
import random

################ SORT DATA ################ 
# cyberduck is annoying and sorts the data in a way that is not useful for us, so we need to sort it into subject folders to then concatenate the data into single files (especially the raw files because they are split into ~30 minutes of data/files)

base_cyberduck_path = "C:/Users/vsun/Documents/Research/GaitGuide_N_Collab/Empatica_Data/AmazonS3_files/main_subjects/participant_data_day/"
sort_data_path = "C:/Users/vsun/Documents/Research/GaitGuide_N_Collab/Empatica_Data/AmazonS3_files/main_subjects/sorted_sub_data/"

for day_folder in os.listdir(base_cyberduck_path):
    # open the day folder, then cycle through all the subject folders
    for subject_folder in os.listdir(base_cyberduck_path + day_folder):
        # get the subject ID from the first two characters of the folder name
        subject_id = subject_folder[:2]
        # create a new folder in the export path with the subject ID
        if not os.path.exists(sort_data_path + subject_id):
            os.makedirs(sort_data_path + subject_id)
        # cycle through all the sub folders in the subject folder and copy all the data to export/sorted path
        for sub_folder in os.listdir(base_cyberduck_path + day_folder + "/" + subject_folder):
            if sub_folder == "raw_data":
                if not os.path.exists(sort_data_path + subject_id + "/raw_data"):
                    os.makedirs(sort_data_path + subject_id + "/raw_data")
                for file in os.listdir(base_cyberduck_path + day_folder + "/" + subject_folder + "/" + sub_folder + "/v6"):
                    shutil.copyfile(base_cyberduck_path + day_folder + "/" + subject_folder + "/" + sub_folder + "/v6/" + file, sort_data_path + subject_id + "/raw_data/" + file)
            if sub_folder == "digital_biomarkers":
                if not os.path.exists(sort_data_path + subject_id + "/biomarkers"):
                    os.makedirs(sort_data_path + subject_id + "/biomarkers")
                for file in os.listdir(base_cyberduck_path + day_folder + "/" + subject_folder + "/" + sub_folder + "/aggregated_per_minute"):
                    shutil.copyfile(base_cyberduck_path + day_folder + "/" + subject_folder + "/" + sub_folder + "/aggregated_per_minute/" + file, sort_data_path + subject_id + "/biomarkers/" + file)

################ CONCATENATE RAW DATA AND BIOMARKERS ################
# raw data that we care about: temperature, EDA, steps, BVP, tags, systolic peaks
# biomarkers that we care about: sleep detection, wearing detection (?)

for subject_folder in os.listdir(sort_data_path):
    for avro_file in os.listdir(sort_data_path + subject_folder + "/raw_data"):
        avro_file_path = sort_data_path + subject_folder + "/raw_data/" + avro_file
        reader = DataFileReader(open(avro_file_path, "rb"), DatumReader())  #rb = read binary, binary mode to prevent corrupting the data file
        schema = json.loads(reader.meta.get('avro.schema').decode('utf-8'))
        data= next(reader)



