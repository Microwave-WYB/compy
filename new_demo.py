import gi

gi.require_version("Gtk", "4.0")
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any, Callable, Dict, List

from gi.repository import GLib, Gtk


# Compose-like system
class ComposeContext:
    def __init__(self):
        self.children: List[Any] = []

    def add_child(self, child: Any):
        self.children.append(child)


_current_context: ComposeContext | None = None


@contextmanager
def compose_context():
    global _current_context
    parent_context = _current_context
    _current_context = ComposeContext()
    yield _current_context
    _current_context = parent_context


def composable(func):
    def wrapper(*args, **kwargs):
        with compose_context() as context:
            result = func(*args, **kwargs)
        return result, context.children

    return wrapper


class State:
    def __init__(self, value: Any):
        self.value = value
        self.listeners: list[Callable[[], None]] = []

    def get(self):
        return self.value

    def set(self, new_value):
        if self.value != new_value:
            self.value = new_value
            for listener in self.listeners:
                listener()

    def subscribe(self, listener: Callable[[], None]):
        self.listeners.append(listener)


# GTK Widgets
def Text(content: Callable[[], str] | str):
    label = Gtk.Label(label=content() if callable(content) else content)

    def update_label():
        label.set_text(content() if callable(content) else content)

    if callable(content):
        for var in content.__closure__ or []:
            if isinstance(var.cell_contents, State):
                var.cell_contents.subscribe(update_label)

    global _current_context
    if _current_context is not None:
        _current_context.add_child(label)

    return label


def Button(content: Callable[[], Gtk.Widget], onClick: Callable[[], None]):
    button = Gtk.Button()
    button.connect("clicked", lambda _: onClick())

    def update_button_content():
        button.set_child(None)  # Remove existing child
        button.set_child(content())

    update_button_content()

    if callable(content):
        for var in content.__closure__ or []:
            if isinstance(var.cell_contents, State):
                var.cell_contents.subscribe(update_button_content)

    global _current_context
    if _current_context is not None:
        _current_context.add_child(button)

    return button


@contextmanager
def Box(orientation: Gtk.Orientation = Gtk.Orientation.VERTICAL, spacing: int = 6):
    global _current_context
    parent_context = _current_context
    box_context = ComposeContext()
    _current_context = box_context
    yield
    _current_context = parent_context

    box = Gtk.Box(orientation=orientation, spacing=spacing)
    for child in box_context.children:
        box.append(child)

    if parent_context is not None:
        parent_context.add_child(box)


# Counter App
@composable
def Counter():
    count = State(0)

    def increment():
        count.set(count.get() + 1)

    with Box(Gtk.Orientation.VERTICAL, spacing=6):
        Text(lambda: f"Count: {count.get()}")
        Button(lambda: Text(lambda: f"Increment ({count.get()})"), onClick=increment)

    return count  # Return the state for updates


@composable
def App():
    return Counter()


# GTK Application
class ComposeApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="org.example.ComposeApp")
        self.window = None
        self.box = None
        self.count_state = None

    def do_activate(self):
        self.window = Gtk.ApplicationWindow(application=self, title="Compose-like Counter")
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.window.set_child(self.box)

        self.render()
        self.window.present()

    def render(self):
        # Clear existing children
        while child := self.box.get_first_child():
            self.box.remove(child)

        # Render new children
        (app_result, app_content) = App()
        (self.count_state, counter_content) = app_result
        for widget in counter_content:
            self.box.append(widget)


def main():
    app = ComposeApp()
    app.run(None)


if __name__ == "__main__":
    main()
