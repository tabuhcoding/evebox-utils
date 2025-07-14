from fastapi import APIRouter

from api.router.revenue import router as revenue_router
from api.router.analytics import router as analytics_router

# router
routers: list[APIRouter] = [
    revenue_router,
    analytics_router
]


def get_routers() -> list[APIRouter]:
    return routers
