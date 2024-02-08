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
'''
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

async def get_characteristic(service, characteristic_uuid):
    characteristic = service.get_characteristic(characteristic_uuid)
    return characteristic

async def write_characteristic(client, characteristic, value):
    await client.write_gatt_char(characteristic, bytearray([value]))

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

    # create a list to store FPA and marker values
    FPA_store = []
    CAL_store = []
    PSI_store = []
    DIFF_store = [0,0,0]
    DIFFDV_store = [0,0,0] # TODO: check if this is how you want to initialize

    ################# ENTER BASELINE FPA ###############
    baselineFPA = float(input("Enter subject's baseline FPA and hit enter: "))

    ################# STEP DETECTION ###################
    print("Press space when ready to start step detection: ")
    keyboard.wait('space')         # TODO: check if keyboard input works; experimenter waits for steady-state

    while True: # wait for keyboard interrupt
        subjectName = subjectNames[0] # select the main subject
        client.GetFrame() # get the frame


        ################# CALCULATE FPA ####################
        

        # calculate FPA (horizontal plane, so X and Y components only):
        footVec = (client.GetMarkerGlobalTranslation( subjectName, 'RTOE')[0][0]- client.GetMarkerGlobalTranslation( subjectName, 'RHEE')[0][0],
                   client.GetMarkerGlobalTranslation( subjectName, 'RTOE')[0][1] - client.GetMarkerGlobalTranslation( subjectName, 'RHEE')[0][1])
        
        # TODO: include error exception for an occluded marker
        FPA = -math.degrees(math.atan(footVec[1]/footVec[0])) # TODO: check signs for right foot    


        # get AP CAL and PSI markers (TODO: should be 0th index -- X component-- but check)
        CAL = client.GetMarkerGlobalTranslation( subjectName, 'RHEE')[0][0]
        CAL_store.append(CAL)
        PSI = client.GetMarkerGlobalTranslation( subjectName, 'RPSI')[0][0]
        PSI_store.append(CAL)

        # take derivative of difference between heel and hip:
        DIFF = CAL - PSI
        DIFF_store.append(DIFF)
        DIFFDV = DIFF_store[-1] - DIFF_store[-2] 
        DIFFDV_store.append(DIFFDV)

        # search for local max 

        if DIFFDV_store[-1]<=0 and DIFFDV_store[-2]>=0 and DIFFDV_store[-3]>=0 and DIFFDV_store[-4]>=0:

            print("local max")
            FPAstep_store = []
            local_min_detected = False

            while not local_min_detected:
                
                # continue to take derivative of difference between heel and hip:
                        # calculate FPA (horizontal plane, so X and Y components only):
                footVec = (client.GetMarkerGlobalTranslation( subjectName, 'RTOE')[0][0]- client.GetMarkerGlobalTranslation( subjectName, 'RHEE')[0][0],
                        client.GetMarkerGlobalTranslation( subjectName, 'RTOE')[0][1] - client.GetMarkerGlobalTranslation( subjectName, 'RHEE')[0][1])
                
                # TODO: include error exception for an occluded marker
                FPA = -math.degrees(math.atan(footVec[1]/footVec[0])) # TODO: check signs for right foot    

                DIFF = CAL - PSI
                DIFF_store.append(DIFF)
                DIFFDV = DIFF_store[-2] - DIFF_store[-3] #one frame lag to compensate for zeros
                DIFFDV_store.append(DIFFDV)

                FPAstep_store.append(FPA)

                # search for local min
                if DIFFDV_store[-1]>=0 and DIFFDV_store[-2]<=0 and DIFFDV_store[-3]<=0 and DIFFDV_store[-4]<=0:
                    
                    local_min_detected = True
                    print("local min")
                    # average FPA throughout stance
                    meanFPAstep = np.mean(FPAstep_store)

                    print("mean FPA for step = " + str(meanFPAstep))

                    # TODO compare avg FPA to target

                ################# CUE GAITGUIDE ###############
                # SCALE FEEDBACK ACCORDING TO DISTANCE FROM TARGET 


        # save FPA value to the list
        FPA_store.append(FPA)

except KeyboardInterrupt: # CTRL-C to exit
    # save calculated FPA
    df = pd.DataFrame(FPA_store)
    csv_file = 'D:\stepdetect_debugging\FPA_Python.csv'
    df.to_csv(csv_file)

    # save DIFF
    df = pd.DataFrame(DIFF_store)
    csv_file = 'D:\stepdetect_debugging\DIFF_Python.csv'
    df.to_csv(csv_file) 

    # save DIFFDV
    df = pd.DataFrame(DIFFDV_store)
    csv_file = 'D:\stepdetect_debugging\DIFFDV_Python.csv'
    df.to_csv(csv_file)

    # TODO: save HS/TO events with time stamps?
    
    # plot the FPA
    plt.plot(FPA_store)
    plt.xlabel('Frame')
    plt.ylabel('FPA [deg]')
    plt.show()


except ViconDataStream.DataStreamException as e:
    print( 'Handled data stream error: ', e )


