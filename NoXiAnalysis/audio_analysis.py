import subprocess
import os
import wave
from os.path import join
import argparse
import pandas as pd
from os.path import dirname

from NoXiAnalysis.utils.dataload import DataLoad
from NoXiAnalysis.utils.utils import copy_file, mv_file

def audio_length(path):
    with wave.open(path, 'rb') as wav_file:
        frames = wav_file.getnframes()
        rate = wav_file.getframerate()
        duration = frames / float(rate)

    return duration

if __name__ == "__main__":
    # audio
    data_load = DataLoad("output/mix_audio/")
    for key, input_path in data_load["audio_expert.wav"].items():
        duration = audio_length(input_path)
        print(f"{input_path}, {duration}")
    
    for key, input_path in data_load["audio_novice.wav"].items():
        duration = audio_length(input_path)
        print(f"{input_path}, {duration}")

    total_duration = 0
    for key, input_path in data_load["audio_mix.wav"].items():
        duration = audio_length(input_path)
        total_duration += duration
        print(f"{input_path}, {duration}")
    print(f"Total: {total_duration}")