import argparse
import sys
import time
import math
import keyboard
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
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
BLE_BATTERY_SERVICE_UUID = '180F'
BLE_BATTERY_LEVEL_CHARACTERISTIC_UUID = '2A19'
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

async def read_characteristic(client, characteristic):
    value = await client.read_gatt_char(characteristic)
    return value

############### STREAMING SETUP ########################
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

# GG battery level checks:    
print('Getting GG battery service...')
BAT_service = GaitGuide.services.get_service(BLE_BATTERY_SERVICE_UUID)

if BAT_service:
    Bat = get_characteristic(BAT_service, BLE_BATTERY_LEVEL_CHARACTERISTIC_UUID)

batteryLevel = asyncio.run(read_characteristic(GaitGuide, Bat))
batteryLevel_int = int.from_bytes(batteryLevel, "little")  # use "big" for big-endian
print(f'Battery Level = [{batteryLevel_int}%]')

print('Setting GaitGuide amplitude to max...')
asyncio.run(set_amp(GaitGuide, Ampl, 127))

# Get pre-recorded FPA file:
meanFPAstep = np.genfromtxt('demo/s_pilot_meanFPA.csv', delimiter=',')
meanFPAstep = meanFPAstep[:][2:26]
# TODO: crop array to video

############## SCALED FEEDBACK SETUP ###############
band = 2 #degrees to either side

feedbackType = float(input("Select feedback type: (0) = no feedback; (1) = trinary; (2) = scaled: "))

if feedbackType == 0.0:
    print("Starting no feedback mode...")
elif feedbackType == 1.0:
    print("Starting trinary feedback mode...")
elif feedbackType == 2.0:
    print("Starting scaled feedback mode...")

################# ENTER BASELINE FPA ###############
baselineFPA = 10.0
targetFPA = baselineFPA - 10.0
print("Target toe-in angle is: ", targetFPA)

################# STEP DETECTION ###################
print("Press space when ready to start step detection: ")
keyboard.wait('space')

# cue
for i in range(len(meanFPAstep)):
    print(meanFPAstep[i][2])
    if feedbackType == 1.0: #trinary mode
        if meanFPAstep[i][2] < targetFPA - band: # too far in
            duration = 330
            duration_packed = struct.pack('<H', int(duration))
            asyncio.run(write_characteristic(GaitGuide, Right, duration_packed))

            time.sleep(22) #todo: check time

        elif meanFPAstep[i][2] > targetFPA - band:
            duration = 330
            duration_packed = struct.pack('<H', int(duration))
            asyncio.run(write_characteristic(GaitGuide, Left, duration_packed))

            time.sleep(2) #todo: check time
    
    elif feedbackType == 2.0: #scaled mode
        if meanFPAstep[i][2] < targetFPA - band: # too far in
            duration = abs((targetFPA - meanFPAstep[i][2])*50-50)#108 - 156)
            print(duration)
            if duration > 600:
                duration = 600
            duration_packed = struct.pack('<H', int(duration))
            asyncio.run(write_characteristic(GaitGuide, Right, duration_packed))

            time.sleep(2) #todo: check time

        elif meanFPAstep[i][2] > targetFPA - band:
            duration = abs((targetFPA - meanFPAstep[i][2])*50-50)#108 - 156)
            print(duration)
            if duration > 600:
                duration = 600
            duration_packed = struct.pack('<H', int(duration))
            asyncio.run(write_characteristic(GaitGuide, Left, duration_packed))

            time.sleep(2) #todo: check time
                    



