from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#DATABASE_URI = "postgresql://adminadsum:passadsum@postgres:5432/transactions_db"
DATABASE_URI = "postgresql+psycopg2://airflow:admin@postgres:5432/airflow"

engine = create_engine(DATABASE_URI)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()