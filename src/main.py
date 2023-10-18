from fastapi import FastAPI

from src.api import ErrorHandlingMiddleware, router

app = FastAPI(
    title="Quiz API",
    version="v1",
)
app.add_middleware(ErrorHandlingMiddleware)
app.include_router(router)
