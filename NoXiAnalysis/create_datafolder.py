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


    multimodal_features["gaze_confidence"] = df["confidence"]
    multimodal_features["gaze_x"] = df["gaze_angle_x"].apply(_normalization) #gaze_X 0 ~ 1
    multimodal_features["gaze_y"] = df["gaze_angle_y"].apply(_normalization) #gaze_Y 0 ~ 1
    multimodal_features["AU01"] = df["AU01_r"]
    multimodal_features["AU02"] = df["AU02_r"] 
    multimodal_features["AU04"] = df["AU04_r"] 
    multimodal_features["AU05"] = df["AU05_r"] 
    multimodal_features["AU06"] = df["AU06_r"] 
    multimodal_features["AU07"] = df["AU07_r"] 
    multimodal_features["AU09"] = df["AU09_r"] 
    multimodal_features["AU10"] = df["AU10_r"] 
    multimodal_features["AU12"] = df["AU12_r"] 
    multimodal_features["AU14"] = df["AU14_r"] 
    multimodal_features["AU15"] = df["AU15_r"] 
    multimodal_features["AU17"] = df["AU17_r"] 
    multimodal_features["AU20"] = df["AU20_r"] 
    multimodal_features["AU23"] = df["AU23_r"] 
    multimodal_features["AU25"] = df["AU25_r"] 
    multimodal_features["AU26"] = df["AU26_r"]
    multimodal_features["AU45"] = df["AU45_r"] 
    x_diff = pow(df["pose_Rx"].diff().fillna(0),2)
    y_diff = pow(df["pose_Ry"].diff().fillna(0),2)
    z_diff = pow(df["pose_Rz"].diff().fillna(0),2)
    multimodal_features["head_x"] = x_diff
    multimodal_features["head_y"] = y_diff
    multimodal_features["head_z"] = z_diff
    # multimodal_features["head"] = (x_diff+y_diff+z_diff)**0.5 #head

    df = pd.read_csv(openpose_path)
    columns = df.columns.str.strip()
    df = df.set_axis(columns, axis="columns")

    pose_1_x = pow(df["1_x"].diff().fillna(0), 2)
    pose_1_y = pow(df["1_y"].diff().fillna(0), 2)
    pose_1_confidence = df["1_score"]
    pose_2_x = pow(df["2_x"].diff().fillna(0), 2)
    pose_2_y = pow(df["2_y"].diff().fillna(0), 2)
    pose_2_confidence = df["2_score"]
    pose_3_x = pow(df["3_x"].diff().fillna(0), 2)
    pose_3_y = pow(df["3_y"].diff().fillna(0), 2)
    pose_3_confidence = df["3_score"]
    pose_4_x = pow(df["4_x"].diff().fillna(0), 2)
    pose_4_y = pow(df["4_y"].diff().fillna(0), 2)
    pose_4_confidence = df["4_score"]
    pose_5_x = pow(df["5_x"].diff().fillna(0), 2)
    pose_5_y = pow(df["5_y"].diff().fillna(0), 2)
    pose_5_confidence = df["5_score"]
    pose_6_x = pow(df["6_x"].diff().fillna(0), 2)
    pose_6_y = pow(df["6_y"].diff().fillna(0), 2)
    pose_6_confidence = df["6_score"]
    pose_7_x = pow(df["7_x"].diff().fillna(0), 2)
    pose_7_y = pow(df["7_y"].diff().fillna(0), 2)
    pose_7_confidence = df["7_score"]

    # pose1 = (pow(df["1_x"],2) + pow(df["1_y"],2))**0.5
    # pose2 = (pow(df["2_x"],2) + pow(df["2_y"],2))**0.5
    # pose3 = (pow(df["3_x"],2) + pow(df["3_y"],2))**0.5
    # pose4 = (pow(df["4_x"],2) + pow(df["4_y"],2))**0.5
    # pose5 = (pow(df["5_x"],2) + pow(df["5_y"],2))**0.5
    # pose6 = (pow(df["6_x"],2) + pow(df["6_y"],2))**0.5
    # pose7 = (pow(df["7_x"],2) + pow(df["7_y"],2))**0.5

    # pose1_diff = pow(pose1.diff().fillna(0),2)
    # pose2_diff = pow(pose2.diff().fillna(0),2)
    # pose3_diff = pow(pose3.diff().fillna(0),2)
    # pose4_diff = pow(pose4.diff().fillna(0),2)
    # pose5_diff = pow(pose5.diff().fillna(0),2)
    # pose6_diff = pow(pose6.diff().fillna(0),2)
    # pose7_diff = pow(pose7.diff().fillna(0),2)

    multimodal_features["pose_1_x"] = pose_1_x
    multimodal_features["pose_1_y"] = pose_1_y
    multimodal_features["pose_1_confidence"] = pose_1_confidence
    multimodal_features["pose_2_x"] = pose_2_x
    multimodal_features["pose_2_y"] = pose_2_y
    multimodal_features["pose_2_confidence"] = pose_2_confidence
    multimodal_features["pose_3_x"] = pose_3_x
    multimodal_features["pose_3_y"] = pose_3_y
    multimodal_features["pose_3_confidence"] = pose_3_confidence
    multimodal_features["pose_4_x"] = pose_4_x
    multimodal_features["pose_4_y"] = pose_4_y
    multimodal_features["pose_4_confidence"] = pose_4_confidence
    multimodal_features["pose_5_x"] = pose_5_x
    multimodal_features["pose_5_y"] = pose_5_y
    multimodal_features["pose_5_confidence"] = pose_5_confidence
    multimodal_features["pose_6_x"] = pose_6_x
    multimodal_features["pose_6_y"] = pose_6_y
    multimodal_features["pose_6_confidence"] = pose_6_confidence
    multimodal_features["pose_7_x"] = pose_7_x
    multimodal_features["pose_7_y"] = pose_7_y
    multimodal_features["pose_7_confidence"] = pose_7_confidence

    # multimodal_features["pose"] = (pose1_diff + pose2_diff + pose3_diff+ pose4_diff + pose5_diff + pose6_diff + pose7_diff)**0.5 #pose

    return multimodal_features

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--output_dir", default="output/noxi/")
    args = parser.parse_args()

    # # audio
    data_load = DataLoad("output/mix_audio/")
    for key, input_path in data_load["audio_expert.wav"].items():
        output_path = join(args.output_dir, key, "audio_expert.wav")
        copy_file(input_path, output_path)
    
    for key, input_path in data_load["audio_novice.wav"].items():
        output_path = join(args.output_dir, key, "audio_novice.wav")
        copy_file(input_path, output_path)
    
    data_load = DataLoad("output/mix_audio/")
    for key, input_path in data_load["audio_mix.wav"].items():
        output_path = join(args.output_dir, key, "audio_mix.wav")
        copy_file(input_path, output_path)
    
    # vad
    # data_load = DataLoad("output/vad/")
    # for key, input_path in data_load["vad_expert.txt"].items():
    #     output_path = join(args.output_dir, key, "vad_expert.txt")
    #     copy_file(input_path, output_path)
    
    # for key, input_path in data_load["vad_novice.txt"].items():
    #     output_path = join(args.output_dir, key, "vad_novice.txt")
    #     copy_file(input_path, output_path)
    
    data_load = DataLoad("NoXiAnalysis/vad_annotation/")
    for key, input_path in data_load["vad_expert.txt"].items():
        output_path = join(args.output_dir, key, "vad_expert.txt")
        copy_file(input_path, output_path)
    
    for key, input_path in data_load["vad_novice.txt"].items():
        output_path = join(args.output_dir, key, "vad_novice.txt")
        copy_file(input_path, output_path)
    
    # non-verbal features
    # data_load_openface = DataLoad("output/openface/")
    # data_load_openpose = DataLoad("output/openpose/")
    # for key, openface_path in data_load_openface["video_expert_openface.csv"].items():
    #     openpose_path = data_load_openpose["video_expert_openpose.csv"][key]
    #     output_path = join(args.output_dir, key, "non_varbal_expert.csv")
    #     os.makedirs(dirname(output_path), exist_ok=True)
    #     multimodal_features = create_multimodal_features(openface_path, openpose_path)
    #     print(output_path)
    #     multimodal_features.to_csv(output_path)

    # for key, openface_path in data_load_openface["video_novice_openface.csv"].items():
    #     openpose_path = data_load_openpose["video_novice_openpose.csv"][key]
    #     output_path = join(args.output_dir, key, "non_varbal_novice.csv")
    #     os.makedirs(dirname(output_path), exist_ok=True)
    #     multimodal_features = create_multimodal_features(openface_path, openpose_path)
    #     print(output_path)
    #     multimodal_features.to_csv(output_path)
