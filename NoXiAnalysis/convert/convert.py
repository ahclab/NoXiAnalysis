import subprocess
import os
import sys
from os.path import join
import argparse
from pydub import AudioSegment
import librosa
import soundfile as sf
import numpy as np
from pysndfx import AudioEffectsChain

from NoXiAnalysis.utils.dataload import DataLoad

def reduceVideoResolution(input_path, output_path, width = 320):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cmd = f"ffmpeg -y -i {input_path} -vf scale={width}:-1 {output_path}"
    print(cmd)
    subprocess.call(cmd, shell=True)

def normalize_audio(audio, target_dBFS):
    difference = target_dBFS - audio.dBFS
    return audio.apply_gain(difference)

def audioMixing(expert_path, novice_path, output_path, target_dBFS=-20.0):
    print(output_path)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    sound1 = AudioSegment.from_file(expert_path, "wav")
    sound2 = AudioSegment.from_file(novice_path, "wav")

    # Normalize the volume of both audio files
    sound1_normalized = normalize_audio(sound1, target_dBFS)
    sound2_normalized = normalize_audio(sound2, target_dBFS)

    sound1_normalized.export(output_path.replace('audio_mix', 'audio_expert'), format="wav")
    sound2_normalized.export(output_path.replace('audio_mix', 'audio_novice'), format="wav")

    sound = sound1_normalized.overlay(sound2_normalized, position=0)

    sound.export(output_path, format="wav")

    
def reduceAudioNoise(input_path, output_path):
    print(input_path)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    y, sr = librosa.load(input_path)
    cent = librosa.feature.spectral_centroid(y=y, sr=sr)

    threshold_h = round(np.median(cent))*1.5
    threshold_l = round(np.median(cent))*0.1

    less_noise = AudioEffectsChain().lowshelf(gain=-30.0, frequency=threshold_l, slope=0.8).highshelf(gain=-12.0, frequency=threshold_h, slope=0.5)#.limiter(gain=6.0)
    y_clean = less_noise(y)
    sf.write(output_path, y_clean, sr, subtype="PCM_16")
