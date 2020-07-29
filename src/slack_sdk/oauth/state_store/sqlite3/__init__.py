import sqlite3
import time
from logging import Logger
from sqlite3 import Connection
from typing import Optional
from uuid import uuid4

from ..state_store import OAuthStateStore


class SQLite3OAuthStateStore(OAuthStateStore):

    def __init__(
        self,
        *,
        database: str,
        expiration_seconds: int,
        logger: Optional[Logger] = None,
    ):
        self.database = database
        self.expiration_seconds = expiration_seconds
        self.logger = logger
        self.init_called = False

    def init(self):
        try:
            with sqlite3.connect(database=self.database) as conn:
                cur = conn.execute("select count(1) from oauth_states;")
                row_num = cur.fetchone()[0]
                self.logger.debug(f"{row_num} oauth states are stored in {self.database}")
        except:
            self.create_tables()
        self.init_called = True

    def connect(self) -> Connection:
        if not self.init_called:
            self.init()
        return sqlite3.connect(database=self.database)

    def create_tables(self):
        with sqlite3.connect(database=self.database) as conn:
            conn.execute("""
            create table oauth_states (
                id integer primary key autoincrement,
                state text not null,
                expire_at datetime not null
            );
            """)
            conn.commit()

    def issue(self) -> str:
        state: str = str(uuid4())
        with self.connect() as conn:
            conn.execute(
                "insert into oauth_states (state, expire_at) values (?, ?);",
                [state, time.time() + self.expiration_seconds, ]
            )
            conn.commit()
        return state

    def consume(self, state: str) -> bool:
        try:
            with self.connect() as conn:
                cur = conn.execute(
                    "select id, expire_at from oauth_states where state = ? and expire_at > ?;",
                    [state, time.time()]
                )
                result = cur.fetchone()
                self.logger.debug(f"Fetched row: {result}")
                if result and len(result) > 0:
                    id = result[0]
                    conn.execute("delete from oauth_states where id = ?;", [id])
                    conn.commit()
                    return True
            return False
        except Exception as e:
            message = f"Failed to find any persistent data for state: {state} - {e}"
            self.logger.warning(message)
            return False
