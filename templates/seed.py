"""Seed file to make sample data for db"""

from models import User, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add users
farheena = User(username='Farheena', password="Coder")
tammy = User(username='Tammy', password="Coding")
tina = User(username='Tina', password="Designer")

# Add new objects to session, so they'll persist
db.session.add(farheena)
db.session.add(tammy)
db.session.add(tina)

# Commit--otherwise, this never gets saved!
db.session.commit()
