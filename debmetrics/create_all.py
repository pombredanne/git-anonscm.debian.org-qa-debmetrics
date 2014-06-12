"""This module creates all the tables from models directory unless the
the database already exists"""

from base import engine, Base, Session
from models.vcs import Vcs
from models.releases import Releases
from models.package_stats import Package_Stats

Base.metadata.create_all(engine)
