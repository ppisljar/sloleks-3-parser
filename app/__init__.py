from contextlib import contextmanager

from config import Config
from .database import Database

db = Database()


@contextmanager
def session_scope(logger=None):
    """Provide a transactional scope around a series of operations."""
    session = db.Session()
    try:
        yield session
        session.commit()
    except Exception as err:
        session.rollback()
        if logger:
            logger.critical(str(err))
        else:
            raise
    finally:
        session.close()