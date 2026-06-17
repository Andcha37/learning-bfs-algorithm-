"""일반 그래프 BFS 탐색 구현."""

from main_package.structures.custom_queue import Queue


def bfs_result(graph, start):
    """시작 정점에서 BFS를 수행하고 방문 순서, 거리, parent를 반환한다."""
    if isinstance(graph, dict):
        if start not in graph:
            raise ValueError("시작 정점이 graph에 없습니다.")
    elif not graph.has_vertex(start):
        raise ValueError(f"시작 정점이 그래프에 존재하지 않습니다: {start!r}")

    visited = {start}
    queue = Queue()
    queue.append(start)

    order = []
    distance = {start: 0}
    parent = {start: None}
    levels = {0: [start]}

    while not queue.is_empty():
        current = queue.popleft()
        order.append(current)

        if isinstance(graph, dict):
            neighbors = graph[current]
        else:
            neighbors = graph.neighbors(current)

        for neighbor in neighbors:
            if neighbor in visited:
                continue

            visited.add(neighbor)
            distance[neighbor] = distance[current] + 1
            parent[neighbor] = current

            level = distance[neighbor]
            if level not in levels:
                levels[level] = []
            levels[level].append(neighbor)

            queue.append(neighbor)

    return {
        "order": order,
        "distance": distance,
        "parent": parent,
        "levels": levels,
    }


def bfs_traversal(graph, start):
    """BFS 방문 순서만 반환한다."""
    return bfs_result(graph, start)["order"]


def bfs_distances(graph, start):
    """시작 정점에서 각 정점까지의 거리를 반환한다."""
    return bfs_result(graph, start)["distance"]


def bfs_parents(graph, start):
    """BFS 과정에서 만들어진 parent 정보를 반환한다."""
    return bfs_result(graph, start)["parent"]


def bfs_levels(graph, start):
    """BFS 결과를 레벨별 정점 목록으로 반환한다."""
    return bfs_result(graph, start)["levels"]


def bfs_all_components(graph):
    """연결 요소별 BFS 방문 순서를 반환한다."""
    all_visited = set()
    components = []

    starts = list(graph.keys()) if isinstance(graph, dict) else graph.vertices()

    for start in starts:
        if start in all_visited:
            continue

        result = bfs_result(graph, start)
        order = result["order"]
        all_visited.update(order)
        components.append(order)

    return components
