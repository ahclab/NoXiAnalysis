import subprocess
import os
import sys
from os.path import join
import argparse

from NoXiAnalysis.utils.utils import repo_root
from NoXiAnalysis.utils.dataload import DataLoad
import NoXiAnalysis.utils.utils as utils

def openposeFeatureExtraction(input_path, output_path, gpus = 0):
    os.environ["CUDA_VISIBLE_DEVICES"] = str(gpus)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    python_file = join(repo_root(), "openpose/video_to_csv.py")
    cmd = f"python {python_file} {input_path} --output_file {output_path}"
    print(cmd)
    if gpus == 0:
        utils.process_num_gpu0 += 1
    if gpus == 1:
        utils.process_num_gpu1 += 1
    subprocess.call(cmd, shell=True)
    if gpus == 0:
        utils.process_num_gpu0 -= 1
    if gpus == 1:
        utils.process_num_gpu1 -= 1
