"""
__authors__     = Yash, Will, Peter
__description__ = Views of pages
"""

from flask import render_template
from app import app

@app.route('/mic')
def mic():
    pass
 
@app.route('/')
def index():
    return render_template('index.html',
                           title='Home')
