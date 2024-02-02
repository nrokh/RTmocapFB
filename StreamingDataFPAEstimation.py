from vicon_dssdk import ViconDataStream
import argparse
import sys
import time
import math
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import keyboard #TODO: make sure this is installed

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
    DIFFDV_store = [10,10,10] # TODO: check if this is how you want to initialize

    while True: # wait for keyboard interrupt
        subjectName = subjectNames[0] # select the main subject
        client.GetFrame() # get the frame



        ################# ENTER BASELINE FPA ###############
        baselineFPA = float(input("Enter subject's baseline FPA and hit enter: "))

        ################# CALCULATE FPA ####################

        # calculate FPA (horizontal plane, so X and Y components only):

        # TODO: include error exception for an occluded marker
        footVec = (client.GetMarkerGlobalTranslation( subjectName, 'RTOE')[0][0]- client.GetMarkerGlobalTranslation( subjectName, 'RHEE')[0][0],
                   client.GetMarkerGlobalTranslation( subjectName, 'RTOE')[0][1] - client.GetMarkerGlobalTranslation( subjectName, 'RHEE')[0][1])

        FPA = -math.degrees(math.atan(footVec[1]/footVec[0])) # TODO: check signs for right foot





        ################# STEP DETECTION ###################
        keyboard.wait('space')         # TODO: check if keyboard input works; experimenter waits for steady-state

        # get AP CAL and PSI markers (TODO: should be 0th index -- X component-- but check)
        CAL = client.GetMarkerGlobalTranslation( subjectName, 'RCAL')[0][0]
        CAL_store.append(CAL)
        PSI = client.GetMarkerGlobalTranslation( subjectName, 'RPSI')[0][0]
        PSI_store.append(CAL)

        # take derivative of difference between heel and hip:
        DIFF = CAL - PSI
        DIFFDV_store.append(DIFF)

        # get heel-strike; search for local max
        if DIFFDV_store[-1]<=0 and DIFFDV_store[-2]>=0 and DIFFDV_store[-3]>=0 and DIFFDV_store[-4]>=0:
            # TODO store stanceFPA

            # get toe-off (continue getting this value while in IF condition; TODO check if this makes sense)
            DIFF = CAL - PSI
            DIFFDV_store.append(DIFF)

            # get toe-off; search for local min
            if DIFFDV_store[-1]>=0 and DIFFDV_store[-2]<=0 and DIFFDV_store[-3]<=0 and DIFFDV_store[-4]<=0:
                # TODO average FPA throughout stance

                # TODO compare avg FPA to target

                ################# CUE GAITGUIDE ###############
                # SCALE FEEDBACK ACCORDING TO DISTANCE FROM TARGET
                ;  
                
        
        
        # save FPA value to the list
        FPA_store.append(FPA)

except KeyboardInterrupt: # CTRL-C to exit
    # save calculated FPA
    df = pd.DataFrame(FPA_store)
    csv_file = 'H:\__CODE\Streaming\DSSDK_Scripts\FPA_Python.csv'
    df.to_csv(csv_file)
    
    # plot the FPA
    plt.plot(FPA_store)
    plt.xlabel('Frame')
    plt.ylabel('FPA [deg]')
    plt.show()


except ViconDataStream.DataStreamException as e:
    print( 'Handled data stream error: ', e )


