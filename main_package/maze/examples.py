"""미로 BFS 예제 실행 모듈."""

from main_package.maze.maze_bfs import bfs_maze_shortest_path
from main_package.visualization.text_visualizer import print_maze, print_maze_result, print_section


def get_sample_maze():
    """가장 기본적인 미로 예시"""
    return [
        "S0010",
        "01010",
        "00000",
        "01110",
        "0000G",
    ]


def get_blocked_maze():
    """경로가 없는 예외 상황 예시"""
    return [
        "S010",
        "1110",
        "0001",
        "010G",
    ]


def get_large_maze():
    """규모가 큰 미로 예시"""
    return [
        "S0001000",
        "11101010",
        "00001010",
        "01111010",
        "00000010",
        "01111110",
        "0000000G",
    ]


def run_maze_demo():
    """미로 BFS 예시를 출력한다."""
    print_section("미로 최단 경로 탐색")
    maze = get_sample_maze()
    print("원본 미로:")
    print_maze(maze)

    result = bfs_maze_shortest_path(maze)
    print_maze_result(result)

    print("\n경로가 없는 미로 예시:")
    blocked_result = bfs_maze_shortest_path(get_blocked_maze())
    print(f"found: {blocked_result['found']}")
    print(f"message: {blocked_result['message']}")
    print(f"visited_count: {blocked_result['visited_count']}")
