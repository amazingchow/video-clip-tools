# -*- coding: utf-8 -*-
import glob
import os
import time

import stable_whisper
import tqdm
from moviepy.editor import AudioFileClip

video_dir = "./data/.video_tmp/"
audio_dir = "./data/.audio_tmp/"


def extract_audio_from_video(video_fn: str):
    my_audio_clip = AudioFileClip(video_fn)
    my_audio_clip.write_audiofile(os.path.join(audio_dir, os.path.basename(video_fn)[:-4] + ".wav"))


if __name__ == "__main__":
    # Step 1
    videos = glob.glob(os.path.join(video_dir, "*.mp4"))
    videos = sorted(videos, reverse=False)
    for video in tqdm.tqdm(videos):
        extract_audio_from_video(video)

    # Step 2
    audios = glob.glob(os.path.join(audio_dir, "*.wav"))
    audios += glob.glob(os.path.join(audio_dir, "*.mp3"))
    audios = sorted(audios, reverse=False)

    print("[进行中] 加载 whisper small.en 模型...")
    st = time.time()
    model = stable_whisper.load_model(name="small.en",
                                      device="cpu",
                                      download_root="./.whisper_model",
                                      in_memory=True)
    ed = time.time()
    print(f"[已完成] 加载 whisper small.en 模型, 耗时: {ed - st:.1f} 秒.")

    for audio in tqdm.tqdm(audios):
        print(f"[进行中] 音频文件({audio})使用 whisper small.en 模型处理...")
        result = model.transcribe(audio,
                                  verbose=True,
                                  word_timestamps=True,
                                  **{"language": "en", "beam_size": 5})
        print(f"[已完成] 音频文件({audio})使用 whisper small.en 模型处理.")
        
        print(f"[进行中] 保存音频文件({audio})的字幕文件...")
        result.to_srt_vtt(os.path.join("./.srt_files", os.path.basename(audio)[:-4] + ".srt"), segment_level=True, word_level=False)
        print(f"[已完成] 保存音频文件({audio})的字幕文件.")
