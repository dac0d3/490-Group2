'''
Things we need to test.

Sensor range exceptions.
Document writing.
Sensor update.
'''
import unittest
import csv
from datetime import datetime
from SensorData import SensorData
from unittest.mock import patch

class testSensorData(unittest.TestCase):
    
    '''
    sensor range
    Pressure
		300 hpa - 1100 hpa
	Temperature
		-40 C - 85C
	Humidity
		0 - 100%
    '''
    
    def setUp(self):
        self.good_sensor = SensorData(1, 0x77, 'good_sensor')
        self.good_sensor.data.id = 0
        self.good_sensor.data.timestamp = datetime.now()
        self.good_sensor.data.temperature = 0
        self.good_sensor.data.pressure = 550
        self.good_sensor.data.humidity = 50
                     
        self.bad_sensor = SensorData(1, 0x77, 'bad_sensor')
        self.bad_sensor.data.id = 0
        self.bad_sensor.data.timestamp = datetime.now()
        self.bad_sensor.data.temperature = 110
        self.bad_sensor.data.pressure = 11000
        self.bad_sensor.data.humidity = 110
        
        self.bad_temp_sensor_low = SensorData(1, 0x77, 'bad_sensor')
        self.bad_sensor.data.id = 0
        self.bad_sensor.data.timestamp = datetime.now()
        self.bad_sensor.data.temperature = -1000
        self.bad_sensor.data.pressure = 550
        self.bad_sensor.data.humidity = 50
        
        self.bad_temp_sensor_high = SensorData(1, 0x77, 'bad_sensor')
        self.bad_sensor.data.id = 0
        self.bad_sensor.data.timestamp = datetime.now()
        self.bad_sensor.data.temperature = 100
        self.bad_sensor.data.pressure = 550
        self.bad_sensor.data.humidity = 50
        
        self.bad_pressure_sensor_low = SensorData(1, 0x77, 'bad_sensor')
        self.bad_sensor.data.id = 0
        self.bad_sensor.data.timestamp = datetime.now()
        self.bad_sensor.data.temperature = 0
        self.bad_sensor.data.pressure = 200
        self.bad_sensor.data.humidity = 50
        
        self.bad_pressure_sensor_high = SensorData(1, 0x77, 'bad_sensor')
        self.bad_sensor.data.id = 0
        self.bad_sensor.data.timestamp = datetime.now()
        self.bad_sensor.data.temperature = 0
        self.bad_sensor.data.pressure = 1150
        self.bad_sensor.data.humidity = 50
        
        self.bad_humidity_sensor_low = SensorData(1, 0x77, 'bad_sensor')
        self.bad_sensor.data.id = 0
        self.bad_sensor.data.timestamp = datetime.now()
        self.bad_sensor.data.temperature = 0
        self.bad_sensor.data.pressure = 550
        self.bad_sensor.data.humidity = -10
        
        self.bad_humidity_sensor_high = SensorData(1, 0x77, 'bad_sensor')
        self.bad_sensor.data.id = 0
        self.bad_sensor.data.timestamp = datetime.now()
        self.bad_sensor.data.temperature = 0
        self.bad_sensor.data.pressure = 550
        self.bad_sensor.data.humidity = 110
        
        self.bad_sensor_range = [
            self.bad_sensor,
            self.bad_temp_sensor_low, self.bad_temp_sensor_high,
            self.bad_pressure_sensor_low, self.bad_pressure_sensor_high,
            self.bad_humidity_sensor_low, self.bad_humidity_sensor_high
            ]
            
    # tests all ranges of that would cause sensor error check to raise error
    def test_sensor_error_check(self):
        for bad_sensor in self.bad_sensor_range:
            self.sensor = self.bad_sensor
            with self.assertRaises(ValueError):
                self.sensor.sensor_error_check()
    
    # tests all update params
    @patch('bme280.sample')
    def test_update(self, mock_sample):
        self.sensor = self.bad_sensor
        
        mock_sample.return_value = self.good_sensor.data
        
        self.assertEqual(f'{self.sensor.data_collection[0]}',
                         f'{self.good_sensor.data_collection[0]}')
        for i in range(1,len(self.sensor.data_collection)):
            self.assertEqual(f'{self.sensor.data_collection[i]:3.1}',
                         f'{self.good_sensor.data_collection[i]:3.1}')
        self.assertEqual(self.sensor.second,
                         self.good_sensor.second)
        
    def test_write(self):
        self.sensor = self.bad_sensor
        
        # write sensor info to file
        self.good_sensor.write()
        
        # open file created in write function
        with open('./Sensor_csv_data/{}'.format(self.good_sensor.document_names[0]),
                  newline='') as file:
            reader = csv.reader(file, delimiter=',', quotechar='|')
            # copy written data to new sensor
            for row in reader:
                self.sensor.data_collection = row
        
        self.assertEqual(self.sensor.data_collection, self.good_sensor.data_collection)
        
if __name__ == '__main__':
    unittest.main()