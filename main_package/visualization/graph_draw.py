"""NetworkX와 Matplotlib을 활용한 선택적 그래프 시각화 모듈.

이 파일은 BFS 핵심 알고리즘을 구현하는 파일이 아니라,
이미 구현된 그래프와 BFS 결과를 이미지로 보기 좋게 저장하는 보조 모듈이다.
"""

import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = PROJECT_ROOT / "outputs"

# Matplotlib이 사용자 홈 폴더에 캐시를 만들지 못하는 환경에서도 실행되게 한다.
os.environ.setdefault("MPLCONFIGDIR", str(PROJECT_ROOT / ".matplotlib_cache"))

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib import font_manager
import networkx as nx

from main_package.bfs.shortest_path import bfs_shortest_path
from main_package.bfs.traversal import bfs_result
from main_package.bipartite.check import check_bipartite_with_colors
from main_package.graph.graph_examples import create_basic_graph, create_bipartite_graph

LABEL_FONT = "DejaVu Sans"


def _set_korean_font_if_available():
    """한글 정점 이름이 깨지지 않도록 사용 가능한 한글 폰트를 설정한다."""
    global LABEL_FONT
    candidates = ["AppleGothic", "NanumGothic", "Arial Unicode MS", "DejaVu Sans"]

    for font_name in candidates:
        try:
            font_manager.findfont(font_name, fallback_to_default=False)
        except ValueError:
            continue

        plt.rcParams["font.family"] = font_name
        plt.rcParams["font.sans-serif"] = [font_name, "DejaVu Sans"]
        plt.rcParams["axes.unicode_minus"] = False
        LABEL_FONT = font_name
        return


_set_korean_font_if_available()


def _graph_vertices(graph_obj):
    if isinstance(graph_obj, dict):
        return list(graph_obj.keys())
    return graph_obj.vertices()


def _graph_neighbors(graph_obj, vertex):
    if isinstance(graph_obj, dict):
        return graph_obj[vertex]
    return graph_obj.neighbors(vertex)


def _create_networkx_graph(graph_obj):
    """커스텀 그래프 객체를 NetworkX 그래프로 변환한다."""
    if getattr(graph_obj, "directed", False):
        graph = nx.DiGraph()
    else:
        graph = nx.Graph()

    for vertex in _graph_vertices(graph_obj):
        graph.add_node(vertex)

    for vertex in _graph_vertices(graph_obj):
        for neighbor in _graph_neighbors(graph_obj, vertex):
            graph.add_edge(vertex, neighbor)

    return graph


def _edge_key(u, v):
    return frozenset((u, v))


def _make_adjacency_matrix(graph, nodes):
    index = {node: i for i, node in enumerate(nodes)}
    matrix = [[0 for _ in nodes] for _ in nodes]

    for u, v in graph.edges():
        matrix[index[u]][index[v]] = 1
        if not graph.is_directed():
            matrix[index[v]][index[u]] = 1

    return matrix


def _save_figure(fig, output_path):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(output_path, dpi=180, bbox_inches="tight")
    plt.close(fig)
    return output_path


def _bfs_level_positions(levels, graph):
    positions = {}

    for level, vertices in levels.items():
        width = len(vertices)
        for index, vertex in enumerate(vertices):
            x = index - (width - 1) / 2
            y = -level
            positions[vertex] = (x, y)

    unvisited = [node for node in graph.nodes() if node not in positions]
    last_level = max(levels.keys(), default=0) + 1
    for index, vertex in enumerate(unvisited):
        x = index - (len(unvisited) - 1) / 2
        positions[vertex] = (x, -last_level)

    return positions


def draw_graph_and_matrix(graph_obj, output_path=OUTPUT_DIR / "graph_and_matrix.png"):
    """그래프 연결 구조와 인접 행렬을 나란히 이미지로 저장한다."""
    graph = _create_networkx_graph(graph_obj)
    nodes = list(graph.nodes())
    matrix = _make_adjacency_matrix(graph, nodes)

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    pos = nx.spring_layout(graph, seed=42, k=1.0)
    nx.draw_networkx_edges(graph, pos, ax=axes[0], edge_color="#94a3b8", width=2)
    nx.draw_networkx_nodes(
        graph,
        pos,
        ax=axes[0],
        node_color="#86efac",
        edgecolors="#14532d",
        linewidths=1.8,
        node_size=1100,
    )
    nx.draw_networkx_labels(graph, pos, ax=axes[0], font_size=11, font_family=LABEL_FONT)
    axes[0].set_title("Graph Network Structure", fontsize=13)
    axes[0].axis("off")

    image = axes[1].imshow(matrix, cmap="Blues", vmin=0, vmax=1)
    axes[1].set_title("Adjacency Matrix", fontsize=13, pad=14)
    axes[1].set_xticks(range(len(nodes)))
    axes[1].set_yticks(range(len(nodes)))
    axes[1].set_xticklabels([str(node) for node in nodes])
    axes[1].set_yticklabels([str(node) for node in nodes])
    axes[1].tick_params(axis="x", rotation=45)

    for row in range(len(nodes)):
        for col in range(len(nodes)):
            axes[1].text(
                col,
                row,
                str(matrix[row][col]),
                ha="center",
                va="center",
                color="#0f172a",
                fontsize=10,
            )

    fig.colorbar(image, ax=axes[1], fraction=0.046, pad=0.04)
    return _save_figure(fig, output_path)


def draw_bfs_levels(graph_obj, start, output_path=OUTPUT_DIR / "bfs_levels.png"):
    """BFS 탐색 결과를 레벨 구조 중심으로 이미지로 저장한다."""
    graph = _create_networkx_graph(graph_obj)
    result = bfs_result(graph_obj, start)
    levels = result["levels"]
    parent = result["parent"]
    positions = _bfs_level_positions(levels, graph)

    tree_edges = []
    for vertex, parent_vertex in parent.items():
        if parent_vertex is not None:
            tree_edges.append((parent_vertex, vertex))

    level_by_node = {}
    for level, vertices in levels.items():
        for vertex in vertices:
            level_by_node[vertex] = level

    palette = ["#2563eb", "#38bdf8", "#86efac", "#facc15", "#fb923c", "#f87171", "#c084fc"]
    node_colors = [palette[level_by_node.get(node, 0) % len(palette)] for node in graph.nodes()]

    fig, ax = plt.subplots(figsize=(10, 6))
    nx.draw_networkx_edges(graph, positions, ax=ax, edge_color="#cbd5e1", width=1.6)
    nx.draw_networkx_edges(graph, positions, ax=ax, edgelist=tree_edges, edge_color="#1d4ed8", width=3.2)
    nx.draw_networkx_nodes(
        graph,
        positions,
        ax=ax,
        node_color=node_colors,
        edgecolors="#0f172a",
        linewidths=1.7,
        node_size=1200,
    )
    nx.draw_networkx_labels(graph, positions, ax=ax, font_size=11, font_family=LABEL_FONT)

    for level, vertices in levels.items():
        left_x = -max(len(vertices), 1) / 2 - 1.0
        ax.text(left_x, -level, f"Level {level}", ha="right", va="center", fontsize=10, color="#334155")

    ax.set_title(f"BFS Level Structure from {start}", fontsize=14)
    ax.axis("off")
    return _save_figure(fig, output_path)


def draw_shortest_path(graph_obj, start, goal, output_path=OUTPUT_DIR / "shortest_path.png"):
    """BFS 최단 경로를 강조한 그래프 이미지를 저장한다."""
    graph = _create_networkx_graph(graph_obj)
    shortest = bfs_shortest_path(graph_obj, start, goal)
    levels = bfs_result(graph_obj, start)["levels"]
    positions = _bfs_level_positions(levels, graph)

    path = shortest["path"]
    path_nodes = set(path)
    path_edges = set()
    for index in range(len(path) - 1):
        path_edges.add(_edge_key(path[index], path[index + 1]))

    normal_edges = []
    highlighted_edges = []
    for u, v in graph.edges():
        if _edge_key(u, v) in path_edges:
            highlighted_edges.append((u, v))
        else:
            normal_edges.append((u, v))

    node_colors = []
    for node in graph.nodes():
        if node == start:
            node_colors.append("#22c55e")
        elif node == goal:
            node_colors.append("#ef4444")
        elif node in path_nodes:
            node_colors.append("#facc15")
        else:
            node_colors.append("#bfdbfe")

    fig, ax = plt.subplots(figsize=(10, 6))
    nx.draw_networkx_edges(graph, positions, ax=ax, edgelist=normal_edges, edge_color="#cbd5e1", width=1.6)
    nx.draw_networkx_edges(graph, positions, ax=ax, edgelist=highlighted_edges, edge_color="#f97316", width=4)
    nx.draw_networkx_nodes(
        graph,
        positions,
        ax=ax,
        node_color=node_colors,
        edgecolors="#0f172a",
        linewidths=1.8,
        node_size=1200,
    )
    nx.draw_networkx_labels(graph, positions, ax=ax, font_size=11, font_family=LABEL_FONT)

    title = f"BFS Shortest Path: {start} to {goal}"
    if shortest["found"]:
        title += f" / distance = {shortest['distance']}"
    else:
        title += " / not found"

    ax.set_title(title, fontsize=14)
    ax.axis("off")
    return _save_figure(fig, output_path)


def draw_bipartite_coloring(graph_obj, output_path=OUTPUT_DIR / "bipartite_coloring.png"):
    """BFS 기반 2-Coloring 결과를 이미지로 저장한다."""
    graph = _create_networkx_graph(graph_obj)
    result = check_bipartite_with_colors(graph_obj)
    colors = result.colors

    group_one = [node for node, color in colors.items() if color == 1]
    if group_one:
        pos = nx.bipartite_layout(graph, group_one)
    else:
        pos = nx.spring_layout(graph, seed=42)

    node_colors = ["#fca5a5" if colors.get(node) == 1 else "#93c5fd" for node in graph.nodes()]

    edge_colors = []
    conflict = result.conflict
    for u, v in graph.edges():
        if conflict is not None and _edge_key(u, v) == _edge_key(conflict[0], conflict[1]):
            edge_colors.append("#dc2626")
        else:
            edge_colors.append("#94a3b8")

    fig, ax = plt.subplots(figsize=(9, 6))
    nx.draw_networkx_edges(graph, pos, ax=ax, edge_color=edge_colors, width=2.4)
    nx.draw_networkx_nodes(
        graph,
        pos,
        ax=ax,
        node_color=node_colors,
        edgecolors="#0f172a",
        linewidths=1.8,
        node_size=1300,
    )
    nx.draw_networkx_labels(graph, pos, ax=ax, font_size=10, font_family=LABEL_FONT)

    if result.is_bipartite:
        title = "Bipartite 2-Coloring"
    else:
        title = "Not Bipartite: Conflict Edge Highlighted"

    ax.set_title(title, fontsize=14)
    ax.axis("off")
    return _save_figure(fig, output_path)


def draw_demo_images(output_dir=OUTPUT_DIR):
    """보고서에 넣을 수 있는 예시 시각화 이미지를 한 번에 생성한다."""
    output_dir = Path(output_dir)
    graph = create_basic_graph()
    bipartite_graph = create_bipartite_graph()

    saved_files = [
        draw_graph_and_matrix(graph, output_dir / "graph_and_matrix.png"),
        draw_bfs_levels(graph, "A", output_dir / "bfs_levels.png"),
        draw_shortest_path(graph, "A", "F", output_dir / "shortest_path.png"),
        draw_bipartite_coloring(bipartite_graph, output_dir / "bipartite_coloring.png"),
    ]

    return saved_files


if __name__ == "__main__":
    for path in draw_demo_images():
        print(f"saved: {path}")
