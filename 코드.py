import time

# 1. 파일 읽기 (판다스 없이 기본 기능 사용)
words = []
try:
    with open('your_file.csv', 'r', encoding='cp949') as f:
        lines = f.readlines()
        for line in lines[1:]:  # 첫 줄(헤더) 제외
            parts = line.strip().split(',')
            # 이름, 학번 뒤의 단어들만 추출 (3번째 열부터 끝까지)
            words.extend(parts[2:])
except:
    # cp949가 안될 경우를 대비한 비상용
    with open('your_file.csv', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines[1:]:
            parts = line.strip().split(',')
            words.extend(parts[2:])

# 2. 스택 선언 및 애니메이션 (기존과 동일)
stack = []
print("--- Stack Animation Start ---")
print("Step: stack = []")
time.sleep(1)

for i, word in enumerate(words):
    if not word: continue # 빈 칸 제외
    
    stack.append(word)
    print(f"\n[Push] stack.push('{word}')")
    print(f"Stack: {stack}")
    time.sleep(0.8)

    if i == 2:
        print(f"[Top]  stack.top() -> '{stack[-1]}'")
        time.sleep(0.8)
    if i == 4:
        p = stack.pop()
        print(f"[Pop]  stack.pop() -> '{p}' 제거")
        print(f"Stack: {stack}")
        time.sleep(0.8)
        
    if len(stack) > 10:
        stack.pop()


