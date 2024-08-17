from abc import ABC, abstractmethod
from typing import Any, Callable, cast


class Widget[T](ABC):
    @abstractmethod
    def create(self) -> Any:
        pass

    @abstractmethod
    def update(self, instance: Any, props: dict[str, Any]) -> None:
        pass

    @abstractmethod
    def set_content(self, instance: Any, content: list[Any]) -> None:
        pass


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

    def set_content(self, content: list["Composable"]) -> None:
        self.content = lambda: content

    def __call__(self, *args: "Composable") -> "Composable":
        def new_content():
            return list(args)

        self.content = new_content
        return self


def compose[**P](
    widget_class: type,
) -> Callable[[Callable[P, Any]], Callable[P, Composable]]:
    def decorator(func):
        def wrapper(*args, **kwargs):
            content_func = kwargs.pop("content", None)
            return Composable(widget_class(), kwargs, content_func)

        return wrapper

    return cast(Callable[[Callable[P, dict[str, Any]]], Callable[P, Composable]], decorator)


class TextWidget(Widget[str]):
    def create(self) -> str:
        return ""

    def update(self, instance: str, props: dict[str, Any]) -> None:
        return props["text"]

    def set_content(self, instance: str, content: list[Any]) -> None:
        if content:
            raise ValueError("Text cannot have content")

    def render(self, instance: str) -> str:
        return instance


class ButtonWidget(Widget[dict]):
    def create(self) -> dict:
        return {"type": "button", "label": "", "on_click": None, "child": None}

    def update(self, instance: dict, props: dict[str, Any]) -> None:
        instance.update(props)

    def set_content(self, instance: dict, content: list[Any]) -> None:
        if len(content) > 1:
            raise ValueError("Button can have at most one child")
        if content:
            instance["child"] = content[0]

    def render(self, instance: dict) -> str:
        child_text = instance["child"].render() if instance["child"] else ""
        return f"[Button: {instance['label']} ({child_text})]"


class BoxWidget(Widget[list]):
    def create(self) -> list:
        return []

    def update(self, instance: list, props: dict[str, Any]) -> None:
        instance.append(props)

    def set_content(self, instance: list, content: list[Any]) -> None:
        instance.extend(content)

    def render(self, instance: list) -> str:
        props = instance[0]
        orientation = props["orientation"]
        spacing = props["spacing"]
        children = instance[1:]
        if orientation == "vertical":
            return "\n".join(child.render() for child in children)
        else:
            return " ".join(child.render() for child in children)


# Composable functions
@compose(BoxWidget)
def Box(
    orientation: str = "vertical",
    spacing: int = 0,
    content: Callable[[], list[Composable]] | None = None,
) -> dict[str, Any]:
    return {"Box": {"orientation": orientation, "spacing": spacing}, "content": content}


@compose(TextWidget)
def Text(text: str) -> dict[str, Any]:
    return {"text": text}


@compose(ButtonWidget)
def Button(
    label: str, on_click: Callable[[], None], content: Callable[[], list[Composable]] | None = None
) -> dict[str, Any]:
    return {"label": label, "on_click": on_click, "child": None}


def App():
    def handle_click():
        print("Button clicked!")

    return Box(
        orientation="vertical",
        spacing=10,
    )(
        Text(text="Welcome to my app!"),
        Button(label="Click me", on_click=handle_click)(Text(text="Button Text")),
    )


# Render function (this would be different for each UI library)
def render_app(root: Composable) -> None:
    print(root.create())  # This creates the entire widget tree


# Usage
app = App()
render_app(app)
