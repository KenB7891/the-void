from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = 'sqlite:///./void.db'

engine = create_engine(DATABASE_URL, connect_args={'check_same_thread': False})
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def connect_db():
    from app import models
    Base.metadata.create_all(bind=engine)
    print('Database connected!')

def disconnect_db():
    SessionLocal.remove()
    print('Database session removed!')