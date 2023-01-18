import subprocess
import os
import sys
from os.path import join
import argparse
from pprint import pprint

from NoXiAnalysis.utils.dataload import DataLoad
from NoXiAnalysis.convert.convert import audioMixing


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--output_dir", default="output/mix_audio/")
    args = parser.parse_args()

    data_load = DataLoad()

    expert_dict = data_load["audio_expert.wav"]
    novice_dict = data_load["audio_novice.wav"]
    data_dict = {}
    for key, input_path in expert_dict.items():
        data_dict[key] = [input_path, novice_dict[key]]
    
    for key, input_path in data_dict.items():
        output_path = join(args.output_dir, key, "audio_mix.wav")
        audioMixing(input_path[0], input_path[1], output_path)
