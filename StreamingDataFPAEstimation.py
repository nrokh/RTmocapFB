from vicon_dssdk import ViconDataStream
import argparse
import sys
import time
import math
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import keyboard
import asyncio
import struct
from bleak import BleakScanner, BleakClient
import tkinter as tk
from tkinter import filedialog
import os

############# GAIT GUIDE SETUP #####################

# gaitguide BLE settings:
BLE_DURATION_STIM_SERVICE_UUID = '1111'
BLE_AMPLITUDE_CHARACTERISTIC_UUID = '1112' 
BLE_DURATION_RIGHT_CHARACTERISTIC_UUID = '1113'  # these need to be chaned at some point for BLE specificatin reasons '48e47602-1b27-11ee-be56-0242ac120002'
BLE_DURATION_LEFT_CHARACTERISTIC_UUID = '1114'  # '63bae092-1b27-11ee-be56-0242ac120002'
timeout = 5

async def connect_to_device():
    devices = await BleakScanner.discover()
    for d in devices:
        if d.name == 'GaitGuide':
            print('Device found - MAC [', d.address, ']')
            client = BleakClient(d.address)
            await client.connect(timeout=timeout)
            print('Connected [', d.address, ']')
            return client

def get_characteristic(service, characteristic_uuid):
    characteristic = service.get_characteristic(characteristic_uuid)
    return characteristic

async def set_amp(client, characteristic, value):
    await client.write_gatt_char(characteristic,  bytearray([value]))

async def write_characteristic(client, characteristic, value):
    await client.write_gatt_char(characteristic, bytearray(value))

############# FILE SAVING #####################

def generate_csv_filename(directory, subject_name, parameter):
    csv_file = os.path.join(directory, subject_name, parameter, '.csv')
    counter = 0
    while os.path.exists(csv_file):
        counter += 1
        csv_file = os.path.join(directory, subject_name, '_Baseline_FPA' + str(counter) + '.csv')
    return csv_file

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
    print('        Subject name: ', subjectNames)

    # Get the desired directory to save the data
    root = tk.Tk()
    root.withdraw() # we don't want a full GUI, so keep the root window from appearing
    directory = filedialog.askdirectory()

    # Connect to Bluetooth
    print(' Connecting to GaitGuide...')
    GaitGuide = asyncio.run(connect_to_device()) 

    print('Getting GaitGuide service...')
    service = GaitGuide.services.get_service(BLE_DURATION_STIM_SERVICE_UUID)

    if service:
        print('Setting Amp, Right and Left GaitGuide characteristics...')
        Right = get_characteristic(service, BLE_DURATION_RIGHT_CHARACTERISTIC_UUID)
        Left = get_characteristic(service, BLE_DURATION_LEFT_CHARACTERISTIC_UUID)
        Ampl = get_characteristic(service, BLE_AMPLITUDE_CHARACTERISTIC_UUID)

    print('Setting GaitGuide amplitude to max...')
    asyncio.run(set_amp(GaitGuide, Ampl, 127))

    # create a list to store FPA and marker values
    FPA_store = []
    CAL_store = []
    PSI_store = []
    DIFF_store = [0,0,0]
    DIFFDV_store = [0,0,0] 
    gaitEvent_store = []
    FPAstep_store = []
    meanFPAstep_store = []  

    # create flag to check for systemic occlusions
    occl_flag_foot = 0 
    occl_flag_hip = 0

    ############## SCALED FEEDBACK SETUP ###############
    band = 2 #degrees to either side

    feedbackType = float(input("Select feedback type: (1) = trinary; (2) = scaled: "))
    if feedbackType == 1.0:
        print("Starting trinary feedback mode...")
    elif feedbackType == 2.0:
        print("Starting scaled feedback mode...")

    ################# ENTER BASELINE FPA ###############
    baselineFPA = float(input("Enter subject's baseline FPA and hit enter: "))
    targetFPA = baselineFPA - 10.0
    print("Target toe-in angle is: ", targetFPA)

    ################# STEP DETECTION ###################
    print("Press space when ready to start step detection: ")
    keyboard.wait('space')        

    local_max_detected = False

    while True: # wait for keyboard interrupt
        subjectName = subjectNames[0] # select the main subject
        client.GetFrame() # get the frame


        ################# CALCULATE FPA ####################

        RTOE_translation = client.GetMarkerGlobalTranslation(subjectName, 'RTOE')[0]
        RHEE_translation = client.GetMarkerGlobalTranslation(subjectName, 'RHEE')[0]
        CAL = RHEE_translation[0]
        PSI = client.GetMarkerGlobalTranslation( subjectName, 'RPSI')[0][0]

        # add error exception for occluded markers
        if RTOE_translation == [0, 0] or RHEE_translation == [0, 0]:
            # Flag this data and check if it's consecutively too frequent
            occl_flag_foot += 1
            if occl_flag_foot > 25:
                print("Too many occlusions for RHEE/RTOE, check the markers")
            #save FPA as a NaN value so we can discard later
            FPA = np.nan
        else:
            # Calculate FPA
            occl_flag_foot = 0
            footVec = (RTOE_translation[0] - RHEE_translation[0], RTOE_translation[1] - RHEE_translation[1])
            FPA = -math.degrees(math.atan(footVec[1] / footVec[0])) 
            CAL_store.append(CAL)

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
        if DIFFDV_store[-1]>=0 and DIFFDV_store[-2]<=0 and DIFFDV_store[-3]<=0 and DIFFDV_store[-4]<=0:

            print("local max")
            FPAstep_store = []
            local_max_detected = True
            gaitEvent_store.append((time.time(), 1.0))

        FPAstep_store.append(FPA)

        # search for min:
        if local_max_detected and DIFFDV_store[-1]<=0 and DIFFDV_store[-2]>=0 and DIFFDV_store[-3]>=0 and DIFFDV_store[-4]>=0:
            print("local min")
            meanFPAstep = np.nanmean(FPAstep_store)
            meanFPAstep_store.append((time.time(), meanFPAstep)) 
            print("mean FPA for step = " + str(meanFPAstep))
            gaitEvent_store.append((time.time(), 2.0))

            local_max_detected = False

            ################# CUE GAITGUIDE ###############
            if feedbackType == 1.0: #trinary mode
                if meanFPAstep < targetFPA - band: # too far in
                    asyncio.run(write_characteristic(GaitGuide, Left, 255))

                elif meanFPAstep > targetFPA + band: # too far out
                    asyncio.run(write_characteristic(GaitGuide, Right, 255))

            elif feedbackType == 2.0: # scaled feedback mode
                if meanFPAstep < targetFPA - band:
                    duration = 100 + (targetFPA - meanFPAstep)*50 
                    duration_packed = struct.pack('<H', int(duration))
                    asyncio.run(write_characteristic(GaitGuide, Left, duration_packed))

                elif meanFPAstep > targetFPA + band:
                    duration = 100 + (meanFPAstep - targetFPA)*50
                    duration_packed = struct.pack('<H', int(duration))
                    asyncio.run(write_characteristic(GaitGuide, Right, duration_packed))



        # save FPA value to the list
        FPA_store.append((time.time(), FPA))



except KeyboardInterrupt: # CTRL-C to exit #TODO: change subjectNames to what we want
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

    # save DIFF
    df = pd.DataFrame(DIFF_store)
    csv_file_df = generate_csv_filename(directory, subjectNames, 'DIFF')
    df.to_csv(csv_file_df) 

    # save DIFFDV
    dfdv = pd.DataFrame(DIFFDV_store)
    csv_file_dfdv = generate_csv_filename(directory, subjectNames, 'DIFFDV')
    dfdv.to_csv(csv_file_dfdv)
    
    # Plot the FPA
    plt.plot(df_FPA.iloc[:,1])
    plt.xlabel('Frame')
    plt.ylabel('FPA [deg]')

    # Plot meanFPAstep_store as circles TODO: fix this vis
    '''
    meanFPAstep_time = [t for t, _ in meanFPAstep_store]
    meanFPAstep_value = [v for _, v in meanFPAstep_store]
    plt.scatter(meanFPAstep_time, meanFPAstep_value, color='red', marker='o')
    '''

    plt.show()
    
    GaitGuide.disconnect()
    print('GaitGuide Disconnected [', GaitGuide.address, ']')

except ViconDataStream.DataStreamException as e:
    print( 'Handled data stream error: ', e )


