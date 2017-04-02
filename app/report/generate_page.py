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

def generate_page(filename):
    print("Generating output...")
    templatefile = "{}/template.html".format(s.REPORT_DIR)
    resultsfile  = "{}/{}.txt".format(s.ANALYZE_DIR, filename)

    with open(templatefile, 'r') as f:
        template = f.read().strip()
        
    with open(resultsfile, 'r') as f:
        parsed = json.load(f)

    tones = parsed["tone"]
    munged_tones = []
    for segment in tones:
        temp = [0, 0, 0]
        if segment != "":
            for tone in segment:
                if tone["tone_name"] == "Anger":
                    temp[0] += tone["score"]
                elif tone["tone_name"] == "Disgust":
                    temp[0] += tone["score"]
                elif tone["tone_name"] == "Fear":
                    temp[1] += tone["score"]
                elif tone["tone_name"] == "Sadness":
                    temp[1] += tone["score"]
                elif tone["tone_name"] == "Joy":
                    temp[2] += tone["score"]
                    temp[0] /= 2
                    temp[1] /= 2
                    munged_tones.append(temp)

    series1 = ", ".join(['{x: ' + str(ind) + ', y: ' + str(data[0]) + '}'
                         for ind, data in enumerate(munged_tones)])
    series2 = ", ".join(['{x: ' + str(ind) + ', y: ' + str(data[1]) + '}'
                         for ind, data in enumerate(munged_tones)])
    series3 = ", ".join(['{x: ' + str(ind) + ', y: ' + str(data[2]) + '}'
                         for ind, data in enumerate(munged_tones)])

    comb = {}
    total_dur = 0
    for segment in parsed["parties"]:
        val = comb.get(segment["speaker_id"], 0.0) + segment["duration"]
        total_dur += segment["duration"]
        comb[segment["speaker_id"]] = val

    speakers = []
    durations = []
    for k in comb:
        speakers.append(k)
        durations.append(comb[k] / total_dur)

    concepts = [concept["key"] for concept in parsed["concepts"]]

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

    final_report = "{}/report_{}.html".format(
        s.OUTPUT_DIR, filename)
    with open(final_report, "w") as f:
        f.write(pystache.render(template, data))

    return final_report
