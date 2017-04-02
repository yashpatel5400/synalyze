import requests
import json
from watson_developer_cloud import ToneAnalyzerV3, SpeechToTextV1, \
									PersonalityInsightsV3, DiscoveryV1

API = {'S2T' : {'KEY':'6e38287f-f949-4389-a5bb-5fff4d30374e', 'PWD':'ZZfb1YQ8k7cl'}, 
		'TA' : {'KEY':'9453ac25-7842-46de-ab9b-3c117538fdc9', 'PWD':'vrmc1sNpyT4j'},
		'PI' : {'KEY':'87bb5354-faa2-4e7e-8a1e-fb171766ff9c', 'PWD':'pdveESHgqX8a'},
		'CS' : {'KEY':'599eec4e-297c-48cf-b538-7c287cb05ef0', 'PWD':'QXxgp6hpqRDJ'}
	}

def transcribe(audio_array):

	speech_to_text = SpeechToTextV1(
	    username = API['S2T']['KEY'],
	    password = API['S2T']['PWD'],
	    x_watson_learning_opt_out=False,
	)

	text_array = []

	for audio_file in audio_array:
	    transcript = speech_to_text.recognize(
	        audio_file, content_type='audio/flac', timestamps=True,
	        word_confidence=True, continuous=True)

	    results = transcript['results'][0]['alternatives']
	    transcript = results[0]['transcript']
	    text_array.append(str(transcript))

	return text_array

def analyze_tone(text_array):

	tone_analyzer = ToneAnalyzerV3(
	    username = API['TA']['KEY'],
	    password = API['TA']['PWD'],
	    version ='2016-05-19')

	tone_array = []

	for text in text_array:
		tone_array.append(json.dumps(tone_analyzer.tone(text=text)))

	return tone_array

def personalize(text_array):

	personality_insights = PersonalityInsightsV3(
	    version = '2016-10-20',
	    username = API['PI']['KEY'],
	    password = API['PI']['PWD'])

	personality_array = []

	for profile_text in text_array:
	    profile = personality_insights.profile(
	        profile_text, content_type='text/plain',
	        raw_scores=True, consumption_preferences=True)

	    personality_array.append(json.dumps(profile, indent=2))

	return personality_array

def cognitive_search(query_options):

	discovery = DiscoveryV1(
	  username = API['CS']['KEY'],
	  password = API['CS']['PWD'],
	  version='2016-12-01'
	)

	environments = discovery.get_environments()

	my_environments = [x for x in environments['environments'] if
	                     x['name'] == 'byod']
	my_environment_id = my_environments[0]['environment_id']

	collections = discovery.list_collections(my_environment_id)
	my_collections = [x for x in collections['collections']]

	configurations = discovery.list_configurations(
	    environment_id=my_environment_id)

	default_config_id = discovery.get_default_configuration_id(
	    environment_id=my_environment_id)

	default_config = discovery.get_configuration(
	    environment_id=my_environment_id, configuration_id=default_config_id)

	query_options = {}
	query_results = discovery.query(my_environment_id,
	                                my_collections[1]['collection_id'],
	                                query_options)
	
	return json.dumps(query_results, indent=2)

# ------------- Test Space ------------------
# a = open('./audio.flac', 'r')
f = open('./transcript.txt', 'r')
lines = f.readlines()
text = ''
for line in lines:
	text += line
# audio_array = [a]
# text_array = transcribe(audio_array)
# tone_array = analyze_tone(['several tornadoes touch down as a line of severe thunderstorms swept through Colorado on Sunday '])
personality_array = personalize([text])

