from compy.composable import Button, Column, Composable, Row, Text
from compy.gtk import GTK_IMPLEMENTATIONS
from compy.gtk.core import App
from compy.gtk.modifier import Modifier
from compy.state import MutableState, rs
from compy.widget_factory import widget_factory

widget_factory.load_implementations(GTK_IMPLEMENTATIONS)


def Hello() -> Composable:
    count = MutableState(0)

    def increment():
        count.set(count.get() + 1)

    def decrement():
        count.set(count.get() - 1)

    def reset():
        count.set(0)

    return Column(modifier=Modifier().fill_max_size().padding(5))(
        Row(modifier=Modifier().fill_max_width())(
            Button(onclick=increment, modifier=Modifier().padding(5))(Text("+")),
            Text(
                rs("Count: {count}", count=count), modifier=Modifier().fill_max_width().padding(5)
            ),
            Button(onclick=decrement, modifier=Modifier().padding(5))(Text("-")),
        ),
        Button(onclick=reset, modifier=Modifier().padding(5))(Text("Reset")),
    )


if __name__ == "__main__":
    hello = Hello()
    app = App()
    app.window().set_content(hello.create())
    app.run()
