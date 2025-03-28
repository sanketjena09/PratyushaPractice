from fastapi import APIRouter

from .dummy import dummy_router

v1_router = APIRouter()

v1_router.include_router(dummy_router,prefix="/dummy")