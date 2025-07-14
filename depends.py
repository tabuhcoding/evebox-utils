from fastapi import APIRouter

from api.router.revenue import router as revenue_router

# router
routers: list[APIRouter] = [
    revenue_router
]


def get_routers() -> list[APIRouter]:
    return routers
