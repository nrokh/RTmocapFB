from vicon_dssdk import ViconDataStream
import argparse
import sys
import time
import math
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import time
import keyboard #TODO: make sure this is installed
import tkinter as tk
from tkinter import filedialog
import os

############### VICON SETUP ########################
# create arg to host (Vicon Nexus)
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('host', nargs='?', help="Host name, in the format of server:port", default = "localhost:801")
args = parser.parse_args()

client = ViconDataStream.Client()

    ############# FILE SAVING #####################

def generate_csv_filename(directory, subject_name, parameter):
            
    csv_file = os.path.join(directory, subject_name[0] + '_baseline_' + parameter + '.csv')
    counter = 0

    while os.path.exists(csv_file):
        counter += 1
        csv_file = os.path.join(directory, subject_name[0] + '_baseline_' + parameter + str(counter) + '.csv')
    print('      Data will be saved to file: ', csv_file)
    return csv_file

try:
    # Connect to Nexus (Nexus needs to be on and either Live or replaying previously collected data)
    client.Connect( args.host)
    print( '        Connected to Nexus')

    # Enable the data type
    client.EnableMarkerData()

    # Report whether data type was enabled successfully:
    print ( '        Markers enabled? ', client.IsMarkerDataEnabled() )

    # start getting frames 
    HasFrame = False
    timeout = 50
    while not HasFrame:
        print( '.' )
        try:
            if client.GetFrame():
                HasFrame = True
            timeout=timeout-1
            if timeout < 0:
                print('Failed to get frame')
                sys.exit()
        except ViconDataStream.DataStreamException as e:
            client.GetFrame()

    # Set streaming mode to Server Push (lowest latency, but buffers could overfill, resulting in dropped frames)
    client.SetStreamMode( ViconDataStream.Client.StreamMode.EServerPush)
    print( '        Current frame rate: ', client.GetFrameRate() )

    # Get the subject's name
    subjectNames = client.GetSubjectNames()
    print('        Subject name: ', subjectNames[0])

    # Get the desired directory to save the data
    root = tk.Tk()
    root.withdraw() # we don't want a full GUI, so keep the root window from appearing
    directory = filedialog.askdirectory()

    # create a list to store FPA and marker values
    FPA_store = []
    CAL_store = []
    PSI_store = []
    DIFF_store = [0,0,0]
    DIFFDV_store = [0,0,0] # TODO: check if this is how you want to initialize
    gaitEvent_store = []
    FPAstep_store = []
    baselineFPA = []
    meanFPAstep_store = []

    # create flag to check for systemic occlusions
    occl_flag_foot = 0 
    occl_flag_hip = 0

    # trial length based on step count
    step_count = 0 
    cadence = 80 # steps per minute
    trial_time = 2 #  minutes

    ################# STEP DETECTION ###################
    print("Press space when ready to measure baseline FPA: ")
    keyboard.wait('space')  
    
    local_max_detected = False

    start_time = time.time() #TODO: figure out why the step count is not working
    while time.time() - start_time < trial_time*60:  # Run for 2 minutes
    # while step_count < trial_time*cadence: 
        # print(step_count)
        subjectName = subjectNames[0]  # select the main subject
        client.GetFrame()  # get the frame
        marker_names = client.GetMarkerNames(subjectName)
        marker_names = [x[0] for x in marker_names]

        ################# CALCULATE FPA ####################
        
        #check if all the main markers are streaming properly 
        if 'RTOE' not in marker_names or 'RHEE' not in marker_names or 'RPSI' not in marker_names:
            print("Missing markers or marker name, please check the VICON software")
            sys.exit()

        RTOE_translation = client.GetMarkerGlobalTranslation(subjectName, 'RTOE')[0]
        RHEE_translation = client.GetMarkerGlobalTranslation(subjectName, 'RHEE')[0]
        CAL = RHEE_translation[0]
        PSI = client.GetMarkerGlobalTranslation(subjectName, 'RPSI')[0][0]

        # add error exception for occluded markers
        if RTOE_translation == [0, 0] or RHEE_translation == [0, 0]:
            # Flag this data and check if it's consecutively too frequent
            occl_flag_foot += 1
            if occl_flag_foot > 25:
                print("Too many occlusions for RHEE/RTOE, check the markers")
            # save FPA as a NaN value so we can discard later
            FPA = np.nan
        else:
            # Calculate FPA
            occl_flag_foot = 0
            footVec = (RTOE_translation[0] - RHEE_translation[0], RTOE_translation[1] - RHEE_translation[1])
            FPA = -math.degrees(math.atan(footVec[1] / footVec[0]))  # TODO: check signs for right foot
            CAL_store.append(CAL)
            PSI_store.append(PSI)

        # get AP CAL and PSI markers 
        if PSI == 0:
            occl_flag_hip += 1
            if occl_flag_hip > 25:
                print("Too many occlusions for PSI, check marker")

        # take derivative of difference between heel and hip:
        DIFF = CAL - PSI
        DIFF_store.append(DIFF)
        DIFFDV = DIFF_store[-1] - DIFF_store[-2]
        DIFFDV_store.append(DIFFDV)

        # search for local max
        if DIFFDV_store[-1] >= 0 and DIFFDV_store[-2] <= 0 and DIFFDV_store[-3] <= 0 and DIFFDV_store[-4] <= 0:
            print("local max")
            FPAstep_store = []
            local_max_detected = True
            gaitEvent_store.append((time.time(), 1.0))

        FPAstep_store.append(FPA)

        # search for min:
        if local_max_detected and DIFFDV_store[-1] <= 0 and DIFFDV_store[-2] >= 0 and DIFFDV_store[-3] >= 0 and DIFFDV_store[-4] >= 0:
            print("local min")
            meanFPAstep = np.nanmean(FPAstep_store)
            meanFPAstep_store.append((time.time_ns(), meanFPAstep)) 

            baselineFPA.append(meanFPAstep)

            print("mean FPA for step = " + str(meanFPAstep))
            gaitEvent_store.append((time.time_ns(), 2.0))

            local_max_detected = False

            step_count += 2
        # save FPA value to the list
        FPA_store.append((time.time_ns(), FPA))

    # save calculated FPA
    df_FPA = pd.DataFrame(FPA_store)
    csv_file_FPA = generate_csv_filename(directory, subjectNames, 'FPA')
    df_FPA.to_csv(csv_file_FPA)

    # save the mean FPA for each step w/ timestamps
    df_mFPA = pd.DataFrame(meanFPAstep_store)
    csv_file_mFPA = generate_csv_filename(directory, subjectNames, 'meanFPA')
    df_mFPA.to_csv(csv_file_mFPA)

    # save gait events
    df_GE = pd.DataFrame(gaitEvent_store)
    csv_file_GE = generate_csv_filename(directory, subjectNames, 'gaitEvents')
    df_GE.to_csv(csv_file_GE)

    # print avg of baseline FPA
    print("-----------------------------------------------------------------")
    print("Baseline FPA: " + str(round(np.nanmean(baselineFPA),2)))
    print("Participant will walk at " + str(round((np.nanmean(baselineFPA) - 10.0),2)) + " degrees for the experiment")
    print("-----------------------------------------------------------------")

    plt.plot(df_FPA.iloc[:,0], df_FPA.iloc[:,1])
    plt.xlabel('Time [ns]')
    plt.ylabel('FPA [deg]')
    plt.scatter(df_mFPA.iloc[:,0], df_mFPA.iloc[:,1], color='red', marker='o')
    plt.title('FPA')
    plt.show()    

except ViconDataStream.DataStreamException as e:
    print( 'Handled data stream error: ', e )
except KeyboardInterrupt:
    print( 'Keyboard interrupt detected, trial ended early...' )
    # save calculated FPA
    df_FPA = pd.DataFrame(FPA_store)
    csv_file_FPA = generate_csv_filename(directory, subjectNames, 'FPA_Interrupted')
    df_FPA.to_csv(csv_file_FPA)

    # save the mean FPA for each step w/ timestamps
    df_mFPA = pd.DataFrame(meanFPAstep_store)
    csv_file_mFPA = generate_csv_filename(directory, subjectNames, 'meanFPA_Interrupted')
    df_mFPA.to_csv(csv_file_mFPA)

    # save gait events
    df_GE = pd.DataFrame(gaitEvent_store)
    csv_file_GE = generate_csv_filename(directory, subjectNames, 'gaitEvents_Interrupted')
    df_GE.to_csv(csv_file_GE)
    
    plt.plot(df_FPA.iloc[:,0], df_FPA.iloc[:,1])
    plt.xlabel('Time [ns]')
    plt.ylabel('FPA [deg]')
    plt.scatter(df_mFPA.iloc[:,0], df_mFPA.iloc[:,1], color='red', marker='o')
    plt.title('FPA')
    plt.show() 

    print('Data saved!')





