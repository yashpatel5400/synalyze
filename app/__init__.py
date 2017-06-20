"""
__authors__     = Yash, Will, Peter
__description__ = Default app directory initialization
"""

from flask import Flask
from flask_socketio import SocketIO
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object("app.config")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

socketio = SocketIO(app)

from app import views, settings