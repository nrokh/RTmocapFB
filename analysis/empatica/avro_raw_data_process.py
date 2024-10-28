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


base_cyberduck_path = "C:/Users/vasu1/OneDrive - UCB-O365/Documents/7_MPI_Postdoc/Empatica/main_subjects/participant_data_day/"
sorted_data_path = "C:/Users/vasu1/OneDrive - UCB-O365/Documents/7_MPI_Postdoc/Empatica/main_subjects/sorted_sub_data/"

flag_sort = False # set to True if you want to sort the data into subject folders
flag_concat = True # set to True if you want the concatenated raw + biomarker data
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

# load the data from "C:\Users\vasu1\Code\RTmocapFB\analysis\scheduler_notes_29Jul2024.xlsx" to get the subject IDs and the days they were in the study



if flag_concat:
    for subject_folder in os.listdir(sorted_data_path):
        #create a dictionary to store the subject's data and then export it to a concatenated csv file
        subject_data = {}
        # cycle through all the raw data files and concatenate them into a single csv file
        for avro_file in os.listdir(sorted_data_path + subject_folder + "/raw_data"):
            
            avro_file_path = sorted_data_path + subject_folder + "/raw_data/" + avro_file
            reader = DataFileReader(open(avro_file_path, "rb"), DatumReader())  #rb = read binary, binary mode to prevent corrupting the data file
            schema = json.loads(reader.meta.get('avro.schema').decode('utf-8'))
            data= next(reader)
            
        
        #     # Eda - electrodermal activity
        #     eda = data["rawData"]["eda"]
        #     timestamp = [round(eda["timestampStart"] + i * (1e6 / eda["samplingFrequency"]))
        #         for i in range(len(eda["values"]))]
        #     if "eda" in subject_data:
        #         subject_data["eda"]["timestamp"] += timestamp
        #         subject_data["eda"]["eda"] += eda["values"]
        #     else:
        #         subject_data["eda"] = {"timestamp": timestamp, "eda": eda["values"]}
            
        #     # BVP
        #     bvp = data["rawData"]["bvp"]
        #     timestamp = [round(bvp["timestampStart"] + i * (1e6 / bvp["samplingFrequency"]))
        #         for i in range(len(bvp["values"]))]
        #     if "bvp" in subject_data:
        #         subject_data["bvp"]["timestamp"] += timestamp
        #         subject_data["bvp"]["bvp"] += bvp["values"]
        #     else:
        #         subject_data["bvp"] = {"timestamp": timestamp, "bvp": bvp["values"]}

        #     # Tags
        #     tags = data["rawData"]["tags"]
        #     if "tags" in subject_data:
        #         subject_data["tags"]["tags"] += tags["tagsTimeMicros"]
        #     else:
        #         subject_data["tags"] = {"tags": tags["tagsTimeMicros"]}

        #     # Steps
        #     steps = data["rawData"]["steps"]
        #     timestamp = [round(steps["timestampStart"] + i * (1e6 / steps["samplingFrequency"]))
        #         for i in range(len(steps["values"]))]
        #     if "steps" in subject_data:
        #         subject_data["steps"]["timestamp"] += timestamp
        #         subject_data["steps"]["steps"] += steps["values"]
        #     else:
        #         subject_data["steps"] = {"timestamp": timestamp, "steps": steps["values"]}
            
        #     # if flag_extra_data:
        #         # Systolic peaks
        #         sps = data["rawData"]["systolicPeaks"]
        #         if "systolic_peaks" in subject_data:
        #             subject_data["systolic_peaks"]["peaks"] += sps["peaksTimeNanos"]
        #         else:
        #             subject_data["systolic_peaks"] = {"peaks": sps["peaksTimeNanos"]}

        #         # Temperature
        #         tmp = data["rawData"]["temperature"]
        #         timestamp = [round(tmp["timestampStart"] + i * (1e6 / tmp["samplingFrequency"]))
        #             for i in range(len(tmp["values"]))]
        #         if "temperature" in subject_data:
        #             subject_data["temperature"]["timestamp"] += timestamp
        #             subject_data["temperature"]["temperature"] += tmp["values"]
        #         else:
        #             subject_data["temperature"] = {"timestamp": timestamp, "temperature": tmp["values"]}
                
        #         # Accelerometer
        #         acc = data["rawData"]["accelerometer"]
        #         timestamp = [round(acc["timestampStart"] + i * (1e6 / acc["samplingFrequency"]))
        #             for i in range(len(acc["x"]))]
        #         # Convert ADC counts in g
        #         delta_physical = acc["imuParams"]["physicalMax"] - acc["imuParams"]["physicalMin"]
        #         delta_digital = acc["imuParams"]["digitalMax"] - acc["imuParams"]["digitalMin"]
        #         x_g = [val * delta_physical / delta_digital for val in acc["x"]]
        #         y_g = [val * delta_physical / delta_digital for val in acc["y"]]
        #         z_g = [val * delta_physical / delta_digital for val in acc["z"]]
        #         if "accelerometer" in subject_data:
        #             subject_data["accelerometer"]["timestamp"] += timestamp
        #             subject_data["accelerometer"]["x"] += x_g
        #             subject_data["accelerometer"]["y"] += y_g
        #             subject_data["accelerometer"]["z"] += z_g
        #         else:
        #             subject_data["accelerometer"] = {"timestamp": timestamp, "x": x_g, "y": y_g, "z": z_g}
        #         # Gyroscope
        #         gyro = data["rawData"]["gyroscope"]
        #         timestamp = [round(gyro["timestampStart"] + i * (1e6 / gyro["samplingFrequency"]))
        #             for i in range(len(gyro["x"]))]
        #         # Convert ADC counts in dps (degree per second)
        #         delta_physical = gyro["imuParams"]["physicalMax"] - gyro["imuParams"]["physicalMin"]
        #         delta_digital = gyro["imuParams"]["digitalMax"] - gyro["imuParams"]["digitalMin"]
        #         x_dps = [val * delta_physical / delta_digital for val in gyro["x"]]
        #         y_dps = [val * delta_physical / delta_digital for val in gyro["y"]]
        #         z_dps = [val * delta_physical / delta_digital for val in gyro["z"]]
        #         if "gyroscope" in subject_data:
        #             subject_data["gyroscope"]["timestamp"] += timestamp
        #             subject_data["gyroscope"]["x"] += x_dps
        #             subject_data["gyroscope"]["y"] += y_dps
        #             subject_data["gyroscope"]["z"] += z_dps
        #         else:
        #             subject_data["gyroscope"] = {"timestamp": timestamp, "x": x_dps, "y": y_dps, "z": z_dps}
                
        # # sort each of the subject's data by timestamp and then match the timestamps of eda, bvp, tags, and steps to export to a csv file with 5 columns (timestamp, eda, bvp, tags, steps)
        # # sort the data by timestamp (microseconds)
        # main_key = ["eda", "bvp", "steps"]
        # for key in main_key:
        #     df = pd.DataFrame(subject_data[key])
        #     df = df.sort_values(by=["timestamp"])
        #     subject_data[key] = df
        
        # # change the timestamps to milliseconds for easier comparison
        # for key in main_key:
        #     earliest_timestamp = min(subject_data["eda"]["timestamp"][0], subject_data["bvp"]["timestamp"][0], subject_data["steps"]["timestamp"][0])
        #     #add timestep_us to each key to make it easier to compare timestamps
        #     subject_data[key]["timestep_us"] = subject_data[key]["timestamp"] - earliest_timestamp

        # # create a df with eda, bvp, and steps where there is one common timestamp for all three data types
        # timestamps = list(set(subject_data["eda"]["timestamp"]) & set(subject_data["bvp"]["timestamp"]) & set(subject_data["steps"]["timestamp"]))
        # timestamps.sort()
        
        # # Filter the data to keep only the common timestamps
        # for key in main_key:
        #     subject_data[key] = subject_data[key][subject_data[key]["timestamp"].isin(common_timestamps)]

        # # the subject's new dataframe should have one timestamp, eda, bvp, and steps with everything synced
        # new_df = pd.DataFrame()
        # new_df["timestamp"] = timestamps
        # new_df["eda"] = [subject_data["eda"][subject_data["eda"]["timestamp"] == ts]["eda"].values[0] for ts in timestamps]
        # new_df["bvp"] = [subject_data["bvp"][subject_data["bvp"]["timestamp"] == ts]["bvp"].values[0] for ts in timestamps]
        # new_df["steps"] = [subject_data["steps"][subject_data["steps"]["timestamp"] == ts]["steps"].values[0] for ts in timestamps]
        # new_df["tags"] = [1 if ts in list(subject_data["tags"]["tags"]) else 0 for ts in timestamps]



        # # # export the data to a csv file
        # # with open(sorted_data_path + subject_folder + "/concatenated_data.csv", 'w', newline='') as f:
        # #     writer = csv.writer(f)
        # #     writer.writerow(["timestamp", "eda", "bvp", "tags", "steps"])
        # #     for ts in timestamps:
        # #         eda_val = subject_data["eda"][subject_data["eda"]["timestamp"] == ts]["eda"].values[0] if ts in list(subject_data["eda"]["timestamp"]) else np.nan
        # #         bvp_val = subject_data["bvp"][subject_data["bvp"]["timestamp"] == ts]["bvp"].values[0] if ts in list(subject_data["bvp"]["timestamp"]) else np.nan
        # #         tags_val = 1 if ts in list(subject_data["tags"]["tags"]) else 0
        # #         steps_val = subject_data["steps"][subject_data["steps"]["timestamp"] == ts]["steps"].values[0] if ts in list(subject_data["steps"]["timestamp"]) else np.nan
        # #         writer.writerow([ts, eda_val, bvp_val, tags_val, steps_val])
    
################ PROCESSING THE BVP: OUTSIDE LAB AND DURING STUDY ################
# get the data from the concatenated csv file for each subject 

for subject_folder in os.listdir(sorted_data_path):
    open_file = open(sorted_data_path + subject_folder + "/concatenated_data.csv")
    main_data = csv.reader(open_file)
    # make a dataframe from the csv file
    df = pd.DataFrame(main_data)
    df.columns = df.iloc[0]


