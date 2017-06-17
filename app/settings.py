"""
__authors__     = Yash, Will, Peter
__description__ = Global variables for the Python files (largely for
doing organization) for app interface
__name__ = settings.py
"""

import pyaudio

# ------------------------------  outputs -----------------------------
OUTPUT_DIR = "app/segment/audio"

# --------------------  recording settings -----------------------------
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100

NAME_LENGTH = 8
