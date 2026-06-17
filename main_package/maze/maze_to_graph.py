"""2차원 미로를 인접 리스트 형태의 그래프로 변환하는 모듈"""


def maze_to_graph(maze):
    """미로에서 이동 가능한 각 칸들을 좌표 정점으로 보고, 상하좌우로 이동 가능한 칸들을 간선으 연결하여
      `{좌표: [이웃 좌표들]}` 형태의 인접 리스트 그래프로 변환하였다.
       이렇게 변환한 그래프는 기존 BFS 모듈의 입력으로 사용할 수 있다.."""

    """`1`은 벽으로 보고 그래프에서 제외한다.
    `S`는 시작점,
    `G`는 목표점으로 저장한다."""
    
    if not maze:
        return {}, None, None

    rows = len(maze)
    cols = len(maze[0])

    for row in maze:
        if len(row) != cols:
            raise ValueError("미로의 행은 길이가 같아야 합니다.")

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    wall = "1"

    graph = {}
    start = None
    goal = None

    for row in range(rows):
        for col in range(cols):
            if maze[row][col] == wall:
                continue

            node = (row, col)
            graph[node] = []

            if maze[row][col] == "S":
                start = node
            elif maze[row][col] == "G":
                goal = node

            for dr, dc in directions:
                next_row = row + dr
                next_col = col + dc

                if (
                    0 <= next_row < rows and
                    0 <= next_col < cols and
                    maze[next_row][next_col] != wall
                ):
                    graph[node].append((next_row, next_col))

    if start is None:
        raise ValueError("미로에 시작점 S가 없습니다.")

    if goal is None:
        raise ValueError("미로에 목표점 G가 없습니다.")

    return graph, start, goal
