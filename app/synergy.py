import requests
import json
from watson_developer_cloud import ToneAnalyzerV3, SpeechToTextV1, \
									PersonalityInsightsV3, DiscoveryV1
import os

API = {'S2T' : {'KEY':'6e38287f-f949-4389-a5bb-5fff4d30374e', 'PWD':'ZZfb1YQ8k7cl'}, 
		'TA' : {'KEY':'9453ac25-7842-46de-ab9b-3c117538fdc9', 'PWD':'vrmc1sNpyT4j'},
		'PI' : {'KEY':'87bb5354-faa2-4e7e-8a1e-fb171766ff9c', 'PWD':'pdveESHgqX8a'},
		'CS' : {'KEY':'599eec4e-297c-48cf-b538-7c287cb05ef0', 'PWD':'QXxgp6hpqRDJ'}
	}

discovery = DiscoveryV1(
	  username = API['CS']['KEY'],
	  password = API['CS']['PWD'],
	  version='2016-12-01'
	)

def transcribe(audio_array):

	speech_to_text = SpeechToTextV1(
	    username = API['S2T']['KEY'],
	    password = API['S2T']['PWD'],
	    x_watson_learning_opt_out=False,
	)

	text_array = []

	for audio_file in audio_array:
		try:
		    transcript = speech_to_text.recognize(
		        audio_file, content_type='audio/wav', timestamps=True,
		        word_confidence=True, continuous=True)

		    results = transcript['results'][0]['alternatives']
		    transcript = results[0]['transcript']
		    text_array.append(str(transcript))
		except:
			text_array.append('')

	return text_array

def analyze_tone(text_array):

	tone_analyzer = ToneAnalyzerV3(
	    username = API['TA']['KEY'],
	    password = API['TA']['PWD'],
	    version ='2016-05-19')

	tone_array = []

	for text in text_array:
		try:
			tone_array.append(tone_analyzer.tone(text=text))
		except:
			tone_array.append('')

	return tone_array

def personalize(text_array):

	personality_insights = PersonalityInsightsV3(
	    version = '2016-10-20',
	    username = API['PI']['KEY'],
	    password = API['PI']['PWD'])

	personality_array = []

	for profile_text in text_array:
		try:
		    profile = personality_insights.profile(
		        profile_text, content_type='text/plain',
		        raw_scores=True, consumption_preferences=True)

		    personality_array.append(profile)
		except:
			personality_array.append('')

	return personality_array

def write_to_discovery(text_array):
	env_id = '56eed52e-0538-4e43-92a8-a7223844e431'
	col_id = 'b5b60b1b-4e2b-4840-8bdc-da30a00f3e29'

	for i, text in enumerate(text_array):
		data = {}
		data['transcript'] = text
		fname = 'transcript' + str(i) + '.json'
		
		if os.path.isfile(fname):
			os.remove(fname)

		with open(fname, 'a+') as outfile:
			json.dump(data, outfile)
		
		with open(fname, 'r') as outfile:	
			add_doc = discovery.add_document(env_id, col_id, file_info=outfile)
	
	return json.dumps(add_doc, indent=2)

def cognitive_search(query_options):

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

	query_results = discovery.query(my_environment_id,
	                                my_collections[0]['collection_id'],
	                                query_options)
	
	return query_results

# ------------- Test Space ------------------

# a = open('./testmeeting/9.flac', 'r')

# t = open('./transcript.txt', 'r')
# lines = t.readlines()
# text = ''
# for line in lines:
# 	text += line

# audio_array = [a]

# text_array = transcribe(audio_array)
# print text_array

# tone_array = analyze_tone([text])
# tone_categories = tone_array[0]['document_tone']['tone_categories'][0]['tones'][0]

# print tone_categories

# personality_array = personalize([text])

# persona_categories = personality_array[0]['personality']

# print(json.dumps(personality_array[0], indent=2))
# write_to_discovery([text])
# result = cognitive_search({'return':'enrichedTitle.entities'})
# print result

# for doc_id in result['results']:
# 	doc_id = doc_id['id']
# 	delete_doc = discovery.delete_document('56eed52e-0538-4e43-92a8-a7223844e431', 'b5b60b1b-4e2b-4840-8bdc-da30a00f3e29', doc_id)
# ------------ Main Script ------------------

def analyze():
        audio_array = []
        i = 1

        while True:
	        audio_filename = './testmeeting/' + str(i) + '.wav'
	        try:
		        a = open(audio_filename, 'r')
		        audio_array.append(a)
		        i += 1
	        except:
		        break

        print("Transcribing Audio...")
        text_array = transcribe(audio_array)

        print("Analysing Tone...")
        tone_array = analyze_tone(text_array)

        print("Building Personas...")
        personality_array = personalize(text_array)

        print("Writing Results...")
        with open('results.txt', 'w') as f:
	        f.write('Transcription Result:\n\n')
	        for text in text_array:
		        f.write(text)
                        
	        f.write('\n\nTone Analysis:\n\n')	
	        for tone in tone_array:
		        if tone:
			        f.write(str(tone))

	        f.write('\n\nPersonality Result:\n\n')
	        for persona in personality_array:
		        f.write(persona)
