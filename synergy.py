import requests
import json
from watson_developer_cloud import ToneAnalyzerV3, SpeechToTextV1, PersonalityInsightsV3, DiscoveryV1

API = {'S2T' : {'KEY':'6e38287f-f949-4389-a5bb-5fff4d30374e', 'PWD':'ZZfb1YQ8k7cl'}, 
		'TA' : {'KEY':'9453ac25-7842-46de-ab9b-3c117538fdc9', 'PWD':'vrmc1sNpyT4j'},
		'PI' : {'KEY':'87bb5354-faa2-4e7e-8a1e-fb171766ff9c', 'PWD':'pdveESHgqX8a'},
		'CS' : {'KEY':'599eec4e-297c-48cf-b538-7c287cb05ef0', 'PWD':'QXxgp6hpqRDJ'}
	}

# speech_to_text = SpeechToTextV1(
#     username = API['S2T']['KEY'],
#     password = API['S2T']['PWD'],
#     x_watson_learning_opt_out=False,
# )

# with open('./audio.flac', 'rb') as audio_file:
#     transcript = speech_to_text.recognize(
#         audio_file, content_type='audio/flac', timestamps=True,
#         word_confidence=True, continuous=True)
#     transcript = transcript['results'][0]['alternatives'][0]['transcript']
#     print transcript

# tone_analyzer = ToneAnalyzerV3(
#     username = API['TA']['KEY'],
#     password = API['TA']['PWD'],
#     version ='2016-05-19')

# with open('./transcript.txt') as tone_text:
# 	print(json.dumps(tone_analyzer.tone(text=transcript), indent=2))

# personality_insights = PersonalityInsightsV3(
#     version = '2016-10-20',
#     username = API['PI']['KEY'],
#     password = API['PI']['PWD'])

# with open('./transcript.txt') as profile_text:
#     profile = personality_insights.profile(
#         profile_text.read(), content_type='text/plain',
#         raw_scores=True, consumption_preferences=True)

#     print(json.dumps(profile, indent=2))

discovery = DiscoveryV1(
  username = API['CS']['KEY'],
  password = API['CS']['PWD'],
  version='2016-12-01'
)

environments = discovery.get_environments()
# print(json.dumps(environments, indent=2))

news_environments = [x for x in environments['environments'] if
                     x['name'] == 'byod']
news_environment_id = news_environments[0]['environment_id']
# print(json.dumps(news_environment_id, indent=2))

collections = discovery.list_collections(news_environment_id)
news_collections = [x for x in collections['collections']]
# print(json.dumps(collections, indent=2))

configurations = discovery.list_configurations(
    environment_id=news_environment_id)
# print(json.dumps(configurations, indent=2))

default_config_id = discovery.get_default_configuration_id(
    environment_id=news_environment_id)
# print(json.dumps(default_config_id, indent=2))

default_config = discovery.get_configuration(
    environment_id=news_environment_id, configuration_id=default_config_id)
# print(json.dumps(default_config, indent=2))

query_options = {}
query_results = discovery.query(news_environment_id,
                                news_collections[1]['collection_id'],
                                query_options)
print(json.dumps(query_results, indent=2))

# with open(os.path.join(os.getcwd(),'..','resources','simple.html')) as fileinfo:
#     res = discovery.add_document(environment_id=writable_environment_id,
#                                 collection_id=collections['collections'][0]['collection_id'],
#                                 fileinfo=fileinfo)
#    print(res)
