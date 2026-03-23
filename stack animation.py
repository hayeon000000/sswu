import matplotlib
matplotlib.rc("font", family="Malgun Gothic")
matplotlib.rcParams["axes.unicode_minus"] = False

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import FancyBboxPatch

# ── 데이터 ──────────────────────────────────────────────
MEMBERS = {
    "벚꽃": "양시언", "커피": "양시언", "의자": "양시언",
    "한강": "유가현", "과제": "유가현", "필기구": "유가현",
    "햇살": "이하연", "꽃": "이하연", "얼그레이": "이하연",
    "아메리카노": "장예은", "꽃샘추위": "장예은", "개강": "장예은",
    "딸기라떼": "전은빈", "피크닉": "전은빈", "바람": "전은빈",
    "아이스커피": "이예은", "시험": "이예은", "디저트": "이예은",
}

MEMBER_COLORS = {
    "양시언": "#FF6B6B",
    "유가현": "#4ECDC4",
    "이하연": "#FFE66D",
    "장예은": "#A8E6CF",
    "전은빈": "#C3A6FF",
    "이예은": "#FFB347",
}

# ── 스택 연산 시나리오 ──────────────────────────────────
OPERATIONS = [
    ("declare", None),
    ("push", "벚꽃"),
    ("push", "한강"),
    ("push", "햇살"),
    ("push", "아메리카노"),
    ("push", "딸기라떼"),
    ("push", "아이스커피"),
    ("top", None),
    ("pop", None),
    ("pop", None),
    ("pop", None),
    ("push", "커피"),
    ("push", "과제"),
    ("push", "꽃"),
    ("push", "꽃샘추위"),
    ("push", "피크닉"),
    ("top", None),
    ("pop", None),
    ("pop", None),
    ("push", "의자"),
    ("push", "필기구"),
    ("push", "얼그레이"),
    ("top", None),
    ("pop", None),
    ("pop", None),
    ("pop", None),
    ("push", "개강"),
    ("push", "바람"),
    ("push", "시험"),
    ("top", None),
    ("pop", None),
    ("pop", None),
    ("pop", None),
    ("push", "디저트"),
    ("top", None),
    ("pop", None),
]

# ── 상태 계산 ───────────────────────────────────────────
def compute_states(operations):
    stack = []
    states = []
    for op, word in operations:
        if op == "declare":
            stack = []
            msg = "Stack 선언  —  빈 스택 생성"
            highlight = None
        elif op == "push":
            stack = stack.copy()
            stack.append(word)
            msg = f"PUSH  →  '{word}'"
            highlight = ("push", len(stack) - 1)
        elif op == "pop":
            if stack:
                popped = stack[-1]
                stack = stack[:-1]
                msg = f"POP   ←  '{popped}'"
                highlight = ("pop", popped)
            else:
                msg = "POP  —  스택이 비어 있음"
                highlight = None
        elif op == "top":
            if stack:
                msg = f"TOP   =   '{stack[-1]}'"
                highlight = ("top", len(stack) - 1)
            else:
                msg = "TOP  —  스택이 비어 있음"
                highlight = None
        states.append({
            "stack": stack.copy(),
            "op": op,
            "word": word,
            "msg": msg,
            "highlight": highlight,
        })
    return states

STATES = compute_states(OPERATIONS)
N_FRAMES = len(STATES)

# ── 그림 설정 ───────────────────────────────────────────
fig = plt.figure(figsize=(13, 8), facecolor="#0F0F1A")
fig.patch.set_facecolor("#0F0F1A")

ax_stack  = fig.add_axes([0.05, 0.08, 0.38, 0.82])
ax_info   = fig.add_axes([0.50, 0.55, 0.46, 0.38])
ax_legend = fig.add_axes([0.50, 0.08, 0.46, 0.42])

for ax in [ax_stack, ax_info, ax_legend]:
    ax.set_facecolor("#0F0F1A")
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

MAX_SIZE = 10
BOX_H = 0.08
BOX_W = 0.75
X0 = 0.125

# ── 범례 (고정) ─────────────────────────────────────────
def draw_legend():
    ax_legend.cla()
    ax_legend.set_facecolor("#0F0F1A")
    ax_legend.set_xticks([])
    ax_legend.set_yticks([])
    for sp in ax_legend.spines.values():
        sp.set_visible(False)
    ax_legend.set_xlim(0, 1)
    ax_legend.set_ylim(0, 1)
    ax_legend.text(0.5, 0.94, "팀원 & 단어",
                   ha="center", va="top", fontsize=11,
                   color="#CCCCFF", fontweight="bold")
    members = list(MEMBER_COLORS.keys())
    cols = 2
    for i, m in enumerate(members):
        row = i // cols
        col = i % cols
        x = 0.05 + col * 0.50
        y = 0.80 - row * 0.18
        color = MEMBER_COLORS[m]
        rect = FancyBboxPatch((x, y - 0.06), 0.44, 0.13,
                               boxstyle="round,pad=0.01",
                               facecolor=color + "33", edgecolor=color,
                               linewidth=1.5, transform=ax_legend.transAxes)
        ax_legend.add_patch(rect)
        ax_legend.text(x + 0.22, y, m, ha="center", va="center",
                       fontsize=9, color=color, fontweight="bold",
                       transform=ax_legend.transAxes)

draw_legend()

# ── 프레임 드로우 ───────────────────────────────────────
def draw_frame(state):
    # 스택 패널
    ax_stack.cla()
    ax_stack.set_facecolor("#0F0F1A")
    ax_stack.set_xlim(0, 1)
    ax_stack.set_ylim(-0.05, 1.0)
    ax_stack.set_xticks([])
    ax_stack.set_yticks([])
    for sp in ax_stack.spines.values():
        sp.set_visible(False)

    ax_stack.text(0.5, 0.97, "Stack", ha="center", va="top",
                  fontsize=14, color="#AAAAFF", fontweight="bold")

    container = FancyBboxPatch((X0 - 0.02, -0.02), BOX_W + 0.04,
                                MAX_SIZE * BOX_H + 0.04,
                                boxstyle="round,pad=0.01",
                                facecolor="#1A1A2E", edgecolor="#3333AA",
                                linewidth=2)
    ax_stack.add_patch(container)

    for i in range(MAX_SIZE):
        y = i * BOX_H
        slot = FancyBboxPatch((X0, y), BOX_W, BOX_H * 0.92,
                               boxstyle="round,pad=0.005",
                               facecolor="#111122", edgecolor="#222244",
                               linewidth=0.8)
        ax_stack.add_patch(slot)
        ax_stack.text(X0 - 0.04, y + BOX_H * 0.46, str(i),
                      ha="right", va="center", fontsize=7, color="#333366")

    stack = state["stack"]
    highlight = state["highlight"]

    for idx, word in enumerate(stack):
        y = idx * BOX_H
        member = MEMBERS.get(word, "")
        color = MEMBER_COLORS.get(member, "#888888")

        is_hl = (highlight and highlight[0] in ("push", "top") and highlight[1] == idx)
        alpha  = 1.0 if is_hl else 0.75
        edge_w = 3   if is_hl else 1.5
        glow   = color if is_hl else color + "88"

        box = FancyBboxPatch((X0, y), BOX_W, BOX_H * 0.92,
                              boxstyle="round,pad=0.008",
                              facecolor=color + ("99" if is_hl else "55"),
                              edgecolor=glow, linewidth=edge_w, alpha=alpha)
        ax_stack.add_patch(box)

        ax_stack.text(0.5, y + BOX_H * 0.46, word,
                      ha="center", va="center",
                      fontsize=11 if len(word) <= 4 else 9,
                      color="white" if is_hl else "#DDDDDD",
                      fontweight="bold" if is_hl else "normal")

        ax_stack.text(X0 + BOX_W - 0.02, y + BOX_H * 0.46, member,
                      ha="right", va="center", fontsize=7,
                      color=color, alpha=0.85)

    if stack:
        top_y = (len(stack) - 1) * BOX_H + BOX_H * 0.46
        ax_stack.annotate("TOP", xy=(X0 + BOX_W + 0.02, top_y),
                          xytext=(X0 + BOX_W + 0.14, top_y),
                          fontsize=9, color="#FFD700", fontweight="bold",
                          arrowprops=dict(arrowstyle="<-", color="#FFD700", lw=2),
                          va="center")

    ax_stack.text(0.5, -0.04, f"size = {len(stack)} / {MAX_SIZE}",
                  ha="center", va="bottom", fontsize=9, color="#8888CC")

    # 정보 패널
    ax_info.cla()
    ax_info.set_facecolor("#0F0F1A")
    ax_info.set_xlim(0, 1)
    ax_info.set_ylim(0, 1)
    ax_info.set_xticks([])
    ax_info.set_yticks([])
    for sp in ax_info.spines.values():
        sp.set_visible(False)

    ax_info.text(0.5, 0.95, "현재 연산",
                 ha="center", va="top", fontsize=11,
                 color="#AAAAFF", fontweight="bold")

    op_colors = {
        "declare": "#4488FF", "push": "#44FF88",
        "pop":     "#FF6644", "top":  "#FFD700",
    }
    op = state["op"]
    badge_color = op_colors.get(op, "#888888")

    badge = FancyBboxPatch((0.15, 0.60), 0.70, 0.28,
                            boxstyle="round,pad=0.02",
                            facecolor=badge_color + "22",
                            edgecolor=badge_color, linewidth=2.5)
    ax_info.add_patch(badge)
    ax_info.text(0.5, 0.745, state["msg"],
                 ha="center", va="center", fontsize=11,
                 color=badge_color, fontweight="bold")

    stack_str = "[ " + ",  ".join(stack) + " ]" if stack else "[ 비어 있음 ]"
    ax_info.text(0.5, 0.42, "스택 내용", ha="center", va="center",
                 fontsize=9, color="#888888")
    ax_info.text(0.5, 0.28, stack_str, ha="center", va="center",
                 fontsize=9, color="#CCCCFF")

    step_idx = STATES.index(state) + 1
    ax_info.text(0.95, 0.05, f"step {step_idx}/{N_FRAMES}",
                 ha="right", va="bottom", fontsize=8, color="#444466")

# ── 애니메이션 실행 ─────────────────────────────────────
# ani를 전역 변수로 유지해야 garbage collection 방지됨
def update(frame):
    draw_frame(STATES[frame])
    return []

ani = animation.FuncAnimation(
    fig, update,
    frames=N_FRAMES,
    interval=1200,
    repeat=True,
    blit=False,
)

fig.suptitle("자료구조 6조 — Stack 애니메이션",
             y=0.99, fontsize=15, color="#EEEEFF", fontweight="bold")

# tight_layout 제거 (add_axes와 충돌)
plt.show()
