# NoXiAnalysis

* **function**
  - Convert Video (1920×1080 -> 320×180)
  - Convert Audio (Remove Noise, Mix)
  - OpenFace
  - OpenPose
  - OpenSmile
  - Voice Activity Detection

## Environment
* Ubuntu 18.04 64bit
* Intel(R) Core(TM) i9-10900X CPU @ 3.70GHz
* RAM 128GB
* NVIDIA GeForce RTX 3090 24GB x2

## Installation
### Install NoXiAnalysis
* Clone the github repository: `git clone `
  - movement: `cd NoXiAnalysis`
* Create conda env: `conda create -n analysis python=3.8`
  - source env: `conda activate analysis`
* Install PyTorch: `conda install pytorch torchvision torchaudio pytorch-cuda=11.7 -c pytorch -c nvidia`
* Dependencies: 
  - Install requirements: `pip install -r requirements.txt`
  - Install repo: `pip install -e .`
* Data Placement:
  - NoXi Database:
  NoXiAnalysis/data/
    ├── Augsburg_01
    │   ├── audio_expert.wav
    │   ├── audio_novice.wav
    │   ├── video_expert.mp4
    │   └── video_novice.mp4
    ├── Augsburg_02
    │   ├── audio_expert.wav
    │   ├── audio_novice.wav
    │   ├── video_expert.mp4
    │   └── video_novice.mp4
    ├── Augsburg_03
    │   ├── audio_expert.wav
    │   ├── audio_novice.wav
    │   ├── video_expert.mp4
    │   └── video_novice.mp4
    ...
  
  - OpenPose Model: (https://drive.google.com/drive/folders/1JsvI4M4ZTg98fmnCZLFM-3TeovnCRElG)
  NoXiAnalysis/openpose/model/[PLACEMENT HERE]



## Run
### Convert Video to Low-pixel
**[NOTE]**  
"ffmpeg" installation is required. 
1. Convert Video

```bash
python NoXiAnalysis/convert_low-pixel_video.py
```

### Mix Expert and Novice audios
1. Mix Audio
```bash
python NoXiAnalysis/convert_mix_audio.py
```

### Remove Audio Noise
1. Noise Removal
```bash
python NoXiAnalysis/convert_remove_noise_audio.py
```

### Feature Extraction with Openface
**[NOTE]**  
"docker" installation is required. It is recommended to set up Docker rootless.
1. Container Creation and Launchdocker 
```bash
docker run -it --rm -v ./:/home/openface-build/data algebr/openface:latest
```
  - Download pip3: `curl https://bootstrap.pypa.io/pip/3.4/get-pip.py -o get-pip.py`
  - Install pip3: `python3 get-pip.py`
  - movement: `cd data`
  - Install Package: `pip3 install scikit-learn`
  - Install repo: `pip3 install -e .`

2. Feature Extraction
```bash
python3 NoXiAnalysis/feature_extraction_openface.py
```

3. Exit from Docker
  - Exit Container: `exit`
  - Exit Without Exiting the Container: `Ctrl+p Ctrl+q`

**[TIPS]**  
Enter the activated container: `docker exec -it [CONTAINER ID] /bin/bash`  
Confirmation of container status: `docker ps`  
Confirmation of the created image: `docker images`  
Deleting Containers: `docker rm -f [CONTAINER ID]`
Delete Images: `docker rmi -f [IMAGE ID]`

### Feature Extraction with Opensmile
1. Feature Extraction
```bash
python NoXiAnalysis/feature_extraction_opensmile.py
```

### Feature Extraction with Openpose
**[NOTE]**  
Depending on the GPU used, memory errors may occur.  
If this is the case, lower the number `if utils.process_num_gpu0 < 10:` in NoXiAnalysis/feature_extraction_openpose.py.
It is also assumed that two GPUs are installed.  
If you have only one, rewrite NoXiAnalysis/feature_extraction_openpose.py accordingly.  

1. Feature Extraction
```bash
python NoXiAnalysis/feature_extraction_openpose.py
```

### Voice Activity Detection
1. VA frame
```bash
python NoXiAnalysis/create_va_frame.py
```

### Create Data Folder
1. Copy File
```bash
python NoXiAnalysis/create_datafolder.py
```
