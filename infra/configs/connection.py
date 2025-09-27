from sqlalchemy.engine import URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DBConecctionHandleMaster:
    def __init__(self):
        self.__connection_string_master = URL.create(
            "mssql+pyodbc",
            username="root",
            password="0000",
            host="AlexSousa",
            database="master",
            query={"driver": "ODBC Driver 17 for SQL Server"}
        )
        self.__engine_master = self.__create_data_base_engine_master()
        self.session = None

    def __create_data_base_engine_master(self):
        __engine_master = create_engine(self.__connection_string_master)
        return __engine_master

    def get_engine_master(self):
        return self.__engine_master

    def __enter__(self):
        session_maker = sessionmaker(bind=self.__engine_master)
        self.session = session_maker()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()


class DBConecctionHandleMasterAutocommit:
    def __init__(self):
        self.__connection_string_master_autocommit = URL.create(
            "mssql+pyodbc",
            username="root",
            password="0000",
            host="AlexSousa",
            database="master",
            query={"driver": "ODBC Driver 17 for SQL Server"},
        )
        self.__engine_master_autocommit = self.__create_data_base_engine_master_autocommit()
        self.session = None

    def __create_data_base_engine_master_autocommit(self):
        engine_master_autocommit = create_engine(
            self.__connection_string_master_autocommit, isolation_level="AUTOCOMMIT")
        return engine_master_autocommit

    def get_engine_master(self):
        return self.__engine_master_autocommit

    def __enter__(self):
        session_maker = sessionmaker(bind=self.__engine_master_autocommit)
        self.session = session_maker()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()


class DBConecctionHandleApp:
    def __init__(self) -> None:
        self.__connection_string_app = URL.create(
            "mssql+pyodbc",
            username="root",
            password="0000",
            host="AlexSousa",
            database="salvados",
            query={"driver": "ODBC Driver 17 for SQL Server"}
        )
        self.__engine_app = self.__create_data_base_engine_app()
        self.session = None

    def __create_data_base_engine_app(self):
        engine_app = create_engine(self.__connection_string_app)
        return engine_app

    def get_engine_app(self):
        return self.__engine_app

    def __enter__(self):
        session_maker = sessionmaker(bind=self.__engine_app)
        self.session = session_maker()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
