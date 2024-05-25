# -*- coding: utf-8 -*-
import glob
import os
import sys
from typing import List

import tqdm
from loguru import logger as loguru_logger
from moviepy.editor import AudioFileClip

video_dir = f"{os.getenv('DATA_STORAGE_DIR')}/.video_tmp/"
audio_dir = f"{os.getenv('DATA_STORAGE_DIR')}/.audio_tmp/"


def prepare_video_files() -> List[str]:
    if not os.path.exists(video_dir):
        os.makedirs(video_dir)
    videos = glob.glob(os.path.join(video_dir, "*.mp4"))
    videos = sorted(videos, reverse=False)
    return videos


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

    videos = prepare_video_files()
    if len(videos) == 0:
        loguru_logger.warning(
            "\n没有视频文件, 请选择以下两种备选方案:\n"
            f"1) 将视频文件放置在路径 '${video_dir}' 下.\n"
            "2) 选择其他路径下的视频文件.\n"
        )
        sys.exit(0)
    loguru_logger.info("视频文件列表:")
    for video in videos:
        loguru_logger.info(f"* {video}")

    for video in tqdm.tqdm(videos):
        loguru_logger.info(f"[进行中] 提取音频文件: {video}...")
        extract_audio_from_video(video)
        loguru_logger.info(f"[已完成] 提取音频文件: {video}.")
