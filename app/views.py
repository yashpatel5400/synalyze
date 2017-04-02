"""
__authors__     = Yash, Will, Peter
__description__ = Views of pages
"""

from flask import render_template
from app import app, mic
from app.segment.get_speaker import get_speaker

import os

recorder = None

@app.route('/record')
def record():
    global recorder
    
    recorder = mic.Mic()
    recorder.startrecording()
    return render_template('record.html')

@app.route('/stop')
def stop():
    global recorder
    filename = recorder.stoprecording()
    get_speaker(filename)
    
    # if child, perform analysis on the recording and store in segmentation
    newpid = os.fork()
    if newpid == 0:
        print("Analyzing...")
        get_speaker(filename)
        os._exit(0)
    else:
        # otherwise, simply return to serving the original page
        return index()

@app.route('/')
def index():
    return render_template('index.html')
