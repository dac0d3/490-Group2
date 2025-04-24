from flask import Blueprint, Response
from .camera import PredictCamera

import random
import json
from time import time
from random import random
from flask import Flask, render_template, make_response

views = Blueprint('views', __name__)


prediction_stream = PredictCamera()

@views.route('/', methods=['GET','POST'])
def home():
    return render_template('index.html', boxes = data_feed())

def gen(camera):
    while True:
        result = camera.get_frame()
        frame = result
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


# @views.route('/video_feed')
# def video_feed():
#      return Response(gen(video_stream),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')

@views.route("/prediction_feed")
def predict_feed():
    return Response(gen(prediction_stream),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@views.route("/data_feed")
def data_feed():
    return prediction_stream.get_data()


@views.route('/data', methods=["GET", "POST"])
def data():
    # Data Format
    # [TIME, Temperature, Humidity]

    temperature = random() * 100
    humidity = random() * 55

    sensor_data = [time() * 1000, temperature, humidity]

    response = make_response(json.dumps(sensor_data))

    response.content_type = 'application/json'

    return response