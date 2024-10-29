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


base_cyberduck_path = "C:/Users/vsun/Documents/Research/GaitGuide_Feedback_Study/Empatica_Data/main_subjects/participant_data_day/"
sorted_data_path = "C:/Users/vsun/Documents/Research/GaitGuide_Feedback_Study/Empatica_Data/main_subjects/sorted_sub_data/"

flag_sort = False # set to True if you want to sort the data into subject folders
flag_concat = True # set to True if you want the concatenated raw + biomarker data
flag_extra_data = False # set to True if you want to include extra data from avro files (temperature, accelerometer, gyroscope, systolic peaks)

# make a function that will read in the date in MM-DD-YYYY format and time in HH:MM for central european time and return the epoch time in microseconds
def convert_time(date, time, session_len = 5):
    date = date.split("/")
    time = time.split(":")
    year = int(date[2])
    month = int(date[0])
    day = int(date[1])
    hour = int(time[0])
    minute = int(time[1])
    end_minute = minute + session_len
    
    # Create a timestamp in CET
    cet_time = pd.Timestamp(year=year, month=month, day=day, hour=hour, minute=minute, tz='CET')
    cet_time_end = pd.Timestamp(year=year, month=month, day=day, hour=hour, minute=end_minute, tz='CET')
    
    # Convert to UTC
    utc_time = cet_time.tz_convert('UTC') 
    utc_time_end = cet_time_end.tz_convert('UTC')
    
    # Return the epoch time in microseconds and the end of the session time 
    return int(utc_time.value * 1e-9) , int(utc_time_end.value * 1e-9)

#make a function to read BVP and EDA data from the avro files given the start and end times of the retention session
def read_avro_data_timeframe(avro_file_path, subject_data, utc_start, utc_end):
    avro_file_path = idx_fol + "/1-1-" + str(df_empatica.iloc[idx]["Subject"].split('S')[-1]) + "_" + str(avro_file_start) + ".avro"
    reader = DataFileReader(open(avro_file_path, "rb"), DatumReader())
    schema = json.loads(reader.meta.get('avro.schema').decode('utf-8'))
    data = next(reader)
    # BVP
    bvp = data["rawData"]["bvp"]
    timestamp = [round(bvp["timestampStart"] + i * (1e6 / bvp["samplingFrequency"]))
                for i in range(len(bvp["values"]))]
    if "bvp" in subject_data:
        subject_data["bvp"]["timestamp"] += timestamp
        subject_data["bvp"]["bvp"] += bvp["values"]
    else:
        subject_data["bvp"] = {"timestamp": timestamp, "bvp": bvp["values"]}
    # EDA
    eda = data["rawData"]["eda"]
    timestamp = [round(eda["timestampStart"] + i * (1e6 / eda["samplingFrequency"]))
                for i in range(len(eda["values"]))]
    if "eda" in subject_data:
        subject_data["eda"]["timestamp"] += timestamp
        subject_data["eda"]["eda"] += eda["values"]
    else:
        subject_data["eda"] = {"timestamp": timestamp, "eda": eda["values"]}

    # round the timestamp so it matches the length of the retention session times (10 digits) and make it a new key in the dictionary
    subject_data["bvp"]["timestamp_rounded"] = [int(str(ts)[:-6]) for ts in subject_data["bvp"]["timestamp"]]
    subject_data["eda"]["timestamp_rounded"] = [int(str(ts)[:-6]) for ts in subject_data["eda"]["timestamp"]]

    # find the first instance that the utc_start is in the bvp data "timestamp_rounded" and the last instance that the utc_end is in the bvp data "timestamp_rounded"
    start_idx_bvp = subject_data["bvp"]["timestamp_rounded"].index(utc_start)
    end_idx_bvp = len(subject_data["bvp"]["timestamp_rounded"]) - 1 - subject_data["bvp"]["timestamp_rounded"][::-1].index(utc_end)

    start_idx_eda = subject_data["eda"]["timestamp_rounded"].index(utc_start)
    end_idx_eda = len(subject_data["eda"]["timestamp_rounded"]) - 1 - subject_data["eda"]["timestamp_rounded"][::-1].index(utc_end)

    # get the bvp and eda data during the retention session
    subject_data["bvp"]["bvp_ret"] = subject_data["bvp"]["bvp"][start_idx_bvp:end_idx_bvp]
    subject_data["eda"]["eda_ret"] = subject_data["eda"]["eda"][start_idx_eda:end_idx_eda]

    # save the mean and std of the bvp and eda data during the retention session
    subject_data["bvp"]["bvp_ret_mean"] = np.mean(subject_data["bvp"]["bvp_ret"])
    subject_data["bvp"]["bvp_ret_std"] = np.std(subject_data["bvp"]["bvp_ret"])
    subject_data["eda"]["eda_ret_mean"] = np.mean(subject_data["eda"]["eda_ret"])
    subject_data["eda"]["eda_ret_std"] = np.std(subject_data["eda"]["eda_ret"])
    
    return subject_data



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

    open_file = open(sorted_data_path + subject_folder + "/concatenated_data.csv")
    main_data = csv.reader(open_file)
    # make a dataframe from the csv file
    df = pd.DataFrame(main_data)
    df.columns = df.iloc[0]

df_empatica = pd.read_csv("C:/Users/vsun/Documents/Code/RTmocapFB/analysis/empatica/empatica_times.csv")
for idx in range(len(df_empatica)):
    day2_date = df_empatica.iloc[idx]["Day 2 Date"]
    ret_time = df_empatica.iloc[idx]["Day 2 Retention"]
    utc_ret, utc_ret_end = convert_time(day2_date, ret_time)

    # get the BVP and EDA data during retention from the sorted data
    idx_fol = sorted_data_path + df_empatica.iloc[idx]["Subject"].split('S')[-1] + "/raw_data" 
    subject_ret_data = {}
    sub_avro_files = os.listdir(idx_fol)
    sub_avro_files = [int(avro_file.split("-")[-1].split("_")[1].split(".")[0]) for avro_file in sub_avro_files]
    sub_avro_files.sort()

    for i in range(len(sub_avro_files) - 1):
        avro_file_start = sub_avro_files[i]
        avro_file_end = sub_avro_files[i + 1]
        
        if avro_file_start <= utc_ret and avro_file_end >= utc_ret_end:
            subject_ret_data = read_avro_data_timeframe(avro_file_start, subject_ret_data, utc_ret, utc_ret_end)

        elif avro_file_start <= utc_ret <= avro_file_end or avro_file_start <= utc_ret_end <= avro_file_end:
            #fix this if the retention time is in the middle of two avro files
            print("Retention time is across two avro files")
        else:
            continue




################ CONCATENATE RAW DATA AND BIOMARKERS ################
# raw data that we care about: temperature, EDA, steps, BVP, tags, systolic peaks
# biomarkers that we care about: sleep detection, wearing detection (?)

# load the data from "C:\Users\vasu1\Code\RTmocapFB\analysis\scheduler_notes_29Jul2024.xlsx" to get the subject IDs and the days they were in the study

# if flag_concat:
#     for subject_folder in os.listdir(sorted_data_path):
#         #create a dictionary to store the subject's data and then export it to a concatenated csv file
#         subject_data = {}
#         # cycle through all the raw data files and concatenate them into a single csv file
#         for avro_file in os.listdir(sorted_data_path + subject_folder + "/raw_data"):
            
#             avro_file_path = sorted_data_path + subject_folder + "/raw_data/" + avro_file
#             reader = DataFileReader(open(avro_file_path, "rb"), DatumReader())  #rb = read binary, binary mode to prevent corrupting the data file
#             schema = json.loads(reader.meta.get('avro.schema').decode('utf-8'))
#             data= next(reader)
            
        
#         #     # Eda - electrodermal activity
#         #     eda = data["rawData"]["eda"]
#         #     timestamp = [round(eda["timestampStart"] + i * (1e6 / eda["samplingFrequency"]))
#         #         for i in range(len(eda["values"]))]
#         #     if "eda" in subject_data:
#         #         subject_data["eda"]["timestamp"] += timestamp
#         #         subject_data["eda"]["eda"] += eda["values"]
#         #     else:
#         #         subject_data["eda"] = {"timestamp": timestamp, "eda": eda["values"]}
            
#         #     # BVP
#         #     bvp = data["rawData"]["bvp"]
#         #     timestamp = [round(bvp["timestampStart"] + i * (1e6 / bvp["samplingFrequency"]))
#         #         for i in range(len(bvp["values"]))]
#         #     if "bvp" in subject_data:
#         #         subject_data["bvp"]["timestamp"] += timestamp
#         #         subject_data["bvp"]["bvp"] += bvp["values"]
#         #     else:
#         #         subject_data["bvp"] = {"timestamp": timestamp, "bvp": bvp["values"]}

#         #     # Tags
#         #     tags = data["rawData"]["tags"]
#         #     if "tags" in subject_data:
#         #         subject_data["tags"]["tags"] += tags["tagsTimeMicros"]
#         #     else:
#         #         subject_data["tags"] = {"tags": tags["tagsTimeMicros"]}

#         #     # Steps
#         #     steps = data["rawData"]["steps"]
#         #     timestamp = [round(steps["timestampStart"] + i * (1e6 / steps["samplingFrequency"]))
#         #         for i in range(len(steps["values"]))]
#         #     if "steps" in subject_data:
#         #         subject_data["steps"]["timestamp"] += timestamp
#         #         subject_data["steps"]["steps"] += steps["values"]
#         #     else:
#         #         subject_data["steps"] = {"timestamp": timestamp, "steps": steps["values"]}
            
#         #     # if flag_extra_data:
#         #         # Systolic peaks
#         #         sps = data["rawData"]["systolicPeaks"]
#         #         if "systolic_peaks" in subject_data:
#         #             subject_data["systolic_peaks"]["peaks"] += sps["peaksTimeNanos"]
#         #         else:
#         #             subject_data["systolic_peaks"] = {"peaks": sps["peaksTimeNanos"]}

#         #         # Temperature
#         #         tmp = data["rawData"]["temperature"]
#         #         timestamp = [round(tmp["timestampStart"] + i * (1e6 / tmp["samplingFrequency"]))
#         #             for i in range(len(tmp["values"]))]
#         #         if "temperature" in subject_data:
#         #             subject_data["temperature"]["timestamp"] += timestamp
#         #             subject_data["temperature"]["temperature"] += tmp["values"]
#         #         else:
#         #             subject_data["temperature"] = {"timestamp": timestamp, "temperature": tmp["values"]}
                
#         #         # Accelerometer
#         #         acc = data["rawData"]["accelerometer"]
#         #         timestamp = [round(acc["timestampStart"] + i * (1e6 / acc["samplingFrequency"]))
#         #             for i in range(len(acc["x"]))]
#         #         # Convert ADC counts in g
#         #         delta_physical = acc["imuParams"]["physicalMax"] - acc["imuParams"]["physicalMin"]
#         #         delta_digital = acc["imuParams"]["digitalMax"] - acc["imuParams"]["digitalMin"]
#         #         x_g = [val * delta_physical / delta_digital for val in acc["x"]]
#         #         y_g = [val * delta_physical / delta_digital for val in acc["y"]]
#         #         z_g = [val * delta_physical / delta_digital for val in acc["z"]]
#         #         if "accelerometer" in subject_data:
#         #             subject_data["accelerometer"]["timestamp"] += timestamp
#         #             subject_data["accelerometer"]["x"] += x_g
#         #             subject_data["accelerometer"]["y"] += y_g
#         #             subject_data["accelerometer"]["z"] += z_g
#         #         else:
#         #             subject_data["accelerometer"] = {"timestamp": timestamp, "x": x_g, "y": y_g, "z": z_g}
#         #         # Gyroscope
#         #         gyro = data["rawData"]["gyroscope"]
#         #         timestamp = [round(gyro["timestampStart"] + i * (1e6 / gyro["samplingFrequency"]))
#         #             for i in range(len(gyro["x"]))]
#         #         # Convert ADC counts in dps (degree per second)
#         #         delta_physical = gyro["imuParams"]["physicalMax"] - gyro["imuParams"]["physicalMin"]
#         #         delta_digital = gyro["imuParams"]["digitalMax"] - gyro["imuParams"]["digitalMin"]
#         #         x_dps = [val * delta_physical / delta_digital for val in gyro["x"]]
#         #         y_dps = [val * delta_physical / delta_digital for val in gyro["y"]]
#         #         z_dps = [val * delta_physical / delta_digital for val in gyro["z"]]
#         #         if "gyroscope" in subject_data:
#         #             subject_data["gyroscope"]["timestamp"] += timestamp
#         #             subject_data["gyroscope"]["x"] += x_dps
#         #             subject_data["gyroscope"]["y"] += y_dps
#         #             subject_data["gyroscope"]["z"] += z_dps
#         #         else:
#         #             subject_data["gyroscope"] = {"timestamp": timestamp, "x": x_dps, "y": y_dps, "z": z_dps}
                
#         # # sort each of the subject's data by timestamp and then match the timestamps of eda, bvp, tags, and steps to export to a csv file with 5 columns (timestamp, eda, bvp, tags, steps)
#         # # sort the data by timestamp (microseconds)
#         # main_key = ["eda", "bvp", "steps"]
#         # for key in main_key:
#         #     df = pd.DataFrame(subject_data[key])
#         #     df = df.sort_values(by=["timestamp"])
#         #     subject_data[key] = df
        
#         # # change the timestamps to milliseconds for easier comparison
#         # for key in main_key:
#         #     earliest_timestamp = min(subject_data["eda"]["timestamp"][0], subject_data["bvp"]["timestamp"][0], subject_data["steps"]["timestamp"][0])
#         #     #add timestep_us to each key to make it easier to compare timestamps
#         #     subject_data[key]["timestep_us"] = subject_data[key]["timestamp"] - earliest_timestamp

#         # # create a df with eda, bvp, and steps where there is one common timestamp for all three data types
#         # timestamps = list(set(subject_data["eda"]["timestamp"]) & set(subject_data["bvp"]["timestamp"]) & set(subject_data["steps"]["timestamp"]))
#         # timestamps.sort()
        
#         # # Filter the data to keep only the common timestamps
#         # for key in main_key:
#         #     subject_data[key] = subject_data[key][subject_data[key]["timestamp"].isin(common_timestamps)]

#         # # the subject's new dataframe should have one timestamp, eda, bvp, and steps with everything synced
#         # new_df = pd.DataFrame()
#         # new_df["timestamp"] = timestamps
#         # new_df["eda"] = [subject_data["eda"][subject_data["eda"]["timestamp"] == ts]["eda"].values[0] for ts in timestamps]
#         # new_df["bvp"] = [subject_data["bvp"][subject_data["bvp"]["timestamp"] == ts]["bvp"].values[0] for ts in timestamps]
#         # new_df["steps"] = [subject_data["steps"][subject_data["steps"]["timestamp"] == ts]["steps"].values[0] for ts in timestamps]
#         # new_df["tags"] = [1 if ts in list(subject_data["tags"]["tags"]) else 0 for ts in timestamps]



#         # # # export the data to a csv file
#         # # with open(sorted_data_path + subject_folder + "/concatenated_data.csv", 'w', newline='') as f:
#         # #     writer = csv.writer(f)
#         # #     writer.writerow(["timestamp", "eda", "bvp", "tags", "steps"])
#         # #     for ts in timestamps:
#         # #         eda_val = subject_data["eda"][subject_data["eda"]["timestamp"] == ts]["eda"].values[0] if ts in list(subject_data["eda"]["timestamp"]) else np.nan
#         # #         bvp_val = subject_data["bvp"][subject_data["bvp"]["timestamp"] == ts]["bvp"].values[0] if ts in list(subject_data["bvp"]["timestamp"]) else np.nan
#         # #         tags_val = 1 if ts in list(subject_data["tags"]["tags"]) else 0
#         # #         steps_val = subject_data["steps"][subject_data["steps"]["timestamp"] == ts]["steps"].values[0] if ts in list(subject_data["steps"]["timestamp"]) else np.nan
#         # #         writer.writerow([ts, eda_val, bvp_val, tags_val, steps_val])
    
# ################ PROCESSING THE BVP: OUTSIDE LAB AND DURING STUDY ################
# # get the data from the concatenated csv file for each subject 

# for subject_folder in os.listdir(sorted_data_path):