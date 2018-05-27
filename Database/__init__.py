from sqlalchemy.orm import sessionmaker, scoped_session
from Database import models

Session = sessionmaker(bind=models.engine)
session = scoped_session(Session)