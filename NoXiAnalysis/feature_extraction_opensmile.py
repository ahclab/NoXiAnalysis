import subprocess
import os
from os.path import join
import argparse

from NoXiAnalysis.utils.dataload import DataLoad
from NoXiAnalysis.opensmile.opensmile import opensmileFeatureExtraction

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--output_dir", default="output/opensmile/")
    args = parser.parse_args()

    data_load = DataLoad()

    for key, input_path in data_load["audio_expert.wav"].items():
        output_path = join(args.output_dir, key, "expert_opensmile.csv")
        opensmileFeatureExtraction(input_path, output_path)
    
    for key, input_path in data_load["audio_novice.wav"].items():
        output_path = join(args.output_dir, key, "novice_opensmile.csv")
        opensmileFeatureExtraction(input_path, output_path)

