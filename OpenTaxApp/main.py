from fastapi import FastAPI
from routers import gets
from database_service.db import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Open-Tax Transaction APP")

app.include_router(gets.router)

