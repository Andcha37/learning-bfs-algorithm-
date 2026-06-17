"""미로를 그래프로 바꾼 뒤 기존 BFS 최단 경로 함수를 적용하는 모듈."""
"""
   <작동 방식>
   1. 이전 maze_to_graph()로 미로를 graph, start, gola로 바꿨음
   2. bfs_shortest_path(graph, start, goal)을 호출해서
   3. BFS 결과의 path를 이용해서 원래 미로에 * 표시를 하고,
   4. 미로용 결과 딕셔너리로 정리해서 보여줌
"""

from main_package.bfs.shortest_path import bfs_shortest_path
# bfs_shortest_path 함수를 가져온다. 이 함수를 통해 start에서 goal 까지의 최단 경로를 찾는다.
from main_package.maze.maze_to_graph import maze_to_graph
# maze_to_graph 함수를 가져온다. {좌표: [이웃 좌표들]} 형태의 그래프로 바꿔주는 역할을 한다.


def count_edges(graph):
    """무방향 그래프의 간선 수를 센다."""
    return sum(len(neighbors) for neighbors in graph.values()) // 2
    """[중요] 예를 들어 무방향 그래프에서 A와 B가 연결되어 있으면 보통
             A: [B]
             B: [A]
             의 형태로 저장되는데, 이렇게 되면 하나의 간선인데 양쪽에 두 번 들어간 게 되기 떄문에
             전체 이웃 개수를 다 더하고 2로 나눠주는 것.
             전체 연결 개수 = 2
             실제 간선 수 = 2 // 2 = 1"""


def draw_path(maze, path, path_symbol="*"):
    """최단 경로를 미로 위에 표시한다."""
    """path_symbol은 경로를 표시해주는 것"""
    
    board = [list(row) for row in maze]
    """ 문자열로 된 미로를 수정할 수 있게 바꿔주는 부분
        원래 미로는 ["S0010", "01010"] 과 같은 형태면 변경이 불가하니까
        각각을 "S0010" -> ["S", "0", "0", "1", "0"] 처럼 리스트로 바꿔줌"""

    for row, col in path:
        """(0,1) 좌표는 row가 0, col이 1"""
        if board[row][col] not in {"S", "G"}:
            """시작점과 도착점은 덮지 않고"""
            board[row][col] = path_symbol
            """특정 좌표를 *로 바꿔주는 것"""
    

    return ["".join(row) for row in board]
    """처리가 완료되면 다시 문자 리스트를 문자열로 합쳐서 반환해준다.
       ["S", "*", "*", "1", "0"] -> "S**10" """


def bfs_maze_shortest_path(maze):
    """미로를 그래프로 변환했으면 BFS로 최단 경로를 찾는다."""
    graph, start, goal = maze_to_graph(maze)
    shortest = bfs_shortest_path(graph, start, goal)
    """변환한 그래프를 bfs_shortest_path에 넣어준다."""

    path = shortest["path"]
    found = shortest["found"]

    if found:
        marked_maze = draw_path(maze, path)
        message = "최단 경로를 찾았습니다."
    else:
        marked_maze = list(maze)
        message = "도착점까지의 경로가 존재하지 않습니다."

    return {
        "found": found,
        "path": path,
        "distance": shortest["distance"],
        "visited_count": shortest["visited_count"],
        "visited_order": shortest["order"],
        "marked_maze": marked_maze,
        "graph_vertex_count": len(graph),
        "graph_edge_count": count_edges(graph),
        "start": start,
        "goal": goal,
        "message": message,
    }
