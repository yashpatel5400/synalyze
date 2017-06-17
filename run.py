"""
__authors__     = Yash, Will, Peter
__description__ = App used to initialize/run the web backend --
runs on localhost by default. Use for deployment
__name__ = run.py
"""

from app import app, socketio

if __name__ == "__main__":
	socketio.run(app)
