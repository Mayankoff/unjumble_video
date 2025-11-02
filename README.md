## ⚙️ How to Run the Code

### 1. Install Required Libraries
Make sure you have Python 3.8+ and install the needed libraries:

```bash
pip install opencv-python numpy tqdm

Change video path accordingly

# Video Reconstruction from Jumbled Frames

This project tries to fix a jumbled video and arrange the frames back in the correct order.  
The idea is to compare every frame with all others, check how similar or different they are, and then arrange them in a way that looks smooth like the original video.

---

## Algorithm Explanation

### My Approach
When I got the jumbled video, my first thought was to find some way to measure how similar two frames are.  
If two frames look almost the same, they are probably next to each other in the original video.  
So I decided to use a simple mathematical method instead of any complex AI model.

### Techniques Used
I used **Mean Squared Error (MSE)** to check how different two frames are.  
Basically, I convert each frame into grayscale (so it’s easier and faster to compare) and then calculate the average squared difference of pixel values between two frames.

- **Lower MSE** → Frames are very similar (most likely consecutive).  
- **Higher MSE** → Frames are far apart or unrelated.

I store all these differences in a matrix and use that to rebuild the video.

### Steps I Followed
1. **Extract frames** from the jumbled video using OpenCV.  
2. **Convert frames to grayscale** to make the comparison faster.  
3. **Compare every frame with every other frame** using MSE and store the results.  
4. **Find the starting frame** — usually the one least similar to all others.  
5. **Rebuild the sequence** using a greedy approach: always choose the next frame with the smallest difference.  
6. **Do a small correction pass** to fix misplaced frames by swapping if it improves smoothness.  
7. **Check forward or reverse direction**, whichever looks smoother is chosen automatically.  
8. **Save the final arranged frames** back into a proper video file.

### Why I Used This Method
I chose this because it’s simple, doesn’t need any AI training, and I could easily understand what’s happening step by step.  
It’s a good balance between logic and coding — something I can actually explain in a viva.

### Design Points
- **Accuracy:** Works best for smooth motion videos (like walking, driving, etc.).  
- **Time Complexity:** Around O(n²) because every frame is compared with every other frame.  
- **Parallelism:** Currently single-threaded, but could be made faster with multiprocessing.  
- **Memory:** Needs to load all frames and a big similarity matrix, so not ideal for very large videos.

---