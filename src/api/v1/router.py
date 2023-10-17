from fastapi import APIRouter
from src.api.v1.questions import router as questions_router
router = APIRouter(prefix="/v1")


registered_routers = [
    questions_router
]

for rout in registered_routers:
    router.include_router(rout)
