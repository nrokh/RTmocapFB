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
import heartpy as hp
import scipy


base_cyberduck_path = "C:/Users/vsun/Documents/Research/GaitGuide_Feedback_Study/Empatica_Data/main_subjects/participant_data_day/"
sorted_data_path = "C:/Users/vsun/Documents/Research/GaitGuide_Feedback_Study/Empatica_Data/main_subjects/sorted_sub_data/"
df_empatica = pd.read_csv("C:/Users/vsun/Documents/Code/RTmocapFB/analysis/empatica/empatica_times.csv")

flag_sort = False # set to True if you want to sort the data into subject folders
flag_concat = True # set to True if you want the concatenated raw + biomarker data
flag_extra_data = False # set to True if you want to include extra data from avro files (temperature, accelerometer, gyroscope, systolic peaks)
flag_raw_data = True

# function to read in the date in MM-DD-YYYY format and time in HH:MM for central european time and return the epoch time
def convert_time(date, time, session_len = 5):
    date = date.split("/")
    time = time.split(":")
    year = int(date[2])
    month = int(date[0])
    day = int(date[1])
    hour = int(time[0])
    minute = int(time[1])
    end_minute = minute + session_len
    
    if end_minute > 59:
        hour_end = hour + 1
        end_minute = end_minute % 60
    else:
        hour_end = hour
    
    # Create a timestamp in CET
    cet_time = pd.Timestamp(year=year, month=month, day=day, hour=hour, minute=minute, tz='CET')
    cet_time_end = pd.Timestamp(year=year, month=month, day=day, hour=hour_end, minute=end_minute, tz='CET')
    
    # Convert to UTC
    utc_time = cet_time.tz_convert('UTC') 
    utc_time_end = cet_time_end.tz_convert('UTC')
    
    # Return the epoch time in microseconds and the end of the session time 
    return int(utc_time.value * 1e-9) , int(utc_time_end.value * 1e-9)

# function to convert the timestamp in the bm files to epoch time
def convert_time_utc(timestamp_iso):
    # change timestamp_iso in YYYY-MM-DDT00:00:00Z to 10 digit epoch time and make it a new column in the dataframe
    date = timestamp_iso.split("T")[0].split("-")
    year = int(date[0])
    month = int(date[1])
    day = int(date[2])
    hour = int(timestamp_iso.split("T")[1].split(":")[0])
    minute = int(timestamp_iso.split("T")[1].split(":")[1])

    # Create a timestamp in UTC
    utc_time = pd.Timestamp(year=year, month=month, day=day, hour=hour, minute=minute, tz='UTC')

    return int(utc_time.value * 1e-9)

# function to read BVP and EDA data from the avro files given the start and end times of a session (raw data)
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

    # round the timestamp so it matches the length of the session times (10 digits) and make it a new key in the dictionary
    subject_data["bvp"]["timestamp_rounded"] = [int(str(ts)[:-6]) for ts in subject_data["bvp"]["timestamp"]]
    subject_data["eda"]["timestamp_rounded"] = [int(str(ts)[:-6]) for ts in subject_data["eda"]["timestamp"]]

    # find the first instance that the utc_start is in the bvp data "timestamp_rounded" and the last instance that the utc_end is in the bvp data "timestamp_rounded"
    start_idx_bvp = subject_data["bvp"]["timestamp_rounded"].index(utc_start)
    end_idx_bvp = len(subject_data["bvp"]["timestamp_rounded"]) - 1 - subject_data["bvp"]["timestamp_rounded"][::-1].index(utc_end)

    start_idx_eda = subject_data["eda"]["timestamp_rounded"].index(utc_start)
    end_idx_eda = len(subject_data["eda"]["timestamp_rounded"]) - 1 - subject_data["eda"]["timestamp_rounded"][::-1].index(utc_end)

    # get the bvp and eda data during the session
    subject_data["bvp"]["bvp_session"] = subject_data["bvp"]["bvp"][start_idx_bvp:end_idx_bvp]
    subject_data["eda"]["eda_session"] = subject_data["eda"]["eda"][start_idx_eda:end_idx_eda]

    # plot the bvp 
    plt.plot(subject_data["bvp"]["bvp_session"])
    plt.title("BVP during retention")
    plt.show()
    
    return subject_data

# similar to the function above but for the biomarker data 
def read_bm_data_timeframe(bm_file_path, subject_data, utc_start, utc_end):
    pulse_data = pd.read_csv(bm_file_path)
    pulse_data["timestamp_utc"] = pulse_data["timestamp_iso"].apply(convert_time_utc)

    start_idx = pulse_data[pulse_data["timestamp_utc"] == utc_start].index[0]
    end_idx = pulse_data[pulse_data["timestamp_utc"] == utc_end].index[0]

    subject_data["pulse_rate_session"] = pulse_data["pulse_rate_bpm"][start_idx:end_idx]
    subject_data["pulse_rate_session_mean"] = np.mean(subject_data["pulse_rate_session"])
    subject_data["pulse_rate_session_std"] = np.std(subject_data["pulse_rate_session"])

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

all_ret_data = {}
for idx in range(len(df_empatica)):
    day2_date = df_empatica.iloc[idx]["Day 2 Date"]
    ret_time = df_empatica.iloc[idx]["Day 2 Retention"]
    utc_ret, utc_ret_end = convert_time(day2_date, ret_time)

    if flag_raw_data:
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
                # calculate the fft of the BVP data
                
                ## sanity check for noicy signal - the empatica data looks filtered... show this to validate 
                # x = np.sin(2 * np.pi * 5 * np.arange(0, 5*60, 1/64))
                # noise = np.random.normal(0,1,5*60*64)
                # x += noise

                # bvp_fft = np.fft.rfft(x)
                # bvp_freqs = np.fft.rfftfreq(len(x), d=1/64.0) # the empatica sampling rate for the PPG sensor is 64 Hz
                # bvp_fft_abs = np.abs(bvp_fft)
                # plt.plot(bvp_freqs, bvp_fft_abs)
                # plt.title("FFT of BVP during retention")
                # plt.xlabel("Frequency (Hz)")
                # plt.ylabel("Magnitude")
                # plt.show()

                bvp_fft = np.fft.rfft(subject_ret_data["bvp"]["bvp_session"])
                bvp_freqs = np.fft.rfftfreq(len(subject_ret_data["bvp"]["bvp_session"]), d=1/64.0) # the empatica sampling rate for the PPG sensor is 64 Hz
                bvp_fft_abs = np.abs(bvp_fft)
                plt.plot(bvp_freqs, bvp_fft_abs)
                plt.title("FFT of BVP during retention")
                plt.xlabel("Frequency (Hz)")
                plt.ylabel("Magnitude")
                plt.show()
        
                # filter the BVP data
                filtered_bvp = hp.filter_signal(subject_ret_data["bvp"]["bvp_session"], [0.8, 3.5], sample_rate=64.0, order=3, filtertype='bandpass') # frequencies below 0.8Hz (48 BPM) and above 3.5 Hz (210 BPM)
                plt.figure(figsize=(12,6))
                plt.plot(filtered_bvp, label='Filtered BVP')
                plt.plot(subject_ret_data["bvp"]["bvp_session"], label='Original BVP')
                plt.plot(filtered_bvp)
                
                plt.title("Original and Filtered BVP during retention")
                plt.legend()

                plt.show()

                # 10/29 @ 6Pm - leaving off here... the peak detection is not working as expected, i need to look at this package more 
                wd, m = hp.process(subject_ret_data["bvp"]["bvp_session"], sample_rate=64.0, high_precision=True) # the empatica sampling rate for the PPG sensor is 64 Hz
                plt.figure(figsize=(12,6))
                hp.plotter(wd, m)
            
                print("plotting")

            elif avro_file_start <= utc_ret <= avro_file_end or avro_file_start <= utc_ret_end <= avro_file_end:
                #TODO: fix this if the retention time is in the middle of two avro files
                print("Retention time is across two avro files")
            else:
                continue
    else: 
        idx_fol = sorted_data_path + df_empatica.iloc[idx]["Subject"].split('S')[-1] + "/biomarkers/"
        subject_ret_data = {}
        day2_date = day2_date.split("/")
        day2_date = day2_date[2] + "-" + day2_date[0].zfill(2) + "-" + day2_date[1].zfill(2)
        pulse_file = idx_fol + "1-1-" + str(df_empatica.iloc[idx]["Subject"].split('S')[-1]) + "_" + day2_date + "_pulse-rate.csv"
        if os.path.exists(pulse_file):
            print("Reading biomarker data for subject " + df_empatica.iloc[idx]["Subject"])
            subject_ret_data = read_bm_data_timeframe(pulse_file, subject_ret_data, utc_ret, utc_ret_end)
            all_ret_data[df_empatica.iloc[idx]["Subject"]] = subject_ret_data




if flag_raw_data:
    print("will export the raw data here")
else:
    # Export the mean and std for the pulse rate data during retention to a csv file, where the rows are the subjects and the columns are the mean and std
    with open("C:/Users/vsun/Documents/Code/RTmocapFB/analysis/empatica/retention_data.csv", "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Subject", "Pulse Rate Mean", "Pulse Rate Std"])
        for subject in all_ret_data:
            writer.writerow([subject, all_ret_data[subject]["pulse_rate_session_mean"], all_ret_data[subject]["pulse_rate_session_std"]])





            
            

            



