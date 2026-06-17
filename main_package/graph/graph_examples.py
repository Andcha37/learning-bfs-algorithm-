"""보고서와 main.py에서 사용할 예제 그래프 모음."""

from __future__ import annotations

from typing import List, Tuple

from main_package.graph.adjacency_list import GraphAdjList

Edge = Tuple[object, object]


def create_basic_graph() -> GraphAdjList:
    """BFS/DFS 방문 순서 비교에 사용할 간단한 무방향 그래프."""
    graph = GraphAdjList(directed=False)
    edges = [
        ("A", "B"),
        ("A", "C"),
        ("B", "D"),
        ("B", "E"),
        ("C", "F"),
        ("E", "F"),
    ]
    for u, v in edges:
        graph.add_edge(u, v)
    return graph


def create_bipartite_graph() -> GraphAdjList:
    """이분 그래프인 예시."""
    graph = GraphAdjList(directed=False)
    edges = [
        ("학생A", "수업1"),
        ("학생A", "수업2"),
        ("학생B", "수업1"),
        ("학생B", "수업3"),
        ("학생C", "수업2"),
    ]
    for u, v in edges:
        graph.add_edge(u, v)
    return graph


def create_non_bipartite_graph() -> GraphAdjList:
    """삼각형 사이클을 포함해 이분 그래프가 아닌 예시."""
    graph = GraphAdjList(directed=False)
    edges = [
        ("A", "B"),
        ("B", "C"),
        ("C", "A"),
    ]
    for u, v in edges:
        graph.add_edge(u, v)
    return graph


def create_edges_for_complexity(vertex_count: int, edge_count: int) -> List[Edge]:
    """복잡도 비교용 결정적 간선 목록 생성.

    랜덤을 사용하지 않아 실행할 때마다 같은 결과가 나오며, 가능한 한 연결 그래프에
    가깝게 만들기 위해 먼저 0-1-2-... 형태의 체인 간선을 넣는다.
    """
    if vertex_count <= 0:
        raise ValueError("vertex_count는 1 이상이어야 합니다.")

    max_edges = vertex_count * (vertex_count - 1) // 2
    target_edges = min(edge_count, max_edges)
    edges: List[Edge] = []
    seen = set()

    def add(u: int, v: int) -> None:
        if u == v:
            return
        a, b = (u, v) if u < v else (v, u)
        if (a, b) in seen:
            return
        seen.add((a, b))
        edges.append((a, b))

    for vertex in range(vertex_count - 1):
        if len(edges) >= target_edges:
            return edges
        add(vertex, vertex + 1)

    step = 2
    while len(edges) < target_edges:
        added_in_round = False
        for vertex in range(vertex_count):
            if len(edges) >= target_edges:
                break
            add(vertex, (vertex + step) % vertex_count)
            added_in_round = True
        step += 1
        if not added_in_round or step > vertex_count:
            break

    return edges
