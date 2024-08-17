from typing import Callable

from compy.widget import Widget


class WidgetFactory:
    def __init__(self) -> None:
        self.implementations: dict[type[Widget], type[Widget]] = {}

    def register(self, widget_class: type[Widget]) -> Callable[[type[Widget]], type[Widget]]:
        def decorator(impl: type[Widget]) -> type[Widget]:
            self.implementations[widget_class] = impl
            return impl

        return decorator

    def load_implementations(self, implementations: dict[type[Widget], type[Widget]]) -> None:
        self.implementations.update(implementations)

    def create(self, widget_class: type[Widget]) -> Widget:
        impl = self.implementations.get(widget_class)
        if not impl:
            impl = widget_class  # Default to the base class
        return impl()


# Global widget factory instance
widget_factory = WidgetFactory()
