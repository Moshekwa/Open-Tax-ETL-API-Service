from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from db import get_db

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


