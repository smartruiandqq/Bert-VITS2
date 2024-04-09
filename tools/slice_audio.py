import librosa  # Optional. Use any library you like to read audio files.
import soundfile  # Optional. Use any library you like to write audio files.
import os,sys,numpy as np
import traceback


from slicer2 import Slicer

# 输入路径，输出路径，
#threshold:音量小于这个值视作静音的备选切割点 , -34
#min_length:每段最小多长，如果第一段太短一直和后面段连起来直到超过这个值,4000
#min_interval:最短切割间隔 , 300
#hop_size:怎么算音量曲线，越小精度越大计算量越高（不是精度越大效果越好）, 10
#max_sil_kept:切完后静音最多留多长 ,500
#max:归一化后最大值多少 value=0.9
#alpha 混多少比例归一化后音频进来,value=0.25


def slice(inp, opt_root,threshold = -34,min_length = 4000,min_interval = 300,hop_size = 10,max_sil_kept = 500,_max = 0.9, alpha = 0.25,i_part = 0,all_part = 1) :
    os.makedirs(opt_root,exist_ok=True)
    if os.path.isfile(inp):
        input=[inp]
    elif os.path.isdir(inp):
        input=[os.path.join(inp, name) for name in sorted(list(os.listdir(inp)))]
    else:
        return "输入路径存在但既不是文件也不是文件夹"
    slicer = Slicer(
        sr = 32000,  # 长音频采样率
        threshold=      int(threshold),  # 音量小于这个值视作静音的备选切割点
        min_length=     int(min_length),  # 每段最小多长，如果第一段太短一直和后面段连起来直到超过这个值
        min_interval=   int(min_interval),  # 最短切割间隔
        hop_size=       int(hop_size),  # 怎么算音量曲线，越小精度越大计算量越高（不是精度越大效果越好）
        max_sil_kept=   int(max_sil_kept),  # 切完后静音最多留多长
    )
    _max=float(_max)
    alpha=float(alpha)
    for inp_path in input[int(i_part)::int(all_part)]:
        print(inp_path)
        try:
            name = os.path.basename(inp_path)
            audio_filename, audio_extension = os.path.splitext(name)

            if audio_extension.lower() in ['.mp3', '.wav']:
                audio, sr = librosa.load(inp_path, sr = 32000, mono = False)  # Load an audio file with librosa.
                chunks = slicer.slice(audio)
                for i, chunk in enumerate(chunks):
                    if len(chunk.shape) > 1:
                        chunk = chunk.T  # Swap axes if the audio is stereo.
                    soundfile.write(f'{opt_root}/{audio_filename}_{i}.wav', chunk, sr)  # Save sliced audio files with soundfile.

        except:
            print(inp_path,"->fail->",traceback.format_exc())
    return "执行完毕，请检查输出文件"

if __name__ == "__main__":
    slice("audio","audio_output")
#print(slice(*sys.argv[1:]))
