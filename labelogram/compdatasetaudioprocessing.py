#!/usr/bin/env python

from __future__ import print_function
from pydub import AudioSegment
from pydub.playback import play
import os, sys
import glob
from tqdm import tqdm, tqdm_notebook
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import librosa
import librosa.display
from pathlib import Path
import pylab

# In[2]:
'''
        {
          "from_name": "label",
          "id": "NhgP-Nlw04",
          "source": "$url",
          "to_name": "audio",
          "type": "labels",
          "value": {
            "end": 640.3204128738946,
            "labels": [
              "Education"
            ],
            "start": 584.0439690069222
          }
        }
'''
import json
def create_resultitem(start=0,end=0,label='label',id='id'):
    resultitem = dict()
    resultitem['from_name'] = 'label'
    resultitem['id'] = '{}'.format(id)
    resultitem['source'] = '$url'
    resultitem['to_name'] = 'audio'
    resultitem['type'] = 'labels'
    value=dict()
    value['end'] = end
    value['start'] = start
    value['labels'] = ['{}'.format(label)]
    resultitem['value'] = value
    return resultitem

def create_results():
    results = []
    results.append(create_resultitem())

def create_completions(results_obj):
    completions = dict()
    completions['result'] = results_obj
    return completions

def create_jsonobj(url,filenameid,completionsobj,task_path='../examples/audio_regions/tasks.json'):
    jsondict= dict()
    urldict = dict()
    jsondict['completions'] = [completionsobj]
    urldict['url'] = '{}_bgm.mp3'.format(url)
    jsondict['data'] = urldict
    jsondict['id'] =  filenameid
    jsondict['task_path'] = "../examples/audio_regions/tasks.json"
    return jsondict

import pandas as pd
df = pd.read_csv('parsedataset.csv')
df['emotion1'] = df['emotion1'].str.strip()
df = df[['videofilename','emotion1','start','end']]
filenames = df['videofilename'].unique()
for filindx,filename in enumerate(filenames):
    filevalues = df.loc[df['videofilename'] == "{}".format(filename)]
    results = []
    for idx,row in enumerate(filevalues.values.tolist()):
        _,emotioname,start,end = row
        results.append(create_resultitem(start=start,end=end,label=emotioname,id='{}{}'.format(emotioname,idx)))

    completions_obj = create_completions(results)
    json_obj = create_jsonobj('/static/mediafiles/{}'.format(filename),filindx,completions_obj)
    with open('label-studio/backend/output/{}.json'.format(filindx), 'w') as f:
        json.dump(json_obj, f)

'''
for every row,
    get start, end, and label. Enumerate it. Pass start, end, label and count through the create_resultitem()
    append it to results.
Finally, pass results obj to create_completions()
'''

'''
For every file, get the start and end list as a DataFrame.
Copy a sample JSON version of label-studio. Generate a random alphanumeric code for ID.
Create a label-studio JSON version of our labelling.

{
    "completions": [
        {
            "result": [
                {
                    "from_name": "label",
                    "id": "8XuAAm0nIi",
                    "source": "$url",
                    "to_name": "audio",
                    "type": "labels",
                    "value": {
                        "end": 111.32184052435466,
                        "labels": [
                            "Politics"
                        ],
                        "start": 54.34194110904516
                    }
                },
                {
                    "from_name": "label",
                    "id": "NhgP-Nlw04",
                    "source": "$url",
                    "to_name": "audio",
                    "type": "labels",
                    "value": {
                        "end": 640.3204128738946,
                        "labels": [
                            "Education"
                        ],
                        "start": 584.0439690069222
                    }
                }
            ]
        }
    ],
    "data": {
        "url": "/static/mediafiles/out2.mp3"
    },
    "id": 0,
    "task_path": "../examples/audio_regions/tasks.json"
}

'''
