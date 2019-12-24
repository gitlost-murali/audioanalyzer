'''
This file is created for converting 'modelling/dataset.csv' into filename|bgm|start|end columns
'''
from __future__ import print_function
import os, sys
import glob
from tqdm import tqdm, tqdm_notebook
import numpy as np
import pandas as pd
from pathlib import Path
import re

path = Path('/media/mano/Data/MyData/Star_MAA/modelling/')
df = pd.read_csv(path/'dataset.csv')
df['Emotion1'] = df['Emotion1'].str.strip()


parseddataset = []

for roe in df.values:
    filename = roe[0]
    emotion1,emotion2,emotion3 = roe[1],roe[2],roe[3]
    videofilename = re.findall("\[(.*?)\]",filename)
    videofilename = videofilename[0].replace("\'",'').replace("_bgm","")
    
    videonum, start, end = re.findall("[0-9]+",filename)
    parseddataset.append([filename,emotion1,emotion2,emotion3,videofilename,start,end])    

parsedf = pd.DataFrame(parseddataset,columns=['filename','emotion1','emotion2','emotion3','videofilename','start','end'])    
print(parsedf.head())

parsedf.to_csv('parsed_dataset.csv',index=False)