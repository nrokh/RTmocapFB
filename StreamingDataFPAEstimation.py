from vicon_dssdk import ViconDataStream
import argparse
import sys
import time
import math
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import keyboard #TODO: make sure this is installed
import asyncio
from bleak import BleakScanner, BleakClient

############# GAIT GUIDE SETUP #####################

# gaitguide BLE settings:
BLE_DURATION_STIM_SERVICE_UUID = '1111'
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


async def write_characteristic(client, characteristic, value):
    await client.write_gatt_char(characteristic, bytearray([value]))

'''

async def run():
    
    print("Searching for BLE GaitGuide...")
    GaitGuide = await connect_to_device()
    service = GaitGuide.services.get_service(BLE_DURATION_STIM_SERVICE_UUID)

    if service:
        Right = await get_characteristic(service, BLE_DURATION_RIGHT_CHARACTERISTIC_UUID)
        Left = await get_characteristic(service, BLE_DURATION_LEFT_CHARACTERISTIC_UUID)

    count = 0
    while (GaitGuide.is_connected and count < 11):
        await write_characteristic(GaitGuide, Right, 120)
        time.sleep(1)  # Sleep for 1 second

        await write_characteristic(GaitGuide, Left, 120)
        time.sleep(1)  # Sleep for 1 second

        count = count +1

    await GaitGuide.disconnect()
    print('GaitGuide Disconnected [', GaitGuide.address, ']')
'''

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


    # Connect to Bluetooth
    print(' Connecting to GaitGuide...')
    GaitGuide = asyncio.run(connect_to_device()) #TODO: check if this works

    print('Getting GaitGuide service...')
    service = GaitGuide.services.get_service(BLE_DURATION_STIM_SERVICE_UUID)

    if service:
        print('Setting Right and Left GaitGuide characteristics...')
        Right = get_characteristic(service, BLE_DURATION_RIGHT_CHARACTERISTIC_UUID)
        Left = get_characteristic(service, BLE_DURATION_LEFT_CHARACTERISTIC_UUID)



    # create a list to store FPA and marker values
    FPA_store = []
    CAL_store = []
    PSI_store = []
    DIFF_store = [0,0,0]
    DIFFDV_store = [0,0,0] # TODO: check if this is how you want to initialize
    gaitEvent_store = []
    FPAstep_store = []
    meanFPAstep_store = []  

    # create flag to check for systemic occlusions
    occl_flag_foot = 0 
    occl_flag_hip = 0

    ################# ENTER BASELINE FPA ###############
    baselineFPA = float(input("Enter subject's baseline FPA and hit enter: "))

    ################# STEP DETECTION ###################
    print("Press space when ready to start step detection: ")
    keyboard.wait('space')         # TODO: check if keyboard input works; experimenter waits for steady-state
    
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
            FPA = -math.degrees(math.atan(footVec[1] / footVec[0]))  # TODO: check signs for right foot
            CAL_store.append(CAL)

        # get AP CAL and PSI markers (TODO: should be 0th index -- X component-- but check)
 
        if PSI == 0:
            occl_flag_hip += 1
            if occl_flag_hip > 25:
                print("Too many occlusions for PSI, check marker")
        else:
            occl_flag_hip = 0
            PSI_store.append(PSI)

            # [NR]: this calculation should be running continually, TODO: check if it makes sense to have it here OR in the next block of code, not both places
            # take derivative of difference between heel and hip:
            DIFF = CAL - PSI
            DIFF_store.append(DIFF)
            DIFFDV = DIFF_store[-1] - DIFF_store[-2] 
            DIFFDV_store.append(DIFFDV)    
        
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
            meanFPAstep_store.append((time.time(), meanFPAstep)) #TODO: where should the timestamp for the meanFPAstep be? at the beginning or end or middle of the step? [NR]: at the time local min is detected, the way you have it, works fine

            print("mean FPA for step = " + str(meanFPAstep))
            gaitEvent_store.append((time.time(), 2.0))

            local_max_detected = False

            ################# CUE GAITGUIDE ###############
            asyncio.run(write_characteristic(GaitGuide, Right, 120))
                # TODO: SCALE FEEDBACK ACCORDING TO DISTANCE FROM TARGET 
            # if meanFPAstep < baselineFPA, cue left; else cue right


        # save FPA value to the list
        FPA_store.append((time.time(), FPA))

except KeyboardInterrupt: # CTRL-C to exit
    # save calculated FPA
    df = pd.DataFrame(FPA_store)
    csv_file = 'D:\stepdetect_debugging\FPA_Python.csv'
    df.to_csv(csv_file)

    # save the mean FPA for each step w/ timestamps
    df = pd.DataFrame(meanFPAstep_store)
    csv_file = 'D:\stepdetect_debugging\meanFPAstep_Python.csv'
    df.to_csv(csv_file)

    # save gait events
    df = pd.DataFrame(gaitEvent_store)
    csv_file = 'D:\stepdetect_debugging\GaitEvent_Python.csv'
    df.to_csv(csv_file)

    # save DIFF
    df = pd.DataFrame(DIFF_store)
    csv_file = 'D:\stepdetect_debugging\DIFF_Python.csv'
    df.to_csv(csv_file) 

    # save DIFFDV
    df = pd.DataFrame(DIFFDV_store)
    csv_file = 'D:\stepdetect_debugging\DIFFDV_Python.csv'
    df.to_csv(csv_file)
    
    #TODO: don't know python well enough to know if this will work... but check! 
    # Plot the FPA
    plt.plot(FPA_store)
    plt.xlabel('Frame')
    plt.ylabel('FPA [deg]')

    # Plot meanFPAstep_store as circles
    meanFPAstep_time = [t for t, _ in meanFPAstep_store]
    meanFPAstep_value = [v for _, v in meanFPAstep_store]
    plt.scatter(meanFPAstep_time, meanFPAstep_value, color='red', marker='o')

    plt.show()
    
    GaitGuide.disconnect()
    print('GaitGuide Disconnected [', GaitGuide.address, ']')

except ViconDataStream.DataStreamException as e:
    print( 'Handled data stream error: ', e )


