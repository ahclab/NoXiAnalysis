import subprocess
import os
import wave
from os.path import join
import argparse
import pandas as pd
import csv
from os.path import dirname
import torch
from decimal import Decimal, ROUND_HALF_UP
from pprint import pprint

from NoXiAnalysis.utils.dataload import DataLoad
from NoXiAnalysis.utils.utils import copy_file, mv_file

from torchaudio.backend.sox_io_backend import info as info_sox
from vap_turn_taking import VAP, TurnTakingMetrics

def get_audio_duration(audio_path):
    info = info_sox(audio_path)
    return info.num_frames / info.sample_rate


def read_txt(path, encoding="utf-8"):
    data = []
    with open(path, "r", encoding=encoding) as f:
        for line in f.readlines():
            data.append(line.strip())
    return data

def time_to_frame(t, hz: int):
    return int(Decimal(str(float(t) * hz)).quantize(Decimal("0"),rounding=ROUND_HALF_UP))

def create_one_hot_vec(path, hz=25):
    trans_list = read_txt(path)

    audio_path = join(dirname(path).replace("vad_by_human", "mix_audio"), "audio_mix.wav")
    tensor_size = time_to_frame(get_audio_duration(audio_path), hz)
    vad_tensor = torch.zeros(tensor_size)

    for row in trans_list:
        utt_idx, utt_start, utt_end, *words = row.split(" ")

        if words[0] in "[speech]":
            s = time_to_frame(utt_start, hz)
            e = time_to_frame(utt_end, hz)
            vad_tensor[s:e] = 1.0
        else:
            pass

    return vad_tensor


def count_events(vad_tensor):
    event_count = 0
    in_sequence = False

    for i in range(vad_tensor.size(1)):
        if vad_tensor[0][i] == 1 and not in_sequence:
            event_count += 1
            in_sequence = True
        elif vad_tensor[0][i] == 0 and in_sequence:
            in_sequence = False

    return event_count

if __name__ == "__main__":
    metric = TurnTakingMetrics(
        hs_kwargs=dict(
            post_onset_shift=1,
            pre_offset_shift=1,
            post_onset_hold=1,
            pre_offset_hold=1,
            non_shift_horizon=2,
            metric_pad=0.05,
            metric_dur=0.1,
            metric_pre_label_dur=0.2,
            metric_onset_dur=0.2),
        bc_kwargs=dict(
            max_duration_frames=1.0,
            pre_silence_frames=1.0,
            post_silence_frames=2.0,
            min_duration_frames=0.2,
            metric_dur_frames=0.2,
            metric_pre_label_dur=0.5),
        metric_kwargs=dict(
            pad=0.05,
            dur=0.1,
            pre_label_dur=0.5,
            onset_dur=0.2,
            min_context=3.0),
        threshold_pred_shift=0.5,
        threshold_short_long=0.3,
        threshold_bc_pred=0.1,
        shift_pred_pr_curve=False,
        bc_pred_pr_curve=False,
        long_short_pr_curve=False,
        frame_hz=25,
    )

    data_load = DataLoad("output/vad_by_human/")
    # events_count_dict = {key: [] for key in (
    #     "key",
    #     "shift_expert", "hold_expert", "short_expert", "long_expert",
    #     "predict_shift_pos_expert", "predict_shift_neg_expert",
    #     "predict_bc_pos_expert", "predict_bc_neg_expert",
    #     "shift_novice", "hold_novice", "short_novice", "long_novice",
    #     "predict_shift_pos_novice", "predict_shift_neg_novice",
    #     "predict_bc_pos_novice", "predict_bc_neg_novice",
    #     "shift", "hold", "short", "long",
    #     "predict_shift_pos", "predict_shift_neg",
    #     "predict_bc_pos", "predict_bc_neg", "duration", "toral_frame", "expert_active_frame", "novice_active_frame", "overlap", "pose"
    # )}

    # for key, input_path in data_load["vad_expert.txt"].items():
    #     print(key)
    #     expert_vad_tensor = create_one_hot_vec(input_path)
    #     novice_vad_tensor = create_one_hot_vec(input_path.replace("expert", "novice"))

    #     vad_tensor = torch.stack([expert_vad_tensor, novice_vad_tensor], dim=0).unsqueeze(-1).transpose(0, 2)
    #     events_count_dict["key"].append(key)

    #     audio_path = join(dirname(input_path).replace("vad_by_human", "mix_audio"), "audio_mix.wav")
    #     events_count_dict["duration"] += [get_audio_duration(audio_path)]
    #     events_count_dict["toral_frame"] += [time_to_frame(get_audio_duration(audio_path), 25)]
    #     events_count_dict["expert_active_frame"] += [int(torch.sum(expert_vad_tensor == 1))]
    #     events_count_dict["novice_active_frame"] += [int(torch.sum(novice_vad_tensor == 1))]
    #     events_count_dict["overlap"] += [int(torch.sum((expert_vad_tensor == 1) & (novice_vad_tensor == 1)))]
    #     events_count_dict["pose"] += [int(torch.sum((expert_vad_tensor == 0) & (novice_vad_tensor == 0)))]

    #     events = metric.extract_events(va=vad_tensor)
    #     for event_key, value in events.items():
    #         expert = value[:, :, 0]
    #         novice = value[:, :, 1]

    #         expert_count = count_events(expert)
    #         novice_count = count_events(novice)
    #         total_count = expert_count + novice_count

    #         events_count_dict[f"{event_key}_expert"].append(expert_count)
    #         events_count_dict[f"{event_key}_novice"].append(novice_count)
    #         events_count_dict[f"{event_key}"].append(total_count)
        
    
    # headers = list(events_count_dict.keys())
    # num_rows = len(events_count_dict[headers[0]])

    # with open('output/noxi_analysis.csv', 'w', newline='', encoding='utf-8') as csvfile:
    #     writer = csv.DictWriter(csvfile, fieldnames=headers)
    #     writer.writeheader()
    #     for i in range(num_rows):
    #         row = {header: events_count_dict[header][i] for header in headers}
    #         writer.writerow(row)

    label_analysis = {"index": list(range(256))}

    vap = VAP(
        type="discrete",
        bin_times=[0.2, 0.4, 0.6, 0.8],
        frame_hz=25,
        pre_frames=2,
        threshold_ratio=0.5,
    )
    window_size = 300
    slide_step = 12
    index_count = [0] * 256

    for key, input_path in data_load["vad_expert.txt"].items():
        print(key)
        expert_vad_tensor = create_one_hot_vec(input_path)
        novice_vad_tensor = create_one_hot_vec(input_path.replace("expert", "novice"))

        vad_tensor = torch.stack([expert_vad_tensor, novice_vad_tensor], dim=0).unsqueeze(-1).transpose(0, 2)

        _, input_length, _ = vad_tensor.size()

        # スライドしながらサブテンソルを抽出する操作を実行
        sub_tensors = []
        for i in range(0, input_length - window_size + 1, slide_step):
            sub_tensor = vad_tensor[:, i:i+window_size, :]
            sub_tensors.append(sub_tensor)

        vad_batch = torch.cat(sub_tensors, dim=0)
        va_labels = vap.extract_label(va=vad_batch)[:,-1].reshape(-1,1).squeeze(dim=1)
        count = [0] * 256

        for i in va_labels:
            count[i] += 1
            index_count[i] += 1
        
        label_analysis[key] = count

    label_analysis["num"] = index_count
    
    headers = list(label_analysis.keys())
    num_rows = len(label_analysis[headers[0]])

    with open('output/label_analysis.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        for i in range(num_rows):
            row = {header: label_analysis[header][i] for header in headers}
            writer.writerow(row)