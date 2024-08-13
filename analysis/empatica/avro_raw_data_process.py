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


base_cyberduck_path = "C:/Users/vsun/Documents/Research/GaitGuide_N_Collab/Empatica_Data/AmazonS3_files/main_subjects/participant_data_day/"
sorted_data_path = "C:/Users/vsun/Documents/Research/GaitGuide_N_Collab/Empatica_Data/AmazonS3_files/main_subjects/sorted_sub_data/"

flag_sort = False # set to True if you want to sort the data into subject folders
flag_extra_data = False # set to True if you want to include extra data from avro files (temperature, accelerometer, gyroscope, systolic peaks)

if flag_sort:
    ################ SORT DATA ################ 
    # cyberduck is annoying and sorts the data in a way that is not useful for us, so we need to sort it into subject folders 
    # to then concatenate the data into single files (especially the raw files because they are split into ~30 minutes of data/files)
    for day_folder in os.listdir(base_cyberduck_path):
        # open the day folder, then cycle through all the subject folders
        for subject_folder in os.listdir(base_cyberduck_path + day_folder):
            # get the subject ID from the first two characters of the folder name
            subject_id = subject_folder[:2]
            # create a new folder in the export path with the subject ID
            if not os.path.exists(sorted_data_path + subject_id):
                os.makedirs(sorted_data_path + subject_id)
            # cycle through all the sub folders in the subject folder and copy all the data to export/sorted path
            for sub_folder in os.listdir(base_cyberduck_path + day_folder + "/" + subject_folder):
                if sub_folder == "raw_data":
                    if not os.path.exists(sorted_data_path + subject_id + "/raw_data"):
                        os.makedirs(sorted_data_path + subject_id + "/raw_data")
                    for file in os.listdir(base_cyberduck_path + day_folder + "/" + subject_folder + "/" + sub_folder + "/v6"):
                        shutil.copyfile(base_cyberduck_path + day_folder + "/" + subject_folder + "/" + sub_folder + "/v6/" + file, sorted_data_path + subject_id + "/raw_data/" + file)
                if sub_folder == "digital_biomarkers":
                    if not os.path.exists(sorted_data_path + subject_id + "/biomarkers"):
                        os.makedirs(sorted_data_path + subject_id + "/biomarkers")
                    for file in os.listdir(base_cyberduck_path + day_folder + "/" + subject_folder + "/" + sub_folder + "/aggregated_per_minute"):
                        shutil.copyfile(base_cyberduck_path + day_folder + "/" + subject_folder + "/" + sub_folder + "/aggregated_per_minute/" + file, sorted_data_path + subject_id + "/biomarkers/" + file)

################ CONCATENATE RAW DATA AND BIOMARKERS ################
# raw data that we care about: temperature, EDA, steps, BVP, tags, systolic peaks
# biomarkers that we care about: sleep detection, wearing detection (?)

for subject_folder in os.listdir(sorted_data_path):
    #create a dictionary to store the subject's data and then export it to a concatenated csv file
    subject_data = {}
    # cycle through all the raw data files and concatenate them into a single csv file
    for avro_file in os.listdir(sorted_data_path + subject_folder + "/raw_data"):
        avro_file_path = sorted_data_path + subject_folder + "/raw_data/" + avro_file
        reader = DataFileReader(open(avro_file_path, "rb"), DatumReader())  #rb = read binary, binary mode to prevent corrupting the data file
        schema = json.loads(reader.meta.get('avro.schema').decode('utf-8'))
        data= next(reader)
        
        # Eda - electrodermal activity
        eda = data["rawData"]["eda"]
        timestamp = [round(eda["timestampStart"] + i * (1e6 / eda["samplingFrequency"]))
            for i in range(len(eda["values"]))]
        if "eda" in subject_data:
            subject_data["eda"]["timestamp"] += timestamp
            subject_data["eda"]["eda"] += eda["values"]
        else:
            subject_data["eda"] = {"timestamp": timestamp, "eda": eda["values"]}
        
        # BVP
        bvp = data["rawData"]["bvp"]
        timestamp = [round(bvp["timestampStart"] + i * (1e6 / bvp["samplingFrequency"]))
            for i in range(len(bvp["values"]))]
        if "bvp" in subject_data:
            subject_data["bvp"]["timestamp"] += timestamp
            subject_data["bvp"]["bvp"] += bvp["values"]
        else:
            subject_data["bvp"] = {"timestamp": timestamp, "bvp": bvp["values"]}

        # Tags
        tags = data["rawData"]["tags"]
        if "tags" in subject_data:
            subject_data["tags"]["tags"] += tags["tagsTimeMicros"]
        else:
            subject_data["tags"] = {"tags": tags["tagsTimeMicros"]}

        # Steps
        steps = data["rawData"]["steps"]
        timestamp = [round(steps["timestampStart"] + i * (1e6 / steps["samplingFrequency"]))
            for i in range(len(steps["values"]))]
        if "steps" in subject_data:
            subject_data["steps"]["timestamp"] += timestamp
            subject_data["steps"]["steps"] += steps["values"]
        else:
            subject_data["steps"] = {"timestamp": timestamp, "steps": steps["values"]}
        
        if flag_extra_data:
            # Systolic peaks
            sps = data["rawData"]["systolicPeaks"]
            if "systolic_peaks" in subject_data:
                subject_data["systolic_peaks"]["peaks"] += sps["peaksTimeNanos"]
            else:
                subject_data["systolic_peaks"] = {"peaks": sps["peaksTimeNanos"]}

            # Temperature
            tmp = data["rawData"]["temperature"]
            timestamp = [round(tmp["timestampStart"] + i * (1e6 / tmp["samplingFrequency"]))
                for i in range(len(tmp["values"]))]
            if "temperature" in subject_data:
                subject_data["temperature"]["timestamp"] += timestamp
                subject_data["temperature"]["temperature"] += tmp["values"]
            else:
                subject_data["temperature"] = {"timestamp": timestamp, "temperature": tmp["values"]}
            
            # Accelerometer
            acc = data["rawData"]["accelerometer"]
            timestamp = [round(acc["timestampStart"] + i * (1e6 / acc["samplingFrequency"]))
                for i in range(len(acc["x"]))]
            # Convert ADC counts in g
            delta_physical = acc["imuParams"]["physicalMax"] - acc["imuParams"]["physicalMin"]
            delta_digital = acc["imuParams"]["digitalMax"] - acc["imuParams"]["digitalMin"]
            x_g = [val * delta_physical / delta_digital for val in acc["x"]]
            y_g = [val * delta_physical / delta_digital for val in acc["y"]]
            z_g = [val * delta_physical / delta_digital for val in acc["z"]]
            if "accelerometer" in subject_data:
                subject_data["accelerometer"]["timestamp"] += timestamp
                subject_data["accelerometer"]["x"] += x_g
                subject_data["accelerometer"]["y"] += y_g
                subject_data["accelerometer"]["z"] += z_g
            else:
                subject_data["accelerometer"] = {"timestamp": timestamp, "x": x_g, "y": y_g, "z": z_g}
            # Gyroscope
            gyro = data["rawData"]["gyroscope"]
            timestamp = [round(gyro["timestampStart"] + i * (1e6 / gyro["samplingFrequency"]))
                for i in range(len(gyro["x"]))]
            # Convert ADC counts in dps (degree per second)
            delta_physical = gyro["imuParams"]["physicalMax"] - gyro["imuParams"]["physicalMin"]
            delta_digital = gyro["imuParams"]["digitalMax"] - gyro["imuParams"]["digitalMin"]
            x_dps = [val * delta_physical / delta_digital for val in gyro["x"]]
            y_dps = [val * delta_physical / delta_digital for val in gyro["y"]]
            z_dps = [val * delta_physical / delta_digital for val in gyro["z"]]
            if "gyroscope" in subject_data:
                subject_data["gyroscope"]["timestamp"] += timestamp
                subject_data["gyroscope"]["x"] += x_dps
                subject_data["gyroscope"]["y"] += y_dps
                subject_data["gyroscope"]["z"] += z_dps
            else:
                subject_data["gyroscope"] = {"timestamp": timestamp, "x": x_dps, "y": y_dps, "z": z_dps}
            
            



