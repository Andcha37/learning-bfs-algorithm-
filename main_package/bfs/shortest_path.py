"""BFS 기반 일반 그래프 최단 경로 탐색."""

from main_package.structures.custom_queue import Queue

def reconstruct_path(parent, start, goal):
    """BFS가 저장한 parent 정보를 이용해서 실제 경로를 복원하는 함수"""
    if goal not in parent:
        return None
    """parent["B"] = "A"
       parent["C"] = "A"
       parent["F"] = "C"
       의 형태로 저장된다. 각 정보는 ["B"]는 A에서 발견됐다. 라는 정보를 담고있음."""

    path = []
    """경로를 담는 리스트"""
    current = goal
    """발표에서 사용한 예시처럼 경로 복원은 goal에서부터 거꾸로 시작함"""

    while current != start:
        """도착점에서 시작해서 현재 위치가 시작점이 될 때 까지 반복"""
        path.append(current)
        current = parent[current]
        """현재 정점을 부모 정점으로 변경"""

    path.append(start)
    path.reverse() # 경로 복원은 거꾸로 시작했으므로 순서를 거꾸로 뒤집어준다.
    return path


def bfs_shortest_path(graph, start, goal):
    """start에서 goal까지 BFS로 최단 경로를 찾는다."""
    if isinstance(graph, dict):
        if start not in graph:
            raise ValueError("start가 graph에 없습니다.") # 예외처리 1: 그래프에 시작점이 없을 때
        if goal not in graph:
            raise ValueError("goal이 graph에 없습니다.") # 예외처리 2: 그래프에 도착점이 없을 때
    else:
        if not graph.has_vertex(start):
            raise ValueError(f"시작 정점이 그래프에 존재하지 않습니다: {start!r}") # 예외처리 1
        if not graph.has_vertex(goal):
            raise ValueError(f"도착 정점이 그래프에 존재하지 않습니다: {goal!r}") # 예외처리 2
    """그래프를 확인하는 부분. 그래프가 딕셔너리 구조인지, 인접리스트, 인접행렬 구조인지 확인함.
       딕셔너리가 아니라 GraphAdjlist 같은 객체일 경우 if not graph.has_vertex(start): 코드를 실행하여
       그래프 내에 시작점이 있늦ㄴ지 확인하고 없다면 오류 메세지가 출력""" 

    visited = {start} # 방문한 정점(정확히는 큐에 넣은 정점)을 저장
    queue = Queue()
    queue.append(start) # 시작 정점을 Queue에 넣는다.

    order = [start] # 정점을 발견한 순서를 저장 (맨 처음은 시작점)
    distance = {start: 0} # 시작 정점까지의 거리는 당연히 0
    parent = {start: None} # 시작 정점은 부모가 없으므로 None.

    if start == goal: # 예외 처리 3: 시작점과 도착점이 같은 경우
        return {
            "found": True,
            "path": [start],
            "distance": 0,
            "visited_count": 1,
            "order": order,
            "parent": parent,
        }

    while not queue.is_empty(): # Queue가 빌 때까지 반복
        current = queue.popleft() # 큐의 맨 앞에서 정점을 하나 꺼내서 현재 정점으로 삼는다. (직접 구현한 큐)

        # 이웃 정점 불러오기 (그래프의 형태에 따라 불러오는 방식이 다름)
        if isinstance(graph, dict): # 딕셔너리 그래프의 경우
            neighbors = graph[current]
        else: # 객체 그래프의 경우
            neighbors = graph.neighbors(current)

        for neighbor in neighbors: # 현재 정점과 연결된 이웃 정점들을 전부 확인해서
            if neighbor in visited: # 이미 visited에 있는(=큐에 넣은 적 있는) 정점이면
                continue # 건너뛴다.

            visited.add(neighbor) # 만약 처음 발견한 정점이면 visited에 저장하고
            parent[neighbor] = current # 현재 정점을 발견한 정점의 부모로 기록한 후,
            distance[neighbor] = distance[current] + 1 # (이웃 정점까지의 거리는 현재 정점 거리보다 당연히 1만큼 더 큼 -> 레벨별 탐색이니까)
            order.append(neighbor) # 방문 순서에 이웃 정점을 추가하고
            queue.append(neighbor) # queue에 이웃 정점을 넣는다.

            if neighbor == goal: # 만약 이웃 정점이 목표 정점이면 최단 경로를 찾은 것이므로
                path = reconstruct_path(parent, start, goal) # 실제 경로를 복원함
                return {
                    "found": True,
                    "path": path,
                    "distance": distance[goal],
                    "visited_count": len(visited),
                    "order": order,
                    "parent": parent,
                }
    #예외 처리 4: 경로가 없는 경우
    return {
        "found": False, # 도착점을 못 찾음
        "path": [], # 최단 경로는 없음
        "distance": None, # 도착점까지의 거리는 당연히 None
        "visited_count": len(visited),
        "order": order,
        "parent": parent,
    }


def shortest_distance(graph, start, goal):
    """start에서 goal까지의 최단 거리만 반환한다."""
    return bfs_shortest_path(graph, start, goal)["distance"]
