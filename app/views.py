"""
__authors__     = Yash, Will, Peter
__description__ = Views of pages
"""

from flask import render_template
from flask_uwsgi_websocket import GeventWebSocket

import numpy as np

from app import app, mic
from app.analyze import synergy
from app.segment.get_speaker import get_speaker
from app.report.generate_page import generate_page

import os

ws = GeventWebSocket(app)

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
    else:
        return render_template('index.html')

@ws.route('/websocket')
def audio(ws):
    while True:
       msg = ws.receive()
       if len(msg) != 0:
          audio_as_int_array = np.frombuffer(msg, 'i2')
          print(audio_as_int_array)
       else:
          break