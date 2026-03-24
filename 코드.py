import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import time

plt.rc('font', family='Malgun Gothic') 
plt.rcParams['axes.unicode_minus'] = False

try:
    df = pd.read_csv('자료.csv', encoding='cp949')
    all_words = []
    for col in ['단어1', '단어2', '단어3']:
        all_words.extend(df[col].dropna().tolist())
except FileNotFoundError:
    print("오류: '자료.csv' 파일을 찾을 수 없습니다.")
    exit()


stack = []

fig, ax = plt.subplots(figsize=(10, 7))
fig.canvas.manager.set_window_title('자료구조 스택 시각화 - 양시언')

def draw_stack(op_type, val=None):
    ax.clear()
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)
    ax.axis('off')
    
    display_text = ""
    if op_type == "PUSH":
        display_text = f'stack.push("{val}")'
    elif op_type == "POP":
        display_text = f'stack.pop() -> "{val}"'
    elif op_type == "TOP":
        display_text = f'stack.top() -> "{val}"'
    else:
        display_text = op_type

    ax.text(1, 10, display_text, fontsize=22, fontweight='bold', color='black', va='top')
    
    ax.plot([6, 6, 9, 9], [11, 1, 1, 11], color='black', lw=3)
    for y in range(2, 11):
        ax.plot([6, 9], [y, y], color='gray', linestyle=':', lw=1)

    for i, item in enumerate(stack):
        rect = patches.Rectangle((6.1, i + 1.1), 2.8, 0.8, facecolor='#77DD77', edgecolor='none')
        ax.add_patch(rect)
        ax.text(7.5, i + 1.5, str(item), fontsize=13, ha='center', va='center', fontweight='bold')

    plt.draw()
    plt.pause(1.0)

draw_stack("stack = [] (시작)")

for i in range(8):
    stack.append(all_words[i])
    draw_stack("PUSH", all_words[i])

draw_stack("TOP", stack[-1])

for _ in range(4):
    popped = stack.pop()
    draw_stack("POP", popped)

for i in range(8, 14):
    stack.append(all_words[i])
    draw_stack("PUSH", all_words[i])

for _ in range(5):
    popped = stack.pop()
    draw_stack("POP", popped)

for i in range(14, len(all_words)):
    stack.append(all_words[i])
    draw_stack("PUSH", all_words[i])

draw_stack("TOP", stack[-1])
draw_stack("모든 연산 및 단어 처리 완료")
plt.show()
