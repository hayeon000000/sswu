import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import time

# [폰트 설정] Windows 사용자용 한글 폰트 설정
plt.rc('font', family='Malgun Gothic') 
plt.rcParams['axes.unicode_minus'] = False

# ==========================================
# 1. 데이터 로드 (CSV 파일 읽기)
# ==========================================
try:
    df = pd.read_csv('자료.csv', encoding='cp949')
    all_words = []
    for col in ['단어1', '단어2', '단어3']:
        all_words.extend(df[col].dropna().tolist())
except FileNotFoundError:
    print("오류: '자료.csv' 파일을 찾을 수 없습니다.")
    exit()

# ==========================================
# 2. 스택 설정 및 시각화 함수
# ==========================================
stack = [] # 초기 스택 선언

fig, ax = plt.subplots(figsize=(10, 7))
fig.canvas.manager.set_window_title('자료구조 스택 시각화 - 양시언')

def draw_stack(op_type, val=None):
    ax.clear()
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)
    ax.axis('off')
    
    # [텍스트 스타일] 요청하신 stack.push("의자") 형식
    display_text = ""
    if op_type == "PUSH":
        display_text = f'stack.push("{val}")'
    elif op_type == "POP":
        display_text = f'stack.pop() -> "{val}"'
    elif op_type == "TOP":
        display_text = f'stack.top() -> "{val}"'
    else:
        display_text = op_type

    # 왼쪽 상단에 큰 글씨로 표시
    ax.text(1, 10, display_text, fontsize=22, fontweight='bold', color='black', va='top')
    
    # [오른쪽 스택 박스] 10칸 가이드라인
    ax.plot([6, 6, 9, 9], [11, 1, 1, 11], color='black', lw=3) # 테두리
    for y in range(2, 11):
        ax.plot([6, 9], [y, y], color='gray', linestyle=':', lw=1) # 점선 칸 구분

    # 스택 내부 상자 그리기
    for i, item in enumerate(stack):
        # 시각적으로 보기 편한 녹색 계열 상자
        rect = patches.Rectangle((6.1, i + 1.1), 2.8, 0.8, facecolor='#77DD77', edgecolor='none')
        ax.add_patch(rect)
        ax.text(7.5, i + 1.5, str(item), fontsize=13, ha='center', va='center', fontweight='bold')

    plt.draw()
    plt.pause(1.0) # 애니메이션 속도 (1초)

# ==========================================
# 3. 10개 미만 유지 시나리오 실행 (핵심 로직)
# ==========================================
# 모든 단어를 사용하되, 10개가 넘지 않도록 중간에 POP을 섞었습니다.

draw_stack("stack = [] (시작)")

# 1단계: 처음 8개 단어 PUSH
for i in range(8):
    stack.append(all_words[i])
    draw_stack("PUSH", all_words[i])

# 2단계: TOP 확인 (가장 위 데이터 확인)
draw_stack("TOP", stack[-1])

# 3단계: 4개 POP 실행 (여유 공간 확보 - 현재 4개 남음)
for _ in range(4):
    popped = stack.pop()
    draw_stack("POP", popped)

# 4단계: 다음 6개 단어 PUSH (현재 10개 꽉 참)
for i in range(8, 14):
    stack.append(all_words[i])
    draw_stack("PUSH", all_words[i])

# 5단계: 다시 5개 POP (여유 공간 확보 - 현재 5개 남음)
for _ in range(5):
    popped = stack.pop()
    draw_stack("POP", popped)

# 6단계: 나머지 모든 단어(14~17번) PUSH
for i in range(14, len(all_words)):
    stack.append(all_words[i])
    draw_stack("PUSH", all_words[i])

# 최종 마무리
draw_stack("TOP", stack[-1])
draw_stack("모든 연산 및 단어 처리 완료")
plt.show()
