"""
__authors__     = Yash, Will, Peter
__description__ = Uses IBM Watson API to do analysis on text/speech
for concept, tone, etc... extraction
"""

from . import settings as s

import requests
import json
import os
from watson_developer_cloud import ToneAnalyzerV3, SpeechToTextV1, \
        PersonalityInsightsV3, DiscoveryV1

from docx import Document

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
			response = tone_analyzer.tone(text=text)
			tone = response['document_tone']['tone_categories'][0]['tones']
			tone_array.append(tone)
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

def clear_documents():
	result = cognitive_search({'return':'id'})

	while result['matching_results']:
		result = cognitive_search({'return':'id'})
		print("Deleting Old Records")
		for doc_id in result['results']:
			doc_id = doc_id['id']
			delete_doc = discovery.delete_document('56eed52e-0538-4e43-92a8-a7223844e431', 'b5b60b1b-4e2b-4840-8bdc-da30a00f3e29', doc_id)

def write_to_discovery(text_array):
	env_id = '56eed52e-0538-4e43-92a8-a7223844e431'
	col_id = 'b5b60b1b-4e2b-4840-8bdc-da30a00f3e29'

	clear_documents()
	add_doc = None
	for i, text in enumerate(text_array):
		if text:
			document = Document()
			document.add_paragraph(text)
			fname = '{}/transcript'.format(s.TRANSCRIPT_DIR) + str(i) + '.docx'
			
			if os.path.isfile(fname):
				os.remove(fname)

			document.save(fname)
			with open(fname, 'rb') as outfile:	
				add_doc = discovery.add_document(env_id, col_id,
                                        file_info=outfile)
	if add_doc is None:
		return json.dumps("", indent=2)
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

def find_parties(filename):
	input_dir = "{}/{}".format(s.INPUT_DIR, filename)
	json_files = [f for f in os.listdir(input_dir) if f.split(".")[-1] == "json"]
	parties = [json.load(open("{}/{}".format(input_dir, json_name), 'rb'))
		for json_name in json_files]
	return parties

# ------------- Test Space ------------------

# a = open('./testmeeting/9.flac', 'r')

# t = open('./transcript.txt', 'r')
# lines = t.readlines()
# text = ''
# for line in lines:
# 	text += line

# text_array = transcribe(audio_array)
# print text_array

# tone_array = analyze_tone([text])
# tone_categories = tone_array[0]['document_tone']['tone_categories'][0]['tones'][0]

# print tone_categories

# personality_array = personalize([text])

# persona_categories = personality_array[0]['personality']

# print(json.dumps(personality_array[0], indent=2))

# write_to_discovery(text_array)
# print result

# r = find_parties()
# print json.dumps(r)
# p = find_parties()
# with open('parties.json', 'w') as party:
# 	party.write(json.dumps(p))

# ------------ Main --------------------------------
def analyze(filename):
        input_dir = "{}/{}".format(s.INPUT_DIR, filename)
        audio_files = os.listdir(input_dir)
        audio_array = [open("{}/{}".format(input_dir, audio_name), 'rb')
                for audio_name in audio_files]

        print("Transcribing Audio...")
        text_array = transcribe(audio_array)
        print(text_array)
        
        print(text_array)        
        print("Analysing Tone...")
        tone_array = analyze_tone(text_array)
        print(tone_array)
        
        print("Building Personas...")
        personality_array = personalize(text_array)
        print(personality_array)
        
        print("Writing to Discovery")
        write_to_discovery(text_array)

        print("Performing Cognitive Search")
        entities = cognitive_search({'aggregation':'term(enriched_text.entities.text%2Ccount%3A5)'})
        concepts = cognitive_search({'aggregation':'term(enriched_text.concepts.text%2Ccount%3A5)'})

        concepts = concepts['aggregations'][0]['results']
        entities = entities['aggregations'][0]['results']

        keys = []
        for entity in entities:
                keys.append(entity['key'])

        parties = find_parties(filename)
        print("Writing Results...")

        data = {}
        data['transcript'] = text_array
        data['tone'] = tone_array
        data['personality'] = personality_array
        data['keys'] = keys
        data['concepts'] = concepts
        data['parties'] = parties
        
        with open('{}/{}.txt'.format(s.OUTPUT_DIR, filename), 'w') as f:
                f.write(json.dumps(data))
