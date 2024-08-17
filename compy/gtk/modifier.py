from abc import ABC
from typing import Callable, Self

import gi

from compy.modifier import ModifierBase, ModifierProtocol

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk  # type: ignore


class GtkModifier(ModifierBase[Gtk.Widget], ABC):
    """Base class for GTK widget modifiers."""


class CompositeModifier(GtkModifier):
    def __init__(self, *modifiers: GtkModifier) -> None:
        self.modifiers = modifiers

    def apply(self, widget: Gtk.Widget) -> None:
        for modifier in self.modifiers:
            modifier.apply(widget)


class Modifier(ModifierProtocol):
    def __init__(self) -> None:
        self.modifiers = []

    def apply(self, widget: Gtk.Widget) -> None:
        for modifier in self.modifiers:
            modifier.apply(widget)

    def padding(self, *paddings: int) -> Self:
        self.modifiers.append(PaddingModifier(*paddings))
        return self

    def background(self, color: str) -> Self:
        self.modifiers.append(BackgroundModifier(color))
        return self

    def clickable(self, on_click: Callable[[], None]) -> Self:
        self.modifiers.append(ClickableModifier(on_click))
        return self

    def fill_max_width(self) -> Self:
        self.modifiers.append(FillModifier(hexpand=True, vexpand=False))
        return self

    def fill_max_height(self) -> Self:
        self.modifiers.append(FillModifier(hexpand=False, vexpand=True))
        return self

    def fill_max_size(self) -> Self:
        self.modifiers.append(FillModifier(hexpand=True, vexpand=True))
        return self

    def size(self, width: int, height: int) -> Self:
        self.modifiers.append(SizeModifier(width, height))
        return self

    def width(self, width: int) -> Self:
        self.modifiers.append(SizeModifier(width, None))
        return self

    def height(self, height: int) -> Self:
        self.modifiers.append(SizeModifier(None, height))
        return self


class PaddingModifier(GtkModifier):
    def __init__(self, *paddings: int) -> None:
        """
        Supports 1, 2, or 4 padding values.
        1 value: all paddings
        2 values: top/bottom, left/right
        4 values: top, right, bottom, left
        """
        self.padding_top = 0
        self.padding_right = 0
        self.padding_bottom = 0
        self.padding_left = 0

        match len(paddings):
            case 1:
                self.padding_top = paddings[0]
                self.padding_right = paddings[0]
                self.padding_bottom = paddings[0]
                self.padding_left = paddings[0]
            case 2:
                self.padding_top = paddings[0]
                self.padding_right = paddings[1]
                self.padding_bottom = paddings[0]
                self.padding_left = paddings[1]
            case 4:
                self.padding_top = paddings[0]
                self.padding_right = paddings[1]
                self.padding_bottom = paddings[2]
                self.padding_left = paddings[3]
            case _:
                raise ValueError("Padding must have 1, 2, or 4 values")

    def apply(self, widget: Gtk.Widget) -> None:
        widget.set_margin_start(self.padding_left)
        widget.set_margin_end(self.padding_right)
        widget.set_margin_top(self.padding_top)
        widget.set_margin_bottom(self.padding_bottom)


class BackgroundModifier(GtkModifier):
    def __init__(self, color: str) -> None:
        self.color = color

    def apply(self, widget: Gtk.Widget) -> None:
        style_context = widget.get_style_context()
        style_context.add_class(f"background-{self.color}")


class ClickableModifier(GtkModifier):
    def __init__(self, on_click: Callable[[], None]) -> None:
        self.on_click = on_click

    def apply(self, widget: Gtk.Widget) -> None:
        if isinstance(widget, Gtk.Button):
            widget.connect("clicked", lambda _: self.on_click())
        else:
            gesture = Gtk.GestureClick.new()
            gesture.connect("released", lambda *_: self.on_click())
            widget.add_controller(gesture)


class FillModifier(GtkModifier):
    def __init__(self, hexpand: bool, vexpand: bool) -> None:
        self.hexpand = hexpand
        self.vexpand = vexpand

    def apply(self, widget: Gtk.Widget) -> None:
        if self.hexpand:
            widget.set_hexpand(True)
        if self.vexpand:
            widget.set_vexpand(True)


class SizeModifier(GtkModifier):
    def __init__(self, width: int | None, height: int | None) -> None:
        self.width = width if width is not None else -1
        self.height = height if height is not None else -1

    def apply(self, widget: Gtk.Widget) -> None:
        widget.set_size_request(self.width, self.height)
