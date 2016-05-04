"""This module creates all the tables from models directory unless the
the table already exists"""

from debmetrics.database import db
from debmetrics.models import models

db.create_all()
