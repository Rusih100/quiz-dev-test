from fastapi import FastAPI

from src.api import router

app = FastAPI(
    title="Quiz API",
    version="v1",
)
app.include_router(router)
