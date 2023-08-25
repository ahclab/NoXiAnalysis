import subprocess
import os
from os.path import join
import argparse

from NoXiAnalysis.utils.dataload import DataLoad
from NoXiAnalysis.openface.openface import openfaceFeatureExtraction

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--output_dir", default="output/openface/")
    args = parser.parse_args()

    data_load = DataLoad()

    for key, input_path in data_load["video_expert.mp4"].items():
        output_path = join(args.output_dir, key, "video_expert_openface.csv")
        openfaceFeatureExtraction(input_path, output_path)
    
    for key, input_path in data_load["video_novice.mp4"].items():
        output_path = join(args.output_dir, key, "video_novice_openface.csv")
        openfaceFeatureExtraction(input_path, output_path)
    