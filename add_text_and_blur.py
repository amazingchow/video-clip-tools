# -*- coding: utf-8 -*-
import argparse
import cv2
import os
import glob
import tqdm

from colorama import Fore, Style
from moviepy.editor import CompositeVideoClip
from moviepy.editor import TextClip
from moviepy.editor import VideoFileClip
from typing import Tuple

video_dir = "./.video_tmp/"
cover_dir = "./.cover_tmp/"
blurred_video_dir = "./.blurred_video_tmp/"
texted_video_dir = "./.texted_video_tmp/"


def save_cover_from_video(video_fn: str):
    # Get video clips for only starting 2 seconds.
    clip = VideoFileClip(video_fn).subclip(0, 2)
    # Save a frame at 1 second.
    clip.save_frame(os.path.join(cover_dir, os.path.basename(video_fn)[:-4] + ".png"), t=1)


def add_blur_to_video(video_fn: str, n_duration: int = 3, rect: Tuple[int] = [0, 0, 0, 0]):
    # Get video clips for only starting N seconds.
    clip = VideoFileClip(video_fn).subclip(0, n_duration)

    def blur(image):
        frame = image.copy()
        bbox = rect
        blured = cv2.blur(frame, (int(frame.shape[0] * .05), int(frame.shape[0] * .05)))
        blured_roi = blured[int(bbox[1]):int(bbox[1] + bbox[3]), int(bbox[0]):int(bbox[0] + bbox[2])]
        frame[int(bbox[1]):int(bbox[1] + bbox[3]), int(bbox[0]):int(bbox[0] + bbox[2])] = blured_roi
        return frame

    final_clip = clip.fl_image(blur)
    final_clip.write_videofile(os.path.join(blurred_video_dir, os.path.basename(video_fn)[:-4] + "_with_blur" + ".mp4"))


def add_text_to_video(video_fn: str, n_duration: int = 3, text: str = "@adamzhou.eth"):
    # Get video clips for only starting N seconds.
    clip = VideoFileClip(video_fn).subclip(0, n_duration)
    txt_clip = TextClip(text, fontsize=18, color="white")
    txt_clip = txt_clip.set_pos("bottom").set_duration(n_duration)
    final_clip = CompositeVideoClip([clip, txt_clip])
    final_clip.write_videofile(os.path.join(texted_video_dir, os.path.basename(video_fn)[:-4] + "_with_text" + ".mp4"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Text and Blur Adding Utility")
    parser.add_argument("--action", type=str, help="action to perform: cover | text | blur", default="cover")
    parser.add_argument("--duration", type=int, help="The duration of the returned clip", default=3)
    parser.add_argument("--text", type=str, help="The text added to the returned clip", default="@adamzhou.eth")
    parser.add_argument("--blur_tx", type=int, help="The blurred area, top left x coordinate")
    parser.add_argument("--blur_ty", type=int, help="The blurred area, top left y coordinate")
    parser.add_argument("--blur_bx", type=int, help="The blurred area, bottom right x coordinate")
    parser.add_argument("--blur_by", type=int, help="The blurred area, bottom right y coordinate")
    args = parser.parse_args()
    action = args.action
    duration = args.duration
    text = args.text
    blur_tx = args.blur_tx
    blur_ty = args.blur_ty
    blur_bx = args.blur_bx
    blur_by = args.blur_by

    if action == "cover":
        print(f"{Fore.GREEN}-> Performing action: {action}\n{Style.RESET_ALL}")
        videos = glob.glob(os.path.join(video_dir, "*.mp4"))
        videos = sorted(videos, reverse=False)
        for video in tqdm.tqdm(videos):
            print(f"{Fore.GREEN}-> Saving cover from video: {video}\n{Style.RESET_ALL}")
            save_cover_from_video(video)
        print(f"{Fore.GREEN}-> Done action: {action}\n{Style.RESET_ALL}")
    elif action == "blur":
        print(f"{Fore.GREEN}-> Performing action: {action}\n{Style.RESET_ALL}")
        videos = glob.glob(os.path.join(video_dir, "*.mp4"))
        videos = sorted(videos, reverse=False)
        for video in tqdm.tqdm(videos):
            print(f"{Fore.GREEN}-> Adding blur to video: {video}\n{Style.RESET_ALL}")
            add_blur_to_video(video, duration, [blur_tx, blur_ty, blur_bx, blur_by])
        print(f"{Fore.GREEN}-> Done action: {action}\n{Style.RESET_ALL}")
    elif action == "text":
        print(f"{Fore.GREEN}-> Performing action: {action}\n{Style.RESET_ALL}")
        videos = glob.glob(os.path.join(blurred_video_dir, "*.mp4"))
        videos = sorted(videos, reverse=False)
        for video in tqdm.tqdm(videos):
            print(f"{Fore.GREEN}-> Adding text to video: {video}\n{Style.RESET_ALL}")
            add_text_to_video(video, duration, text)
        print(f"{Fore.GREEN}-> Done action: {action}\n{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}-> Unknown action: {action}\n{Style.RESET_ALL}")
