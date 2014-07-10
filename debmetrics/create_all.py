"""This module creates all the tables from models directory unless the
the table already exists"""

from debmetrics.base import engine, Base, Session
from debmetrics.models import models

Base.metadata.create_all(engine)
