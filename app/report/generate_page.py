"""
__authors__     = Yash, Will, Peter
__description__ = Generates report HTML pages given analysis performed using
the Watson API
"""

from . import settings as s

import pystache
import sys
import json

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

    for k in comb:
        comb[k] /= total_dur

    data = {
        'title': 'Report from Meeting',
        'topic': 'Daily Meeting About Saddness',
        'date_str': '2017-04-02',
        'dur_str': '1:23',
        'ideas': ["First Idea", "Second Idea", "Third Idea"],
        'series1_str': series1,
        'series2_str': series2,
        'series3_str': series3,
    }

    report_name  = "report_{}.html".format(filename) 
    final_report = "{}/{}".format(s.OUTPUT_DIR, report_name)
    with open(final_report, "w") as f:
        f.write(pystache.render(template, data))

    return report_name
