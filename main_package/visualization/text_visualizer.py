"""외부 라이브러리 없이 결과를 보기 좋게 출력하는 텍스트 출력 모듈."""


def print_section(title):
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)


def format_path(path):
    return " -> ".join(str(item) for item in path)


def print_graph(graph):
    for vertex in graph.vertices():
        neighbors = ", ".join(str(neighbor) for neighbor in graph.neighbors(vertex))
        print(f"{vertex}: {neighbors}")


def print_maze(maze):
    for row in maze:
        print(row)


def print_maze_result(result):
    print("\n경로 표시 미로:")
    print_maze(result["marked_maze"])
    print(f"\n탐색 결과: {result['message']}")
    print(f"최단 이동 횟수: {result['distance']}")
    print(f"방문 처리한 칸 수: {result['visited_count']}")
    print(f"최단 경로 좌표: {result['path']}")


def print_bipartite_result(title, result):
    print(f"\n{title}")
    print(f"판별 결과: {result.is_bipartite}")
    print(f"메시지: {result.message}")
    print(f"색 정보: {result.colors}")
    if result.conflict is not None:
        print(f"충돌 간선: {result.conflict}")


def print_complexity_table(rows):
    print("정점 수 | 간선 수 | 인접 리스트 BFS 시간(s) | 인접 행렬 BFS 시간(s) | 방문 정점 수")
    print("-" * 86)
    for row in rows:
        print(
            f"{row.vertex_count:>6} | "
            f"{row.edge_count:>6} | "
            f"{row.adj_list_time:>20.8f} | "
            f"{row.adj_matrix_time:>20.8f} | "
            f"{row.adj_list_visited:>10}"
        )
