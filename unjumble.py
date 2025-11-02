import cv2
import numpy as np
from tqdm import tqdm

video_path = r"C:\Users\ymaya\OneDrive\Desktop\unjumble\jumbled_video.mp4"
output_file = "video_fixed.mp4"
video_fps = 30

cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print("Could not load video file. Check the path again.")
    exit()

total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
frame_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

all_frames = []
print(f"Reading {total_frames} frames...")

for i in tqdm(range(total_frames)):
    ret, frame = cap.read()
    if not ret:
        break
    all_frames.append(frame)

cap.release()
print("✅ Frames captured successfully!")

