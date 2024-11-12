# create_db.py
from sqlalchemy import create_engine
from app.models import Base

engine = create_engine('sqlite:///profile.db')
Base.metadata.create_all(engine)
