from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from database.models import Base

DATABASE_URL = 'sqlite:///taskcontrol.db'

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = scoped_session(sessionmaker(bind=engine, autoflush=False, autocommit=False))

def init_db():
    Base.metadata.create_all(bind=engine)

def get_session():
    return SessionLocal()
