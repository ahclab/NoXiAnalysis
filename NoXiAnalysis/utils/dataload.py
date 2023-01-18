import os
import copy
import sys
from os.path import join
from NoXiAnalysis.utils.utils import repo_root, read_txt


class DataLoad:
    def __init__(self, repo = None):
        self.folder_name_list = read_txt(join(repo_root(), "config/folder_name.txt"))
        self.path_dict = {}
        self.repo = repo

    def _file_path_load(self, name):
        for folder_name in self.folder_name_list:
            if self.repo == None:
                file_path = join(repo_root(), "data", folder_name, name)
            else:
                file_path = join(self.repo, folder_name, name)
            self.path_dict[folder_name] = file_path

    def __getitem__(self, name:str):
        self._file_path_load(name)
        path_dict = copy.copy(self.path_dict)
        return path_dict


if __name__ == "__main__":
    data_load = DataLoad()
    path_dict = data_load["audio_expert.wav"]
    print(path_dict)

    


