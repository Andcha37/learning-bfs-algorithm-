# BFS 알고리즘 구현 프로젝트

빅데이터프로그래밍1 과제로 진행한 BFS 구현 + 보고서용 코드입니다.

Queue 기반 탐색, 레벨 구조, 최단 경로, parent를 이용한 경로 복원까지 BFS의 핵심 동작을 외부 라이브러리 없이 직접 구현했습니다. 여기에 미로 최단 경로 탐색과 이분 그래프 판별을 포함하여 같은 BFS 코드가 실제 문제에서도 잘 돌아가는지 확인하는 데 초점을 뒀습니다.

## 실행 방법

```bash
python main.py
```

`main.py`를 돌리면 다음 순서로 결과가 출력됩니다.

1. 일반 그래프 BFS 방문 순서
2. BFS 최단 경로와 parent 정보
3. 미로를 그래프로 바꿔서 BFS 최단 경로 탐색
4. BFS 기반 이분 그래프 판별
5. BFS / DFS 방문 순서 비교
6. 복잡도 비교 + 인접 리스트 vs 인접 행렬 BFS 시간 측정

## 의존성

BFS 핵심 로직은 순수 파이썬으로만 짜서 별도 설치가 필요 없습니다. 외부 라이브러리는 **선택 기능인 시각화**에서만 `networkx`, `matplotlib`을 씁니다.

```bash
pip install -r requirements.txt
```

가상환경을 쓴다면:

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

## 폴더 구조

```text
main.py
main_package/
├── structures/      # 직접 구현한 Queue, Stack
│   ├── custom_queue.py
│   └── stack.py
├── graph/           # 인접 리스트 / 인접 행렬 그래프
│   ├── adjacency_list.py
│   ├── adjacency_matrix.py
│   └── graph_examples.py
├── bfs/             # BFS 탐색, 최단 경로
│   ├── traversal.py
│   └── shortest_path.py
├── maze/            # 미로 → 그래프 변환 후 BFS
│   ├── maze_to_graph.py
│   ├── maze_bfs.py
│   └── examples.py
├── bipartite/       # 이분 그래프 판별
│   └── check.py
├── dfs/             # 비교용 DFS
│   └── iterative.py
├── complexity/      # 실행 시간 측정
│   └── measure.py
└── visualization/   # 선택 기능
    ├── text_visualizer.py
    ├── graph_draw.py
    └── graphviz_draw.py
```

최종 실행/검토 기준은 `main.py`와 `main_package/`입니다.

## 직접 구현한 핵심

### Queue 직접 구현 (`structures/custom_queue.py`)

`collections.deque`나 `list.pop(0)`을 쓰지 않고, `head`와 `tail` 인덱스로 FIFO를 구현했습니다. 
`append`, `popleft`, `is_empty`, `__len__`을 제공합니다.

BFS에서는 정점을 **큐에 넣는 순간** 방문 처리하는데, 중복 처리를 막는 기능입니다.

### BFS 탐색 (`bfs/traversal.py`)

핵심은 `bfs_result(graph, start)`입니다. 한 번 돌리면 필요한 정보를 한꺼번에 묶어서 돌려줍니다.

```python
{
    "order":    방문 순서,
    "distance": 시작 정점에서 각 정점까지의 거리,
    "parent":   각 정점을 처음 발견했을 때의 이전 정점,
    "levels":   BFS 레벨 구조,
}
```

거리만, parent만, 레벨만 따로 필요할 때를 위해 `bfs_distances`, `bfs_parents`, `bfs_levels` 같은 단일 결과 버전도 같이 뒀습니다.

### BFS 최단 경로 (`bfs/shortest_path.py`)

비가중치 그래프에서는 BFS만으로 최단 경로가 나옵니다. 위에서 모은 `parent`를 이용해 도착점에서 시작점까지 거슬러 올라간 다음, `reverse()`로 뒤집어 실제 경로 순서로 복원합니다. (`bfs_shortest_path`, `reconstruct_path`, `shortest_distance`)

## 확장 기능

### 그래프: 인접 리스트 / 인접 행렬 (`graph/`)

`GraphAdjList`와 `GraphAdjMatrix` 둘 다 `neighbors()`, `vertices()`, `has_vertex()`를 똑같이 제공합니다. 덕분에 어느 그래프를 넣어도 동일한 방식으로 동작이 가능합니다.

### 미로 최단 경로 (`maze/`)

`S`(시작), `G`(도착), `0`(길), `1`(벽)으로 표현된 2차원 미로를 그래프로 변환해 BFS를 돌립니다. 이동 가능한 칸 하나를 정점으로 보고, 상하좌우로 붙어 있는 칸끼리 간선으로 잇는 방식입니다.

### 이분 그래프 판별 (`bipartite/check.py`)

BFS로 2-coloring을 하면서, 인접한 두 정점이 같은 색이 되는 순간을 잡아 이분 그래프가 아니라고 판정합니다. 연결 요소가 여러 개인 그래프도 처리하고, 이분 그래프가 아닐 때는 충돌이 난 간선도 함께 돌려줍니다. (`is_bipartite`, `check_bipartite_with_colors`)

### BFS vs DFS (`dfs/iterative.py`)

같은 그래프를 Stack 기반 DFS(`dfs_traversal`)로도 돌려서 방문 순서가 어떻게 달라지는지 비교합니다. 큐를 쓰느냐 스택을 쓰느냐의 차이가 코드에서 그대로 드러납니다.

## 복잡도 비교 (`complexity/measure.py`)

|     | 시간복잡도 | 공간복잡도 |
| --- | --------- | --------- |
| BFS | O(V + E)  | O(V)      |
| DFS | O(V + E)  | O(V)      |

이론값만 적어두는 데 그치지 않고, BFS 레벨 구조 생성과 DFS 전체 방문 시간을 직접 재서 비교하고(`compare_bfs_level_and_dfs_visit`), 인접 리스트 BFS와 인접 행렬 BFS의 실행 시간도 측정합니다(`compare_adj_list_and_matrix`).

## 시각화 (선택)

BFS 계산과는 분리된 부가 기능이라, 없어도 알고리즘 동작에는 영향이 없습니다.

- **텍스트 출력** (`visualization/text_visualizer.py`): `main.py` 결과를 보기 좋게 정리해서 찍는 용도
- **NetworkX + Matplotlib**: `python -m main_package.visualization.graph_draw` → `outputs/*.png` 생성
- **Graphviz**: `python -m main_package.visualization.graphviz_draw` → `outputs/graphviz/*.dot|png|svg` 생성


## 참고

- 저장소에 `bfs_dfs_comparison/`, `bipartite_check/`, `maze_shortest_path/` 같은 초안 폴더가 남아 있을 수 있는데, 검토는 `main.py` + `main_package/` 기준으로 봐주시면 됩니다.
- `.venv/`, `__pycache__/`, `.DS_Store`, `.env` 등은 `.gitignore`로 제외했습니다.
