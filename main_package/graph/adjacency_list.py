"""인접 리스트 기반 그래프 구현."""


class GraphAdjList:
    """딕셔너리와 리스트를 이용한 인접 리스트 그래프."""

    def __init__(self, directed=False):
        self.directed = directed
        self.graph = {}

    def add_vertex(self, vertex):
        """정점을 추가한다."""
        if vertex not in self.graph:
            self.graph[vertex] = []

    def add_edge(self, u, v):
        """두 정점을 간선으로 연결한다."""
        self.add_vertex(u)
        self.add_vertex(v)

        if v not in self.graph[u]:
            self.graph[u].append(v)

        if not self.directed and u not in self.graph[v]:
            self.graph[v].append(u)

    def neighbors(self, vertex):
        """정점과 연결된 이웃 정점들을 반환한다."""
        if vertex not in self.graph:
            raise KeyError(f"그래프에 없는 정점입니다: {vertex!r}")
        return self.graph[vertex]

    def vertices(self):
        """그래프의 전체 정점 목록을 반환한다."""
        return list(self.graph.keys())

    def has_vertex(self, vertex):
        """정점이 그래프에 있는지 확인한다."""
        return vertex in self.graph

    def edge_count(self):
        """그래프의 간선 수를 반환한다."""
        total = sum(len(neighbors) for neighbors in self.graph.values())
        if self.directed:
            return total
        return total // 2

    def __len__(self):
        return len(self.graph)

    def __str__(self):
        lines = []
        for vertex in self.graph:
            lines.append(f"{vertex}: {self.graph[vertex]}")
        return "\n".join(lines)
