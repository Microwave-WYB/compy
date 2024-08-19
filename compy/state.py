from typing import Any, Callable


class State[T]:
    def __init__(self, initial: T):
        self._value = initial
        self.observers: list[Callable[[T], None]] = []

    def get(self) -> T:
        return self._value

    def subscribe(self, observer: Callable[[T], None]) -> None:
        self.observers.append(observer)
        observer(self.get())  # Immediately call the observer with the current value

    def _notify(self) -> None:
        for observer in self.observers:
            observer(self.get())


class MutableState[T](State[T]):
    def set(self, value: T) -> None:
        if value != self._value:
            self._value = value
            self._notify()


def derived[T](compute: Callable[[], T], *dependencies: State) -> State[T]:
    state = State(compute())

    def update(_: Any) -> None:
        new_value = compute()
        if new_value != state._value:
            state._value = new_value
            state._notify()

    for dependency in dependencies:
        dependency.subscribe(update)

    return state


def auto_derived[T](compute: Callable[[], T]) -> State[T]:
    dependencies = [
        var.cell_contents
        for var in (compute.__closure__ or [])
        if isinstance(var.cell_contents, State)
    ]
    return derived(compute, *dependencies)
