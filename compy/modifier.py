from abc import ABC, abstractmethod
from typing import Callable, Protocol, Self


class ModifierBase[T](ABC):
    """Base class for widget modifiers."""

    @abstractmethod
    def apply(self, widget: T) -> None:
        pass


class ModifierProtocol[T](Protocol):
    def apply(self, widget: T) -> None: ...
    def padding(self, *paddings: int) -> Self:
        """
        Supports 1, 2, or 4 padding values.
        1 value: all
        2 values: top/bottom, left/right
        4 values: top, right, bottom, left
        """
        ...

    def size(self, width: int, height: int) -> Self: ...

    def width(self, width: int) -> Self: ...

    def height(self, height: int) -> Self: ...

    def background(self, color: str) -> Self: ...

    def clickable(self, on_click: Callable[[], None]) -> Self: ...

    def fill_max_width(self) -> Self: ...

    def fill_max_height(self) -> Self: ...

    def fill_max_size(self) -> Self: ...
