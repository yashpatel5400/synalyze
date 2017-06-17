=begin
File used for speech diarization that can be outputted to a format
that can be read directly into Python
=end

require 'diarize'
require 'json'

AUDIO_INPUT = "app/segment/audio"
JSON_OUTPUT = "app/segment/output"

def segment_audio(filename)
	base_dir = Dir.getwd
	base_output = filename.split(".")[0]
	uri = URI.join('file:///', File.join(File.expand_path(File.dirname(__FILE__)), 
		"audio/#{filename}.wav"))
	print(uri)
	audio = Diarize::Audio.new(uri)
	audio.analyze!
	segments = audio.segments

	i = 0
	segments_data = {}

	for segment in segments do
		segment_data = {}
		speaker = segment.speaker
		segment_data["speaker_id"] = speaker.uri.to_s.split("#")[-1]
		segment_data["start_time"] = segment.start
		segment_data["duration"]   = segment.duration

		segments_data[i] = segment_data

		File.open(File.join(File.expand_path(File.dirname(__FILE__)), 
			"output/#{filename}/#{i}.json"), "w") do |f|
			f.write(segment_data.to_json)
		end

		i += 1
	end
	
	return segments_data
end

segment_audio(ARGV[0])
