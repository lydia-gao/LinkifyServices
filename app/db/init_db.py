from sqlalchemy.ext.declarative import declarative_base
from .session import engine

Base = declarative_base()

def init_db():
    Base.metadata.create_all(bind=engine)
