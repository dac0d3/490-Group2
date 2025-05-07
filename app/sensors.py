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


