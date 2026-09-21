import asyncio
from inspect import isawaitable

from awaitlet import async_def, awaitlet
from dishka import AsyncContainer, make_async_container

from di import HANDLERS, BaseProvider, HandlersProvider, HandlersRegistry
from domain import Effect, workflow


class RegistryEffectRunner:
    def __init__(self, registry: HandlersRegistry, container: AsyncContainer):
        self._registry = registry
        self._container = container

    def __call__[T](self, effect: Effect[T]) -> T:
        eff_type = type(effect)
        if eff_type not in self._registry:
            raise RuntimeError(f"Нет обработчика для эффекта {eff_type}")

        handler_cls = self._registry[eff_type]
        handler = awaitlet(self._container.get(handler_cls))
        return awaitlet(handler(effect)) if isawaitable(handler) else handler(effect)


def run_with_handlers(gen, handlers: HandlersRegistry, container: AsyncContainer):
    return gen(RegistryEffectRunner(handlers, container))


async def run_in_request_scope(
    gen, handlers: HandlersRegistry, container: AsyncContainer
):
    async with container() as scoped_container:
        return await async_def(run_with_handlers, gen, handlers, scoped_container)


container = make_async_container(BaseProvider("mysql://"), HandlersProvider())
asyncio.run(run_in_request_scope(workflow, HANDLERS, container))
