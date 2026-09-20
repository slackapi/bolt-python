from typing import Generic, Iterator, List, TypeVar, Union, overload

ListenerT = TypeVar("ListenerT")


class ListenerRegistry(Generic[ListenerT]):
    def __init__(self) -> None:
        self._assistant_listeners: List[ListenerT] = []
        self._listeners: List[ListenerT] = []

    def append(self, listener: ListenerT) -> None:
        self._listeners.append(listener)

    def append_assistant(self, listener: ListenerT) -> None:
        self._assistant_listeners.append(listener)

    def __iter__(self) -> Iterator[ListenerT]:
        yield from self._assistant_listeners
        yield from self._listeners

    def __len__(self) -> int:
        return len(self._assistant_listeners) + len(self._listeners)

    @overload
    def __getitem__(self, index: int) -> ListenerT:
        pass

    @overload
    def __getitem__(self, index: slice) -> List[ListenerT]:
        pass

    def __getitem__(self, index: Union[int, slice]) -> Union[ListenerT, List[ListenerT]]:
        return list(self)[index]
