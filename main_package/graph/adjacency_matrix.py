"""인접 행렬 기반 그래프 구현.

정점 수가 V일 때 V x V 행렬을 사용한다. 두 정점의 연결 여부 확인은 빠르지만,
BFS에서 한 정점의 이웃을 찾으려면 행 전체를 확인해야 하므로 정점 수가 커질수록
인접 리스트보다 비효율적일 수 있다.
"""

from __future__ import annotations

from typing import Any, Dict, Iterable, List, Tuple

Vertex = Any
Edge = Tuple[Vertex, Vertex]


class GraphAdjMatrix:
    """2차원 리스트로 구현한 인접 행렬 그래프."""

    def __init__(self, directed: bool = False) -> None:
        self.directed = directed
        self._vertices: List[Vertex] = []
        self._index: Dict[Vertex, int] = {}
        self._matrix: List[List[int]] = []

    @classmethod
    def from_edges(cls, edges: Iterable[Edge], directed: bool = False) -> "GraphAdjMatrix":
        graph = cls(directed=directed)
        for u, v in edges:
            graph.add_edge(u, v)
        return graph

    def add_vertex(self, vertex: Vertex) -> None:
        if vertex in self._index:
            return

        self._index[vertex] = len(self._vertices)
        self._vertices.append(vertex)

        for row in self._matrix:
            row.append(0)
        self._matrix.append([0] * len(self._vertices))

    def add_edge(self, u: Vertex, v: Vertex) -> None:
        self.add_vertex(u)
        self.add_vertex(v)
        i, j = self._index[u], self._index[v]
        self._matrix[i][j] = 1
        if not self.directed:
            self._matrix[j][i] = 1

    def neighbors(self, vertex: Vertex) -> List[Vertex]:
        if vertex not in self._index:
            raise KeyError(f"그래프에 존재하지 않는 정점입니다: {vertex!r}")

        row_index = self._index[vertex]
        row = self._matrix[row_index]
        return [self._vertices[col_index] for col_index, connected in enumerate(row) if connected]

    def vertices(self) -> List[Vertex]:
        return list(self._vertices)

    def has_vertex(self, vertex: Vertex) -> bool:
        return vertex in self._index

    def has_edge(self, u: Vertex, v: Vertex) -> bool:
        if u not in self._index or v not in self._index:
            return False
        return self._matrix[self._index[u]][self._index[v]] == 1

    def edge_count(self) -> int:
        total = sum(sum(row) for row in self._matrix)
        return total if self.directed else total // 2

    def as_matrix(self) -> List[List[int]]:
        return [list(row) for row in self._matrix]

    def __contains__(self, vertex: Vertex) -> bool:
        return self.has_vertex(vertex)

    def __len__(self) -> int:
        return len(self._vertices)

    def __repr__(self) -> str:
        return f"GraphAdjMatrix(directed={self.directed}, vertices={self._vertices!r})"
