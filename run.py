"""
__authors__     = Yash, Will, Peter
__description__ = App used to initialize/run the web backend --
runs on localhost by default
"""

#!flask/bin/python
from app import app
app.run(debug=True)
