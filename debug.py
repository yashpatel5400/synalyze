"""
__authors__     = Yash, Will, Peter
__description__ = App used to initialize/run the web backend. ONLY use this
for deployment version. Use run.py instead for Debug mode execution
"""

from app import app

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
