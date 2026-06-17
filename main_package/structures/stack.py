"""DFS 비교 실험에 사용할 직접 구현 Stack 자료구조."""

from __future__ import annotations

from typing import Generic, Iterable, List, Optional, TypeVar

T = TypeVar("T")


class EmptyStackError(IndexError):
    """비어 있는 Stack에서 pop 또는 peek를 호출했을 때 발생하는 예외."""


class CustomStack(Generic[T]):
    """리스트 기반 LIFO Stack.

    DFS는 한 경로를 깊게 탐색하는 방식이므로, 나중에 들어온 데이터가 먼저 나가는
    Stack 구조와 잘 맞는다.
    """

    def __init__(self, values: Optional[Iterable[T]] = None) -> None:
        self._items: List[T] = list(values) if values is not None else []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        if self.is_empty():
            raise EmptyStackError("비어 있는 Stack에서는 pop을 수행할 수 없습니다.")
        return self._items.pop()

    def peek(self) -> T:
        if self.is_empty():
            raise EmptyStackError("비어 있는 Stack에서는 peek를 수행할 수 없습니다.")
        return self._items[-1]

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def size(self) -> int:
        return len(self._items)

    def clear(self) -> None:
        self._items.clear()

    def to_list(self) -> List[T]:
        return list(self._items)

    def __len__(self) -> int:
        return self.size()

    def __bool__(self) -> bool:
        return not self.is_empty()

    def __repr__(self) -> str:
        return f"CustomStack({self._items!r})"
