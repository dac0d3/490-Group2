from flask import (Blueprint,
                   render_template,
                   redirect, url_for, session)

from flask import Flask, request, session, send_file
import random
import json
from time import time
from random import random
from flask import Flask, render_template, make_response

sensors = Blueprint('Sensor', __name__)

@sensors.route('/data', methods=["GET", "POST"])
def data():
    # Data Format
    # [TIME, Temperature, Humidity]

    temperature = random() * 100
    humidity = random() * 55

    sensor_data = [time() * 1000, temperature, humidity]

    response = make_response(json.dumps(sensor_data))

    response.content_type = 'application/json'

    return response
