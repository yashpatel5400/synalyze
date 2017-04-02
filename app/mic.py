"""
__authors__     = Yash, Will, Peter
__description__ = Python microphone interface (i.e for recording the business
meetings after interacting with the web page)
"""

from app import settings as s

import pyaudio
import wave
import threading
import time
import random

class Mic:
    def __init__(self):
        self.isrecording = False
        self.starttime   = None
        self.stoptime    = None
        self.filename    = "{}.wav".format(''.join([random.choice(
            'abcdefghijklmnopqrstuvwxyz') for _ in range(s.NAME_LENGTH)]))

        self.p = pyaudio.PyAudio()
        
    def startrecording(self):
        self.isrecording = True
        self.starttime   = time.time()
        self.stream = self.p.open(format=s.FORMAT,
                             channels=s.CHANNELS,
                             rate=s.RATE,
                             input=True,
                             frames_per_buffer=s.CHUNK)
        t = threading.Thread(target=self._record)
        t.start()

    def stoprecording(self):
        self.isrecording = False
        self.stoptime    = time.time()
        record_seconds   = self.stoptime - self.starttime

        frames = []
        for i in range(int(s.RATE / s.CHUNK * record_seconds)):
            data = self.stream.read(s.CHUNK)
            frames.append(data)
            print("* done recording")

        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
            
        wf = wave.open("{}/{}".format(s.OUTPUT_DIR, self.filename), 'wb')
        wf.setnchannels(s.CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(s.FORMAT))
        wf.setframerate(s.RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        return self.filename
        
    def _record(self):
        pass
