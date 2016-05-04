"""This module creates all the tables from models directory unless the
the table already exists"""

from debmetrics.app import app
from debmetrics.database import db
from debmetrics.models import models

with app.app_context():
    db.create_all()
