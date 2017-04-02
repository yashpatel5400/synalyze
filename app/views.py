"""
__authors__     = Yash, Will, Peter
__description__ = Views of pages
"""

from app import app

@app.route('/mic')
def mic():
    pass

@app.route('/')
def index():
    return("Hello, World!")
