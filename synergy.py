import requests
import json
from watson_developer_cloud import ToneAnalyzerV3, SpeechToTextV1, \
									PersonalityInsightsV3, DiscoveryV1
import os
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
		if text:
			document = Document()
			document.add_paragraph(text)
			fname = 'transcript' + str(i) + '.docx'
			
			if os.path.isfile(fname):
				os.remove(fname)

			document.save(fname)
			# with open(fname, 'a+') as outfile:
			# 	json.dump(data, outfile)
			
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

# text_array = transcribe(audio_array)
# print text_array

# tone_array = analyze_tone([text])
# tone_categories = tone_array[0]['document_tone']['tone_categories'][0]['tones'][0]

# print tone_categories

# personality_array = personalize([text])

# persona_categories = personality_array[0]['personality']

# print(json.dumps(personality_array[0], indent=2))
text_array = ['', '', '', "like I'm Peter Morgan finance manager with a team of five reporting to me ", "but I'm glad we have me unfriendly fat head IT that have lost ", "hi Judy I might Raynaud's I we spoke on the phone last week I'm in charge of production through our sky fifty ", 'absolutely Adam figures are up on the previous quarter by two percent on products streams have one time to have down by north point five percent on port ', 'three ', "black and yellow safety take the top and bottom of the stairs to warn people is a visual sign now unfortunately you ever put the take down didn't do a particularly good job they have to live somebody trick though that the safe schools themselves an injury so we need to be aware that sort of thing ", "outside system went out just about to approach the implementation phase so I'd appreciate your input on two options that roadmap actually and how to best wrote out the training program on site ", 'we need to consider the impact on shifts performing for nine ', "that's not be too hasty in his hips right first time by facing we can sell its success the departments as we ", "we've sort of that we got it dummy testing systems which is coming next week so we can actually stop to that train within our individual teams for actually next Wednesday ", "I think it's an excellent opportunity to get some system champions ", 'please make sure that called it into training the system ', 'I am in my team that I had a good idea what it will allow people ', "okay what's other ideas without ", 'we could put a stop to it all together noni allow people access to already treatment system ', 'yeah if if all we do is take away from them W. Russians ', "welcome to our department meeting a nice to see old memories now we have a new team member and we should think jury Chama Nietzsche so I'd like to start with some introductions ", 'that is a significant amount ', 'okay mine job datus on the production figures philosophy courses please ', 'moving on to the next ', "phased rollout so we can check for full it's what's keeping the level of service high actually I disagree ", 'season ', '', "I'm ", 'absolutely out basically the full figures are in the HL report on the internet ', 'yeah I know I have successfully complete deprivation led just one woman she runs she left off to three weeks a husband ', 'and interestingly as successful recruits came from the radio ads rather than traditional advertising ', 'so therefore I would suggest that we review our toys ', "that's all very well but we need to keep people motivated and some people use the internet for work ", "you're about to see a meeting taking place at ABC manufacturing ", 'take a moment now to gather pens and paper and position yourself to take the role of minutes teca ', 'yeah I think for a culture change do a swift implementation of just both people expect that that the longer the week alley that the more resistance ', "for the training I really don't want to risk ", "no no we don't have the results ", 'I mean from the pilot we can develop ', "I just think we need to make sure people are motivated knife is too harsh a penalty that that people are just gonna maybe Missy's assisted me home "]
write_to_discovery(text_array)
# result = cognitive_search({'return':'enrichedTitle.entities'})
# print result

# for doc_id in result['results']:
# 	doc_id = doc_id['id']
# 	delete_doc = discovery.delete_document('56eed52e-0538-4e43-92a8-a7223844e431', 'b5b60b1b-4e2b-4840-8bdc-da30a00f3e29', doc_id)

# ------------ Main Script ------------------

# audio_array = []
# i = 1

# while True:
# 	audio_filename = './testmeeting/' + str(i) + '.wav'
# 	try:
# 		a = open(audio_filename, 'r')
# 		audio_array.append(a)
# 		i += 1
# 	except:
# 		break

# print "Transcribing Audio..."
# text_array = transcribe(audio_array)
# print text_array

# print "Analysing Tone..."
# tone_array = analyze_tone(text_array)

# print "Building Personas..."
# personality_array = personalize(text_array)

# print "Writing Results..."
# with open('results.txt', 'w') as f:
# 	f.write('Transcription Result:\n\n')
# 	for text in text_array:
# 		f.write(text)
# 	f.write('\n\nTone Analysis:\n\n')
	
# 	for tone in tone_array:
# 		if tone:
# 			f.write(str(tone))

# 	f.write('\n\nPersonality Result:\n\n')
	
# 	for persona in personality_array:
# 		f.write(persona)


