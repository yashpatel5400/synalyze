"""
__authors__     = Yash, Will, Peter
__description__ = Views of pages
"""

from flask import render_template
from flask_uwsgi_websocket import GeventWebSocket

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
    first_message = True
    total_msg = ""
    sample_rate = 0

    while True:
       msg = ws.receive()

       if first_message and msg is not None: # the first message should be the sample rate
          sample_rate = getSampleRate(msg)
          first_message = False
          continue
       elif msg is not None:
          audio_as_int_array = numpy.frombuffer(msg, 'i2')
          doSomething(audio_as_int_array)
       else:
          break