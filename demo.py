from typing import Callable

from compy.composable import Button, Column, Composable, Row, Text
from compy.gtk import GTK_IMPLEMENTATIONS
from compy.gtk.core import App
from compy.gtk.modifier import Modifier
from compy.state import MutableState
from compy.widget_factory import widget_factory

widget_factory.load_implementations(GTK_IMPLEMENTATIONS)


def Counter(initial: int = 0, step: int = 1) -> Composable:
    count = MutableState(initial)

    def increment():
        count.set(count.get() + step)

    def decrement():
        count.set(count.get() - step)

    def reset():
        count.set(0)

    return Column(modifier=Modifier().fill_max_size().padding(5))(
        Row(modifier=Modifier().fill_max_width())(
            Button(onclick=decrement, modifier=Modifier().padding(5))(Text("-")),
            Text(lambda: f"Count: {count.get()}", modifier=Modifier().fill_max_width().padding(5)),
            Button(onclick=increment, modifier=Modifier().padding(5))(Text("+")),
        ),
        Button(onclick=reset, modifier=Modifier().padding(5))(Text("Reset")),
    )


if __name__ == "__main__":
    hello = Counter(0, 10)
    app = App()
    app.window().set_content(hello.resolve())
    app.run()
