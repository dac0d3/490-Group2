from dateutil.relativedelta import relativedelta as delta
from datetime import datetime as dt
import csv
import random
from time import sleep

start_data = 'start_data.csv' # first 75 entries
test_seconds = 'test_seconds.csv'
fmt = '%x %H:%M:%S'
c_time = dt.now()

def add_data():
    '''
    bme280 sensor ranges

    Temperature:    -40     to      85      C
    Humidity:         0     to      100     %
    Pressure:       300     to      1100    hPa
    Altitude:         0     to      9144   m

    [time.time(),random.randrange(0, 50), random.randrange(0, 100), random.randrange(300, 1100), random.randrange(0, 9144)]
    '''
    file = open(test_seconds, 'a', newline='')
    writer = csv.writer(file)
    writer.writerow([dt.now().strftime(fmt),random.randrange(0, 50), random.randrange(0, 100), random.randrange(300, 1100)])

    file.close()

def setup_csv(): # copy values from start_data.csv to test_seconds.csv
    r = []
    # create a new file called test_seconds.csv or overwrite the prvious one
    with open(test_seconds, 'w',newline='') as eraser_file:
        eraser_file.close()

    # open start_data.csv
    with open(start_data, newline='') as start_file:
        reader = csv.reader(start_file,delimiter=',')
        # copy each line into test_seconds.csv
        count = 74
        for row in reader:
            r = [(c_time - delta(seconds=count)).strftime(fmt), row[1], row[2], row[3]]
            count -= 1
            with open(test_seconds, 'a', newline='') as writer_file:
                    writer = csv.writer(writer_file, delimiter=',',
                                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow(r)
            writer_file.close()
        start_file.close()

setup_csv()

while True:
     sleep(1)
     add_data()