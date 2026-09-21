from domain import GetUserEffect, LogEffect
from infra import ConsoleLogger, UserRepo


class GetUserEffectHandler:
    def __init__(self, repo: UserRepo):
        self.repo = repo

    def __call__(self, effect: GetUserEffect):
        return self.repo.fetch(effect.user_id)


class LogEffectHandler:
    def __init__(self, logger: ConsoleLogger):
        self.logger = logger

    def __call__(self, effect: LogEffect):
        self.logger.log(effect.message)
