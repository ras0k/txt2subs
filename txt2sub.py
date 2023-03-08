"""
#########################################################
#     __           __  ________              ___        #
#   _/  |____  ___/  |_\_____  \  ________ __\_ |__     #
#   \   __\  \/  /   __\/   ___/ /  ___/  |  \| __ \    #
#    |  |  \    / |  | /  /____  \___ \|  |  /| \_\ \   #
#    |__| /__/\_ \|__| \_______ \____  \____/ |___  /   #
#               \/             \/    \/           \/    #
#########################################################

txt2sub - A speech-to-text program that generates subtitle files from a lyrics text file and an audio file.
Usage: txt2sub.py -i <lyrics_text_file> -a <audio_file> -o <captions_text_file>

Arguments:
-i/--input:  Path to the lyrics text file (required)
-a/--audio:  Path to the audio file (required)
-o/--output: Path to the output captions text file (required)
"""
import argparse
import os
import re
import speech_recognition as sr
from tqdm import tqdm  # Importing tqdm library for progress bar

# Parse command line arguments
parser = argparse.ArgumentParser(description="A speech-to-text program that generates subtitle files from a lyrics text file and an audio file.")
parser.add_argument("-i", "--input", type=str, required=True, help="Path to the lyrics text file")
parser.add_argument("-a", "--audio", type=str, required=True, help="Path to the audio file")
parser.add_argument("-o", "--output", type=str, required=True, help="Path to the output captions text file")
args = parser.parse_args()

# Load the lyrics text file
with open(args.input) as f:
    lines = f.readlines()

lyrics = []

for line in lines:
    line = line.strip()
    if line and not line.startswith('['):
        lyrics.append(line)

# Load the audio file
r = sr.Recognizer()
with sr.AudioFile(args.audio) as source:
    audio = r.record(source)

# Transcribe the audio
text = r.recognize_google(audio)

# Match the text to the lyrics strings
lyric_idx = 0
captions = []
for word in tqdm(text.split()):  # Wrapping for-loop with tqdm
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
with open(args.output, 'w') as f:
    f.writelines(captions)
