#!/usr/bin/python3
import os
import numpy as np
import pandas as pd

import collections
import contextlib
import sys
import wave
import contextlib

import parselmouth

from parselmouth.praat import call

from argparse import ArgumentParser, RawTextHelpFormatter

DESCRIPTION = """
"""

file_list = []
duration = []
mean_F0_list = []
sd_F0_list = []
hnr_list = []
localJitter_list = []
localabsoluteJitter_list = []
rapJitter_list = []
ppq5Jitter_list = []
ddpJitter_list = []
localShimmer_list = []
localdbShimmer_list = []
apq3Shimmer_list = []
aqpq5Shimmer_list = []
apq11Shimmer_list = []
ddaShimmer_list = []


def get_duration(wav_filepath):
    with contextlib.closing(wave.open(wav_filepath,'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        return duration


def analyze_speech(wav_filepath, f0min, f0max, unit):
    sound = parselmouth.Sound(wav_filepath)    
    pitch = call(sound, "To Pitch", 0.0, f0min, f0max) #create a praat pitch object
    meanF0 = call(pitch, "Get mean", 0, 0, unit) # get mean pitch
    stdevF0 = call(pitch, "Get standard deviation", 0 ,0, unit) # get standard deviation
    harmonicity = call(sound, "To Harmonicity (cc)", 0.01, 75, 0.1, 1.0)
    hnr = call(harmonicity, "Get mean", 0, 0)
    pointProcess = call(sound, "To PointProcess (periodic, cc)", f0min, f0max)
    localJitter = call(pointProcess, "Get jitter (local)", 0, 0, 0.0001, 0.02, 1.3)
    localabsoluteJitter = call(pointProcess, "Get jitter (local, absolute)", 0, 0, 0.0001, 0.02, 1.3)
    rapJitter = call(pointProcess, "Get jitter (rap)", 0, 0, 0.0001, 0.02, 1.3)
    ppq5Jitter = call(pointProcess, "Get jitter (ppq5)", 0, 0, 0.0001, 0.02, 1.3)
    ddpJitter = call(pointProcess, "Get jitter (ddp)", 0, 0, 0.0001, 0.02, 1.3)
    localShimmer =  call([sound, pointProcess], "Get shimmer (local)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    localdbShimmer = call([sound, pointProcess], "Get shimmer (local_dB)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    apq3Shimmer = call([sound, pointProcess], "Get shimmer (apq3)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    aqpq5Shimmer = call([sound, pointProcess], "Get shimmer (apq5)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    apq11Shimmer =  call([sound, pointProcess], "Get shimmer (apq11)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    ddaShimmer = call([sound, pointProcess], "Get shimmer (dda)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
        
    file_list.append(wav_filepath) # make an ID list
    duration.append(get_duration(wav_filepath))
    mean_F0_list.append(meanF0) # make a mean F0 list
    sd_F0_list.append(stdevF0) # make a sd F0 list
    hnr_list.append(hnr)
    localJitter_list.append(localJitter)
    localabsoluteJitter_list.append(localabsoluteJitter)
    rapJitter_list.append(rapJitter)
    ppq5Jitter_list.append(ppq5Jitter)
    ddpJitter_list.append(ddpJitter)
    localShimmer_list.append(localShimmer)
    localdbShimmer_list.append(localdbShimmer)
    apq3Shimmer_list.append(apq3Shimmer)
    aqpq5Shimmer_list.append(aqpq5Shimmer)
    apq11Shimmer_list.append(apq11Shimmer)
    ddaShimmer_list.append(ddaShimmer)

    print (wav_filepath, str(meanF0), str(stdevF0), str(hnr))


def save_speech_analysis(output_filepath):
    df = pd.DataFrame(np.column_stack([file_list, duration, mean_F0_list, sd_F0_list, hnr_list, localJitter_list, localabsoluteJitter_list,
                                       rapJitter_list, ppq5Jitter_list, ddpJitter_list, localShimmer_list, localdbShimmer_list,
                                       apq3Shimmer_list, aqpq5Shimmer_list, apq11Shimmer_list, ddaShimmer_list]),
                      columns=['voiceID', 'duration', 'meanF0Hz', 'stdevF0Hz', 'HNR', 'localJitter', 'localabsoluteJitter', 'rapJitter',
                                       'ppq5Jitter', 'ddpJitter', 'localShimmer', 'localdbShimmer', 'apq3Shimmer', 'apq5Shimmer',
                                       'apq11Shimmer', 'ddaShimmer'])

    # Write out the updated dataframe\n",
    df.to_csv(output_filepath, index=False)



def main(wav_dirpath, **args):
    for wavfile in os.listdir(os.path.join(wav_dirpath, "wav")):
        analyze_speech(os.path.join(wav_dirpath, "wav", wavfile), 75, 500, "Hertz") 
        save_speech_analysis(os.path.join(wav_dirpath, "speech_analysis.csv"))
    
    total_duration = sum(duration)
    print ("%s recordings\t\t%.2f hours\t(%.2f seconds)" % (len(duration), total_duration/60.0/60.0, total_duration))



if __name__ == '__main__':

    parser = ArgumentParser(description=DESCRIPTION, formatter_class=RawTextHelpFormatter) 
    parser.add_argument("--wav_dirpath", dest="wav_dirpath", required=True, help="path to bangor dict")
    parser.set_defaults(func=main)
    args = parser.parse_args()
    args.func(**vars(args))
