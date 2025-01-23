from flask import render_template, url_for, redirect
from flask_socketio import emit
from astrocultivators import app, socket
from get_most_recent import return_most_recent_in_folder

# imports for charts
import base64 
from io import BytesIO
from sensor_figure import get_figure, get_current_data, get_time_data
from sensor_data import SensorData
from detect_distance import RS_Camera

port = 1
address = 0x77
document_name = 'test'

# pathing starts from where run.py is being called NOT from where the file is in dir
rgb_image_folder = 'astrocultivators/static/images/rgb/'
objdet_image_folder = 'astrocultivators/static/images/object_detection/'
hyperspectral_image_folder = 'astrocultivators/static/images/hyperspectral/'

sensor = SensorData(port, address, document_name)

print(f"rgb file: {return_most_recent_in_folder(rgb_image_folder)}")
print(f"object detected file: {return_most_recent_in_folder(objdet_image_folder)}")
print(f"hyperspectral file: {return_most_recent_in_folder(hyperspectral_image_folder)}")

@socket.on('connect')
def handle_init_chart():
    print('Connected!')
    emit('init-chart', get_figure())

# Update emitted from liveChart.js
@socket.on('update')
def handle_update():
    sensor.run()
    emit('update-current', get_current_data(), broadcast=True)
    emit('update-chart', get_current_data(), broadcast=True)

@socket.on('take-picture')
def handle_take_picture():
    print('Smile!')
    camera = RS_Camera()
    # Take RGB photo and run object detection on image 
    camera.take_picture()
    # get the new images and send them to the JS event script for 
    new_images = [
        url_for('static', filename=f'images/rgb/{return_most_recent_in_folder(rgb_image_folder)}'),
        url_for('static', filename=f'images/object_detection/{return_most_recent_in_folder(objdet_image_folder)}'),
        url_for('static', filename=f'images/hyperspectral/{return_most_recent_in_folder(hyperspectral_image_folder)}')
    ]
    emit('update-recent-images', new_images)


@app.route("/")
@app.route("/home")
def home():
    current_sensor_readings = get_current_data()

    return render_template('home.html', 
                           rgb_image=url_for('static', filename=f'images/rgb/{return_most_recent_in_folder(rgb_image_folder)}'), 
                           objdet_image=url_for('static', filename=f'images/object_detection/{return_most_recent_in_folder(objdet_image_folder)}'),
                           hyperspectral_image=url_for('static', filename=f'images/hyperspectral/{return_most_recent_in_folder(hyperspectral_image_folder)}'),
                           current = current_sensor_readings )

