import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk  # type: ignore


class GtkApp:
    def __init__(self, app_id: str = "com.example.app"):
        self.app = Gtk.Application(application_id=app_id)
        self.windows = []

    def window(self, *, title: str = "Untitled") -> "ApplicationWindow":
        window = ApplicationWindow(self.app, title=title)
        self.windows.append(window)
        self.app.connect("activate", window._activate)
        return window

    def run(self, argv=None):
        self.app.run(argv)


class ApplicationWindow:
    def __init__(
        self, app: Gtk.Application, *, title: str = "Untitled", content: Gtk.Widget | None = None
    ):
        self.app = app
        self.title = title
        self.content = content

    def set_content(self, content: Gtk.Widget):
        self.content = content

    def _activate(self, app):
        if self.content is None:
            raise ValueError("Window content is not set")
        window = Gtk.ApplicationWindow(application=app)
        window.set_title(self.title)
        window.set_child(self.content)
        window.present()
