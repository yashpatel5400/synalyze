"""
__authors__     = Yash, Will, Peter
__description__ = App used to initialize/run the web backend --
runs on localhost by default. Use for debugging (wsgi.py for prod)
"""

from app import app

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
