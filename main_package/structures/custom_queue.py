"""BFS에서 사용할 직접 구현 Queue 자료구조.
리스트의 pop(0)은 앞 원소를 꺼낼 때 나머지 원소들이 모두 앞으로 이동해야 해서 비효율적이고
front 인덱스를 증가시키는 방식도 실제 값이 리스트에 계속 남아 있어서 비효율적이므로
head와 tail을 직접 관리하는 연결구조 방식으로 Queue를 구현했다.
"""


class _QueueNode:
    """큐에 들어갈 값과 다음 노드 위치를 저장하는 노드"""

    def __init__(self, value):
        self.value = value # 노드에 실제 저장할 값
        self.next = None # 다음 노드를 가리키는 변수. ex) A가 B랑 연결되면 A.next = B 가 됨


# FIFO
class Queue:
    def __init__(self, values=None):
        self.head = None
        self.tail = None
        self.size = 0
        # 큐가 비어있으므로 초기값은 head = None, tail = None, size = 0

        if values is not None:
            for value in values:
                self.append(value)

    def is_empty(self):
        """큐가 비어 있는지 확인(큐가 비어있으면 당연히 head가 없으니까 None)"""
        return self.head is None
        # shortest_path에서는 while not queue.is_empty(): 로 사용

    def append(self, value):
        """큐의 뒤쪽에 값을 넣는다"""
        node = _QueueNode(value) # 값을 저장한 새 노드를 만듦

        if self.tail is None: # 큐가 비어있다면
            self.head = node
            self.tail = node
            """처음 들어온 노드는 head이자 tail (하나밖에 없으니까)"""
        else: # 큐가 비어있지 않다면
            self.tail.next = node # 기존 tail 의 next에 방금 추가한 노드를 연결하고
            self.tail = node # tail을 기존tail에서 방금 추가한 노드로 옮긴다

        self.size += 1 # 큐에 노드가 하나 추가되었으므로 사이즈를 1만큼 늘림

    def popleft(self):
        """큐의 앞쪽 값을 꺼낸다"""
        if self.head is None: # 예외처리 : 빈 큐에서 값을 꺼내려고 할 때 에러
            raise IndexError("빈 큐에서 값을 꺼낼 수 없습니다.")

        node = self.head # 꺼낼 노드
        self.head = node.next # 맨 앞 head는 이제 빠져야 하니까 그 다음 노드로 head를 옮겨준다

        if self.head is None: # 만약 head를 꺼낸 후 큐가 완전히 비었다면
            self.tail = None # tail도 존재할 수 없으므로 없애준다

        self.size -= 1 # 큐에서 노드가 하나 빠졌으므로 사이즈를 1만큼 줄임
        return node.value

    def __len__(self):
        return self.size
