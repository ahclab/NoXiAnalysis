import subprocess
import os
import sys
from os.path import join
import argparse

from NoXiAnalysis.utils.dataload import DataLoad

def opensmileFeatureExtraction(input_path, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cmd = f"SMILExtract -C /ahc/work2/kazuyo-oni/opensmile/myconfig/noxi.conf -I {input_path} -O {output_path}"
    print(cmd)
    subprocess.call(cmd, shell=True)

