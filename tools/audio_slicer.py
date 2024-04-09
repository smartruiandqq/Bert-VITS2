import librosa  # Optional. Use any library you like to read audio files.
import soundfile  # Optional. Use any library you like to write audio files.

import shutil
import os
import webbrowser
import subprocess
import datetime
import json
import os


"""
# 单个音频文件切分
"""

model_name = "lc"

from slicer2 import Slicer

audio_path = "./audio"
audio_files =  f"{audio_path}/20240116_180017.wav"

audio, sr = librosa.load(audio_files, sr=None, mono=False)  # Load an audio file with librosa.
slicer = Slicer(
    sr=sr,
    threshold=-40,
    min_length=2000,
    min_interval=300,
    hop_size=10,
    max_sil_kept=500
)
chunks = slicer.slice(audio)
print(chunks)
for i, chunk in enumerate(chunks):
    if len(chunk.shape) > 1:
        chunk = chunk.T  # Swap axes if the audio is stereo.
    soundfile.write(f'{audio_path}/{model_name}_{i}.wav', chunk, sr)  # Save sliced audio files with soundfile.

#if os.path.exists(f'./Data/{model_name}/raw/{model_name}/{model_name}.wav'):  # 如果文件存在
    #os.remove(f'./Data/{model_name}/raw/{model_name}/{model_name}.wav')  