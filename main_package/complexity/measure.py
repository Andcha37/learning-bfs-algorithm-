"""BFS 복잡도 비교 실험 모듈.

인접 리스트와 인접 행렬에서 동일한 간선 데이터를 사용하여 BFS 실행 시간을 비교한다.
보고서의 복잡도 분석을 보조하기 위한 간단한 실험용 코드이다.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Iterable, List, Tuple

from main_package.bfs.traversal import bfs_levels, bfs_result
from main_package.dfs.iterative import dfs_traversal
from main_package.graph.adjacency_list import GraphAdjList
from main_package.graph.adjacency_matrix import GraphAdjMatrix
from main_package.graph.graph_examples import create_edges_for_complexity

Edge = Tuple[object, object]


@dataclass
class ComplexityRow:
    vertex_count: int
    edge_count: int
    adj_list_time: float
    adj_matrix_time: float
    adj_list_visited: int
    adj_matrix_visited: int


@dataclass
class SearchBasisRow:
    vertex_count: int
    edge_count: int
    bfs_level_count: int
    bfs_visited_count: int
    dfs_visited_count: int
    bfs_level_time: float
    dfs_visit_time: float


def _build_adj_list(vertex_count: int, edges: Iterable[Edge]) -> GraphAdjList:
    graph = GraphAdjList(directed=False)
    for vertex in range(vertex_count):
        graph.add_vertex(vertex)
    for u, v in edges:
        graph.add_edge(u, v)
    return graph


def _build_adj_matrix(vertex_count: int, edges: Iterable[Edge]) -> GraphAdjMatrix:
    graph = GraphAdjMatrix(directed=False)
    for vertex in range(vertex_count):
        graph.add_vertex(vertex)
    for u, v in edges:
        graph.add_edge(u, v)
    return graph


def measure_bfs_time(graph, start: object, repeat: int = 5) -> Tuple[float, int]:
    """BFS 실행 시간을 측정한다.

    repeat 횟수만큼 실행한 뒤 가장 짧은 시간을 사용한다. 작은 입력에서는 운영체제 상태에
    따라 시간이 흔들릴 수 있으므로, 최소 시간을 사용하면 비교가 조금 더 안정적이다.
    """
    if repeat <= 0:
        raise ValueError("repeat는 1 이상이어야 합니다.")

    best_time = float("inf")
    visited_count = 0

    for _ in range(repeat):
        start_time = time.perf_counter()
        result = bfs_result(graph, start)
        elapsed = time.perf_counter() - start_time
        best_time = min(best_time, elapsed)
        visited_count = len(result["order"])

    return best_time, visited_count


def measure_bfs_level_time(graph, start: object, repeat: int = 5) -> Tuple[float, int, int]:
    """BFS로 레벨 구조를 만드는 시간을 측정한다."""
    if repeat <= 0:
        raise ValueError("repeat는 1 이상이어야 합니다.")

    best_time = float("inf")
    level_count = 0
    visited_count = 0

    for _ in range(repeat):
        start_time = time.perf_counter()
        levels = bfs_levels(graph, start)
        elapsed = time.perf_counter() - start_time

        best_time = min(best_time, elapsed)
        level_count = len(levels)
        visited_count = sum(len(vertices) for vertices in levels.values())

    return best_time, level_count, visited_count


def measure_dfs_visit_time(graph, start: object, repeat: int = 5) -> Tuple[float, int]:
    """DFS로 방문 가능한 모든 정점을 순회하는 시간을 측정한다."""
    if repeat <= 0:
        raise ValueError("repeat는 1 이상이어야 합니다.")

    best_time = float("inf")
    visited_count = 0

    for _ in range(repeat):
        start_time = time.perf_counter()
        order = dfs_traversal(graph, start)
        elapsed = time.perf_counter() - start_time

        best_time = min(best_time, elapsed)
        visited_count = len(order)

    return best_time, visited_count


def compare_adj_list_and_matrix(
    cases: Iterable[Tuple[int, int]] | None = None,
    repeat: int = 5,
) -> List[ComplexityRow]:
    """여러 그래프 크기에 대해 인접 리스트와 인접 행렬 BFS 실행 시간을 비교한다."""
    if cases is None:
        cases = [
            (50, 100),
            (100, 250),
            (300, 700),
        ]

    rows: List[ComplexityRow] = []

    for vertex_count, edge_count in cases:
        edges = create_edges_for_complexity(vertex_count, edge_count)
        adj_list_graph = _build_adj_list(vertex_count, edges)
        adj_matrix_graph = _build_adj_matrix(vertex_count, edges)

        list_time, list_visited = measure_bfs_time(adj_list_graph, 0, repeat=repeat)
        matrix_time, matrix_visited = measure_bfs_time(adj_matrix_graph, 0, repeat=repeat)

        rows.append(
            ComplexityRow(
                vertex_count=vertex_count,
                edge_count=len(edges),
                adj_list_time=list_time,
                adj_matrix_time=matrix_time,
                adj_list_visited=list_visited,
                adj_matrix_visited=matrix_visited,
            )
        )

    return rows


def compare_bfs_level_and_dfs_visit(
    cases: Iterable[Tuple[int, int]] | None = None,
    repeat: int = 5,
) -> List[SearchBasisRow]:
    """BFS는 레벨 구조 생성 기준, DFS는 전체 방문 기준으로 실행 시간을 비교한다."""
    if cases is None:
        cases = [
            (50, 100),
            (100, 250),
            (300, 700),
        ]

    rows: List[SearchBasisRow] = []

    for vertex_count, edge_count in cases:
        edges = create_edges_for_complexity(vertex_count, edge_count)
        graph = _build_adj_list(vertex_count, edges)

        bfs_time, level_count, bfs_visited = measure_bfs_level_time(graph, 0, repeat=repeat)
        dfs_time, dfs_visited = measure_dfs_visit_time(graph, 0, repeat=repeat)

        rows.append(
            SearchBasisRow(
                vertex_count=vertex_count,
                edge_count=len(edges),
                bfs_level_count=level_count,
                bfs_visited_count=bfs_visited,
                dfs_visited_count=dfs_visited,
                bfs_level_time=bfs_time,
                dfs_visit_time=dfs_time,
            )
        )

    return rows
