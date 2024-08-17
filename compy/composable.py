from functools import wraps
from typing import Any, Callable, Self, cast

from compy.modifier import ModifierProtocol
from compy.widget import ButtonWidget, ColumnWidget, RowWidget, TextWidget, Widget
from compy.widget_factory import widget_factory


class Composable:
    def __init__(
        self,
        widget: Widget,
        props: dict[str, Any],
        content: Callable[[], list["Composable"]] | None = None,
    ):
        self.widget = widget
        self.props = props
        self.content = content
        self._instance: Any = None

    def create(self) -> Any:
        if self._instance is None:
            self._instance = self.widget.create()
            self.widget.update(self._instance, self.props)
            if self.content:
                content_instances = [child.create() for child in self.content()]
                self.widget.set_content(self._instance, content_instances)
        return self._instance

    def __call__(self, *args: "Composable") -> Self:
        def new_content():
            return list(args)

        self.content = new_content
        return self


def composes[**P](
    widget_class: type,
) -> Callable[[Callable[P, Any]], Callable[P, Composable]]:
    """Convert a function into a composable component of a given widget class."""

    def decorator(func: Callable[P, Any]) -> Callable[P, Composable]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Composable:
            content_func = kwargs.pop("content", None)
            props = func(*args, **kwargs)
            widget = widget_factory.create(widget_class)
            return Composable(widget, props, content_func)

        return cast(Callable[P, Composable], wrapper)

    return decorator


@composes(TextWidget)
def Text(text: Any, *, modifier: ModifierProtocol | None = None) -> dict[str, Any]:
    return {"text": text, "modifier": modifier}


@composes(RowWidget)
def Row(*, modifier: ModifierProtocol | None = None) -> dict[str, Any]:
    return {"modifier": modifier}


@composes(ColumnWidget)
def Column(*, modifier: ModifierProtocol | None = None) -> dict[str, Any]:
    return {"modifier": modifier}


@composes(ButtonWidget)
def Button(
    onclick: Callable[[], None], *, modifier: ModifierProtocol | None = None
) -> dict[str, Any]:
    return {"onclick": onclick, "modifier": modifier}
