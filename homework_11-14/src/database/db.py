from fastapi import HTTPException, status
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from src.conf.config import settings


URL = settings.sqlalchemy_database_url

engine = create_engine(URL, echo=True)
DBSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
def get_db():
    """
    The get_db function is a context manager that will automatically close the database connection when it goes out of scope.
    It also handles any exceptions that occur within the with block, rolling back any changes to the database and closing the connection before re-raising them.

    :return: A context manager, which is a special kind of object that supports the context management protocol
    :doc-author: Trelent
    """
    db = DBSession()
    try:
        yield db
    except SQLAlchemyError as err:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))
    finally:
        db.close()
