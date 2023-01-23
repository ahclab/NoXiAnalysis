import subprocess
import os
from os.path import join
import argparse

from NoXiAnalysis.utils.dataload import DataLoad
from NoXiAnalysis.utils.utils import copy_file, mv_file

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--output_dir", default="output/noxi/")
    args = parser.parse_args()

    # # audio
    # data_load = DataLoad()
    for key, input_path in data_load["audio_expert.wav"].items():
        output_path = join(args.output_dir, key, "audio_expert.wav")
        copy_file(input_path, output_path)
    
    for key, input_path in data_load["audio_novice.wav"].items():
        output_path = join(args.output_dir, key, "audio_novice.wav")
        reduceVideoResolution(input_path, output_path)
    
    data_load = DataLoad("output/mix_audio/")
    for key, input_path in data_load["audio_mix.wav"].items():
        output_path = join(args.output_dir, key, "audio_mix.wav")
        reduceVideoResolution(input_path, output_path)
    
    # # vad
    data_load = DataLoad("output/vad/")
    for key, input_path in data_load["vad_expert.txt"].items():
        output_path = join(args.output_dir, key, "vad_expert.txt")
        copy_file(input_path, output_path)
    
    for key, input_path in data_load["vad_novice.txt"].items():
        output_path = join(args.output_dir, key, "vad_novice.txt")
        copy_file(input_path, output_path)
    
    # non-verbal features
    data_load = DataLoad("output/openface/")
    for key, input_path in data_load["video_expert_openface.csv"].items():
        output_path = join(args.output_dir, key, "openface_expert.csv")
        copy_file(input_path, output_path)
    
    for key, input_path in data_load["video_novice_openface.csv"].items():
        output_path = join(args.output_dir, key, "openface_novice.csv")
        copy_file(input_path, output_path)

    data_load = DataLoad("output/openpose/")
    for key, input_path in data_load["video_expert_openpose.csv"].items():
        output_path = join(args.output_dir, key, "openpose_expert.csv")
        copy_file(input_path, output_path)
    
    for key, input_path in data_load["video_novice_openpose.csv"].items():
        output_path = join(args.output_dir, key, "openpose_novice.csv")
        copy_file(input_path, output_path)
