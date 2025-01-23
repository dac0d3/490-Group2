import smbus2
import bme280
import csv
from time import sleep

# grab / assign sensor information
port = 1
address = 0x77
bus = smbus2.SMBus(port)
calibration_params = bme280.load_calibration_params(bus, address)

# initialize data
data = None
data_collection = []
second = 0

# csv file setup
fieldNames = ['timestamp', 'temperature', 'humidity', 'pressure']
document_names = ['five_minutes_data.csv']

def updateSensor(): # updates all important sensor information
    global data
    global data_collection
    global second 
    
    data = bme280.sample(bus, address, calibration_params)
    data_collection = [data.timestamp.strftime('%x %H:%M:%S'), f'{data.temperature:3.2f}', f'{data.humidity:3.2f}', f'{data.pressure:3.2f}']
    second = data.timestamp.second

# while True:
for i in range(300):
    updateSensor()
    
    with open(document_names[0],'a', newline='') as seconds_csv:
        writer = csv.writer(seconds_csv, delimiter=',')
        writer.writerow(data_collection)
        print(second)
        seconds_csv.close()
        sleep(1)