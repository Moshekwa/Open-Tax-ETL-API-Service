from fastapi import FastAPI
from routers.gets import router as get_router

app = FastAPI(title="Open-Tax Transaction API")

app.include_router(get_router)
