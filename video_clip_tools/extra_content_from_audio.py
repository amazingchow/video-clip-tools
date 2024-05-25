# -*- coding: utf-8 -*-
import glob
import os
import sys
import time
from typing import List

import stable_whisper
import tqdm
from loguru import logger as loguru_logger
from moviepy.editor import AudioFileClip

audio_dir = f"{os.getenv('DATA_STORAGE_DIR')}/.audio_tmp/"


def prepare_audio_files() -> List[str]:
    if not os.path.exists(audio_dir):
        os.makedirs(audio_dir)
    audios = glob.glob(os.path.join(audio_dir, "*.wav"))
    audios += glob.glob(os.path.join(audio_dir, "*.mp3"))
    audios = sorted(audios, reverse=False)
    return audios


def extract_audio_from_video(video_fn: str):
    my_audio_clip = AudioFileClip(video_fn)
    my_audio_clip.write_audiofile(os.path.join(audio_dir, os.path.basename(video_fn)[:-4] + ".wav"))


if __name__ == "__main__":
    loguru_logger.remove()
    loguru_logger.add(
        sink=sys.stderr,
        level="DEBUG",
        format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | - <level>{message}</level>"
    )

    audios = prepare_audio_files()
    if len(audios) == 0:
        loguru_logger.warning(
            "\n没有音频文件, 请选择以下两种备选方案:\n"
            "1) 运行 extract_audio_from_video 函数提取音频文件.\n"
            f"2) 将音频文件放置在路径 '${audio_dir}' 下.\n"
        )
        sys.exit(0)
    loguru_logger.info("音频文件列表:")
    for audio in audios:
        loguru_logger.info(f"* {audio}")

    loguru_logger.info("[进行中] 加载 whisper small 模型...")
    st = time.time()
    model = stable_whisper.load_model(
        name="small",
        device="cpu",
        download_root=f"{os.getenv('DATA_STORAGE_DIR')}/.whisper_model",
        in_memory=True
    )
    ed = time.time()
    loguru_logger.info(f"[已完成] 加载 whisper small 模型, 耗时: {ed - st:.1f} 秒.")

    for audio in tqdm.tqdm(audios):
        loguru_logger.info(f"[进行中] 使用 whisper small 模型处理音频文件({audio})...")
        result = model.transcribe(
            audio,
            verbose=True,
            word_timestamps=True,
            **{"language": "zh", "beam_size": 5}
        )
        loguru_logger.info(f"[已完成] 音频文件({audio})处理完毕.")
        
        loguru_logger.info(f"[进行中] 保存音频文件({audio})的字幕文件...")
        result.to_srt_vtt(
            os.path.join(f"{os.getenv('DATA_STORAGE_DIR')}/.srt_files", os.path.basename(audio)[:-4] + ".srt"),
            segment_level=True,
            word_level=False
        )
        loguru_logger.info(f"[已完成] 已保存音频文件({audio})的字幕文件.")
