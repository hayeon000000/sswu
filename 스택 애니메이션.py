import cv2
import numpy as np
import csv
import re
from PIL import Image, ImageDraw, ImageFont

# 1. 데이터 로드 (스택 과제.csv)
all_words = []
csv_filename = '스택 과제.csv'

try:
    with open(csv_filename, mode='r', encoding='utf-8-sig') as f:
        content = f.read()
        raw_words = re.split(r'[,\n\r]+', content)
        all_words = [w.strip() for w in raw_words if w.strip()]
    print(f">>> 성공: 총 {len(all_words)}개의 단어를 불러왔습니다.")
except Exception as e:
    all_words = ["벚꽃", "커피", "의자", "한강", "과제", "필기구", "햇살", "꽃", "얼그레이", "아메리카노", "꽃샘추위", "개강", "딸기라떼", "피크닉", "바람", "아이스커피", "시험", "디저트"]

# 2. 영상 설정
width, height = 800, 600
out = cv2.VideoWriter('stack_full_sequence.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 2.0, (width, height))
font_path = "C:/Windows/Fonts/malgun.ttf"

try:
    main_font = ImageFont.truetype(font_path, 35)
except:
    main_font = ImageFont.load_default()

# [조건 3] 스택 선언
stack = []

def draw_frame(code_text, info=""):
    img = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # 좌측: 실행 코드
    draw.text((50, 250), code_text, font=main_font, fill=(0, 0, 0))
    if info:
        draw.text((50, 310), f"({info})", font=main_font, fill=(150, 150, 150))
    
    # 우측: 스택 시각화 (10칸)
    box_w, box_h = 250, 50
    start_x, start_y = 450, 500
    for i in range(10):
        y_pos = start_y - (i * box_h)
        draw.rectangle([start_x, y_pos, start_x + box_w, y_pos + box_h], outline=(200, 200, 200))
        
    # 스택 데이터 그리기
    for i, item in enumerate(stack):
        y_pos = start_y - (i * box_h)
        draw.rectangle([start_x, y_pos, start_x + box_w, y_pos + box_h], outline=(0, 0, 0), width=3)
        draw.text((start_x + 20, y_pos + 5), str(item), font=main_font, fill=(255, 0, 0))
        
    frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    out.write(frame)

# 3. 애니메이션 실행
print("전체 시퀀스 영상 제작 시작...")

# [STEP 1] 스택 선언
for _ in range(4):
    draw_frame("stack = []", "Initialize Stack")

# [STEP 2] 모든 단어 처리 (10개 제한 유지하며 Push)
for idx, word in enumerate(all_words):
    if len(stack) >= 9:
        for _ in range(4):
            if stack:
                p = stack.pop()
                draw_frame("stack.pop()", f"Temporary Pop: {p}")
    
    stack.append(word)
    draw_frame(f"stack.push(\"{word}\")", f"Word {idx+1}/{len(all_words)}")

# [STEP 3] TOP 연산 (현재 상태 확인)
if stack:
    draw_frame(f"stack.top()", f"Check Top: {stack[-1]}")

# [STEP 4] 스택 완전히 비우기 (중요: 추가된 부분)
print("마지막 스택 비우기 진행 중...")
while len(stack) > 0:
    p = stack.pop()
    draw_frame("stack.pop()", f"Final Emptying: {p}")

# 빈 스택 상태를 잠시 보여주며 종료
draw_frame("stack is empty", "Sequence Finished")
for _ in range(4):
    draw_frame("", "End of Video")

out.release()
print("\n[성공] 모든 단어 Push 및 전체 Pop 과정이 포함된 'stack_full_sequence.mp4'가 생성되었습니다.")
