#!/usr/bin/python3
# -*- coding:utf-8 -*-
import os, sys
import getopt
import codecs
import wave
import contextlib

from praatio import tgio


def get_wav_duration(wav_file):
    with contextlib.closing(wave.open(wav_file, 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        return duration


def convert_to_textgrid_file(text, wav_file, tg_file):
   tg = tgio.Textgrid()
   tg_entries_list = []

   tg_entry = (0.0, get_wav_duration(wav_file), text)
   tg_entries_list.append(tg_entry)
   
   utteranceTier = tgio.IntervalTier('utterance', tg_entries_list, 0, pairedWav=wav_file)
   tg.addTier(utteranceTier)
   tg.save(tg_file)
   

def convert_directory_to_textgrids(source_dir):
    for fn in os.listdir(source_dir):
        name, ext = os.path.splitext(fn)
        if ext != ".wav":
            continue

        with codecs.open(os.path.join(source_dir, name + '.txt'), 'r', encoding='utf-8') as txt_file:
            txt = txt_file.read().replace('\n','')

        convert_to_textgrid_file(txt, os.path.join(source_dir, fn), os.path.join(source_dir, name + '.TextGrid'))



def display_help():
    print ("")
    print ("Build TextGrids from wav and txt files")
    print ("")
    print ("Usage:")
    print ("")
    print ("$ create_textgrids.py -s <source> ")

def main(argv):

    try:
        opts, args = getopt.getopt(argv,"hs:", ["source=",])
    except getopt.GetoptError:
        display_help()
        return

    if len(opts) < 1:
        display_help()
        return

    source_audio_dir = ''
    for opt, arg in opts:
        if opt == '-h':
            display_help()
        elif opt in ("-s","--source"):
            source_audio_dir = arg

    if len(source_audio_dir) > 0: 
        convert_directory_to_textgrids(source_audio_dir)
    else:
        display_help()


if __name__ == "__main__":

    main(sys.argv[1:])

