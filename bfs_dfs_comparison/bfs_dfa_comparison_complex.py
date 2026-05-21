import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import matplotlib.patheffects as pe

# =========================================================
# 밝은 테마
# =========================================================
plt.style.use("default")

# =========================================================
# Queue 구현
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


# =========================================================
# Stack 구현
# =========================================================
class Stack:

    def __init__(self):
        self.data = []

    def push(self, value):
        self.data.append(value)

    def pop(self):

        if not self.is_empty():
            return self.data.pop()

    def top(self):

        if not self.is_empty():
            return self.data[-1]

        return None

    def is_empty(self):
        return len(self.data) == 0


# =========================================================
# 그래프
# BFS는 짧게 가고
# DFS는 깊게 돌아가게 설계
# =========================================================
graph = {

    0: [1, 2],

    1: [0, 3, 4],

    2: [0, 5],

    3: [1, 6],

    4: [1, 7, 8],

    5: [2, 8],

    6: [3],

    7: [4, 9],

    8: [4, 5, 13, 10],

    9: [7],

    10: [8, 11],

    11: [10, 12],

    12: [11, 13],

    13: [8, 12]
}

# =========================================================
# 노드 위치
# =========================================================
positions = {

    0: (0, 5),

    1: (-3, 4),
    2: (3, 4),

    3: (-4, 3),
    4: (-1.5, 3),

    5: (3, 3),

    6: (-5, 2),

    7: (-2.5, 2),
    8: (1, 2),

    9: (-3, 1),

    10: (3, 1),

    11: (4, 0),

    12: (3, -1),

    13: (0.5, -1)
}

start_node = 0


# =========================================================
# BFS
# =========================================================
def bfs(graph, start):

    visited_nodes = []
    visited_edges = []
    front_history = []

    seen = set()

    queue = Queue()

    queue.enqueue(start)
    seen.add(start)

    while not queue.is_empty():

        current_front = queue.front()

        current = queue.dequeue()

        front_history.append(current_front)

        visited_nodes.append(current)

        for neighbor in graph[current]:

            if neighbor not in seen:

                seen.add(neighbor)

                queue.enqueue(neighbor)

                visited_edges.append((current, neighbor))

    return visited_nodes, visited_edges, front_history


# =========================================================
# DFS
# =========================================================
def dfs(graph, start):

    visited_nodes = []
    visited_edges = []
    front_history = []

    seen = set()

    stack = Stack()

    stack.push((start, None))

    while not stack.is_empty():

        current_front = stack.top()[0]

        current, parent = stack.pop()

        front_history.append(current_front)

        if current not in seen:

            seen.add(current)

            visited_nodes.append(current)

            if parent is not None:
                visited_edges.append((parent, current))

            # DFS 깊게 들어가도록 reverse
            neighbors = graph[current][::-1]

            for neighbor in neighbors:

                if neighbor not in seen:
                    stack.push((neighbor, current))

    return visited_nodes, visited_edges, front_history


bfs_nodes, bfs_edges, bfs_fronts = bfs(graph, start_node)

dfs_nodes, dfs_edges, dfs_fronts = dfs(graph, start_node)

print("BFS 방문 순서:")
print(bfs_nodes)

print("\nDFS 방문 순서:")
print(dfs_nodes)

# =========================================================
# Figure
# =========================================================
fig, axes = plt.subplots(
    1,
    2,
    figsize=(18, 9),
    facecolor="white"
)

ax1, ax2 = axes


# =========================================================
# 그래프 그리기
# =========================================================
def draw_graph(ax,
               visited_nodes,
               visited_edges,
               current_front,
               title,
               node_color,
               edge_color):

    ax.clear()

    ax.set_facecolor("white")

    # -----------------------------------------------------
    # 기본 간선
    # -----------------------------------------------------
    drawn_edges = set()

    for node in graph:

        for neighbor in graph[node]:

            if (neighbor, node) in drawn_edges:
                continue

            drawn_edges.add((node, neighbor))

            x1, y1 = positions[node]
            x2, y2 = positions[neighbor]

            ax.plot(
                [x1, x2],
                [y1, y2],
                color="#bbbbbb",
                linewidth=2,
                alpha=0.7,
                zorder=1
            )

    # -----------------------------------------------------
    # 방문 edge 강조
    # -----------------------------------------------------
    for edge in visited_edges:

        x1, y1 = positions[edge[0]]
        x2, y2 = positions[edge[1]]

        line = ax.plot(
            [x1, x2],
            [y1, y2],
            color=edge_color,
            linewidth=6,
            alpha=0.95,
            zorder=2
        )[0]

        line.set_path_effects([
            pe.Stroke(
                linewidth=14,
                foreground=edge_color,
                alpha=0.20
            ),
            pe.Normal()
        ])

    # -----------------------------------------------------
    # 노드
    # -----------------------------------------------------
    for node in graph:

        x, y = positions[node]

        visited = node in visited_nodes

        if visited:

            color = node_color
            size = 2200

        else:

            color = "#dddddd"
            size = 1600

        scatter = ax.scatter(
            x,
            y,
            s=size,
            c=color,
            edgecolors="black",
            linewidths=2,
            zorder=3
        )

        # glow
        if visited:

            scatter.set_path_effects([
                pe.withStroke(
                    linewidth=16,
                    foreground=color,
                    alpha=0.25
                )
            ])

        # -------------------------------------------------
        # 현재 탐색 노드 강조
        # -------------------------------------------------
        if node == current_front:

            ring = plt.Circle(
                (x, y),
                0.45,
                fill=False,
                linewidth=5,
                color="#ffcc00",
                alpha=0.95,
                zorder=5
            )

            ax.add_patch(ring)

            ring.set_path_effects([
                pe.Stroke(
                    linewidth=15,
                    foreground="#ffe066",
                    alpha=0.35
                ),
                pe.Normal()
            ])

        ax.text(
            x,
            y,
            str(node),
            fontsize=16,
            fontweight='bold',
            color='black',
            ha='center',
            va='center',
            zorder=6
        )

    # -----------------------------------------------------
    # 제목
    # -----------------------------------------------------
    ax.set_title(
        title,
        fontsize=23,
        color="black",
        pad=20,
        fontweight='bold'
    )

    ax.set_xlim(-6, 6)
    ax.set_ylim(-2, 6)

    ax.set_xticks([])
    ax.set_yticks([])

    for spine in ax.spines.values():
        spine.set_visible(False)


# =========================================================
# 애니메이션
# =========================================================
max_frames = max(len(bfs_nodes), len(dfs_nodes))


def update(frame):

    bfs_current_nodes = bfs_nodes[:frame + 1]
    bfs_current_edges = bfs_edges[:frame]

    dfs_current_nodes = dfs_nodes[:frame + 1]
    dfs_current_edges = dfs_edges[:frame]

    draw_graph(
        ax1,
        bfs_current_nodes,
        bfs_current_edges,
        bfs_fronts[frame],
        f"BFS\nVisited: {bfs_current_nodes}",
        "#00b7ff",
        "#00b7ff"
    )

    draw_graph(
        ax2,
        dfs_current_nodes,
        dfs_current_edges,
        dfs_fronts[frame],
        f"DFS\nVisited: {dfs_current_nodes}",
        "#ff8800",
        "#ff8800"
    )


ani = FuncAnimation(
    fig,
    update,
    frames=max_frames,
    interval=1200,
    repeat=False
)

# =========================================================
# GIF 저장
# =========================================================
writer = PillowWriter(fps=1)

ani.save(
    "bfs_vs_dfs_final.gif",
    writer=writer
)

print("\nGIF 저장 완료!")
print("파일명: bfs_vs_dfs_final.gif")

plt.tight_layout()
plt.show()