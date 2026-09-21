class Database:
    def __init__(self, dsn: str, logger: ConsoleLogger):
        self.dsn = dsn
        self.logger = logger

    def select(self, sql: str):
        self.logger.log(f'On {self.dsn} run "{sql}"')

    async def aselect(self, sql: str):
        self.logger.log(f'On {self.dsn} run "{sql}"')


class UserRepo:
    def __init__(self, db: Database):
        self.db = db

    def fetch(self, user_id: int):
        self.db.select(f"select name from users where id={user_id};")
        return {"id": user_id, "name": "Алексей из БД"}

    async def afetch(self, user_id: int):
        await self.db.aselect(f"select name from users where id={user_id};")
        return {"id": user_id, "name": "Алексей из БД"}


class ConsoleLogger:
    def log(self, message):
        print(f"[LOG]: {message}")
