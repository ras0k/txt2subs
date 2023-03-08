#########################################################
#     __           __  ________              ___        #
#   _/  |____  ___/  |_\_____  \  ________ __\_ |__     #
#   \   __\  \/  /   __\/  ____/ /  ___/  |  \| __ \    #
#    |  |  \    / |  | /       \ \___ \|  |  /| \_\ \   #
#    |__| /__/\_ \|__| \_______ \____  \____/ |___  /   #
#               \/             \/    \/           \/    #
#########################################################

import re
import speech_recognition as sr

# Parse the lyrics text file
with open('lyrics.txt') as f:
    lines = f.readlines()

lyrics = []

for line in lines:
    line = line.strip()
    if line and not line.startswith('['):
        lyrics.append(line)

# Load the audio file
r = sr.Recognizer()
with sr.AudioFile('audio.wav') as source:
    audio = r.record(source)

# Transcribe the audio
text = r.recognize_google(audio)

# Match the text to the lyrics strings
lyric_idx = 0
captions = []
for word in text.split():
    if word.lower() == lyrics[lyric_idx].split()[0].lower():
        start = 0  # Start time of the caption (in seconds)
        end = 0  # End time of the caption (in seconds)
        for i in range(len(lyrics)):
            if lyrics[i].lower().startswith(word.lower()):
                start = end
                end += 1  # We assume each caption lasts 1 second
                caption = f"{start:.3f},{end:.3f}\n{lyrics[i]}"
                captions.append(caption)
                lyric_idx = i + 1
                break

# Write the captions to a file
with open('captions.txt', 'w') as f:
    f.writelines(captions)
