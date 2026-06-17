"""Graphviz를 활용한 선택적 그래프 시각화 모듈.

Graphviz는 그래프를 바로 파이썬 그림으로 그리는 방식이 아니라,
먼저 DOT 언어로 그래프 구조를 설명한 뒤 `dot` 명령으로 PNG/SVG 이미지로 변환한다.
"""

import shutil
import subprocess
from pathlib import Path

from main_package.bfs.shortest_path import bfs_shortest_path
from main_package.bfs.traversal import bfs_result
from main_package.bipartite.check import check_bipartite_with_colors
from main_package.graph.graph_examples import (
    create_basic_graph,
    create_bipartite_graph,
    create_non_bipartite_graph,
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "graphviz"


def _dot_quote(value):
    """DOT 파일에서 안전하게 쓸 수 있도록 문자열을 큰따옴표로 감싼다."""
    text = str(value)
    text = text.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{text}"'


def _node_id(vertex):
    """정점 이름이 한글이거나 특수문자를 포함해도 DOT에서 안전하게 쓰기 위한 내부 id."""
    return "node_" + str(abs(hash(vertex)))


def _graph_vertices(graph_obj):
    if isinstance(graph_obj, dict):
        return list(graph_obj.keys())
    return graph_obj.vertices()


def _graph_neighbors(graph_obj, vertex):
    if isinstance(graph_obj, dict):
        return graph_obj[vertex]
    return graph_obj.neighbors(vertex)


def _edge_key(u, v):
    return frozenset((u, v))


def _graph_edges(graph_obj):
    """무방향 그래프의 간선을 한 번씩만 반환한다."""
    edges = []
    seen = set()

    for vertex in _graph_vertices(graph_obj):
        for neighbor in _graph_neighbors(graph_obj, vertex):
            key = _edge_key(vertex, neighbor)
            if key in seen:
                continue
            seen.add(key)
            edges.append((vertex, neighbor))

    return edges


def _base_dot_lines(title):
    return [
        "graph G {",
        '  graph [',
        '    charset="UTF-8",',
        '    bgcolor="white",',
        '    labelloc="t",',
        f"    label={_dot_quote(title)},",
        '    fontsize="22",',
        '    fontname="AppleGothic",',
        '    pad="0.4",',
        '    nodesep="0.55",',
        '    ranksep="0.75"',
        "  ];",
        '  node [',
        '    shape="circle",',
        '    style="filled",',
        '    fixedsize="true",',
        '    width="0.8",',
        '    height="0.8",',
        '    fontname="AppleGothic",',
        '    fontsize="15",',
        '    color="#0f172a",',
        '    penwidth="1.8"',
        "  ];",
        '  edge [',
        '    color="#94a3b8",',
        '    penwidth="2",',
        '    fontname="AppleGothic"',
        "  ];",
    ]


def _add_nodes(lines, graph_obj, colors=None):
    colors = colors or {}
    for vertex in _graph_vertices(graph_obj):
        fill = colors.get(vertex, "#bfdbfe")
        lines.append(
            f"  {_node_id(vertex)} "
            f'[label={_dot_quote(vertex)}, fillcolor="{fill}"];'
        )


def _add_edges(lines, graph_obj, highlighted_edges=None, default_color="#94a3b8"):
    highlighted_edges = highlighted_edges or {}
    for u, v in _graph_edges(graph_obj):
        style = highlighted_edges.get(_edge_key(u, v))
        if style is None:
            lines.append(
                f"  {_node_id(u)} -- {_node_id(v)} "
                f'[color="{default_color}", penwidth="2"];'
            )
        else:
            lines.append(
                f"  {_node_id(u)} -- {_node_id(v)} "
                f'[color="{style["color"]}", penwidth="{style["penwidth"]}"];'
            )


def _render_dot(dot_text, name):
    """DOT 내용을 .dot, .png, .svg 파일로 저장한다."""
    dot_path = OUTPUT_DIR / f"{name}.dot"
    png_path = OUTPUT_DIR / f"{name}.png"
    svg_path = OUTPUT_DIR / f"{name}.svg"

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    dot_path.write_text(dot_text, encoding="utf-8")

    dot_command = shutil.which("dot")
    if dot_command is None:
        raise RuntimeError("Graphviz의 dot 명령을 찾을 수 없습니다. brew install graphviz 후 다시 실행하세요.")

    subprocess.run([dot_command, "-Tpng", str(dot_path), "-o", str(png_path)], check=True)
    subprocess.run([dot_command, "-Tsvg", str(dot_path), "-o", str(svg_path)], check=True)

    return dot_path, png_path, svg_path


def make_bfs_level_dot(graph_obj, start):
    """BFS 레벨 구조를 Graphviz DOT 문자열로 만든다."""
    result = bfs_result(graph_obj, start)
    levels = result["levels"]
    parent = result["parent"]

    tree_edges = {}
    for vertex, parent_vertex in parent.items():
        if parent_vertex is not None:
            tree_edges[_edge_key(vertex, parent_vertex)] = {
                "color": "#2563eb",
                "penwidth": "4",
            }

    colors = {}
    palette = ["#2563eb", "#38bdf8", "#86efac", "#fde68a", "#fdba74", "#fca5a5"]
    for level, vertices in levels.items():
        for vertex in vertices:
            colors[vertex] = palette[level % len(palette)]

    lines = _base_dot_lines(f"BFS Level Structure from {start}")
    lines.insert(1, '  rankdir="TB";')
    _add_nodes(lines, graph_obj, colors)
    _add_edges(lines, graph_obj, tree_edges)

    for level, vertices in levels.items():
        rank_nodes = " ".join(_node_id(vertex) for vertex in vertices)
        lines.append(f"  {{ rank=same; {rank_nodes}; }}")

    lines.append("}")
    return "\n".join(lines) + "\n"


def make_shortest_path_dot(graph_obj, start, goal):
    """BFS 최단 경로를 강조한 Graphviz DOT 문자열로 만든다."""
    shortest = bfs_shortest_path(graph_obj, start, goal)
    path = shortest["path"]

    highlighted_edges = {}
    for index in range(len(path) - 1):
        highlighted_edges[_edge_key(path[index], path[index + 1])] = {
            "color": "#f97316",
            "penwidth": "5",
        }

    colors = {}
    for vertex in _graph_vertices(graph_obj):
        if vertex == start:
            colors[vertex] = "#22c55e"
        elif vertex == goal:
            colors[vertex] = "#ef4444"
        elif vertex in path:
            colors[vertex] = "#facc15"
        else:
            colors[vertex] = "#bfdbfe"

    lines = _base_dot_lines(f"BFS Shortest Path: {start} to {goal}")
    lines.insert(1, '  rankdir="TB";')
    _add_nodes(lines, graph_obj, colors)
    _add_edges(lines, graph_obj, highlighted_edges)
    lines.append("}")
    return "\n".join(lines) + "\n"


def make_bipartite_dot(graph_obj):
    """BFS 2-Coloring 결과를 Graphviz DOT 문자열로 만든다."""
    result = check_bipartite_with_colors(graph_obj)

    colors = {}
    left_nodes = []
    right_nodes = []

    for vertex, color in result.colors.items():
        if color == 0:
            colors[vertex] = "#93c5fd"
            left_nodes.append(vertex)
        else:
            colors[vertex] = "#fca5a5"
            right_nodes.append(vertex)

    highlighted_edges = {}
    if result.conflict is not None:
        highlighted_edges[_edge_key(result.conflict[0], result.conflict[1])] = {
            "color": "#dc2626",
            "penwidth": "5",
        }

    title = "Bipartite 2-Coloring" if result.is_bipartite else "Not Bipartite: Conflict Edge"
    lines = _base_dot_lines(title)
    lines.insert(1, '  rankdir="LR";')
    _add_nodes(lines, graph_obj, colors)
    _add_edges(lines, graph_obj, highlighted_edges)

    if left_nodes:
        lines.append("  { rank=same; " + " ".join(_node_id(vertex) for vertex in left_nodes) + "; }")
    if right_nodes:
        lines.append("  { rank=same; " + " ".join(_node_id(vertex) for vertex in right_nodes) + "; }")

    lines.append("}")
    return "\n".join(lines) + "\n"


def draw_graphviz_demo_images():
    """Graphviz로 보고서용 DOT/PNG/SVG 파일을 생성한다."""
    graph = create_basic_graph()
    bipartite_graph = create_bipartite_graph()
    non_bipartite_graph = create_non_bipartite_graph()

    outputs = []
    outputs.append(_render_dot(make_bfs_level_dot(graph, "A"), "graphviz_bfs_levels"))
    outputs.append(_render_dot(make_shortest_path_dot(graph, "A", "F"), "graphviz_shortest_path"))
    outputs.append(_render_dot(make_bipartite_dot(bipartite_graph), "graphviz_bipartite_coloring"))
    outputs.append(_render_dot(make_bipartite_dot(non_bipartite_graph), "graphviz_non_bipartite_conflict"))

    return outputs


if __name__ == "__main__":
    for dot_path, png_path, svg_path in draw_graphviz_demo_images():
        print(f"dot: {dot_path}")
        print(f"png: {png_path}")
        print(f"svg: {svg_path}")
