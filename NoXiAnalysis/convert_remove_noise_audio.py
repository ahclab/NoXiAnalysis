import subprocess
import os
import sys
from os.path import join
import argparse

from NoXiAnalysis.utils.dataload import DataLoad
from NoXiAnalysis.convert.convert import reduceAudioNoise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--output_dir", default="output/remove_noise/")
    args = parser.parse_args()

    data_load = DataLoad()

    for key, input_path in data_load["audio_expert.wav"].items():
        output_path = join(args.output_dir, key, "audio_expert_remove_noise.wav")
        reduceAudioNoise(input_path, output_path)
    
    for key, input_path in data_load["audio_novice.wav"].items():
        output_path = join(args.output_dir, key, "audio_novice_remove_noise.wav")
        reduceAudioNoise(input_path, output_path)
