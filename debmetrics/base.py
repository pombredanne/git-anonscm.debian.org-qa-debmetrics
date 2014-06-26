"""This module provides a single SQLAlchemy Base for the entire debmetrics
project."""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from config_reader import settings, read_config

try:
    read_config('.debmetrics.ini')
except Exception:
    try:
        read_config('debmetrics/.debmetrics.ini')
    except Exception:
        read_config('../debmetrics/.debmetrics.ini')

engine = create_engine(settings['DB_URI'], echo=True)
Base = declarative_base(bind=engine)
Session = scoped_session(sessionmaker(engine))
