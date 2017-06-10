"""
__authors__     = Yash, Will, Peter
__description__ = App used to initialize/run the web backend --
runs on localhost by default
"""

from app import app

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
