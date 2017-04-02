"""
__authors__     = Yash, Will, Peter
__description__ = Default app directory initialization
"""

from flask import Flask

app = Flask(__name__)
from app import views
