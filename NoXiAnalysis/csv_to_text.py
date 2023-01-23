import os
from os.path import join
import sys
import wave
import re
import csv

def _createTxt(file_name, start, end, label):
    txt = f"{file_name} {start:.6f} {end:.6f} [{label}]"
    return txt

def createVadList(vad, end_time, basename_without_ext):
    vad_list = []
    buf = 0.0
    for va in vad:
        text = _createTxt(basename_without_ext, buf, va[0], "silence")
        vad_list.append(text)
        text = _createTxt(basename_without_ext, va[0], va[1], "speech")
        buf = va[1]
        vad_list.append(text)
    
    text = _createTxt(basename_without_ext, buf, end_time, "silence")
    vad_list.append(text)
    
    return vad_list


if __name__ == "__main__":
    args = sys.argv
    input_path = args[1]

    file_name = os.path.splitext(os.path.basename(input_path))[0]
    num = "".join(re.sub(r"\D", "", file_name))
    user = "".join(re.findall('[a-z]+', file_name))

    if user == "e":
        output_path = f"NoXiAnalysis/vad_using_opensmile/Paris_{num.zfill(2)}/vad_expert.txt"
        audio_path = f"NoXiAnalysis/data/Paris_{num.zfill(2)}/audio_expert.wav"
    elif user == "n":
        output_path = f"NoXiAnalysis/vad_using_opensmile/Paris_{num.zfill(2)}/vad_novice.txt"
        audio_path = f"NoXiAnalysis/data/Paris_{num.zfill(2)}/audio_novice.wav"

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with wave.open(audio_path,  'rb') as wr:
        fr = wr.getframerate()
        fn = wr.getnframes()
        end_time = 1.0 * fn / fr

    basename_without_ext = os.path.splitext(os.path.basename(audio_path))[0]

    vad = []
    with open(input_path) as f:
        reader = csv.reader(f)
        for line in reader:
            vad.append([float(line[0]), float(line[1])])
    
    vad_list = createVadList(vad, end_time, basename_without_ext)

    with open(output_path, "w") as f:
        for d in vad_list:
            f.write("%s\n" % d)
            
            
