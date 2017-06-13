"""
__authors__     = Yash, Will, Peter
__description__ = Default app directory initialization
"""

from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

from app import views, settings