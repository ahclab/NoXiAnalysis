import subprocess
import os
import sys
from os.path import join
import argparse
# import docker
import multiprocessing

from NoXiAnalysis.utils.utils import repo_root
from NoXiAnalysis.utils.dataload import DataLoad

def openfaceFeatureExtraction(input_path, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    output_dir = os.path.dirname(output_path)
    output_file = os.path.basename(output_path)
    cmd = "/home/openface-build/build/bin/FeatureExtraction -f {input_path} -pose -aus -gaze -out_dir {output_dir} -of {output_file}".format(input_path=input_path, output_dir=output_dir, output_file=output_file)
    print(cmd)
    subprocess.call(cmd, shell=True)

    # cli = docker.from_env()

    # # Delete old container if it's runninng
    # try:
    #     container = cli.containers.get('openface')
    #     container.stop()
    #     container.remove()
    # except:
    #     pass

    # print(repo_root())
    # out = cli.containers.run(
    #     image='algebr/openface', 
    #     command = cmd,
    #     auto_remove=True, 
    #     detach=False, 
    #     cpu_count=multiprocessing.cpu_count(),
    #     volumes = {"/ahc/work2/kazuyo-oni/NoXiAnalysis": {'bind': '/home/openface-build', 'mode': 'rw'}},
    #     name="openface",
    #     )
    
    # print(out)

