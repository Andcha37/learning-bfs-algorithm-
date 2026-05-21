import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import matplotlib.patheffects as pe

# =========================================================
# 다크 테마
# =========================================================
plt.style.use("default")

# =========================================================
# Queue 직접 구현
# =========================================================
class Queue:

    def __init__(self):
        self.data = []

    def enqueue(self, value):
        self.data.append(value)

    def dequeue(self):

        if not self.is_empty():
            return self.data.pop(0)

    def front(self):

        if not self.is_empty():
            return self.data[0]

        return None

    def is_empty(self):
        return len(self.data) == 0

    def get_data(self):
        return self.data[:]


# =========================================================
# 그래프 직접 구현
# =========================================================
graph = {
    0: [3, 4],
    1: [3, 5],
    2: [4, 5],

    3: [0, 1],
    4: [0, 2],
    5: [1, 2]
}

# =========================================================
# 노드 위치
# =========================================================
positions = {

    0: (-3, 2),
    1: (0, 2),
    2: (3, 2),

    3: (-3, -2),
    4: (0, -2),
    5: (3, -2)
}


# =========================================================
# BFS 이분 그래프 판별 + 시각화 데이터 저장
# =========================================================
def bfs_bipartite_visual(graph, start):

    color = {}

    queue = Queue()

    queue.enqueue(start)

    color[start] = 0

    frames = []

    while not queue.is_empty():

        current_front = queue.front()

        current = queue.dequeue()

        for neighbor in graph[current]:

            # 현재 상태 저장
            frames.append({
                "current": current,
                "front": current_front,
                "edge": (current, neighbor),
                "queue": queue.get_data(),
                "colors": color.copy()
            })

            # 아직 방문 안한 경우
            if neighbor not in color:

                color[neighbor] = 1 - color[current]

                queue.enqueue(neighbor)

            else:
                # 같은 색이면 실패
                if color[neighbor] == color[current]:

                    return False, frames, color

    return True, frames, color


is_bipartite, frames_data, final_colors = bfs_bipartite_visual(graph, 0)

print("이분 그래프 여부:", is_bipartite)

# =========================================================
# Figure
# =========================================================
fig, ax = plt.subplots(
    figsize=(11, 10),
    facecolor="white"
)

# =========================================================
# 모든 간선 목록
# =========================================================
all_edges = []

for node in graph:
    for neighbor in graph[node]:

        if (neighbor, node) not in all_edges:
            all_edges.append((node, neighbor))


# =========================================================
# 그래프 그리기
# =========================================================
def draw(frame_index):

    ax.clear()

    ax.set_facecolor("white")

    data = frames_data[frame_index]

    current_node = data["current"]
    current_front = data["front"]

    current_edge = data["edge"]

    queue_state = data["queue"]

    current_colors = data["colors"]

    # -----------------------------------------------------
    # 간선
    # -----------------------------------------------------
    for edge in all_edges:

        x1, y1 = positions[edge[0]]
        x2, y2 = positions[edge[1]]

        # 현재 탐색중인 간선
        if edge == current_edge or edge[::-1] == current_edge:

            color = "#00ffcc"
            width = 6
            alpha = 1

        else:
            color = "#999"
            width = 2
            alpha = 0.35

        line = ax.plot(
            [x1, x2],
            [y1, y2],
            color=color,
            linewidth=width,
            alpha=alpha,
            zorder=1
        )[0]

        # Glow 효과
        if edge == current_edge or edge[::-1] == current_edge:

            line.set_path_effects([
                pe.Stroke(
                    linewidth=14,
                    foreground="#00ffcc",
                    alpha=0.25
                ),
                pe.Normal()
            ])

    # -----------------------------------------------------
    # 노드
    # -----------------------------------------------------
    for node in graph:

        x, y = positions[node]

        # 아직 색칠 안된 노드
        if node not in current_colors:

            node_color = "#2a2d36"

        else:

            if current_colors[node] == 0:
                node_color = "#00bfff"

            else:
                node_color = "#ff7b00"

        size = 2500

        # 현재 Queue Front 강조
        if node == current_front:
            size = 3500

        scatter = ax.scatter(
            x,
            y,
            s=size,
            c=node_color,
            edgecolors="white",
            linewidths=3,
            zorder=3
        )

        # Glow
        scatter.set_path_effects([
            pe.withStroke(
                linewidth=18,
                foreground=node_color,
                alpha=0.35
            )
        ])

        # Queue Front 링 강조
        if node == current_front:

            ring = plt.Circle(
                (x, y),
                0.55,
                fill=False,
                linewidth=5,
                color="yellow",
                alpha=0.9,
                zorder=4
            )

            ax.add_patch(ring)

        ax.text(
            x,
            y,
            str(node),
            fontsize=18,
            color="black",
            fontweight='bold',
            ha='center',
            va='center',
            zorder=5
        )

    # -----------------------------------------------------
    # 제목
    # -----------------------------------------------------
    ax.set_title(
        "BFS Bipartite Graph Check",
        fontsize=24,
        color="black",
        pad=20,
        fontweight='bold'
    )

    # -----------------------------------------------------
    # Queue 상태
    # -----------------------------------------------------
    ax.text(
        0,
        -3.7,
        f"QUEUE : {queue_state}",
        fontsize=18,
        color="#00ffcc",
        ha='center',
        fontweight='bold'
    )

    # -----------------------------------------------------
    # 현재 처리 노드
    # -----------------------------------------------------
    ax.text(
        0,
        -4.5,
        f"CURRENT FRONT NODE : {current_front}",
        fontsize=20,
        color="yellow",
        ha='center',
        fontweight='bold'
    )

    # -----------------------------------------------------
    # 결과
    # -----------------------------------------------------
    result_text = (
        "BIPARTITE GRAPH"
        if is_bipartite
        else
        "NOT BIPARTITE"
    )

    ax.text(
        0,
        3.2,
        result_text,
        fontsize=20,
        color="#00ff99",
        ha='center',
        fontweight='bold'
    )

    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 4)

    ax.set_xticks([])
    ax.set_yticks([])

    for spine in ax.spines.values():
        spine.set_visible(False)


# =========================================================
# 애니메이션
# =========================================================
ani = FuncAnimation(
    fig,
    draw,
    frames=len(frames_data),
    interval=1200,
    repeat=False
)

# =========================================================
# GIF 저장
# =========================================================
writer = PillowWriter(fps=1)

ani.save(
    "bipartite_bfs_queue_visualization.gif",
    writer=writer
)

print("\nGIF 저장 완료!")
print("파일명: bipartite_bfs_queue_visualization.gif")

plt.tight_layout()
plt.show()