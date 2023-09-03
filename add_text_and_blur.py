# -*- coding: utf-8 -*-
import cv2
import os
import glob
import tqdm

from moviepy.editor import CompositeVideoClip
from moviepy.editor import TextClip
from moviepy.editor import VideoFileClip

video_dir = "./.video_tmp/"
texted_video_dir = "./.texted_video_tmp/"
blurred_video_dir = "./.blurred_video_tmp/"


def add_text_to_video(video_fn: str):
    # Get video clips for only starting 13 seconds.
    clip = VideoFileClip(video_fn).subclip(0, 13)
    txt_clip = TextClip("@adamzhou.eth", fontsize=18, color="white")
    txt_clip = txt_clip.set_pos("bottom").set_duration(13)
    final_clip = CompositeVideoClip([clip, txt_clip])
    final_clip.write_videofile(os.path.join(texted_video_dir, os.path.basename(video_fn)[:-4] + "_with_text" + ".mp4"))


def add_blur_to_video(video_fn: str):
    # Get video clips for only starting 13 seconds.
    clip = VideoFileClip(video_fn).subclip(0, 13)
    w, h = clip.w, clip.h
    print(f"video w == {w}, h == {h}")

    def blur(image):
        frame = image.copy()
        bbox = [807, 0, 1076, 120]
        blured = cv2.blur(frame, (int(frame.shape[0] * .05), int(frame.shape[0] * .05)))
        blured_roi = blured[int(bbox[1]):int(bbox[1] + bbox[3]), int(bbox[0]):int(bbox[0] + bbox[2])]
        frame[int(bbox[1]):int(bbox[1] + bbox[3]), int(bbox[0]):int(bbox[0] + bbox[2])] = blured_roi
        return frame

    final_clip = clip.fl_image(blur)
    final_clip.write_videofile(os.path.join(blurred_video_dir, os.path.basename(video_fn)[:-4] + "_with_blur" + ".mp4"))


if __name__ == "__main__":

    videos = glob.glob(os.path.join(video_dir, "*.mp4"))
    videos = sorted(videos, reverse=False)
    for video in tqdm.tqdm(videos):
        print(f"add text to video:{video}")
        add_text_to_video(video)

    videos = glob.glob(os.path.join(texted_video_dir, "*.mp4"))
    videos = sorted(videos, reverse=False)
    for video in tqdm.tqdm(videos):
        print(f"add blur to video:{video}")
        add_blur_to_video(video)
