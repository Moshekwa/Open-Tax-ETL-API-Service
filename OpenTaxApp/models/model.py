from ..db_service.db import Base
from sqlalchemy import Column, Integer, String, Float, Date

class Transactions(Base):
    __tablename__ = 'transactions'

    transaction_id = Column(String(50), primary_key="True", unique=True, index=True, nullable=False )
    user_id = Column(Integer, index=True,unique=True)
    amount = Column(Float)
    transaction_date = Column(Date,nullable=False)