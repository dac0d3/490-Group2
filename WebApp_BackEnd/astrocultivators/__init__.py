from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cb8830318b22945dc6f811d2812ef6be' # for use with cookies
socket = SocketIO(app, cors_allowed_origins='*')
socket.init_app(app)

from astrocultivators import routes # placed at end of file to avoid import loops