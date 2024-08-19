# Compy: A Composable GUI Framework for Python

## Demo

```python
from compy.composable import Button, Column, Composable, Row, Text
from compy.gtk import GTK_IMPLEMENTATIONS
from compy.gtk.core import GtkApp
from compy.gtk.modifier import Modifier
from compy.state import MutableState, auto_derived
from compy.widget_factory import widget_factory

widget_factory.register(GTK_IMPLEMENTATIONS)

def Counter() -> Composable:
    """Defines a simple counter"""
    count = MutableState(0)
    return Row()(
        Button(on_click=lambda: count.set(count.get() - 1))(Text("Decrement")),
        Text(auto_derived(lambda: f"Count: {count.get()}")),
        Button(on_click=lambda: count.set(count.get() + 1))(Text("Increment")),
    )

if __name__ == "__main__":
    with GtkApp("com.example.app") as app:
        with app.application_window("Counter App") as window:
            window(CounterApp().compose())

      app.run()
```

Let's break down the code above:

#### Defining a Composable function

```python
def Counter() -> Composable:
```

You need to define a function that returns a `Composable`. A `Composable` is the base unit of all GUI components in Compy.

#### Using built-in Composables

```python
Row()
```

This creates a horizontal layout using the `Row` Composable.

```python
Row()(
    Button(on_click=lambda: count.set(count.get() - 1))(Text("Decrement")),
)
```

By calling the `Row` with a `Button` as an argument, we are creating a horizontal layout with a button as a child.

Similarly, we call the `Button` with a `Text` as an argument to create a button with text.

#### Using State

Compy provides `MutableState` and `State` to manage the state of your application.

```python
count = MutableState(0)
```

This creates a mutable state with an initial value of `0`.

You can access the value of the state by calling `get` method.

```python
count.get()
```

You can set the value of the state by calling `set` method.

```python
count.set(10)
```

To setup callback on the state change, you can call `subscribe` method with a callback function.

```python
count.subscribe(lambda new_value: print(f"New value: {new_value}"))
```

##### Derived State

Sometimes you may want to derive a state from other states. You can use `derived` to create a derived state.

```python
count_text = derived(lambda: f"Count: {count.get()}", [count])
```

Or, you can use `auto_derived` to automatically derive the state. `auto_derived` automatically subscribes to states used within the function's `__closure__`.

```python
count_text = auto_derived(lambda: f"Count: {count.get()}")
```
