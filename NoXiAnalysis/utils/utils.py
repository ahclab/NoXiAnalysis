from os.path import dirname
import os

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
    os.makedirs(dirname(output_path), exist_ok=True)
    cmd = "cp {input_path} {output_path}".format(input_path=input_path, output_path=output_path)
    print(cmd)
    import subprocess
    subprocess.call(cmd, shell=True)

def mv_file(input_path, output_path):
    os.makedirs(dirname(output_path), exist_ok=True)
    cmd = "mv {input_path} {output_path}".format(input_path=input_path, output_path=output_path)
    print(cmd)
    import subprocess
    subprocess.call(cmd, shell=True)

def _is_num(s):
    try:
        float(s)
    except ValueError:
        return False
    else:
        return True
