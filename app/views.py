"""
__authors__     = Yash, Will, Peter
__description__ = Views of pages
"""

from flask import render_template
from app import app, mic

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
    return index()

@app.route('/')
def index():
    return render_template('index.html')
