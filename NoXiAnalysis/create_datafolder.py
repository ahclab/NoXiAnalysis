import subprocess
import os
from os.path import join
import argparse
import pandas as pd
from os.path import dirname

from NoXiAnalysis.utils.dataload import DataLoad
from NoXiAnalysis.utils.utils import copy_file, mv_file

def _normalization(x):
    return (x+1)/2

def create_multimodal_features(openface_path, openpose_path):
    multimodal_features = pd.DataFrame()

    df = pd.read_csv(openface_path)
    columns = df.columns.str.strip()
    df = df.set_axis(columns, axis="columns")


    multimodal_features["gaze_x"] = df["gaze_angle_x"].apply(_normalization) #gaze_X 0 ~ 1
    multimodal_features["gaze_y"] = df["gaze_angle_y"].apply(_normalization) #gaze_Y 0 ~ 1
    multimodal_features["AU01"] = df["AU01_c"] #AU1
    multimodal_features["AU02"] = df["AU02_c"] #AU2
    multimodal_features["AU04"] = df["AU04_c"] #AU4
    x_diff = pow(df["pose_Rx"].diff().fillna(0),2)
    y_diff = pow(df["pose_Ry"].diff().fillna(0),2)
    z_diff = pow(df["pose_Rz"].diff().fillna(0),2)
    multimodal_features["head"] = (x_diff+y_diff+z_diff)**0.5 #head

    df = pd.read_csv(openpose_path)
    columns = df.columns.str.strip()
    df = df.set_axis(columns, axis="columns")

    pose1 = (pow(df["1_x"],2) + pow(df["1_y"],2))**0.5
    pose2 = (pow(df["2_x"],2) + pow(df["2_y"],2))**0.5
    pose3 = (pow(df["3_x"],2) + pow(df["3_y"],2))**0.5
    pose4 = (pow(df["4_x"],2) + pow(df["4_y"],2))**0.5
    pose5 = (pow(df["5_x"],2) + pow(df["5_y"],2))**0.5
    pose6 = (pow(df["6_x"],2) + pow(df["6_y"],2))**0.5
    pose7 = (pow(df["7_x"],2) + pow(df["7_y"],2))**0.5

    pose1_diff = pow(pose1.diff().fillna(0),2)
    pose2_diff = pow(pose2.diff().fillna(0),2)
    pose3_diff = pow(pose3.diff().fillna(0),2)
    pose4_diff = pow(pose4.diff().fillna(0),2)
    pose5_diff = pow(pose5.diff().fillna(0),2)
    pose6_diff = pow(pose6.diff().fillna(0),2)
    pose7_diff = pow(pose7.diff().fillna(0),2)

    multimodal_features["pose"] = (pose1_diff + pose2_diff + pose3_diff+ pose4_diff + pose5_diff + pose6_diff + pose7_diff)**0.5 #pose

    return multimodal_features

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--output_dir", default="output/noxi/")
    args = parser.parse_args()

    # audio
    data_load = DataLoad()
    # for key, input_path in data_load["audio_expert.wav"].items():
    #     output_path = join(args.output_dir, key, "audio_expert.wav")
    #     copy_file(input_path, output_path)
    
    # for key, input_path in data_load["audio_novice.wav"].items():
    #     output_path = join(args.output_dir, key, "audio_novice.wav")
    #     copy_file(input_path, output_path)
    
    data_load = DataLoad("output/mix_audio/")
    for key, input_path in data_load["audio_mix.wav"].items():
        output_path = join(args.output_dir, key, "audio_mix.wav")
        copy_file(input_path, output_path)
    
    # vad
    data_load = DataLoad("output/vad/")
    for key, input_path in data_load["vad_expert.txt"].items():
        output_path = join(args.output_dir, key, "vad_expert.txt")
        copy_file(input_path, output_path)
    
    for key, input_path in data_load["vad_novice.txt"].items():
        output_path = join(args.output_dir, key, "vad_novice.txt")
        copy_file(input_path, output_path)
    
    # non-verbal features
    data_load_openface = DataLoad("output/openface/")
    data_load_openpose = DataLoad("output/openpose/")
    for key, openface_path in data_load_openface["video_expert_openface.csv"].items():
        openpose_path = data_load_openpose["video_expert_openpose.csv"][key]
        output_path = join(args.output_dir, key, "non_varbal_expert.csv")
        os.makedirs(dirname(output_path), exist_ok=True)
        multimodal_features = create_multimodal_features(openface_path, openpose_path)
        print(output_path)
        multimodal_features.to_csv(output_path)

    for key, openface_path in data_load_openface["video_novice_openface.csv"].items():
        openpose_path = data_load_openpose["video_novice_openpose.csv"][key]
        output_path = join(args.output_dir, key, "non_varbal_novice.csv")
        os.makedirs(dirname(output_path), exist_ok=True)
        multimodal_features = create_multimodal_features(openface_path, openpose_path)
        print(output_path)
        multimodal_features.to_csv(output_path)