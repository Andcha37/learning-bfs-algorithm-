import numpy as np


def bfs_shortest_path(graph, start, end):
    """
    인접 리스트 형태의 그래프에서 시작점부터 도착점까지의 최단 거리를 구하는 함수
    (큐와 거리 배열은 numpy만 사용, 예외 처리 포함)

    :param graph: 인접 리스트 (예: [[1, 2], [0, 3], ...])
    :param start: 시작 노드
    :param end: 도착 노드
    :return: 최단 거리 또는 예외 메시지
    """
    n = len(graph)

    # 1. 예외 처리: 시작점이나 도착점이 그래프 범위를 벗어난 경우
    if start < 0 or start >= n or end < 0 or end >= n:
        return "해당 점이 경로 내에 없습니다"

    # 2. numpy를 활용한 Queue 및 거리 배열 초기화
    # 최대 n개의 노드가 들어가므로 크기를 n으로 설정
    queue = np.zeros(n, dtype=int)
    head = 0
    tail = 0

    # 거리를 기록할 배열 (-1로 초기화하여 미방문 상태 표시)
    distances = np.full(n, -1, dtype=int)

    # 시작점 초기화
    queue[tail] = start
    tail += 1
    distances[start] = 0

    # 3. BFS 탐색 진행
    while head < tail:
        current = queue[head]
        head += 1

        # 목적지에 도달한 경우 현재까지의 거리 반환
        if current == end:
            return distances[current]

        # 인접 리스트를 활용하여 연결된 이웃 노드만 탐색
        for neighbor in graph[current]:
            if distances[neighbor] == -1:  # 아직 방문하지 않은 노드인 경우
                distances[neighbor] = distances[current] + 1
                queue[tail] = neighbor
                tail += 1

    # 4. 예외 처리: 큐를 모두 비웠으나 목적지에 도달하지 못한 경우
    return "경로를 찾을 수 없습니다"


# ==========================================
# 💡 사용 예시 및 테스트
# ==========================================

# 노드가 0부터 5까지 있는 그래프의 인접 리스트 구현
# 0-1, 1-2, 2-3, 3-4 연결 (노드 5는 고립됨)
adj_list = [
    [1],  # 노드 0과 연결된 노드들
    [0, 2],  # 노드 1과 연결된 노드들
    [1, 3],  # 노드 2와 연결된 노드들
    [2, 4],  # 노드 3과 연결된 노드들
    [3],  # 노드 4와 연결된 노드들
    []  # 노드 5 (어디와도 연결되지 않음)
]

print("--- 테스트 결과 ---")
# 1. 정상적인 최단 거리
print(f"0 -> 4: {bfs_shortest_path(adj_list, 0, 4)}")

# 2. 경로가 단절된 경우
print(f"0 -> 5: {bfs_shortest_path(adj_list, 0, 5)}")

# 3. 그래프에 없는 점을 입력한 경우 (범위 초과)
print(f"0 -> 9: {bfs_shortest_path(adj_list, 0, 9)}")
print(f"-1 -> 2: {bfs_shortest_path(adj_list, -1, 2)}")