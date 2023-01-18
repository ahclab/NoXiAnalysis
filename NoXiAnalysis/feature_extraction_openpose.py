import subprocess
import os
from os.path import join
import argparse
import threading
import time

from NoXiAnalysis.utils.dataload import DataLoad
from NoXiAnalysis.openpose.openpose import openposeFeatureExtraction
import NoXiAnalysis.utils.utils as utils

def process_gpu0(data_load, output_dir):
    for key, input_path in data_load["video_expert_low.mp4"].items():
        output_path = join(output_dir, key, "video_expert_openface.csv")
        thread = threading.Thread(target=openposeFeatureExtraction, args=(input_path, output_path, 0))
        thread.start()
        while True:
            time.sleep(1)
            if utils.process_num_gpu0 < 10:
                break

def process_gpu1(data_load, output_dir):
    for key, input_path in data_load["video_novice_low.mp4"].items():
        output_path = join(output_dir, key, "video_novice_openface.csv")
        thread = threading.Thread(target=openposeFeatureExtraction, args=(input_path, output_path, 1))
        thread.start()
        while True:
            time.sleep(1)
            if utils.process_num_gpu1 < 10:
                break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--output_dir", default="output/openpose/")
    args = parser.parse_args()

    data_load = DataLoad("output/low_video/")

    thread_0 = threading.Thread(target=process_gpu0, args=(data_load,args.output_dir))
    thread_1 = threading.Thread(target=process_gpu1, args=(data_load,args.output_dir))
    thread_0.start()
    thread_1.start()