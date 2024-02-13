from bleak import BleakClient, BleakScanner
import asyncio
import time

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

try:
    # Connect to Bluetooth
    print(' Connecting to GaitGuide...')
    GaitGuide = asyncio.run(connect_to_device()) #TODO: check if this works

    print('Getting GaitGuide service...')
    service = GaitGuide.services.get_service(BLE_DURATION_STIM_SERVICE_UUID)

    if service:
        print('Setting Right and Left GaitGuide characteristics...')
        Right = get_characteristic(service, BLE_DURATION_RIGHT_CHARACTERISTIC_UUID)
        Left = get_characteristic(service, BLE_DURATION_LEFT_CHARACTERISTIC_UUID)

    count = 0
    while (GaitGuide.is_connected and count < 11):
        asyncio.run(write_characteristic(GaitGuide, Right, 120))
        time.sleep(1)
        print('Right')

        asyncio.run(write_characteristic(GaitGuide, Left, 120))
        time.sleep(1)
        print('Left')

        count = count+1

except KeyboardInterrupt:
    GaitGuide.disconnect()
    print('GaitGuide Disconnected [', GaitGuide.address, ']')