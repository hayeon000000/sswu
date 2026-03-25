import matplotlib.pyplot as plt
import csv
import os
import numpy as np
import cv2
from matplotlib import font_manager, rc

if os.name == 'nt':
    font_path = "C:/Windows/Fonts/malgun.ttf"
    font_name = font_manager.FontProperties(fname=font_path).get_name()
    rc('font', family=font_name)

script_dir = os.path.dirname(__file__)
data_file_path = os.path.join(script_dir, '자료구조6조.csv')
output_mp4 = os.path.join(script_dir, 'stack_animation.mp4')

words = ["벚꽃", "필기구", "햇살", "개강", "피크닉", "디저트"]

scenario = [("Stack Init", [])]
temp_stack = []
for w in words:
    temp_stack.append(w)
    scenario.append((f"stack.push('{w}')", list(temp_stack)))

if temp_stack:
    scenario.append((f"stack.top()", list(temp_stack)))

for _ in range(2):
    if temp_stack:
        p = temp_stack.pop()
        scenario.append((f"stack.pop()", list(temp_stack)))

fig, ax = plt.subplots(figsize=(6, 8), dpi=100)
frames = []

for cmd, current_stack in scenario:
    ax.clear()
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 11)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(cmd, fontsize=18, pad=20)

    for i, word in enumerate(current_stack):
        rect = plt.Rectangle((2, i+1), 6, 0.8, ec='deepskyblue', fc='white', lw=2)
        ax.add_patch(rect)
        ax.text(5, i+1.4, word, ha='center', va='center', fontsize=14)

    ax.plot([2, 8], [1, 1], color='black', lw=3)

    fig.canvas.draw()
    rgba_buffer = fig.canvas.buffer_rgba()
    img = np.array(rgba_buffer)
    img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
    frames.append(img)

height, width, _ = frames[0].shape
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video = cv2.VideoWriter(output_mp4, fourcc, 0.5, (width, height))

for frame in frames:
    video.write(frame)

video.release()
plt.close()

print(f" {output_mp4}")