from vicon_dssdk import ViconDataStream
import argparse
import sys
import time
import math
import matplotlib.pyplot as plt
import pandas as pd

# create arg to host (Vicon Nexus)
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('host', nargs='?', help="Host name, in the format of server:port", default = "localhost:801")
args = parser.parse_args()

client = ViconDataStream.Client()

try:
    # Connect to Nexus (Nexus needs to be on and either Live or replaying previosly collected data)
    client.Connect( args.host)
    print( '        Connected to Nexus')

    # Enable the data type
    client.EnableMarkerData()

    # Report whether data type was enabled successfully:
    print ( '        Markers enabled? ', client.IsMarkerDataEnabled() )


    # start getting frames (check if this is needed??)
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

    # create a list to store FPA values
    FPA_store = []

    while True: # wait for keyboard interrupt
        subjectName = subjectNames[0] # select the main subject
        client.GetFrame() # get the frame

        # calculate FPA (horizontal plane, so X and Y components only):
        footVec = (client.GetMarkerGlobalTranslation( subjectName, 'LTOE')[0][0]- client.GetMarkerGlobalTranslation( subjectName, 'LHEE')[0][0],
                   client.GetMarkerGlobalTranslation( subjectName, 'LTOE')[0][1] - client.GetMarkerGlobalTranslation( subjectName, 'LHEE')[0][1])

        FPA = math.degrees(math.atan(footVec[1]/footVec[0]))

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