import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import matplotlib.patheffects as pe

# =========================================================
# 다크 테마
# =========================================================
plt.style.use("dark_background")

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

    def is_empty(self):
        return len(self.data) == 0


# =========================================================
# 그래프 직접 구현
# =========================================================
graph = {
    0: [1, 2],
    1: [3, 4],
    2: [5, 6],
    3: [7],
    4: [7],
    5: [8],
    6: [8],
    7: [],
    8: []
}


# =========================================================
# 노드 위치
# =========================================================
positions = {
    0: (0, 4),

    1: (-2, 3),
    2: (2, 3),

    3: (-3, 2),
    4: (-1, 2),
    5: (1, 2),
    6: (3, 2),

    7: (-2, 1),
    8: (2, 1)
}

start_node = 0


# =========================================================
# BFS
# =========================================================
def bfs(graph, start):

    visited_nodes = []
    visited_edges = []

    seen = set()

    queue = Queue()

    queue.enqueue(start)
    seen.add(start)

    while not queue.is_empty():

        current = queue.dequeue()

        visited_nodes.append(current)

        for neighbor in graph[current]:

            if neighbor not in seen:

                seen.add(neighbor)

                queue.enqueue(neighbor)

                visited_edges.append((current, neighbor))

    return visited_nodes, visited_edges


# =========================================================
# DFS
# =========================================================
def dfs(graph, start):

    visited_nodes = []
    visited_edges = []

    seen = set()

    stack = Stack()
    stack.push((start, None))

    while not stack.is_empty():

        current, parent = stack.pop()

        if current not in seen:

            seen.add(current)

            visited_nodes.append(current)

            if parent is not None:
                visited_edges.append((parent, current))

            neighbors = graph[current][::-1]

            for neighbor in neighbors:

                if neighbor not in seen:
                    stack.push((neighbor, current))

    return visited_nodes, visited_edges


bfs_nodes, bfs_edges = bfs(graph, start_node)
dfs_nodes, dfs_edges = dfs(graph, start_node)

print("BFS:", bfs_nodes)
print("DFS:", dfs_nodes)

# =========================================================
# Figure
# =========================================================
fig, axes = plt.subplots(
    1,
    2,
    figsize=(16, 8),
    facecolor="#0f1117"
)

ax1, ax2 = axes

# =========================================================
# 그래프 그리기
# =========================================================
def draw_graph(ax,
               visited_nodes,
               visited_edges,
               title,
               node_color,
               edge_color):

    ax.clear()

    ax.set_facecolor("#0f1117")

    # --------------------------------------
    # 기본 edge
    # --------------------------------------
    for node in graph:

        for neighbor in graph[node]:

            x1, y1 = positions[node]
            x2, y2 = positions[neighbor]

            ax.plot(
                [x1, x2],
                [y1, y2],
                color="#444",
                linewidth=2,
                alpha=0.4,
                zorder=1
            )

    # --------------------------------------
    # 방문 edge 강조
    # --------------------------------------
    for edge in visited_edges:

        x1, y1 = positions[edge[0]]
        x2, y2 = positions[edge[1]]

        line = ax.plot(
            [x1, x2],
            [y1, y2],
            color=edge_color,
            linewidth=5,
            alpha=0.95,
            zorder=2
        )[0]

        # glow 효과
        line.set_path_effects([
            pe.Stroke(linewidth=10, foreground=edge_color, alpha=0.25),
            pe.Normal()
        ])

    # --------------------------------------
    # 노드
    # --------------------------------------
    for node in graph:

        x, y = positions[node]

        visited = node in visited_nodes

        if visited:
            color = node_color
            size = 1800
        else:
            color = "#2a2d36"
            size = 1200

        scatter = ax.scatter(
            x,
            y,
            s=size,
            c=color,
            edgecolors="white",
            linewidths=2,
            zorder=3
        )

        # glow 효과
        if visited:
            scatter.set_path_effects([
                pe.withStroke(linewidth=14,
                              foreground=color,
                              alpha=0.35)
            ])

        ax.text(
            x,
            y,
            str(node),
            fontsize=16,
            fontweight='bold',
            color='white',
            ha='center',
            va='center',
            zorder=4
        )

    # --------------------------------------
    # 제목
    # --------------------------------------
    ax.set_title(
        title,
        fontsize=22,
        color="white",
        pad=20,
        fontweight='bold'
    )

    ax.set_xlim(-4, 4)
    ax.set_ylim(0, 5)

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
        f"BFS\nVisited: {bfs_current_nodes}",
        "#00d0ff",
        "#00d0ff"
    )

    draw_graph(
        ax2,
        dfs_current_nodes,
        dfs_current_edges,
        f"DFS\nVisited: {dfs_current_nodes}",
        "#ff7b00",
        "#ff7b00"
    )


ani = FuncAnimation(
    fig,
    update,
    frames=max_frames,
    interval=1200,
    repeat=False
)

# =========================================================
# 저장
# =========================================================
writer = PillowWriter(fps=1)

ani.save(
    "bfs_vs_dfs_cinematic.gif",
    writer=writer
)

print("\n저장 완료!")
print("파일명: bfs_vs_dfs_cinematic.gif")

plt.tight_layout()
plt.show()