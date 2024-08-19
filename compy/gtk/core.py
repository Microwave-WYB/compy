import gi

from compy.composable import Composable

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk  # type: ignore


class GtkApp:
    def __init__(self, app_id: str = "com.example.app"):
        self.app = Gtk.Application(application_id=app_id)
        self.windows = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def application_window(self, title: str = "Untitled") -> "ApplicationWindow":
        window = ApplicationWindow(self.app, title=title)
        self.windows.append(window)
        return window

    def run(self, argv=None):
        for window in self.windows:
            self.app.connect("activate", window._activate)
        self.app.run(argv)


class ApplicationWindow:
    def __init__(self, app: Gtk.Application, title: str = "Untitled"):
        self.app = app
        self.title = title
        self.composable: Composable[Gtk.Widget] | None = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.content is None:
            raise ValueError("Window content is not set")

    def set_content(self, content: Composable[Gtk.Widget]):
        self.content = content

    def _activate(self, app):
        if self.content is None:
            raise ValueError("Window content is not set")
        window = Gtk.ApplicationWindow(application=app)
        window.set_title(self.title)
        window.set_child(self.content.compose())
        window.present()

    def __call__(self, composable: Composable[Gtk.Widget]) -> None:
        self.set_content(composable)
