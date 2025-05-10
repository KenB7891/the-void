import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
from dotenv import load_dotenv

load_dotenv()

ENVIRONMENT = os.getenv('ENVIRONMENT', 'PROD')

if ENVIRONMENT == 'TEST':
    engine = create_engine('sqlite:///:memory:', connect_args={'check_same_thread': False})
    SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

else:
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME')
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')

    DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    engine = create_engine(DATABASE_URL)
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