from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text,func

from db import get_db
from model import Transaction
from schema import UserTransactionSummary

router = APIRouter()

@router.get("/db")
async def HelloWorld():
    return {"message": "Hello World"}

@router.get("/db_health")
async def test_db_conn(db: Session= Depends(get_db)):
    try:
        result = db.execute(text('SELECT 1'))
        result.scalar()
        return {'message':'Succesfully connected to OpenTax Database'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Failed to connect to database: str{e}')

@router.get("/user_metrics/{user_id}", response_model=UserTransactionSummary)
def get_transaction_summary(user_id: int, db: Session = Depends(get_db)):

    # manually check if user is present in db..

    # Calculating a user's metrics
    result = db.query(
        func.count().label("total_transactions"),
        func.sum(func.coalesce(Transaction.amount, 0)).label("total_amount"),
        func.avg(func.coalesce(Transaction.amount, 0)).label("average_transaction_amount")
    ).filter(Transaction.user_id == user_id).first()

    if not result or result.total_transactions == 0:
        raise HTTPException(status_code=404, detail="User transactions not found")

    # if result is empty or total number of transactions is zero, raise
    return {
        "user_id": user_id,
        "total_transactions": result.total_transactions,
        "total_amount": result.total_amount or 0.0,
        "average_transaction_amount": result.average_transaction_amount or 0.0
    }
