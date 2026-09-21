from dataclasses import dataclass
from typing import Protocol, TypeVar

ResponseT = TypeVar("ResponseT")


class Effect[ResponseT]:
    """Базовый класс для всех эффектов"""


class EffectRunner(Protocol):
    def __call__[T](self, effect: Effect[T]) -> T: ...


@dataclass
class User:
    id: int
    name: str


@dataclass
class GetUserEffect(Effect[User]):
    user_id: int


@dataclass
class LogEffect(Effect[None]):
    message: str


def workflow(run: EffectRunner) -> User:
    run(LogEffect("Старт запроса к БД"))
    user = run(GetUserEffect("user_42"))
    run(LogEffect(f"Получен пользователь: {user}"))
    return user
