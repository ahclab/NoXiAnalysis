import subprocess
import os
from os.path import join
import argparse
import wave

from NoXiAnalysis.utils.dataload import DataLoad
from NoXiAnalysis.model.vad import pyannoteVAD
from NoXiAnalysis.model.vad import read_vadtxt_to_list, evaluate_vad

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--output_dir", default="output/vad_by_pyannote/")
    args = parser.parse_args()

    # label =[]
    # label += read_vadtxt_to_list("NoXiAnalysis/vad_annotation/Paris_01/vad_expert.txt")
    # label += read_vadtxt_to_list("NoXiAnalysis/vad_annotation/Paris_01/vad_novice.txt")
    # pred = []
    # pred += read_vadtxt_to_list("NoXiAnalysis/vad_using_opensmile/Paris_01/vad_expert.txt")
    # pred += read_vadtxt_to_list("NoXiAnalysis/vad_using_opensmile/Paris_01/vad_novice.txt")

    # acc, recall, precision, f1 = evaluate_vad(label, pred)

    # print(f"acc: {acc}")
    # print(f"recall: {recall}")
    # print(f"precision: {precision}")
    # print(f"f1: {f1}")

    # label = []
    # pred = []
    # hyper_parameters = {
    #     "onset": 0.95,
    #     "offset": 0.95,  # onset/offset activation thresholds
    #     "min_duration_on": 0.0,  # remove speech regions shorter than that many seconds.
    #     "min_duration_off": 0.0,  # fill non-speech regions shorter than that many seconds.
    # }

    # data_load = DataLoad(repo = "NoXiAnalysis/vad_annotation/", config = "config/annotation_done.txt")
    # for key, label_path in data_load["vad_expert.txt"].items():
    #     label += read_vadtxt_to_list(label_path)
        
    # for key, label_path in data_load["vad_novice.txt"].items():
    #     label += read_vadtxt_to_list(label_path)

    
    # data_load = DataLoad(config = "config/annotation_done.txt")
    # for key, input_path in data_load["audio_expert.wav"].items():
    #     output_path = join(args.output_dir, key, "vad_expert.txt")
    #     pyannoteVAD(input_path, output_path, hyper_parameters)
    #     pred += read_vadtxt_to_list(output_path)
    

    # for key, input_path in data_load["audio_novice.wav"].items():
    #     output_path = join(args.output_dir, key, "vad_novice.txt")
    #     pyannoteVAD(input_path, output_path, hyper_parameters)
    #     pred += read_vadtxt_to_list(output_path)
    
    # acc, recall, precision, f1 = evaluate_vad(label, pred)

    # print(f"acc: {acc}")
    # print(f"recall: {recall}")
    # print(f"precision: {precision}")
    # print(f"f1: {f1}")
    

    data_load = DataLoad()

    for key, input_path in data_load["audio_expert.wav"].items():
        output_path = join(args.output_dir, key, "vad_expert.txt")
        pyannoteVAD(input_path, output_path)

    for key, input_path in data_load["audio_novice.wav"].items():
        output_path = join(args.output_dir, key, "vad_novice.txt")
        pyannoteVAD(input_path, output_path)

    
    # label =[]
    # label += read_vadtxt_to_list("NoXiAnalysis/vad_annotation/Paris_01/vad_expert.txt")
    # label += read_vadtxt_to_list("NoXiAnalysis/vad_annotation/Paris_01/vad_novice.txt")
    # pred = []
    # pred += read_vadtxt_to_list("output/vad/Paris_01/vad_expert.txt")
    # pred += read_vadtxt_to_list("output/vad/Paris_01/vad_novice.txt")

    # acc, recall, precision, f1 = evaluate_vad(label, pred)

    # print(f"acc: {acc}")
    # print(f"recall: {recall}")
    # print(f"precision: {precision}")
    # print(f"f1: {f1}")
