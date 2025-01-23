import smbus2
import bme280
import csv

class SensorData:
    
    FIELDNAMES = ['timestamp', 'temperature',
                  'humidity', 'pressure']
    
    def __init__(self, port, address, document_name):
        self.port = port
        self.address = address
        self.bus = smbus2.SMBus(self.port)
        self.calibration_params = bme280.load_calibration_params(self.bus, self.address)
        
        self.data = bme280.sample(self.bus, self.address, self.calibration_params)
        self.second = self.data.timestamp.second
        self.data_collection = [self.data.timestamp.strftime('%x %H:%M:%S'),
                           f'{self.data.temperature:3.2f}',
                           f'{self.data.humidity:3.2f}',
                           f'{self.data.pressure:3.2f}']
        
        self.document_name = document_name
        self.document_names = ['{}_seconds.csv'.format(self.document_name)]

    def update(self): # updates all important sensor information
        self.data = bme280.sample(self.bus, self.address, self.calibration_params)
        self.second = self.data.timestamp.second
        self.data_collection = [self.data.timestamp.strftime('%x %H:%M:%S'),
                           f'{self.data.temperature:3.2f}',
                           f'{self.data.humidity:3.2f}',
                           f'{self.data.pressure:3.2f}']
    
    def write(self): #writes sensor data to a single line in a CSV file
        with open('./Sensor_csv_data/{}'.format(self.document_names[0]),'a', newline='') as seconds_csv:
            self.writer = csv.writer(seconds_csv, delimiter=',')
            self.writer.writerow(self.data_collection)
            seconds_csv.close()
        
    def run(self):
        self.update()
        self.sensor_error_check()
        self.write()
    
    def sensor_error_check(self):    
        if(self.data.temperature < -40 or self.data.temperature > 85):
            raise ValueError("Temperature is outside detectable range. -45 to 85 degrees C")
        
        if(self.data.humidity < 0 or self.data.humidity > 100):
            raise ValueError("Humidity is outside of range. 0 to 100%")
        
        if(self.data.pressure < 300 or self.data.pressure > 1100):
            raise ValueError("Pressure is outside of range. 300 to 1100")
