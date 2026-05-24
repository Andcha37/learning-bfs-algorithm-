# =============================================================================
# Maze -> Graph
# =============================================================================

def maze_to_graph(maze):
    """2차원 미로를 인접 리스트 형태의 그래프로 변환한다.

    `#`은 벽으로 보고 그래프에서 제외한다. `S`는 시작점, `G`는 목표점으로
    저장하며, 나머지 이동 가능한 칸은 모두 `(행, 열)` 좌표를 노드로 사용한다.
    각 노드는 상하좌우로 이동할 수 있는 칸들과 연결된다.

    Args:
        maze: 문자열 또는 문자 리스트로 표현한 2차원 미로.

    Returns:
        `(graph, start, goal)` 튜플.
        `graph`는 `{좌표: [이웃 좌표들]}` 형태의 인접 리스트이고,
        `start`와 `goal`은 각각 시작점과 목표점 좌표이다.

    Raises:
        ValueError: 미로의 행 길이가 서로 다르거나, S 또는 G가 없을 때 발생한다.
    """
    if not maze:
        return {}, None, None

    rows = len(maze)
    cols = len(maze[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    graph = {}
    start = None
    goal = None

    for row in range(rows):
        if len(maze[row]) != cols:
            raise ValueError("maze의 모든 행은 길이가 같아야 합니다.")

        for col in range(cols):
            if maze[row][col] == "#":
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
                    maze[next_row][next_col] != "#"
                ):
                    graph[node].append((next_row, next_col))

    if start is None:
        raise ValueError("미로에 시작점 S가 없습니다.")

    if goal is None:
        raise ValueError("미로에 목표점 G가 없습니다.")

    return graph, start, goal


# =============================================================================
# Path Reconstruction
# =============================================================================

def reconstruct_path(parent, start, goal):
    """BFS 탐색 중 기록한 parent 정보를 이용해 최단 경로를 복원한다.

    `parent[child] = previous` 형태로 저장된 값을 goal에서 start 방향으로
    거꾸로 따라간 뒤, 마지막에 순서를 뒤집어 start에서 goal까지의 경로로 만든다.

    Args:
        parent: 각 노드를 처음 발견한 이전 노드를 저장한 딕셔너리.
        start: 경로의 시작 노드.
        goal: 경로의 목표 노드.

    Returns:
        start부터 goal까지의 경로 리스트.
        goal에 도달하지 못한 경우에는 'None'을 반환한다.
    """
    if goal not in parent:
        return None

    path = []
    current = goal

    while current != start:
        path.append(current)
        current = parent[current]

    path.append(start)
    path.reverse()
    return path


# =============================================================================
# BFS
# =============================================================================

class _QueueNode:
    """직접 구현한 큐에서 값과 다음 노드 위치를 함께 저장하는 노드."""

    __slots__ = ("value", "next")

    def __init__(self, value):
        self.value = value
        self.next = None


class Queue:
    """외부 모듈 없이 head-tail 방식으로 구현한 FIFO 큐.

    리스트의 `pop(0)`은 맨 앞 원소를 제거할 때 뒤쪽 원소들을 한 칸씩
    당겨야 해서 O(n)이 된다. 이 큐는 head와 tail을 직접 관리해 삽입과
    삭제를 모두 O(1)에 처리한다.
    """

    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def is_empty(self):
        """큐가 비어 있는지 확인한다."""
        return self.head is None

    def append(self, value):
        """enqueue: tail 뒤에 새 값을 붙인다. O(1)."""
        node = _QueueNode(value)

        if self.tail is None:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            self.tail = node

        self.size += 1

    def popleft(self):
        """dequeue: head 값을 꺼내고 head를 다음 노드로 옮긴다. O(1)."""
        if self.head is None:
            raise IndexError("빈 큐에서 값을 꺼낼 수 없습니다.")

        node = self.head
        self.head = node.next

        if self.head is None:
            self.tail = None

        self.size -= 1
        return node.value

    def to_list(self):
        """현재 큐 상태를 앞에서 뒤 순서의 리스트로 반환한다."""
        result = []
        current = self.head

        while current is not None:
            result.append(current.value)
            current = current.next

        return result

    def __len__(self):
        """큐에 들어 있는 값의 개수를 반환한다."""
        return self.size


def bfs(graph, start, goal=None):
    """BFS로 그래프를 탐색하고, 필요하면 start에서 goal까지의 경로를 찾는다.

    BFS는 큐를 사용해 시작점에서 가까운 노드부터 차례대로 방문한다.
    가중치가 없는 그래프에서는 goal을 처음 발견했을 때의 경로가 최단 경로가 된다.

    Args:
        graph: `{노드: [이웃 노드들]}` 형태의 인접 리스트.
        start: 탐색을 시작할 노드.
        goal: 찾고 싶은 목표 노드. 생략하면 전체 탐색 순서만 반환한다.

    Returns:
        `{"order": 탐색 순서, "path": 최단 경로 또는 None}` 형태의 딕셔너리.

    Raises:
        ValueError: start 또는 goal이 graph 안에 없을 때 발생한다.
    """
    if start not in graph:
        raise ValueError("start가 graph에 없습니다.")

    if goal is not None and goal not in graph:
        raise ValueError("goal이 graph에 없습니다.")

    visited = {start}
    queue = Queue()
    queue.append(start)
    order = [start]
    parent = {start: None}

    if goal is not None and start == goal:
        return {"order": order, "path": [start]}

    # 리스트의 pop(0) 대신 직접 구현한 큐로 맨 앞 원소를 O(1)에 꺼낸다.
    while not queue.is_empty():
        current = queue.popleft()

        for neighbor in graph[current]:
            if neighbor in visited:
                continue

            visited.add(neighbor)
            parent[neighbor] = current
            order.append(neighbor)
            queue.append(neighbor)

            if goal is not None and neighbor == goal:
                path = reconstruct_path(parent, start, goal)
                return {"order": order, "path": path}

    return {"order": order, "path": None}
