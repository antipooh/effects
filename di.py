from collections.abc import Callable
from typing import Any

from dishka import Provider, Scope, provide

from domain import GetUserEffect, LogEffect
from handlers import GetUserEffectHandler, LogEffectHandler
from infra import ConsoleLogger, Database, UserRepo


class BaseProvider(Provider):
    scope = Scope.APP

    def __init__(self, dsn: str) -> None:
        super().__init__()
        self.dsn = dsn

    @provide
    def database(self, console_logger: ConsoleLogger) -> Database:
        return Database(self.dsn, console_logger)

    console_logger = provide(ConsoleLogger)
    user_repo = provide(UserRepo, scope=Scope.REQUEST)


class HandlersProvider(Provider):
    log_handler = provide(LogEffectHandler, scope=Scope.APP)
    user_handler = provide(GetUserEffectHandler, scope=Scope.REQUEST)


type HandlersRegistry = dict[type, Callable[[Any], Any]]
HANDLERS = {LogEffect: LogEffectHandler, GetUserEffect: GetUserEffectHandler}
