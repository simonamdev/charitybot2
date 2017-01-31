from charitybot2.paths import production_logs_db_path
from charitybot2.persistence.sqlite_repository import SQLiteRepository


class RepositoryLogger(SQLiteRepository):
    def __init__(self):
        super().__init__(db_path=production_logs_db_path)
