"""
__authors__     = Yash, Will, Peter
__description__ = Views of pages
"""

from flask import render_template

import app.settings as s

from app import app, socketio
from app.segment.get_speaker import get_speaker
from app.analyze import synergy
from app.report.generate_page import generate_page

import os
import time

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/record/', methods=['GET', 'POST'])
def record():
    return render_template('record.html')

@app.route('/report/<filename>/')
def report(filename):
    """Route that performs the analytics on the filename 
    specified. Note that only the root of the filename (i.e.
    without extension) should be provided to the function, as
    that is what is later processed and used for naming

    Args:
    filename (str): root of the filename that is to be processed

    Returns: Rendered template of the analytics file
    """
    time.sleep(2) # gives time to complete writing file before analyzing
    get_speaker(filename)
    # synergy.analyze(dirname)
    # report = generate_page(dirname)
    return render_template('report.html')

@socketio.on('process')
def process(audio):
    with open("{}/{}.wav".format(s.OUTPUT_DIR, audio['filename']), 'wb') as f:
        f.write(audio['data'])