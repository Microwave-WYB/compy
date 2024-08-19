"""GTK implementations of the Widget class"""

from typing import Any, override

import gi

from compy.modifier import ModifierProtocol

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk  # type: ignore

from compy.widget import Widget


class ManagedBox(Gtk.Box):
    """Wrapper around Gtk.Box to provide child management"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.children = []

    @override
    def append(self, child: Gtk.Widget) -> None:
        """Append a child widget to the box"""
        self.children.append(child)
        self.append(child)

    @override
    def prepend(self, child: Gtk.Widget) -> None:
        super().prepend(child)
        self.children.insert(0, child)

    @override
    def remove(self, child: Gtk.Widget) -> None:
        """Remove a child widget from the box"""
        self.children.remove(child)
        self.remove(child)

    @override
    def insert_child_after(self, child: Gtk.Widget, sibling: Gtk.Widget | None = None) -> None:
        super().insert_child_after(child, sibling)
        self.children.insert(self.children.index(sibling) + 1, child)

    def clear(self) -> None:
        """Remove all children from the box"""
        for child in self.children:
            self.remove(child)
        self.children.clear()

    def set_children(self, children: list[Gtk.Widget]) -> None:
        """Set the children of the box"""
        self.clear()
        for child in children:
            self.append(child)


class GtkWidget[T: Gtk.Widget](Widget[T]):
    def update(self, instance: T, props: dict[str, Any]) -> None:
        modifier = props.get("modifier")
        if modifier:
            self.apply_modifier(instance, modifier)

    def apply_modifier(self, instance: T, modifier: ModifierProtocol[Gtk.Widget]) -> None:
        modifier.apply(instance)


class GtkTextWidget(GtkWidget[Gtk.Label]):
    def create(self) -> Gtk.Label:
        return Gtk.Label()

    def update(self, instance: Gtk.Label, props: dict[str, Any]) -> None:
        super().update(instance, props)
        text = props.get("text")
        if text:
            instance.set_text(text)

    def set_content(self, instance: Gtk.Label, content: list[Gtk.Widget]) -> None:
        raise ValueError("Text widget cannot set content")


class GtkButtonWidget(GtkWidget[Gtk.Button]):
    def create(self) -> Gtk.Button:
        return Gtk.Button()

    def update(self, instance: Gtk.Button, props: dict[str, Any]) -> None:
        super().update(instance, props)
        onclick = props.get("onclick")
        if onclick:
            instance.connect("clicked", lambda _: onclick())

    def set_content(self, instance: Gtk.Button, content: list[Gtk.Widget]) -> None:
        assert len(content) == 1, "Button can only have one child"
        instance.set_child(content[0])


class GtkBoxWidget(GtkWidget[Gtk.Box]):
    def create(self) -> Gtk.Box:
        return Gtk.Box()

    def update(self, instance: Gtk.Box, props: dict[str, Any]) -> None:
        super().update(instance, props)
        orientation = (
            Gtk.Orientation.VERTICAL
            if props["orientation"] == "vertical"
            else Gtk.Orientation.HORIZONTAL
        )
        instance.set_orientation(orientation)

    def set_content(self, instance: Gtk.Box, content: list[Gtk.Widget]) -> None:
        for child in content:
            instance.append(child)


class GtkRowWidget(GtkWidget[Gtk.Box]):
    def create(self) -> Gtk.Box:
        return Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

    def update(self, instance: Gtk.Box, props: dict[str, Any]) -> None:
        super().update(instance, props)
        instance.set_orientation(Gtk.Orientation.HORIZONTAL)

    def set_content(self, instance: Gtk.Box, content: list[Gtk.Widget]) -> None:
        for child in content:
            instance.append(child)


class GtkColumnWidget(GtkWidget[Gtk.Box]):
    def create(self) -> Gtk.Box:
        return Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

    def update(self, instance: Gtk.Box, props: dict[str, Any]) -> None:
        super().update(instance, props)
        instance.set_orientation(Gtk.Orientation.VERTICAL)

    def set_content(self, instance: Gtk.Box, content: list[Gtk.Widget]) -> None:
        for child in content:
            instance.append(child)
