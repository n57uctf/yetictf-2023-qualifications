"""
Пакет содержит обертку для запросов в базу данных

Пример использования:

Подключамся к базе данных

    MyDB = SQLDB({
        'host': '127.0.0.1',
        'port': '5432',
        'database': 'database',
        'user': 'postgres',
        'password': 'postgres'
    })

Определяем модель пользователя

    class User(BaseModel):
        user_id: int
        username: str

Создаем наш sql запрос напрмиер в файле по такому пути: "my_fastapi_application/sql/get_user_by_username.sql"

    SELECT
        u._user as user_id,
        u.user as username
    FROM users u
    WHERE u.user = %(user)s

Теперь выполним наш запрос

    result = MyDB.execute('my_fastapi_application.sql.get_user_by_username', {'user': 'vasya'}).one()
    print(result)
    >> {'user_id': 123, 'username': 'vasya'}

Тперь выполним наш запрос с использованием модели

    result = MyDB.execute('my_fastapi_application.sql.get_user_by_username', {'user': 'vasya'}).one(User)
    print(result)
    >> User(user_id=123, username='vasay')
    print(result.username)  # Работают подсказки
    >> 'vasay'

"""
from pathlib import Path
from typing import Type, TypeVar, List

import psycopg2
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel


AnyModel = TypeVar('AnyModel', bound=BaseModel)


class SQLDBException(Exception):
    pass


class Statement:
    """
    Класс описывает выполненный sql запрос из которого можно получить данные
    """
    def __init__(self, connection: psycopg2.connect, query: str, params: dict):
        """
        Инициализцаия класса

        :param connection: объект коннекта к базе данных
        :param query: текст запроса
        :param params: параметры запроса
        """
        self.query = query
        self.connection = connection
        self.params = params

    def one(self, model: Type[AnyModel] = None) -> dict | None | AnyModel:
        """
        Метод возвращает 1 запись из базы данных, если задана модель, то запись запаковывается в модель.
        По умолчанию возвращается словарь в котором ключи - это название столбцов из бд,
        значения - это значение данных столбцов. Если запрос в бд ничего не вернул возвращается None.

        :param model: модель на основе BaseModel
        :return: По умолчанию возвращается словарь в котором ключи - это название столбцов из бд, значения - это
            значение данных столбцов. Если запрос в бд ничего не вернул возвращается None.
        """
        try:
            with self.connection.cursor(cursor_factory=RealDictCursor) as curs:
                curs.execute(self.query, self.params)
                self.connection.commit()
                data = curs.fetchone()
                if not data:
                    return None
                if model:
                    return model(**data)
                else:
                    return data
        except Exception as e:
            self.connection.rollback()
            raise SQLDBException(f'QUERY ERROR: \n{self.query}\nPARAMS: {str(self.params)}\nEXCEPTION: {e}\n')

    def all(self, model: Type[AnyModel] = None) -> list | None | List[AnyModel]:
        """
        Метод возвращает все записи из базы данных, если задана модель, то записи запаковывается в модель и
        возвращается список моделей.
        По умолчанию возвращается список словарей в котором ключи - это название столбцов из бд,
        значения - это значение данных столбцов. Если запрос в бд ничего не вернул возвращается None.

        :param model: модель
        :return: По умолчанию возвращается список словарей в котором ключи - это название столбцов из бд,
            значения - это значение данных столбцов. Если запрос в бд ничего не вернул возвращается None.
        """
        try:
            with self.connection.cursor(cursor_factory=RealDictCursor) as curs:
                curs.execute(self.query, self.params)
                self.connection.commit()
                data = curs.fetchall()
                if not data:
                    return None
                if model:
                    return [model(**_) for _ in data]
                else:
                    return data
        except Exception as e:
            self.connection.rollback()
            raise SQLDBException(f'QUERY ERROR: \n{self.query}\nPARAMS: {str(self.params)}\nEXCEPTION: {e}\n')

    def none(self) -> None:
        """
        Метод не возвращает данных из запроса, полезно например при INSERT, UPDATE или DELETE

        :return:
        """
        try:
            with self.connection.cursor(cursor_factory=RealDictCursor) as curs:
                curs.execute(self.query, self.params)
                self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            raise SQLDBException(f'QUERY ERROR: \n{self.query}\nPARAMS: {str(self.params)}\nEXCEPTION: {e}\n')


class SQLDB:
    """
    Класс является абстракцией над базой данных, 1 объект класса является одной базой данных
    """
    def __init__(self, configuration: dict = None):
        """
        Инициализация класса

        :param configuration: конфигурация подключения к базе данных
        """
        self.configuration = {}
        self.connection = None
        if configuration:
            self.connection = configuration
            self.connection = psycopg2.connect(**configuration)

    def set_configuration(self, host: str, port: str, database: str, user: str, password: str) -> None:
        """
        Метод для установки конфигурации для подключения к бд, если была передана конфигурация
        во время инициализации класса, то данный метод вызывать не нужно

        :param host: хост
        :param port: порт
        :param database: имя базы данных
        :param user: имя пользователя
        :param password: пароль
        :return:
        """
        self.configuration = {
            'host': host,
            'port': port,
            'database': database,
            'user': user,
            'password': password
        }
        self.connection = psycopg2.connect(
            **self.configuration
        )

    def execute(self, sql_path: str, params: dict = None) -> Statement:
        """
        Метод выполняет sql и либо возвращает стэйтмент либо выбрасывает ошибку

        :param params: словарь с данными для sql
        :param sql_path: services.auth.sql.create_user (парситься в путь services/auth/sql/create_user.sql)
        :return: стейтмент
        """
        if self.connection is None:
            raise SQLDBException('No database connections')
        path = ['./sql'] + sql_path.split('.')
        path[-1] += '.sql'
        try:
            with open(Path(*path), 'r') as sql:
                query = sql.read()
        except Exception as e:
            raise SQLDBException(f'No such file: {str(Path(*path))}')
        else:
            return Statement(self.connection, query, params)
