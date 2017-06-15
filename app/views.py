"""
__authors__     = Yash, Will, Peter
__description__ = Views of pages
"""

from flask import render_template

from app import app, socketio
from app.analyze import synergy
from app.segment.get_speaker import get_speaker
from app.report.generate_page import generate_page

import os

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/record/', methods=['GET', 'POST'])
def record():
    return render_template('record.html')

@app.route('/report/')
def report():
    # get_speaker(filename)
    # synergy.analyze(dirname)
    # report = generate_page(dirname)
    return render_template('report.html')

@socketio.on('process')
def process(audio):
    with open("audio.wav", 'wb') as f:
        f.write(audio['data'])