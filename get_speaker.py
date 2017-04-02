"""
__authors__     = Yash, Will, Peter
__description__ = HackPrinceton 2017 file for doing speaker diarization
using external Ruby hook -- i.e. API of specifying input file and doing
processing w/ Ruby package for diarization with cleaned outputs
"""

from pydub import AudioSegment
import settings as s
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
    for i, json_file in enumerate(json_files):
        cur_json_file = "{}/{}".format(json_folder, json_file)
        output_file   = "{}/{}.wav".format(json_folder, i)
        with open(cur_json_file) as df:
            data = json.load(df)

        start_milli = data["start_time"] * 1000
        end_milli   = data["end_time"] * 1000
        data[start_milli:end_milli].export(output_file, format="wav")
        
def main(filename):
    # sets up for output used for diarizer
    base_name = filename.split(".")[0]
    os.mkdir("{}/{}".format(s.OUTPUT_DIR, base_name))
    
    # complete diarizataion of the input audio -- run through external
    # Ruby script and dumps result analyses into output/ JSON files
    os.system('echo \"{}\" | jruby ./{}'.format(s.DIARIZER, filename))
    
    # extracts the audio clips that correspond to the metadata identified
    # in Ruby script
    split_audio(filename)
    
if __name__ == "__main__":
    test_names = ["test1.wav", "test2.wav", "test3.wav"]
    for name in test_names:
        print(get_speaker(name))
