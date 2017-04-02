"""
__authors__     = Yash, Will, Peter
__description__ = HackPrinceton 2017 file for doing speaker diarization
using external Ruby hook -- i.e. API of specifying input file and doing
processing w/ Ruby package for diarization with cleaned outputs
"""

import settings as s
import json

def get_speaker(filename):
    """
    description = given a filename (MUST be WAV file format) does segmentation
    to see how the split amongst the speakers looks like (returns
    an array of audio objects with corresponding metadata (i.e. speakers))
    """
    s.DIARIZER

if __name__ == "__main__":
    test_names = [""]
    for name in test_names:
        print(get_speaker("{}/{}".format(s.INPUT_DIR, name)))
