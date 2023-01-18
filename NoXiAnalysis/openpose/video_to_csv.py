import copy
import numpy as np
import cv2
from glob import glob
import os
import argparse
import json
import torch
import time

# video file processing setup
# from: https://stackoverflow.com/a/61927951
import argparse
import subprocess
import sys
from pathlib import Path
from typing import NamedTuple
import itertools
import csv

# os.environ["CUDA_VISIBLE_DEVICES"] = "0,1"


class FFProbeResult(NamedTuple):
    return_code: int
    json: str
    error: str


def ffprobe(file_path) -> FFProbeResult:
    command_array = [
        "ffprobe",
        "-v",
        "quiet",
        "-print_format",
        "json",
        "-show_format",
        "-show_streams",
        file_path,
    ]
    result = subprocess.run(
        command_array,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )
    return FFProbeResult(
        return_code=result.returncode, json=result.stdout, error=result.stderr
    )


# openpose setup
from src import model
from src import util
from src.body import Body_original
from src.hand import Hand

body_estimation = Body_original(
    "/ahc/work2/kazuyo-oni/pytorch-openpose/model/body_pose_model.pth"
)
hand_estimation = Hand(
    "/ahc/work2/kazuyo-oni/pytorch-openpose/model/hand_pose_model.pth"
)


def process_frame(frame, body=True):
    if body:
        candidate = list(body_estimation(frame))
        for i, cand in enumerate(candidate):
            if cand:
                candidate[i] = list(candidate[i][0])
                del candidate[i][-1]
                candidate[i][0] /= width
                candidate[i][1] /= height
            else:
                candidate[i] = [0, 0, 0]

    return list(itertools.chain.from_iterable(candidate))


# writing video with ffmpeg because cv2 writer failed
# https://stackoverflow.com/questions/61036822/opencv-videowriter-produces-cant-find-starting-number-error
import ffmpeg

# open specified video
parser = argparse.ArgumentParser(
    description="Process a video annotating poses detected."
)
parser.add_argument("file", type=str, help="Video file location to process.")
parser.add_argument("--no_body", action="store_true", help="No body pose")
parser.add_argument("--output_file", type=str, help="Output file name")
args = parser.parse_args()
video_file = args.file
cap = cv2.VideoCapture(video_file)
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
print(f"w:h = {width}:{height}")

# get video file info
ffprobe_result = ffprobe(args.file)
info = json.loads(ffprobe_result.json)
videoinfo = [i for i in info["streams"] if i["codec_type"] == "video"][0]
input_fps = videoinfo["avg_frame_rate"]
# input_fps = float(input_fps[0])/float(input_fps[1])
input_pix_fmt = videoinfo["pix_fmt"]
input_vcodec = videoinfo["codec_name"]
if args.output_file is not None:
    output_file = args.output_file
else:
    output_file = ".".join(video_file.split(".")[:-1]) + ".processed.csv"

from tqdm import tqdm

print(f"OUTPUT -> {output_file}")
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using {device} device")

os.makedirs(os.path.dirname(output_file), exist_ok=True)

pbar = tqdm(total=int(cap.get(cv2.CAP_PROP_FRAME_COUNT)))
with open(output_file, "w") as f:
    writer = csv.writer(f)
    header = []
    for i in range(18):
        header.extend([f"{i}_x", f"{i}_y", f"{i}_score"])
    writer.writerow(header)
    while cap.isOpened():
        ret, frame = cap.read()
        if frame is None:
            break

        posed_frame = process_frame(frame, body=not args.no_body)
        writer.writerow(posed_frame)
        pbar.update(1)

        # exit()
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()
