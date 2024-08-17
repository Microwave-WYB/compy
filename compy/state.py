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


class ReactiveStr:
    def __init__(self, template: str, /, **fields: Any):
        self._template = template
        self._fields = fields
        self._states: dict[str, State[Any]] = {}
        self._observers: list[Callable[[str], None]] = []

        for field, value in fields.items():
            if isinstance(value, State):
                self._states[field] = value
            else:
                self._states[field] = State(value)

        self._value = self._format()

        for state in self._states.values():
            state.subscribe(self._update)

    def __str__(self) -> str:
        return self._value

    def _format(self) -> str:
        return self._template.format_map(
            {field: state.get() for field, state in self._states.items()}
        )

    def _update(self, _: Any) -> None:
        new_value = self._format()
        if new_value != self._value:
            self._value = new_value
            self._notify()

    def _notify(self) -> None:
        for observer in self._observers:
            observer(self._value)

    def subscribe(self, observer: Callable[[str], None]) -> None:
        self._observers.append(observer)
        observer(self._value)  # Immediately call the observer with the current value

    def get(self) -> str:
        return self._value


def rs(template: str, /, **fields: Any) -> ReactiveStr:
    return ReactiveStr(template, **fields)


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
