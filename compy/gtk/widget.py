"""GTK implementations of the Widget class"""

from typing import Any, Callable

import gi

from compy.modifier import ModifierProtocol
from compy.state import State, auto_derived

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk  # type: ignore

from compy.widget import Widget


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
