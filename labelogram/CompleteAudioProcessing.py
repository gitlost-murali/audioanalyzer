#!/usr/bin/env python

from __future__ import print_function
from pydub import AudioSegment
from pydub.playback import play
import os, sys
import glob
from tqdm import tqdm, tqdm_notebook
import numpy as np
import matplotlib.pyplot as plt

import librosa
import librosa.display
from pathlib import Path
import pylab

# In[2]:


def extract_music_bgm(myAudioFile):
    # read in audio file and get the two mono tracks
    os.chdir(videos_folder) # Go to videos folder
    sound_stereo = AudioSegment.from_file(myAudioFile, format="mp4")
    os.chdir("..")  # Come back to root directory
    sound_monoL = sound_stereo.split_to_mono()[0]
    sound_monoR = sound_stereo.split_to_mono()[1]


    # Invert phase of the Right audio file
    sound_monoR_inv = sound_monoR.invert_phase()

    # Merge two L and R_inv files, this cancels out the centers
    sound_CentersOut = sound_monoL.overlay(sound_monoR_inv)

    # Export merged audio file
    fh = sound_CentersOut.export('{}/{}_bgm.mp3'.format(bgm_folder,myAudioFile.split(".")[0]), format="mp3")


# In[3]:



def mkdir_ifnot(foldr):  # If the folder passed doesn't exist, this function creates one
    if not os.path.exists(foldr): os.mkdir(foldr)


# In[4]:



# In[5]:


def process_videos(videos_folder):
    for vid in tqdm_notebook(glob.glob("{}*.mp4".format(videos_folder))):
        vid = os.path.basename(vid)
        try:
            extract_music_bgm(vid)
        except Exception as e:
            print("error is ",e,vid)


# In[6]:


# process_videos(videos_folder)


# In[ ]:





# In[7]:

# In[8]:


def produce_chunks(audio,sr):

    checkpoints = [0]

    checkpoint_flag = 0          # 0 means off

    for idx,amp in enumerate(audio):

        if amp>start and amp<end and checkpoint_flag == 0:
            checkpoint_flag = 1
            checkpoints.append(idx/sr)

        elif amp>start and amp<end and checkpoint_flag == 1:
            checkpoint_flag = 1

        elif ( amp<start or amp>end ) and checkpoint_flag == 1:
            checkpoint_flag = 0
            checkpoints.append(idx/sr)


#     return checkpoints
#     print(checkpoints)


    ## Making tuples for storing chunks
    prev = 0
    chunks = []
    for checkpoint in checkpoints:
        if not checkpoint - prev > 4: continue
        chunks.append((prev,checkpoint))
        prev = checkpoint

    del checkpoints  # Saving space. Not needed

    return chunks


# In[9]:


def make_chunks(audio,sr):

    checkpoints = [0]

    checkpoint_flag = 0          # 0 means off

    for idx,amp in enumerate(audio):

        if amp == 0.0 and checkpoint_flag == 0:
            checkpoint_flag = 1
            checkpoints.append(idx/sr)

        elif amp == 0.0 and checkpoint_flag == 1:
            checkpoint_flag = 1

        elif amp!=0 and checkpoint_flag == 1:
            checkpoint_flag = 0
            checkpoints.append(idx/sr)


#     return checkpoints
#     print(checkpoints)


    ## Making tuples for storing chunks
    prev = 0
    chunks = []
    for checkpoint in checkpoints:
        if not checkpoint - prev > 2: continue
        chunks.append((prev,checkpoint))
        prev = checkpoint

    del checkpoints # Saving space, not needed.

    return chunks


# In[ ]:





# In[10]:




def save_images(S_full,y,sr,strtend_list,filesavename='test'):


    pylab.axis('off') # no axis
    pylab.axes([0., 0., 1., 1.], frameon=False, xticks=[], yticks=[]) # Remove the white edge


    for indx,(start,end) in tqdm(enumerate(strtend_list),desc='Creating files',total=len(strtend_list)):
        start=int(start)
        end = int(end)
        idx = slice(*librosa.time_to_frames([start, end], sr=sr))

        librosa.display.specshow(librosa.amplitude_to_db(S_full[:, idx], ref=np.max),
                                 y_axis='log', x_axis='time', sr=sr)

# Saving space


        filnamenow = "{}to{}.jpg".format(start,end)
        filnamefldr = "{}/{}".format(str(img_dir),str(filesavename))

        if not os.path.exists(filnamefldr):          # Storing every image with its own name
            mkdir_ifnot(filnamefldr)

        pylab.savefig("{}/{}".format(filnamefldr,filnamenow), bbox_inches=None, pad_inches=0) # Saving space
        # librosa.output.write_wav('{}/file_trim_{}to{}.wav'.format(filnamefldr,start,end), y[start*sr:end*sr], sr)

    pylab.close()

# In[11]:


def make_aud_chunks_images(mp3_file):

    os.chdir(bgm_folder)
    print("Chunking ...")
    y, sr = librosa.load('{}'.format(mp3_file), duration=None)
    os.chdir("..")

    print("Producing chunks ...")
    # And compute the spectrogram magnitude and phase
    S_full, phase = librosa.magphase(librosa.stft(y))
    audio_chunks = produce_chunks(y,sr)


    save_images(S_full,y,sr,audio_chunks,"{}".format(mp3_file.split(".")[:-1]))
    del audio_chunks  # Saving space.

#     return audio_chunks # No need to return


# In[12]:
if __name__ == '__main__':
        
    start,end = -0.0000001, 0.0000001
    videos_folder = 'videos/'
    bgm_folder = 'bgm/'
    img_dir ='gen_bgm_img/'

    mkdir_ifnot(videos_folder)
    mkdir_ifnot(bgm_folder)
    mkdir_ifnot(img_dir)
    videofilename = str(sys.argv[1])
    videofilename = os.path.basename(videofilename)
    extract_music_bgm(videofilename)
    audiofilename = '{}/{}_bgm.mp3'.format(bgm_folder,videofilename.split(".")[0])
    audiofilename = os.path.basename(audiofilename)
    make_aud_chunks_images(audiofilename)
    print("{} is processed ".format(videofilename))

# In[ ]:





# In[ ]:
