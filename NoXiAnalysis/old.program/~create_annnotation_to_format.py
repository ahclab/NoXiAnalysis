import os
from os.path import join, dirname
import sys
import wave
import re
import csv

from NoXiAnalysis.utils.dataload import DataLoad

def convert_tab_separated_to_audio_novice(input_file_path, output_file_path):
    with open(input_file_path, 'r') as input_file, open(output_file_path, 'w') as output_file:
        prev_end_time = 0.0
        for line in input_file:
            start_time, end_time = line.strip().split('\t')
            start_time, end_time = float(start_time), float(end_time)

            output_file.write(f'audio_novice {prev_end_time:.6f} {start_time:.6f} [silence]\n')
            output_file.write(f'audio_novice {start_time:.6f} {end_time:.6f} [speech]\n')

            prev_end_time = end_time

def convert_vad(input_file, output_file):
    os.makedirs(dirname(output_path), exist_ok=True)
    with open(input_file, 'r') as infile:
        input_lines = infile.readlines()

    output_lines = []

    for line in input_lines:
        if '[speech]' in line:
            _, start, end, _ = line.split()
            output_lines.append(f"\t{start}\t{end}")

    with open(output_file, 'w') as outfile:
        outfile.write('\n'.join(output_lines))

if __name__ == "__main__":
    data_load = DataLoad("output/vad/")
    for key, input_path in data_load["vad_expert.txt"].items():
        output_path = join("output/tab_vad/", key, "vad_expert.txt")
        convert_vad(input_path, output_path)
    
    for key, input_path in data_load["vad_novice.txt"].items():
        output_path = join("output/tab_vad/", key, "vad_novice.txt")
        convert_vad(input_path, output_path)