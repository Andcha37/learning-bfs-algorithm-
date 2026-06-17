"""BFS 기반 이분 그래프 판별.

그래프의 정점을 두 색으로 칠하면서, 인접한 두 정점이 같은 색을 갖는 충돌이
발생하는지 확인한다. 연결 요소가 여러 개인 그래프도 처리하기 위해 모든 정점을
순회한다.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Protocol, Tuple

from main_package.structures.custom_queue import Queue

Vertex = Any
Color = int
Conflict = Tuple[Vertex, Vertex]


class NeighborGraph(Protocol):
    def neighbors(self, vertex: Vertex) -> List[Vertex]:
        ...

    def vertices(self) -> List[Vertex]:
        ...


@dataclass
class BipartiteResult:
    """이분 그래프 판별 결과."""

    is_bipartite: bool
    colors: Dict[Vertex, Color]
    conflict: Conflict | None
    message: str

    def to_dict(self) -> Dict[str, object]:
        return {
            "is_bipartite": self.is_bipartite,
            "colors": self.colors,
            "conflict": self.conflict,
            "message": self.message,
        }


def check_bipartite_with_colors(graph: NeighborGraph) -> BipartiteResult:
    """BFS 2-Coloring으로 이분 그래프 여부와 색 정보를 함께 반환한다."""
    colors: Dict[Vertex, Color] = {}

    for start in graph.vertices():
        if start in colors:
            continue

        colors[start] = 0
        queue: Queue[Vertex] = Queue([start])

        while not queue.is_empty():
            current = queue.popleft()
            current_color = colors[current]

            for neighbor in graph.neighbors(current):
                if neighbor not in colors:
                    colors[neighbor] = 1 - current_color
                    queue.append(neighbor)
                    continue

                if colors[neighbor] == current_color:
                    return BipartiteResult(
                        is_bipartite=False,
                        colors=colors,
                        conflict=(current, neighbor),
                        message=(
                            f"같은 색의 정점이 서로 연결되어 있습니다: "
                            f"{current!r} - {neighbor!r}"
                        ),
                    )

    return BipartiteResult(
        is_bipartite=True,
        colors=colors,
        conflict=None,
        message="모든 간선이 서로 다른 색의 정점 사이에 있으므로 이분 그래프입니다.",
    )


def is_bipartite(graph: NeighborGraph) -> bool:
    """그래프가 이분 그래프이면 True를 반환한다."""
    return check_bipartite_with_colors(graph).is_bipartite
