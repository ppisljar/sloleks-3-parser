from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists

from . import Config
from .models import Base


class Database:
    engine = None
    Session = None

    def __init__(self):
        self.Session = sessionmaker()
        self.engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
        if not database_exists(Config.SQLALCHEMY_DATABASE_URI):
            self._create_db_tables()
        self.Session.configure(bind=self.engine)

    def _create_db_tables(self):
        Base.metadata.create_all(self.engine)
