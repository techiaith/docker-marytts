#!/usr/bin/python

import os
import pygame
import textwrap
import Prompts 
import time
import SimpleRecorder

# Variables for Pygame
width = 850
height = 480
text_width = 20;

def make_font(fonts, size):
    available = pygame.font.get_fonts()
    # get_fonts() returns a list of lowercase spaceless font names
    choices = map(lambda x:x.lower().replace(' ', ''), fonts)
    for choice in choices:
        if choice in available:
            return pygame.font.SysFont(choice, size)
    return pygame.font.Font(None, size)
    
_cached_fonts = {}
def get_font(font_preferences, size):
    global _cached_fonts
    key = str(font_preferences) + '|' + str(size)
    font = _cached_fonts.get(key, None)
    if font == None:
        font = make_font(font_preferences, size)
        _cached_fonts[key] = font
    return font

_cached_text = {}
def create_text(text, fonts, size, color):
    global _cached_text
    key = '|'.join(map(str, (fonts, size, color, text)))
    image = _cached_text.get(key, None)
    if image == None:
        font = get_font(fonts, size)
        image = font.render(text, True, color)
        _cached_text[key] = image
    return image

def get_outstanding_prompts():
    completedIds = set(os.path.splitext(x)[0] for x in os.listdir('audio'))
    allIds = set(p["identifier"] for p in Prompts.PROMPTS)
    outstandingIds = allIds - completedIds
    outstandingPrompts = [p for p in Prompts.PROMPTS if p["identifier"] in outstandingIds]
    return outstandingPrompts

def display_clear():
    screen.fill((255, 255, 255))
    pygame.display.flip()

def display_prompt(prompt_idx):
    text = outstanding_prompts[prompt_idx]["text"]
    print textwrap.wrap(text, text_width)
    texts = textwrap.wrap(text, text_width)
    for idx, t in enumerate(texts):
        ydelta = 0 if idx == 0 else (idx * 50) #+ 20
        print idx, t, ydelta
        label = create_text(t, font_preferences, 72, (0, 128, 0))
        screen.blit(label, (50, (50 + ydelta)))
    pygame.display.flip()

def display_message(message):
    label = create_text(message, font_preferences, 72, (0, 128, 0))
    screen.blit(label, (20, 400))
    pygame.display.flip()


os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()

screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()
done = False

font_preferences = [
    "Bizarre-Ass Font Sans Serif",
    "They definitely dont have this installed Gothic",
    "Papyrus",
    "Comic Sans MS"]

outstanding_prompts = get_outstanding_prompts()
prompt_count = len(outstanding_prompts)
current_prompt_idx = -1

recording = False
recorder = None

display_clear()
display_message("Bysell bwlch i gychwyn")
current_wav_file = None
sound = None

while not done:

    if recording:
        recorder.continue_recording()

    for event in pygame.event.get():

        if event.type == pygame.KEYDOWN and \
            (event.key == pygame.K_SPACE or \
            event.key == pygame.K_BACKSPACE) and \
            recording is False:

            if event.key == pygame.K_SPACE:
                current_prompt_idx += 1

            if sound is not None:
                sound.stop()

            display_clear()
            display_prompt(current_prompt_idx)
            display_message("recordio...")
            print "Recordio......"

            fname = outstanding_prompts[current_prompt_idx]["identifier"]
            current_wav_file = 'audio/' + fname + '.wav'

            recorder = SimpleRecorder.SimpleRecorder(fname=current_wav_file)
            recorder.start_recording()
            recording = True
            break

        if event.type == pygame.KEYDOWN and \
           event.key == pygame.K_SPACE and \
           recording is True:

            print "Stop recordio"
            recorder.stop_recording()
            recording = False

            sound = pygame.mixer.Sound(current_wav_file)
            sound.play()

            display_clear()
            display_message("Bwlch i barhau. Backspace am eto")
            break

        if event.type == pygame.QUIT:
            if recording:
                recorder.stop_recording()
            done = True

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if recording:
                recorder.stop_recording()
            done = True

    #clock.tick(60)
