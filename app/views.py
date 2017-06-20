"""
__authors__     = Yash, Will, Peter
__description__ = Flask routes of site pages
__name__        = views.py
"""

from flask import render_template, request
from flask_socketio import emit
from flask_login import LoginManager, UserMixin, login_user, logout_user,\
    current_user
from oauth import OAuthSignIn

import app.settings as s

from app import app, socketio
from app.segment.get_speaker import get_speaker
from app.analyze import synalyze
from app.report.generate_page import generate_page

import os
import time
import soundfile as sf

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/authorize/<provider>/')
def authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()

@app.route('/callback/<provider>/')
def callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email = oauth.callback()
    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('index'))
    user = User.query.filter_by(social_id=social_id).first()
    if not user:
        user = User(social_id=social_id, nickname=username, email=email)
        db.session.add(user)
        db.session.commit()
    login_user(user, True)
    return redirect(url_for('index'))

@app.route('/landing/')
def landing():
    return render_template('landing.html')

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
    # waits for the file to be asynchronously written to disk before
    # performing any analytics
    get_speaker(filename)
    synalyze.analyze(filename)
    data = generate_page(filename)
    return render_template("report.html", data=data)

@socketio.on('process')
def process(audio):
    # EXTREMELY JANK implementation: clean up if possible
    # write raw audio binary stream to disk
    print("Reading raw audio stream...")
    fn = "{}/{}".format(s.OUTPUT_DIR, audio['filename'])
    with open("{}.raw".format(fn), 'wb') as f:
        f.write(audio['data'])

    # converts RAW file to intermediary MP3 since could not directly convert
    mp3_command = "ffmpeg -i {}.raw -acodec libmp3lame {}.mp3".format(fn, fn) 

    # converts the MP3 intermediary to the desired WAV to be analyzed
    wav_command = "mpg123 -w {}.wav {}.mp3".format(fn, fn)

    print("Converting to MP3...")
    os.system(mp3_command)

    print("Converting to WAV...")
    os.system(wav_command)
    emit('completedwrite')