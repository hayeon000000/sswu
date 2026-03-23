import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

# [폰트 설정] Windows 사용자용 (Mac은 'AppleGothic' 사용)
plt.rc('font', family='Malgun Gothic') 
plt.rcParams['axes.unicode_minus'] = False

# 1. CSV 파일 읽기
df = pd.read_csv('자료구조6조.csv', encoding='cp949')
df.columns = df.columns.str.strip() 

# 2. 팀원들의 모든 단어 수집 (총 18개 단어)
words = []
for index, row in df.iterrows():
    words.extend([row['단어1'], row['단어2'], row['단어3']])

# 제약조건 3: stack 선언부터 시작할 것
stack = []

# --- 제약조건 시나리오 (크기 10 이하 유지, 모든 단어 및 연산 1번 이상 사용) ---
operations = []

# 1. 처음 8개 단어 PUSH (스택 크기 8)
for i in range(8):
    operations.append(('PUSH', words[i]))

# 2. TOP 확인
operations.append(('TOP', None))

# 3. 4개 POP (스택 크기 4)
for _ in range(4):
    operations.append(('POP', None))

# 4. 다음 6개 단어 PUSH (스택 크기 10 -> 제약조건 4 만족)
for i in range(8, 14):
    operations.append(('PUSH', words[i]))

# 5. TOP 확인
operations.append(('TOP', None))

# 6. 5개 POP (스택 크기 5)
for _ in range(5):
    operations.append(('POP', None))

# 7. 남은 4개 단어 PUSH (스택 크기 9, 총 18개 단어 모두 사용 완료)
for i in range(14, 18):
    operations.append(('PUSH', words[i]))

# 8. 마지막 TOP 확인 및 3개 POP
operations.append(('TOP', None))
for _ in range(3):
    operations.append(('POP', None))
# --------------------------------------------------------------------------

# 시각화 설정 (가로로 넓은 비율)
fig, ax = plt.subplots(figsize=(10, 6))
fig.canvas.manager.set_window_title('Stack Animation')

def update(frame):
    ax.clear()
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 11)
    ax.axis('off')
    
    # ★ 버그 수정: 매 프레임마다 스택을 비우고 현재 프레임까지 상태를 재계산 ★
    stack.clear()
    op_str = ""
    
    # 현재 프레임(frame)까지 연산을 다시 시뮬레이션
    for i in range(min(frame + 1, len(operations))):
        op, val = operations[i]
        if op == 'PUSH':
            stack.append(val)
            if i == frame: op_str = f'stack.push("{val}")'
        elif op == 'POP':
            if stack:
                popped = stack.pop()
                if i == frame: op_str = f'stack.pop()\n-> "{popped}"'
        elif op == 'TOP':
            if stack:
                if i == frame: op_str = f'stack.top()\n-> "{stack[-1]}"'
                
    # 애니메이션이 모든 연산을 마쳤을 때
    if frame >= len(operations):
        op_str = "모든 연산 종료"

    # [왼쪽 상단] 연산 텍스트 표시
    ax.text(0.5, 9.5, op_str, fontsize=22, fontweight='bold', color='#333333', va='top', ha='left')

    # [오른쪽] 스택 표 (단어만 들어가는 형태)
    # 스택 컨테이너 그리기 (x=6 ~ 9)
    ax.plot([6, 6], [0, 10], color='black', lw=3) # 왼쪽 벽
    ax.plot([9, 9], [0, 10], color='black', lw=3) # 오른쪽 벽
    ax.plot([6, 9], [0, 0], color='black', lw=3)  # 바닥
    
    # 스택 칸을 구분하는 연한 점선 (최대 10칸)
    for y in range(1, 11):
        ax.plot([6, 9], [y, y], color='gray', linestyle=':', lw=1)

    # 스택 내부 단어 채우기
    for i, item in enumerate(stack):
        # 파란색 배경 박스
        rect = patches.Rectangle((6.1, i + 0.1), 2.8, 0.8, facecolor='#87CEEB', edgecolor='none')
        ax.add_patch(rect)
        # 단어 텍스트
        ax.text(7.5, i + 0.5, str(item), fontsize=16, ha='center', va='center', fontweight='bold')

# 애니메이션 실행
ani = FuncAnimation(fig, update, frames=len(operations) + 1, interval=1000, repeat=False)

plt.tight_layout()
plt.show()