from fastapi import FastAPI
import gets
from db import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Open-Tax Transaction APP")

app.include_router(gets.router)

