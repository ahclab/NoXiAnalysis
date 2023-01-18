from os.path import dirname
from sklearn.metrics import confusion_matrix

process_num_gpu0 = 0
process_num_gpu1 = 0

def repo_root():
    """
    Returns the absolute path to the git repository
    """
    root = dirname(__file__)
    root = dirname(root)
    return root

def read_txt(path):
    f = open(path)
    contents = f.read().split()
    f.close()
    return contents

def copy_file(input_path, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cmd = "cp {input_path} {output_path}".format(input_path=input_path, output_path=output_path)
    print(cmd)
    # subprocess.call(cmd, shell=True)

def _is_num(s):
    try:
        float(s)
    except ValueError:
        return False
    else:
        return True

def read_vadtxt_to_list(path):
    f = open(path)
    vad_list = []
    for line in f:
        if "speech" in line:
            content = line.split()
            vad_list.append([round(float(content[1]), 2), round(float(content[2]), 2)])
        end_time = round(float(line.split()[2]), 2)
    
    f.close()

    onehot_vad_list = [0]*int(end_time*100)

    flag = False
    for va in vad_list:
        onehot_vad_list[int(va[0]*100):int(va[1]*100)] = [1]*int(va[1]*100-va[0]*100)
    
    # print(onehot_vad_list)

    return onehot_vad_list

def evaluate_vad(lable, pred):
    cm = confusion_matrix(lable, pred)
    tn, fp, fn, tp = cm.flatten()
    acc = (tn + tp) / (tn + tp + fn + fp)
    recall = tp / (tp + fn)
    precision = tp / (tp + fp)
    f1 = 2* (recall * precision) / (recall + precision)
    print(acc)
    print(recall)
    print(precision)
    print(f1)
