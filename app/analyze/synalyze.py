"""
__authors__     = Yash, Will, Peter
__description__ = Uses IBM Watson API to do analysis on text/speech
for concept, tone, etc... extraction
__name__ = synalyze.py
"""

from . import settings as s

import requests
import json
import os
from watson_developer_cloud import ToneAnalyzerV3, SpeechToTextV1, \
    PersonalityInsightsV3, DiscoveryV1, NaturalLanguageUnderstandingV1
import watson_developer_cloud.natural_language_understanding.features.v1 as features

from docx import Document

API = {
    'S2T': {'KEY':'62a56f0f-7cef-498f-a5e6-ba83cc22bbf8', 'PWD':'SjlpcX70cY60'},
    'NLU': {'KEY': '71a9a1ea-09eb-4e15-b61e-5de9c761b060','PWD': 'gYLOmrZVQYYR'}
}

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
                audio_file, content_type='audio/wav', 
                timestamps=True, word_confidence=True, continuous=True)

            results = transcript['results'][0]['alternatives']
            text_array.append(str(results[0]['transcript']))
        except:
            text_array.append('')

    return text_array

def nlu(text_array):
    nlu_insights = NaturalLanguageUnderstandingV1(
        version = '2016-10-20',
        username = API['NLU']['KEY'],
        password = API['NLU']['PWD']) 

    extracting = [
        features.Concepts(),
        features.Categories(),
        features.Emotion(),
        features.Entities(),
        features.Keywords(),
        features.Sentiment()
    ]
    nlu_array = []
    for text in text_array:
        try:
            nlu_array.append(nlu_insights.analyze(extracting, text=text))
        except:
            nlu_array.append({}) # error in the request likely due to empty content
    return nlu_array

def update_segments(filename, text_array):
    input_dir = '{}/{}'.format(s.INPUT_DIR, filename)
    json_files = [f for f in os.listdir(input_dir) if f.split('.')[-1] == 'json']
    for json_id in range(len(json_files)):
        json_path = '{}/{}.json'.format(input_dir, json_id)
        segment = json.load(open(json_path, 'r'))
        segment.update({"text": text_array[json_id]})
        with open(json_path, 'w') as jf:
            jf.write(json.dumps(segment))

def analyze(filename):
    input_dir = '{}/{}'.format(s.INPUT_DIR, filename)
    audio_files = os.listdir(input_dir)
    audio_array = [open('{}/{}'.format(input_dir, audio_name), 'rb')
        for audio_name in audio_files if 'wav' in audio_name]
    
    print('Transcribing Audio...')
    text_array = transcribe(audio_array)
    print(text_array)
    update_segments(filename, text_array)

    print('Analyze Text...')
    results = nlu(text_array)
    
    print('Writing Results...')    
    with open('{}/{}.txt'.format(s.OUTPUT_DIR, filename), 'w') as f:
        f.write(json.dumps(results))
