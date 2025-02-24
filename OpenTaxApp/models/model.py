from database_service.db import Base
from sqlalchemy import Column, Integer, String, Float, Date,Text,TIMESTAMP
from sqlalchemy.sql import func

class Transaction(Base):
    __tablename__ = 'transactions'

    index = Column(Integer, primary_key=True, autoincrement=True)
    transaction_id = Column(String(50), unique=True, nullable=False)
    user_id = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)
    transaction_date = Column(Date, nullable=False)

class TaskExecutionLog(Base):
    __tablename__ = "task_execution_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    dag_id = Column(String(50), nullable=False)
    task_id = Column(String(50), nullable=False)
    log_level = Column(String(50), nullable=False)
    message = Column(String(255), nullable=False)
    timestamp = Column(TIMESTAMP, server_default=func.current_timestamp())