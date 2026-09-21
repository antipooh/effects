from dishka import Container, make_container

from di import HANDLERS, BaseProvider, HandlersProvider, HandlersRegistry
from domain import Effect, workflow


class RegistryEffectRunner:
    def __init__(self, registry: HandlersRegistry, container: Container):
        self._registry = registry
        self._container = container

    def __call__[T](self, effect: Effect[T]) -> T:
        eff_type = type(effect)
        if eff_type not in self._registry:
            raise RuntimeError(f"Нет обработчика для эффекта {eff_type}")

        handler_cls = self._registry[eff_type]
        handler = self._container.get(handler_cls)
        return handler(effect)


def run_with_handlers(gen, handlers, container):
    with container() as scoped_container:
        effect_runner = RegistryEffectRunner(handlers, scoped_container)
        return gen(effect_runner)


container = make_container(BaseProvider("mysql://"), HandlersProvider())
run_with_handlers(workflow, HANDLERS, container)
