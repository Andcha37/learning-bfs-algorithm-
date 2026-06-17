"""BFS 알고리즘 과제 실행 파일.

이 파일은 알고리즘을 직접 구현하지 않고, `main_package` 안의 모듈을 호출해
보고서에 넣을 수 있는 실행 결과를 순서대로 보여준다.
"""

from __future__ import annotations

from main_package.bfs.shortest_path import bfs_shortest_path
from main_package.bfs.traversal import bfs_result
from main_package.bipartite.check import check_bipartite_with_colors
from main_package.complexity.measure import (
    compare_adj_list_and_matrix,
    compare_bfs_level_and_dfs_visit,
)
from main_package.dfs.iterative import dfs_traversal
from main_package.graph.graph_examples import (
    create_basic_graph,
    create_bipartite_graph,
    create_non_bipartite_graph,
)
from main_package.maze.examples import get_blocked_maze, get_sample_maze
from main_package.maze.maze_bfs import bfs_maze_shortest_path
from main_package.maze.maze_to_graph import maze_to_graph
from main_package.visualization.text_visualizer import (
    format_path,
    print_bipartite_result,
    print_complexity_table,
    print_graph,
    print_maze,
    print_maze_result,
    print_section,
)


def run_basic_bfs_demo() -> None:
    """일반 그래프에서 BFS 방문 순서, distance, parent를 출력한다."""
    print_section("1. 일반 그래프 BFS 탐색")
    graph = create_basic_graph()

    print("그래프 인접 리스트:")
    print_graph(graph)

    result = bfs_result(graph, "A")
    print("\nBFS 방문 순서:")
    print(format_path(result["order"]))

    print("\n시작 정점 A로부터의 거리:")
    print(result["distance"])

    print("\nBFS 레벨 구조:")
    print(result["levels"])

    print("\nparent 정보:")
    print(result["parent"])


def run_shortest_path_demo() -> None:
    """비가중치 그래프에서 BFS 최단 경로와 parent 기반 경로 복원을 보여준다."""
    print_section("2. BFS 기반 최단 경로")
    graph = create_basic_graph()
    result = bfs_shortest_path(graph, "A", "F")

    print("A에서 F까지의 최단 경로:")
    print(format_path(result["path"]))
    print(f"최단 거리: {result['distance']}")
    print(f"방문 처리한 정점 수: {result['visited_count']}")
    print("\nparent 정보:")
    print(result["parent"])


def run_maze_demo() -> None:
    """미로를 그래프로 변환한 뒤 기존 BFS 최단 경로 함수를 적용한다."""
    print_section("3. 미로 -> 그래프 변환 -> BFS 최단 경로")
    maze = get_sample_maze()

    print("원본 미로:")
    print_maze(maze)

    maze_graph, start, goal = maze_to_graph(maze)
    edge_count = sum(len(neighbors) for neighbors in maze_graph.values()) // 2
    print("\n미로를 그래프로 변환한 결과:")
    print(f"시작점: {start}")
    print(f"도착점: {goal}")
    print(f"그래프 정점 수: {len(maze_graph)}")
    print(f"그래프 간선 수: {edge_count}")

    result = bfs_maze_shortest_path(maze)
    print_maze_result(result)

    print("\n경로가 없는 미로 예시:")
    blocked_result = bfs_maze_shortest_path(get_blocked_maze())
    print(f"found: {blocked_result['found']}")
    print(f"message: {blocked_result['message']}")
    print(f"visited_count: {blocked_result['visited_count']}")


def run_bipartite_demo() -> None:
    """BFS 2-Coloring으로 이분 그래프 여부를 판별한다."""
    print_section("4. BFS 기반 이분 그래프 판별")

    bipartite_result = check_bipartite_with_colors(create_bipartite_graph())
    non_bipartite_result = check_bipartite_with_colors(create_non_bipartite_graph())

    print_bipartite_result("이분 그래프 예시", bipartite_result)
    print_bipartite_result("이분 그래프가 아닌 예시", non_bipartite_result)


def run_bfs_dfs_compare_demo() -> None:
    """같은 그래프에서 BFS와 DFS 방문 순서 차이를 비교한다."""
    print_section("5. BFS와 DFS 탐색 순서 비교")
    graph = create_basic_graph()

    bfs_order = bfs_result(graph, "A")["order"]
    dfs_order = dfs_traversal(graph, "A")

    print("그래프 인접 리스트:")
    print_graph(graph)
    print("\nBFS 방문 순서:")
    print(format_path(bfs_order))
    print("\nDFS 방문 순서:")
    print(format_path(dfs_order))


def run_complexity_demo() -> None:
    """인접 리스트와 인접 행렬에서 같은 그래프 데이터의 BFS 실행 시간을 비교한다."""
    print_section("6. BFS/DFS 복잡도 비교")

    print("복잡도 계산 기준:")
    print("BFS: 레벨 구조를 만드는 과정 기준, 시간복잡도 O(V + E), 공간복잡도 O(V)")
    print("DFS: 시작 정점에서 방문 가능한 모든 정점을 순회하는 과정 기준, 시간복잡도 O(V + E), 공간복잡도 O(V)")

    print("BFS 레벨 구조 생성 기준 / DFS 전체 방문 기준:")
    basis_rows = compare_bfs_level_and_dfs_visit()
    print("정점 수 | 간선 수 | BFS 레벨 수 | BFS 방문 수 | DFS 방문 수 | BFS 레벨 시간(s) | DFS 방문 시간(s)")
    print("-" * 105)
    for row in basis_rows:
        print(
            f"{row.vertex_count:>6} | "
            f"{row.edge_count:>6} | "
            f"{row.bfs_level_count:>10} | "
            f"{row.bfs_visited_count:>10} | "
            f"{row.dfs_visited_count:>10} | "
            f"{row.bfs_level_time:>16.8f} | "
            f"{row.dfs_visit_time:>16.8f}"
        )

    print("\n인접 리스트와 인접 행렬 BFS 시간 비교:")
    rows = compare_adj_list_and_matrix()
    print_complexity_table(rows)


def main() -> None:
    run_basic_bfs_demo()
    run_shortest_path_demo()
    run_maze_demo()
    run_bipartite_demo()
    run_bfs_dfs_compare_demo()
    run_complexity_demo()


if __name__ == "__main__":
    main()
