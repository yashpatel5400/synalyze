"""
__authors__     = Yash, Will, Peter
__description__ = Views of pages
"""

from flask import render_template
from app import app, mic
from app.segment.analyze import synergy
from app.segment.get_speaker import get_speaker
from app.report.generate_page import generate_page

import os

recorder = None

@app.route('/record')
def record():
    global recorder
    
    recorder = mic.Mic()
    recorder.startrecording()
    return render_template('record.html')

@app.route('/')
def index():
    global recorder
    if recorder is not None:
        filename = recorder.stoprecording()
        # if child, perform analysis on the recording and store in segmentation
        # newpid = os.fork()
        # if newpid == 0:
        get_speaker(filename)        
        synergy.analyze(filename)
        
        report = generate_page(filename.split(".")[0])
        recorder = None
        return render_template(report)
    else:
        return render_template('index.html')
