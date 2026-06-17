"""Stack을 이용한 반복 방식 DFS 구현.

보고서에서 BFS와 DFS의 자료구조 차이를 비교하기 위한 보조 모듈이다.
"""

from __future__ import annotations

from typing import Any, List, Protocol

from main_package.structures.stack import CustomStack

Vertex = Any


class NeighborGraph(Protocol):
    def neighbors(self, vertex: Vertex) -> List[Vertex]:
        ...

    def has_vertex(self, vertex: Vertex) -> bool:
        ...


def dfs_traversal(graph: NeighborGraph, start: Vertex) -> List[Vertex]:
    """반복 방식 DFS 방문 순서를 반환한다."""
    if hasattr(graph, "has_vertex") and not graph.has_vertex(start):
        raise ValueError(f"시작 정점이 그래프에 존재하지 않습니다: {start!r}")

    stack: CustomStack[Vertex] = CustomStack([start])
    visited = set()
    order: List[Vertex] = []

    while not stack.is_empty():
        current = stack.pop()
        if current in visited:
            continue

        visited.add(current)
        order.append(current)

        # Stack은 나중에 넣은 정점이 먼저 나오므로, 인접 리스트 순서와 유사하게 방문하려면 역순으로 push한다.
        for neighbor in reversed(graph.neighbors(current)):
            if neighbor not in visited:
                stack.push(neighbor)

    return order
