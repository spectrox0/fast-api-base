from fastapi import APIRouter


def get_api_router(module: str) -> APIRouter:
    return APIRouter(prefix=f"/{module}")
