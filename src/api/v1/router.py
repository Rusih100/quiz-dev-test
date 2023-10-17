from fastapi import APIRouter

router = APIRouter(prefix="/v1")


registered_routers = []

for rout in registered_routers:
    router.include_router(rout)
