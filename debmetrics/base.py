"""This module provides a single SQLAlchemy Base for the entire debmetrics
project."""

import os.path
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from debmetrics.config_reader import settings, read_config

read_config()

if settings['TEST']:
    engine = create_engine(settings['DB_URI'], echo=False,
                           connect_args={'connect_timeout': 90})
else:
    engine = create_engine(settings['DB_URI'], echo=True,
                           connect_args={'connect_timeout': 90})
Base = declarative_base(bind=engine)
Session = scoped_session(sessionmaker(engine))
