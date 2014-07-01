"""This module provides a single SQLAlchemy Base for the entire debmetrics
project."""

import os.path
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from config_reader import settings, read_config

pkg_dir = os.path.dirname(os.path.abspath(__file__))
read_config(os.path.join(pkg_dir, '.debmetrics.ini'))

engine = create_engine(settings['DB_URI'], echo=True)
Base = declarative_base(bind=engine)
Session = scoped_session(sessionmaker(engine))
