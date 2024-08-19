from compy.composable import Button, Column, Composable, Row, Text
from compy.gtk import GTK_IMPLEMENTATIONS
from compy.gtk.core import GtkApp
from compy.gtk.modifier import Modifier
from compy.state import MutableState, State, auto_derived
from compy.widget_factory import widget_factory

widget_factory.load_implementations(GTK_IMPLEMENTATIONS)


def Counter(count: MutableState[int], step: MutableState[int]) -> Composable:
    def increment():
        count.set(count.get() + step.get())

    def decrement():
        count.set(count.get() - step.get())

    def reset():
        count.set(0)

    return Column(modifier=Modifier().fill_max_size().padding(5))(
        Row(modifier=Modifier().fill_max_width())(
            Button(onclick=decrement, modifier=Modifier().padding(5))(Text("-")),
            Text(
                auto_derived(lambda: f"Count: {count.get()}"),
                modifier=Modifier().fill_max_width().padding(5),
            ),
            Button(onclick=increment, modifier=Modifier().padding(5))(Text("+")),
        ),
        Button(onclick=reset, modifier=Modifier().padding(5))(Text("Reset")),
    )


def StepController(step: MutableState[int]) -> Composable:
    def increase_step():
        step.set(step.get() + 1)

    def decrease_step():
        if step.get() > 1:
            step.set(step.get() - 1)

    def reset_step():
        step.set(1)

    return Column(modifier=Modifier().padding(5))(
        Text("Adjust Step Value:"),
        Row(modifier=Modifier().fill_max_width())(
            Button(onclick=decrease_step, modifier=Modifier().padding(5))(Text("-")),
            Text(
                auto_derived(lambda: str(step.get())),
                modifier=Modifier().fill_max_width().padding(5),
            ),
            Button(onclick=increase_step, modifier=Modifier().padding(5))(Text("+")),
        ),
        Button(onclick=reset_step, modifier=Modifier().padding(5))(Text("Reset")),
    )


def CounterApp() -> Composable:
    count = MutableState(0)
    step = MutableState(1)

    return Column(modifier=Modifier().fill_max_size().padding(5))(
        Counter(count, step),
        Row(modifier=Modifier().height(50)),
        StepController(step),
    )


if __name__ == "__main__":
    app = GtkApp()
    app.window().set_content(CounterApp().compose())
    app.run()
