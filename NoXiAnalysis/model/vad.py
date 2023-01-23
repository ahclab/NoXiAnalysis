from pyannote.audio import Pipeline
from pyannote.audio import Model
from pyannote.audio.pipelines import VoiceActivityDetection
from sklearn.metrics import confusion_matrix
import os
import wave


def _createTxt(file_name, start, end, label):
    txt = f"{file_name} {start:.6f} {end:.6f} [{label}]"
    return txt


def pyannoteVAD(input_path, output_path, hyper_parameters = None):
    basename_without_ext = os.path.splitext(os.path.basename(input_path))[0]
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # pipeline = Pipeline.from_pretrained("pyannote/voice-activity-detection")
    model = Model.from_pretrained(
        "pyannote/segmentation", use_auth_token="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"
    )
    pipeline = VoiceActivityDetection(segmentation=model)
    if hyper_parameters == None:
        HYPER_PARAMETERS = {
            "onset": 0.95,
            "offset": 0.95,  # onset/offset activation thresholds
            "min_duration_on": 0.0,  # remove speech regions shorter than that many seconds.
            "min_duration_off": 0.0,  # fill non-speech regions shorter than that many seconds.
        }
    else:
        HYPER_PARAMETERS = hyper_parameters
    pipeline.instantiate(HYPER_PARAMETERS)

    with wave.open(input_path,  'rb') as wr:
        fr = wr.getframerate()
        fn = wr.getnframes()
        end_time = 1.0 * fn / fr

    vad = pipeline(input_path)

    vad_list = []
    firstLoop = True
    time_buf = 0.0
    for turn, _, _ in vad.itertracks(yield_label=True):
        if firstLoop:
            firstLoop = False
            time_buf = turn.end

            if turn.start == 0.0:
                text = _createTxt(basename_without_ext, turn.start, turn.end, "speech")
                vad_list.append(text)
            else:
                text = _createTxt(basename_without_ext, 0, turn.start, "silence")
                vad_list.append(text)
                text = _createTxt(basename_without_ext, turn.start, turn.end, "speech")
                vad_list.append(text)

        else:
            text = _createTxt(basename_without_ext, time_buf, turn.start, "silence")
            vad_list.append(text)
            text = _createTxt(basename_without_ext, turn.start, turn.end, "speech")
            vad_list.append(text)
            time_buf = turn.end
    
    text = _createTxt(basename_without_ext, time_buf, end_time, "silence")
    vad_list.append(text)


    with open(output_path, "w") as f:
        for d in vad_list:
            f.write("%s\n" % d)

def read_vadtxt_to_list(path):
    f = open(path)
    vad_list = []
    for line in f:
        if "speech" in line:
            content = line.split()
            vad_list.append([round(float(content[1]), 2), round(float(content[2]), 2)])
        end_time = round(float(line.split()[2]), 2)
    
    f.close()

    frame_num = end_time*100.00
    onehot_vad_list = [0]*int(frame_num)

    for va in vad_list:
        s = int(va[0]*100)
        e = int(va[1]*100)
        onehot_vad_list[s:e] = [1]*(e-s)


    return onehot_vad_list

def evaluate_vad(label, pred):
    label = label[:len(pred)]
    pred = pred[:len(label)]
    cm = confusion_matrix(label, pred)
    tn, fp, fn, tp = cm.flatten()
    acc = (tn + tp) / (tn + tp + fn + fp)
    recall = tp / (tp + fn)
    precision = tp / (tp + fp)
    f1 = 2* (recall * precision) / (recall + precision)
    # print(f"acc: {acc}")
    # print(f"recall: {recall}")
    # print(f"precision: {precision}")
    # print(f"f1: {f1}")

    return acc, recall, precision, f1


if __name__ == "__main__":
    # pyannoteVAD("./NoXiAnalysis/data/Paris_01/audio_expert.wav", "./test.txt")
    pred = read_vadtxt_to_list("./test.txt")
    label = read_vadtxt_to_list("./NoXiAnalysis/vad_annotation/Paris_01/vad_expert.txt")
    evaluate_vad(label, pred)
