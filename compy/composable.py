from functools import wraps
from typing import Any, Callable, Self, cast

from compy.modifier import ModifierProtocol
from compy.state import State
from compy.widget import ButtonWidget, ColumnWidget, RowWidget, TextWidget, Widget
from compy.widget_factory import widget_factory


class Composable[T]:
    def __init__(
        self,
        widget: Widget[T],
        props: dict[str, Any],
        content: Callable[[], list["Composable[Any]"]] | None = None,
    ):
        self.widget = widget
        self._props = props
        self.content = content
        self._instance: Any = None
        self._subscriptions: list[tuple[str, State]] = []
        self._setup_subscriptions()

    def _setup_subscriptions(self) -> None:
        for key, value in self._props.items():
            if isinstance(value, State):
                resolved_value = value.get()
                self._props[key] = resolved_value
                self._subscriptions.append((key, value))

        for key, state in self._subscriptions:
            state.subscribe(lambda value, k=key: self.recompose({k: value}))

    def compose(self) -> T:
        if self._instance is None:
            self._instance = self.widget.create()
            self.widget.update(self._instance, self._props)
            if self.content:
                content_instances = [child.compose() for child in self.content()]
                self.widget.set_content(self._instance, content_instances)
        return self._instance

    def recompose(self, new_props: dict[str, Any]) -> None:
        updated_props = {**self._props, **new_props}

        if updated_props == self._props:
            return

        self._props = updated_props

        if self._instance is not None:
            self.widget.update(self._instance, self._props)

    def __call__(self, *args: "Composable[Any]") -> Self:
        def new_content():
            return list(args)

        self.content = new_content
        return self


def composes[**P](
    widget_class: type,
) -> Callable[[Callable[P, dict[str, Any]]], Callable[P, Composable]]:
    """Convert a function into a composable component of a given widget class."""

    def decorator(func: Callable[P, dict[str, Any]]) -> Callable[P, Composable]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> Composable:
            content_func = cast(
                Callable[[], list[Composable[Any]]] | None, kwargs.pop("content", None)
            )
            props = func(*args, **kwargs)

            widget = widget_factory.create(widget_class)
            return Composable(widget, props, content_func)

        return cast(Callable[P, Composable], wrapper)

    return decorator


@composes(TextWidget)
def Text(text: str | State[str], *, modifier: ModifierProtocol | None = None) -> dict[str, Any]:
    return locals()


@composes(RowWidget)
def Row(*, modifier: ModifierProtocol | None = None) -> dict[str, Any]:
    return locals()


@composes(ColumnWidget)
def Column(*, modifier: ModifierProtocol | None = None) -> dict[str, Any]:
    return locals()


@composes(ButtonWidget)
def Button(
    onclick: Callable[[], None], *, modifier: ModifierProtocol | None = None
) -> dict[str, Any]:
    return locals()
