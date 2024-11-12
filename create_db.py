# create_db.py
try:
 from sqlalchemy import create_engine
 from app.models import Base

 engine = create_engine('sqlite:///profile.db')
 Base.metadata.create_all(engine)
except Exception as e:
    print(f"error{str(e)}")