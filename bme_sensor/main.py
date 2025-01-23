from SensorData import SensorData
from time import sleep

port = 1
address = 0x77
document_name = 'test'

def main():
    sensor = SensorData(port, address, document_name)
    
    print(type(sensor.data))
    
    while True:
        sensor.run()
        sleep(1)
    
    
if __name__ == '__main__':
    main()
    
