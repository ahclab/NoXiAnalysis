from pyannote.audio import Pipeline
from pyannote.audio import Model
from pyannote.audio.pipelines import VoiceActivityDetection
import os
import wave

from NoXiAnalysis.utils.utils import read_vadtxt_to_list, evaluate_vad


def _createTxt(file_name, start, end, label):
    txt = f"{file_name} {start:.6f} {end:.6f} [{label}]"
    return txt

# def _evaluate():


def pyannoteVAD(input_path, output_path):
    basename_without_ext = os.path.splitext(os.path.basename(input_path))[0]

    # pipeline = Pipeline.from_pretrained("pyannote/voice-activity-detection")
    model = Model.from_pretrained(
        "pyannote/segmentation", use_auth_token="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"
    )
    pipeline = VoiceActivityDetection(segmentation=model)
    HYPER_PARAMETERS = {
        "onset": 0.5,
        "offset": 0.5,  # onset/offset activation thresholds
        "min_duration_on": 0.0,  # remove speech regions shorter than that many seconds.
        "min_duration_off": 0.0,  # fill non-speech regions shorter than that many seconds.
    }
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


if __name__ == "__main__":
    # pyannoteVAD("./NoXiAnalysis/data/Paris_01/audio_expert.wav", "./test.txt")
    va_frame = read_vadtxt_to_list("./test.txt")
    evaluate_vad(va_frame, va_frame)
