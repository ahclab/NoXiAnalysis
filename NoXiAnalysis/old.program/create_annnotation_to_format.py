import os
from os.path import join, dirname
import sys
import wave
import re
import csv

from NoXiAnalysis.utils.dataload import DataLoad

def time_to_seconds(time_str):
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + float(s)

def read_input_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        data = [line.strip().split('\t') for line in lines[1:]]
    return data

def convert_to_output_format(input_file, output_file, audio_path):

    os.makedirs(dirname(output_file), exist_ok=True)
    input_lines = read_input_file(input_file)
    
    with wave.open(audio_path,  'rb') as wr:
        fr = wr.getframerate()
        fn = wr.getnframes()
        final_time = 1.0 * fn / fr

    output = []
    prev_end_time = "00:00:00.000"

    for row in input_lines:
        start_time = row[2]
        end_time = row[3]

        output.append(f"audio_novice {time_to_seconds(prev_end_time):.3f} {time_to_seconds(start_time):.3f} [silence]")
        output.append(f"audio_novice {time_to_seconds(start_time):.3f} {time_to_seconds(end_time):.3f} [speech]")

        prev_end_time = end_time

    output.append(f"audio_expert {time_to_seconds(prev_end_time):.3f} {final_time:.3f} [silence]")

    with open(output_file, 'w') as outfile:
        outfile.write('\n'.join(output))


if __name__ == "__main__":
    data_load = DataLoad("NoXiAnalysis/ONISHI_vad/")
    audio = DataLoad("output/mix_audio/")
    for key, input_path in data_load["vad_expert.txt"].items():
        try:
            output_path = join("/ahc/work2/kazuyo-oni/NoXiAnalysis/output/vad/", key, "vad_expert.txt")
            convert_to_output_format(input_path, output_path, audio["audio_expert.wav"][key])
            print(input_path)
        except:
            print(f"ERROR: {input_path}")
    
    for key, input_path in data_load["vad_novice.txt"].items():
        try:
            output_path = join("/ahc/work2/kazuyo-oni/NoXiAnalysis/output/vad/", key, "vad_novice.txt")
            convert_to_output_format(input_path, output_path, audio["audio_novice.wav"][key])
            print(input_path)
        except:
            print(f"ERROR: {input_path}")