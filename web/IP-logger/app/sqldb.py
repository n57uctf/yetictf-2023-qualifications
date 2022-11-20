from dataclasses import dataclass

import psycopg2
from psycopg2.extras import RealDictCursor

from app.logger import log


@dataclass
class Config:
    user: str
    password: str
    host: str
    port: str
    database: str


class SQLDB:
    def __init__(self, config: Config):
        self.connection = psycopg2.connect(
            user=config.user,
            password=config.password,
            host=config.host,
            port=config.port,
            database=config.database
        )
        self.execute('create_db', None)

    def execute(self, cte: str, fetchall: bool | None, *args):
        """
        Метод для выполнения sql

        :param cte:
        :param fetchall: True - return fetchall, False - return fetchone, None - return True
        :param args:
        :return:
        """
        statement = SQLDB.get_cte(cte)
        log(f'QUERY: {statement}')
        try:
            with self.connection.cursor(cursor_factory=RealDictCursor) as curs:
                curs.execute(statement, args)
                self.connection.commit()
                if fetchall is True:
                    data = curs.fetchall()
                    log(f'DATA: {data}')
                elif fetchall is False:
                    data = curs.fetchone()
                    log(f'DATA: {data}')
                else:
                    data = True
                    log(f'DATA: {data}')
                return data
        except Exception as e:
            self.connection.rollback()
            log(f'QUERY ERROR: {e}')

    @staticmethod
    def get_cte(cte: str):
        with open("./sql/{}.sql".format(cte), "r") as cte:
            return str(cte.read())
