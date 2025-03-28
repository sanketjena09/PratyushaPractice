from fastapi import APIRouter

dummy_router = APIRouter()

@dummy_router.get('/')
def dummy():
    return "hello world"