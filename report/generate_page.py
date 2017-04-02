import pystache
import sys
import json

templatefile = "./testtemplate"
template = ""
with open(templatefile, 'r') as f:
    template = f.read().strip()

parsed = json.load(sys.stdin)

munged = []
for segment in parsed:
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
    munged.append(temp)

series1 = ", ".join(['{x: ' + str(ind) + ', y: ' + str(data[0]) + '}' for ind, data in enumerate(munged)])
series2 = ", ".join(['{x: ' + str(ind) + ', y: ' + str(data[1]) + '}' for ind, data in enumerate(munged)])
series3 = ", ".join(['{x: ' + str(ind) + ', y: ' + str(data[2]) + '}' for ind, data in enumerate(munged)])

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

print(pystache.render(template, data))
