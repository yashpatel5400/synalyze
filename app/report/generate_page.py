"""
__authors__     = Yash, Will, Peter
__description__ = Generates report HTML pages given analysis performed using
the Watson API
"""

from . import settings as s

import pystache
import sys
import json

import time
import datetime

def generate_page(filename):
    print("Generating output...")
    templatefile = "{}/template.html".format(s.REPORT_DIR)
    resultsfile  = "{}/{}.txt".format(s.ANALYZE_DIR, filename)

    with open(templatefile, 'r') as f:
        template = f.read().strip()
        
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
    print(munged_tones)
    series1 = ", ".join(['{x: ' + str(ind) + ', y: ' + str(data[0]) + '}'
                         for ind, data in enumerate(munged_tones)])
    series2 = ", ".join(['{x: ' + str(ind) + ', y: ' + str(data[1]) + '}'
                         for ind, data in enumerate(munged_tones)])
    series3 = ", ".join(['{x: ' + str(ind) + ', y: ' + str(data[2]) + '}'
                         for ind, data in enumerate(munged_tones)])

    comb = {}
    total_dur = 0
    for analysis in analyzed["parties"]:
        val = comb.get(analysis["speaker_id"], 0.0) + analysis["duration"]
        total_dur += analysis["duration"]
        comb[analysis["speaker_id"]] = val

    speakers = []
    durations = []
    for k in comb:
        speakers.append(k)
        durations.append(comb[k] / total_dur)

    concepts = [concept["key"] for concept in analyzed["concepts"]]

    data = {
        'title': 'Meeting Report',
        'topic': 'The Topic of the Meeting',
        'date_str': datetime.datetime.today().strftime('%Y-%m-%d'),
        'dur_str':  time.strftime("%H:%M:%S", time.gmtime(total_dur)),
        'ideas': concepts,
        'series1_str': series1,
        'series2_str': series2,
        'series3_str': series3,
        'speakers': speakers,
        'durations': durations,
    }

    report_name  = "report_{}.html".format(filename) 
    final_report = "{}/{}".format(s.OUTPUT_DIR, report_name)
    with open(final_report, "w") as f:
        f.write(pystache.render(template, data))

    return report_name
