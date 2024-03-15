from vicon_dssdk import ViconDataStream
import argparse
import sys
import time
import math
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
    subjectName = subjectNames[0]  # select the main subject

    # Get the desired directory to save the data
    root = tk.Tk()
    root.withdraw() # we don't want a full GUI, so keep the root window from appearing
    directory = filedialog.askdirectory()
    csv_file = os.path.join(directory, subjectNames[0] + '_Baseline_FPA.csv')
    counter = 0
    # Check if the file already exists
    while os.path.exists(csv_file):
        counter += 1
        csv_file = os.path.join(directory, subjectNames[0] + '_Baseline_FPA' + str(counter) + '.csv')
    print('        Data will be saved to: ', csv_file)
    print("        NOTE TO USER: Make sure the proprioception testing device is in the correct spot (aligned with the treadmil)")


    ################# Proprioception Test ###################
    FPA_store = []
    err_prop = []
    err_prop_in = []
    err_prop_out = []
    deg_test = [-15, -10, -5, 5, 10, 15] #angles to test for FPA proprioception
    for deg_i in range(len(deg_test)):

        ################# Manually moving the participant's foot to the desired angle #################
        print("        Press space after moving the participant's foot to " + str(deg_test[deg_i]) + " deg: ")
        keyboard.wait('space')  
    
        client.GetFrame()  # get the frame
        names = client.GetMarkerNames(subjectName)
        # Baseline markers - note: if there is a marker issue, then delete the segment in VICON and label the markers in the properties section, not in the subjects tab
        #TODO: check if the symmetric nature of the device messes with the coordination system 
        deg_15_in = client.GetMarkerGlobalTranslation(subjectName, 'deg_15_in')[0]
        deg_10_in = client.GetMarkerGlobalTranslation(subjectName, 'deg_10_in')[0]
        deg_5_in = client.GetMarkerGlobalTranslation(subjectName, 'deg_5_in')[0]
        deg_0 = client.GetMarkerGlobalTranslation(subjectName, 'deg_0')[0]
        deg_5_out = client.GetMarkerGlobalTranslation(subjectName, 'deg_5_out')[0]
        deg_10_out = client.GetMarkerGlobalTranslation(subjectName, 'deg_10_out')[0]
        deg_15_out= client.GetMarkerGlobalTranslation(subjectName, 'deg_15_out')[0]

        # Foot markers
        RTOE_manual = client.GetMarkerGlobalTranslation(subjectName, 'RTOE')[0]
        RHEE_manual = client.GetMarkerGlobalTranslation(subjectName, 'RHEE')[0]

        # #Heading vector to look at FPA
        # headingVec = (deg_0[0] - RHEE_manual[0], deg_0[1] - RHEE_manual[1])

        # add error exception for occluded markers
        if RTOE_manual == [0, 0] or RHEE_manual == [0, 0]:
            # Flag this data 
            print("Too many occlusions for RHEE/RTOE, check the markers")
            FPA_manual = np.nan
        else:
            # Calculate FPA
            footVec_manual = (RTOE_manual[0] - RHEE_manual[0], RTOE_manual[1] - RHEE_manual[1])
            FPA_manual = -math.degrees(math.atan(footVec_manual[1] / footVec_manual[0])) 
            # print("The manual angle is: " + str(FPA_manual))

        ################# Allowing the participant to move foot to the desired angle #################
             
        print("        Press space after allowing the participant to move their own foot to " + str(deg_test[deg_i]) + " deg: ")
        keyboard.wait('space')  
    
        client.GetFrame()  # get the frame
        
        # Foot markers
        RTOE_prop = client.GetMarkerGlobalTranslation(subjectName, 'RTOE')[0]
        RHEE_prop = client.GetMarkerGlobalTranslation(subjectName, 'RHEE')[0]

        # add error exception for occluded markers
        if RTOE_prop == [0, 0] or RHEE_prop == [0, 0]:
            # Flag this data 
            print("Too many occlusions for RHEE/RTOE, check the markers")
            FPA_prop = np.nan
        else:
            # Calculate FPA
            footVec_prop = (RTOE_prop[0] - RHEE_prop[0], RTOE_prop[1] - RHEE_prop[1])
            FPA_prop = -math.degrees(math.atan(footVec_prop[1] / footVec_prop[0]))
            # print("The current angle is: " + str(FPA_prop))

        if deg_test[deg_i] > 0:
            err_prop.append(FPA_prop - FPA_manual)
            err_prop_out.append(err_prop[deg_i])
        elif deg_test[deg_i] < 0:
            err_prop.append(-1*(FPA_prop - FPA_manual)) #flipping this so all positive errors mean over-correction in both directions 
            err_prop_in.append(err_prop[deg_i])
        
        print("        The error for this trial was: " + str(err_prop[deg_i]))
        FPA_store.append((time.time_ns(), deg_test[deg_i], FPA_manual, FPA_prop, err_prop[deg_i]))
        

    # save calculated FPA
    df = pd.DataFrame(FPA_store)
    df.to_csv(csv_file)
    # print avg error
    print("**---------------------------------------------------------------------------------------------------**")
    print("        Average error: " + str(np.nanmean(err_prop)) + "+/-" + str(np.nanstd(err_prop_in)))
    print("        Average toe-in error: " + str(np.nanmean(err_prop_in)) + "+/-" + str(np.nanstd(err_prop_in)))
    print("        Average toe-out error: " + str(np.nanmean(err_prop_out)) + "+/-" + str(np.nanstd(err_prop_out)))
    print("**---------------------------------------------------------------------------------------------------**")
        
except ViconDataStream.DataStreamException as e:
    print( 'Handled data stream error: ', e )
except KeyboardInterrupt:
    print( 'Keyboard interrupt detected, trial ended early and data was not saved' )





