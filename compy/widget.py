from abc import ABC, abstractmethod
from typing import Any

from compy.modifier import ModifierProtocol


class Widget[T](ABC):
    @abstractmethod
    def create(self) -> T:
        """Create a new instance of the widget."""

    @abstractmethod
    def update(self, instance: T, props: dict[str, Any]) -> None:
        """Update the properties of the widget instance."""

    @abstractmethod
    def set_content(self, instance: T, content: list[Any]) -> None:
        """Set the content within the widget instance."""

    @abstractmethod
    def apply_modifier(self, instance: T, modifier: ModifierProtocol) -> None:
        """Apply a modifier to the widget instance."""

    def render(self, instance: T) -> str:
        """Render the widget instance to a string for debugging."""
        return f"{instance}"


class TextWidget(Widget[Any]):
    def create(self) -> str:
        return ""

    def update(self, instance: str, props: dict[str, Any]) -> None:
        return props["text"]

    def render(self, instance: str) -> str:
        return f"Text({instance})"


class ButtonWidget(Widget[Any]):
    def create(self) -> dict:
        return {"type": "button", "content": []}

    def update(self, instance: dict, props: dict[str, Any]) -> None:
        return props["text"]

    def set_content(self, instance: dict, content: list[Any]) -> None:
        assert len(content) == 1, "Button can only have one child"
        instance["content"] = content

    def render(self, instance: dict) -> str:
        child_text = instance["content"][0].render() if instance["content"] else ""
        return f"Button({child_text})"


class BoxWidget(Widget[Any]):
    def create(self) -> dict:
        return {"type": "box", "orientation": "vertical", "content": []}

    def update(self, instance: dict, props: dict[str, Any]) -> None:
        instance.update(props)

    def set_content(self, instance: dict, content: list[Any]) -> None:
        instance["content"] = content

    def render(self, instance: dict) -> str:
        orientation = instance["orientation"]
        children = instance["content"]
        if orientation == "vertical":
            return "\n".join(child.render() for child in children)
        else:
            return " ".join(child.render() for child in children)


class RowWidget(Widget[Any]):
    def create(self) -> dict:
        return {"type": "row", "content": []}

    def update(self, instance: dict, props: dict[str, Any]) -> None:
        instance.update(props)

    def set_content(self, instance: dict, content: list[Any]) -> None:
        instance["content"] = content

    def render(self, instance: dict) -> str:
        children = instance["content"]
        return " ".join(child.render() for child in children)


class ColumnWidget(Widget[Any]):
    def create(self) -> dict:
        return {"type": "column", "content": []}

    def update(self, instance: dict, props: dict[str, Any]) -> None:
        instance.update(props)

    def set_content(self, instance: dict, content: list[Any]) -> None:
        instance["content"] = content

    def render(self, instance: dict) -> str:
        children = instance["content"]
        return "\n".join(child.render() for child in children)
