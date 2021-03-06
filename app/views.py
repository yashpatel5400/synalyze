"""
__authors__     = Yash, Will, Peter
__description__ = Flask routes of site pages
__name__        = views.py
"""

from flask import render_template, redirect, url_for, request, g, send_from_directory
from flask import session as flask_session
from flask_socketio import emit
from flask_login import login_user, logout_user, current_user
from werkzeug import secure_filename

import app.settings as s

from app import app, socketio, login_manager
from app.oauth import OAuthSignIn
from app.user import User
from app.segment.get_speaker import get_speaker
from app.analyze import synalyze
from app.report.generate_page import generate_page

import sqlite3
import json
import os
import time
import soundfile as sf

import plotly
import plotly.plotly as py
import plotly.graph_objs as go

# ======================= DB Helper Functions =========================== #

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(s.DB_NAME)
    return db

def get_recordings():
    c    = get_db()
    cur  = c.cursor()
    record_rows = cur.execute("""SELECT * FROM userreports 
        WHERE userid = (?)""", [current_user.userid]).fetchall()
    return [record[1] for record in record_rows]

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

def mp3_to_wav(fn):
    # converts the MP3 intermediary to the desired WAV to be analyzed
    wav_command = "mpg123 -w {}.wav {}.mp3".format(fn, fn)
    print("Converting to WAV...")
    os.system(wav_command)

# ========================== Login Routes =============================== #

@login_manager.user_loader
def load_user(userid):
    userrow = get_db().cursor().execute("""SELECT * FROM users 
        WHERE userid = (?)""", [userid]).fetchone()
    return User(
        userid=userrow[0],
        name  =userrow[1],
        email =userrow[2]
    )

@app.route('/')
def index():
    if current_user.is_anonymous:
        return render_template('index.html')
    return redirect(url_for('landing'))

@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/authorize/<provider>/')
def authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('landing'))
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

    flask_session["user_id"] = social_id
    c    = get_db()
    cur  = c.cursor()
    
    user_vals = cur.execute("""SELECT * FROM users 
        WHERE userid = (?)""", [social_id]).fetchone()

    if not user_vals:
        user = User(
            userid=social_id,
            name=username,
            email=email
        )
        cur.execute("""INSERT INTO users(userid, name, email) 
            VALUES(?,?,?)""",[user.userid, user.name, user.email])
        c.commit()
    else:
        user = User(
            userid=user_vals[0],
            name  =user_vals[1],
            email =user_vals[2]
        )

    login_user(user, True)
    return redirect(url_for('landing'))

# ========================== Analytics Routes =============================== #

@app.route('/landing/')
def landing():
    if current_user.is_anonymous:
        return redirect(url_for('index'))
    return render_template('landing.html', recordings=get_recordings())

@app.route('/record/', methods=['GET', 'POST'])
def record():
    if current_user.is_anonymous:
        return redirect(url_for('index'))
    return render_template('record.html')

@app.route('/report/<recordid>/')
def report(recordid):
    if current_user.is_anonymous:
        return redirect(url_for('index'))
    jsonrecord = '{}/{}.json'.format(s.REPORT_DIR, recordid)
    with open(jsonrecord, 'r') as fp:
        data = json.load(fp)

    trace = go.Pie(
        labels=data["overall_speaker"], 
        values=data["overall_durations"],
        hoverinfo='label+percent', textinfo='value', 
        textfont=dict(size=20),
        marker=dict(
            line=dict(
            color='#000000', 
            width=2))
    )
    layout = go.Layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )

    fig = go.Figure(data=[trace], layout=layout)
    # url = py.plot(fig, auto_open=False)
    div = plotly.offline.plot({
        "data": [trace], 
        "layout": layout
    }, include_plotlyjs=False, output_type='div')
    return render_template('report.html', data=data, 
        div=div,
        recordings=get_recordings(),
        recordid=recordid)

@app.route('/report/<recordid>/wav/')
def audio_cache(recordid):
    if current_user.is_anonymous:
        return redirect(url_for('index'))
    return open("{}/{}.wav".format(s.OUTPUT_DIR, 
        recordid), 'rb').read()

@app.route('/analyze/<recordid>/')
def analyze(recordid):
    """Route that performs the analytics on the filename 
    specified. Note that only the root of the filename (i.e.
    without extension) should be provided to the function, as
    that is what is later processed and used for naming

    Args:
    recordid (str): root of the filename that is to be processed

    Returns: Rendered template of the analytics file
    """
    if current_user.is_anonymous:
        return redirect(url_for('index'))
    c    = get_db()
    cur  = c.cursor()

    cur_records = cur.execute("""SELECT * FROM userreports 
        WHERE userid = (?)
        AND reportid = (?)""", 
        [current_user.userid, recordid]).fetchall()

    # if we are not being asked to analyze a file with the identical name
    if len(cur_records) == 0:
        cur.execute("""INSERT INTO userreports(userid, reportid) 
            VALUES(?,?)""",[current_user.userid, recordid])
        c.commit()

    # waits for the file to be asynchronously written to disk before
    # performing any analytics
    get_speaker(recordid)
    synalyze.analyze(recordid)
    generate_page(recordid)
    return redirect(url_for('report', recordid=recordid))

# Route that will process the file upload
@app.route('/landing/upload', methods=['POST'])
def upload():
    f = request.files['file']
    if f and allowed_file(f.filename):
        filename = secure_filename(f.filename)
        recordid = filename.split(".")[0]
        fn = "{}/{}".format(s.OUTPUT_DIR, recordid)
        f.save(os.path.join(s.OUTPUT_DIR, filename))
        mp3_to_wav(fn)
        return redirect(url_for('analyze', recordid=recordid))
    return redirect('landing')

@app.route('/favicon.ico')
def favicon():
    return redirect(url_for('static', filename='favicon.ico'))

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
    print("Converting to MP3...")
    os.system(mp3_command)

    mp3_to_wav(fn)
    emit('completedwrite')