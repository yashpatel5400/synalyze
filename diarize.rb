=begin
File used for speech diarization that can be outputted to a format
that can be read directly into Python
=end

require 'diarize'
require 'json'

AUDIO_INPUT = "audio"
JSON_OUTPUT = "output"

def segment_audio(filename)
  base_dir = Dir.getwd
  base_output = filename.split(".")[0]
  audio = Diarize::Audio.new URI(
      "file:#{base_dir}/#{AUDIO_INPUT}/#{filename}")
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
    i += 1

    File.open("file:#{base_dir}/#{JSON_OUTPUT}/#{base_output}/#{i}.json",
              "w") do |f|
      f.write(segment_data.to_json)
    end
  end
  
  return segments_data
end

segment_audio(gets.chomp)
