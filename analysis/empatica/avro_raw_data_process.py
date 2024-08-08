import avro.schema
from avro.datafile import DataFileReader
from avro.io import DatumReader
import json
import csv
import os
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import filedialog
import pandas as pd
import random

base_import_path = "C:/Users/vsun/Documents/Research/GaitGuide_N_Collab/Empatica_Data/Avro_files/main_subjects/participant_data_day/"
base_export_path = "C:/Users/vsun/Documents/Research/GaitGuide_N_Collab/Empatica_Data/Avro_files/main_subjects/sorted_sub_data/"

# cycle through all the day folders in the import path 
# within each day folder, look at the first two characters of the folder name to get the subject ID, and create a new folder in the export path with the subject ID
# transfer all the data from the day folder to the subject folder
# repeat for all day folders

for day_folder in os.listdir(base_import_path):
    # open the day folder, then cycle through all the subject folders
    for subject_folder in os.listdir(base_import_path + day_folder):
        # get the subject ID from the first two characters of the folder name
        subject_id = subject_folder[:2]
        # create a new folder in the export path with the subject ID
        if not os.path.exists(base_export_path + subject_id):
            os.makedirs(base_export_path + subject_id)
        # transfer all the data from the day folder to the subject folder
        for data_file in os.listdir(base_import_path + day_folder + "/" + subject_folder):
            # copy the file to the new folder
            file_path = base_import_path + day_folder + "/" + subject_folder + "/" + data_file
            new_file_path = base_export_path + subject_id + "/" + data_file
            os.rename(file_path, new_file_path)
            print("Moved " + data_file + " to " + new_file_path)
        # remove the empty day folder
        os.rmdir(base_import_path + day_folder + "/" + subject_folder)
        print("Removed " + base_import_path + day_folder + "/" + subject_folder)

