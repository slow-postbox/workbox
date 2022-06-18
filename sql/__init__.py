from os import environ

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

if 'SQLALCHEMY_DATABASE_URI' not in environ:
    load_dotenv()

engine = create_engine(
    url=environ['SQLALCHEMY_DATABASE_URI'],
    pool_size=1,
    max_overflow=5
)
session_factory = sessionmaker(bind=engine)


def get_session():
    return session_factory()
