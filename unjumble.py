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

gray_list = []
for frame in all_frames:
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_list.append(gray)

def calc_mse(img1, img2):
    return np.mean((img1.astype("float") - img2.astype("float")) ** 2)

print("Analyzing frame similarities...")
num_frames = len(gray_list)
similarity = np.zeros((num_frames, num_frames))

for i in tqdm(range(num_frames)):
    for j in range(i + 1, num_frames):
        diff = calc_mse(gray_list[i], gray_list[j])
        similarity[i][j] = diff
        similarity[j][i] = diff

np.fill_diagonal(similarity, np.inf)

mean_diff = np.mean(similarity, axis=1)
first_frame = np.argmax(mean_diff)
print(f"Possible first frame: {first_frame}")

used = set([first_frame])
sequence = [first_frame]

print("Reordering frames...")
for _ in tqdm(range(num_frames - 1)):
    last = sequence[-1]
    next_frame = np.argmin(similarity[last])
    while next_frame in used:
        similarity[last][next_frame] = np.inf
        next_frame = np.argmin(similarity[last])
    sequence.append(next_frame)
    used.add(next_frame)

def refine_sequence(seq):
    fixed = seq.copy()
    for i in range(1, len(fixed) - 1):
        prev = gray_list[fixed[i - 1]]
        curr = gray_list[fixed[i]]
        nxt = gray_list[fixed[i + 1]]
        if calc_mse(prev, nxt) < calc_mse(prev, curr):
            fixed[i], fixed[i + 1] = fixed[i + 1], fixed[i]
    return fixed

sequence = refine_sequence(sequence)

