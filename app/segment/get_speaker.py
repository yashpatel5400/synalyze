"""
__authors__     = Yash, Will, Peter
__description__ = HackPrinceton 2017 file for doing speaker diarization
using external Ruby hook -- i.e. API of specifying input file and doing
processing w/ Ruby package for diarization with cleaned outputs
"""

from . import settings as s

from pydub import AudioSegment
import json
import os

def split_audio(filename):
    """
    given a filename, inspects the corresponding outputted JSON files from
    the diarization analysis (MUST be called after diarization) and splits
    audio according to the times specified in JSONs
    """
    base_name = filename.split(".")[0]
    input_audio = "{}/{}".format(s.INPUT_DIR, filename)

    sound = AudioSegment.from_wav(input_audio) 
    json_folder = "{}/{}".format(s.OUTPUT_DIR, base_name)
    json_files  = os.listdir(json_folder)

    for json_file in json_files:
        json_i = json_file.split(".")[0]
        cur_json_file = "{}/{}".format(json_folder, json_file)
        output_file   = "{}/{}.wav".format(json_folder, json_i)
        data = json.load(open(cur_json_file, "r"))
        
        start_milli = int(data["start_time"] * 1000)
        end_milli   = int(start_milli + data["duration"] * 1000)
        sound[start_milli:end_milli].export(output_file, format="wav")
        
def get_speaker(filename):
    # sets up for output used for diarizer
    print("Setting {} directories".format(filename))
    base_name = filename.split(".")[0]
    out_dir   = "{}/{}".format(s.OUTPUT_DIR, base_name)
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    
    # complete diarizataion of the input audio -- run through external
    # Ruby script and dumps result analyses into output/ JSON files
    print("Diarizing {}".format(filename))
    os.system('echo "{}" | jruby ./{}'.format(filename, s.DIARIZER))
    
    # extracts the audio clips that correspond to the metadata identified
    # in Ruby script
    print("Splitting audio {}".format(filename))
    split_audio(filename)
    
if __name__ == "__main__":
    test_names = ["testmeeting.wav"]
    for name in test_names:
        print("Processing {}".format(name))
        get_speaker(name)
        print("Completed {}".format(name))
