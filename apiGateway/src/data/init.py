from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

user = 'postgres'
password = 'abc'
host = 'localhost'
port = '5432'
database = 'postgres'
connection_str = f'postgresql://{user}:{password}@{host}:{port}/{database}'
engine = create_engine(connection_str)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    print("create_tables")
    Base.metadata.create_all(bind=engine)