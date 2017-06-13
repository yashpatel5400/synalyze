"""
__authors__     = Yash, Will, Peter
__description__ = Views of pages
"""

from flask import render_template
from flask_socketio import emit

import numpy as np

from app import app, socketio
from app.analyze import synergy
from app.segment.get_speaker import get_speaker
from app.report.generate_page import generate_page

import os

@app.route('/')
def index():
    recorder = None
    if recorder is not None:
        filename = recorder.stoprecording()
        get_speaker(filename)

        dirname = filename.split(".")[0]
        synergy.analyze(dirname)
        report = generate_page(dirname)
        recorder = None
        return render_template(report)
    return render_template('index.html')

@socketio.on('test', namespace='/test')
def test_message(message):
    print(message['data'])