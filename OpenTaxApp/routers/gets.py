from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text,func

from database_service.db import get_db
from models.model import Transaction
from schemas.schema import UserTransactionSummary

router = APIRouter()

@router.get("/")
async def HelloWorld():
    return {"message": "Welcome to the OpenTax API Solution"}

@router.get("/db_health")
async def test_db_conn(db: Session= Depends(get_db)):
    """
    Test the database connection to ensure it is healthy and accessible.

    This endpoint executes a simple SQL query (`SELECT 1`) to verify that the application
    can successfully connect to the database. If the query executes successfully, the database
    connection is considered healthy. If the query fails, an error is raised.

    Args:
        db (Session): The database session dependency injected by FastAPI.

    Returns:
        dict: A dictionary containing a success message if the database connection is healthy.

    Raises:
        HTTPException (500): If the database connection fails, an HTTP 500 error is raised
                            with details about the failure.
    """
    try:
        result = db.execute(text('SELECT 1'))
        result.scalar()
        return {'message':'Succesfully connected to OpenTax Database'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Failed to connect to database: str{e}')

@router.get("/user_metrics/{user_id}", response_model=UserTransactionSummary)
async def get_transaction_summary(user_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a summary of transaction metrics for a specific user.

    This endpoint calculates and returns the total number of transactions, the total amount spent,
    and the average transaction amount for a given user.

    Args:
        user_id (int): The unique identifier of the user for whom the metrics are calculated.
        db (Session): The database session dependency injected by FastAPI.

    Returns:
        dict: A dictionary containing the following metrics:
            - user_id (int): The ID of the user.
            - total_transactions (int): The total number of transactions for the user.
            - total_amount (float): The total amount spent by the user across all transactions.
            - average_transaction_amount (float): The average amount spent per transaction.

    Raises:
        HTTPException (404): If the user does not exist in the database or if no transactions are found.
    """
    try:
        # We Check if the user exists
        user_exists = db.query(Transaction).filter(Transaction.user_id == user_id).first()
        if not user_exists:
            raise HTTPException(status_code=404, detail="User not found in database")

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

    except SQLAlchemyError as e:
        db.rollback()  # Rollback in case of a failed operation
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
