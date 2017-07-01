"""
__authors__	 = Yash, Will, Peter
__description__ = Speaker diarization and audio segmentation
using external Ruby hook -- i.e. API of specifying input file and doing
processing w/ Ruby package for diarization with cleaned outputs
__name__ = get_speaker.py
"""

from app.segment import settings as s

from pydub import AudioSegment
import json
import os

def split_audio(filename):
	"""
	given a filename, inspects the corresponding outputted JSON files from
	the diarization analysis (MUST be called after diarization) and splits
	audio according to the times specified in JSONs
	"""
	input_audio = "{}/{}.wav".format(s.INPUT_DIR, filename)
	sound = AudioSegment.from_wav(input_audio) 
	json_folder = "{}/{}".format(s.OUTPUT_DIR, filename)
	json_files  = [fn for fn in os.listdir(json_folder) if "json" in fn]

	for json_file in json_files:
		json_i = json_file.split(".")[0]
		cur_json_file = "{}/{}".format(json_folder, json_file)
		output_file   = "{}/{}.wav".format(json_folder, json_i)
		print(cur_json_file)
		data = json.load(open(cur_json_file, "r"))

		start_milli = int(data["start_time"] * 1000)
		end_milli   = int(start_milli + data["duration"] * 1000)
		sound[start_milli:end_milli].export(output_file, format="wav")
		
def get_speaker(filename):
	# sets up for output used for diarizer
	print("Setting {} directories".format(filename))
	out_dir   = "{}/{}".format(s.OUTPUT_DIR, filename)
	if not os.path.exists(out_dir):
		os.mkdir(out_dir)
	
	# complete diarizataion of the input audio -- run through external
	# Ruby script and dumps result analyses into output/ JSON files
	print("Diarizing {}".format(filename))
	os.system('jruby ./{} {}'.format(s.DIARIZER, filename))

	# extracts the audio clips that correspond to the metadata identified
	# in Ruby script
	print("Splitting audio {}".format(filename))
	split_audio(filename)
	
if __name__ == "__main__":
	test_names = ["meeting.mp3"]
	for name in test_names:
		print("Processing {}".format(name))
		get_speaker(name)
		print("Completed {}".format(name))
