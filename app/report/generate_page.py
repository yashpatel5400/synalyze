"""
__authors__     = Yash, Will, Peter
__description__ = Generates report HTML pages given analysis performed using
the Watson API
"""

from . import settings as s

import pystache
import json
import os

import time
import datetime

def find_segments(filename):
    input_dir = '{}/{}'.format(s.SEGMENTED_DIR, filename)
    json_files = [f for f in os.listdir(input_dir) if f.split('.')[-1] == 'json']
    segments = [json.load(open('{}/{}'.format(input_dir, json_name), 'rb'))
        for json_name in json_files]
    return segments

def generate_page(filename):
    """ 
    Returns data with the following fields:

        title: HTML page title
        topic: Meeting topic (used for header)
        date_str: Date when meeting occurred (assumed to be recording date)
        dur_str: Duration of the meeting
        ideas: Ideas extracted from discussion
        series1_str: String representing 1st flow of emotions in meeting
        series2_str: String representing 2nd flow of emotions in meeting
        series3_str: String representing 3rd flow of emotions in meeting
        speakers: List of speakers in meeting (arbitrary IDs)
        durations: Durations each of the speakers talked for (same order as speakers)
        start_times: Start times correspond to each time a person talks
        text: What the person said (i.e. personal breakdwon of transcript)
    """

    # ======================== NLU Analytics ============================= #
    print("Generating output...")
    resultsfile  = "{}/{}.txt".format(s.ANALYZE_DIR, filename)
    with open(resultsfile, 'r') as f:
        analyzed = json.load(f)

    munged_tones = []
    for analysis in analyzed:
        temp = [0, 0, 0]
        if analysis != {}: # account for empty response case
            tone_scores = analysis["emotion"]["document"]["emotion"]
            
            temp[0] += tone_scores["disgust"]
            temp[0] += tone_scores["anger"]
            temp[1] += tone_scores["sadness"]
            temp[1] += tone_scores["fear"]
            temp[2] += tone_scores["joy"]
            
            # normalize the scores for graphing
            temp[0] /= 2
            temp[1] /= 2
            munged_tones.append(temp)
    series1 = ", ".join(['{x: ' + str(ind) + ', y: ' + str(data[0]) + '}'
                         for ind, data in enumerate(munged_tones)])
    series2 = ", ".join(['{x: ' + str(ind) + ', y: ' + str(data[1]) + '}'
                         for ind, data in enumerate(munged_tones)])
    series3 = ", ".join(['{x: ' + str(ind) + ', y: ' + str(data[2]) + '}'
                         for ind, data in enumerate(munged_tones)])
    flatten = lambda l: [item for sublist in l for item in sublist]
    concepts = flatten([analysis["concepts"] for analysis in analyzed])
    
    # ====================== Metadata Analytics =========================== #
    segments = find_segments(filename)
    comb = {}
    total_dur = 0
    for segment in segments:
        val = comb.get(segment["speaker_id"], 0.0) + segment["duration"]
        total_dur += segment["duration"]
        comb[segment["speaker_id"]] = val

    for speaker in comb:
        comb[speaker] = comb[speaker]/total_dur 

    speakers    = [segment["speaker_id"] for segment in segments]
    start_times = [segment["start_time"] for segment in segments]
    texts       = [segment["text"] for segment in segments]
    durations   = [segment["duration"] for segment in segments]

    # ========================= Produce Report ============================ #
    data = {
        'title': 'Meeting Report',
        'topic': 'The Topic of the Meeting',
        'date_str': datetime.datetime.today().strftime('%Y-%m-%d'),
        'dur_str':  time.strftime("%H:%M:%S", time.gmtime(total_dur)),
        'ideas': concepts,

        'overall_speaker'  : list(comb.keys()),
        'overall_durations': list(comb.values()),

        'series1_str': series1,
        'series2_str': series2,
        'series3_str': series3,

        'speakers': speakers,
        'durations': durations,
        'start_times': start_times,
        'text': texts,
    }

    return data