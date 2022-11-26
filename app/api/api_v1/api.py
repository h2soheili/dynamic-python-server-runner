from fastapi import APIRouter

from app.api.api_v1.endpoints import announcement, docker_image

api_router = APIRouter()

api_router.include_router(announcement.router, prefix="/announcement", tags=["announcement"])
api_router.include_router(docker_image.router, prefix="/docker_image", tags=["docker_image"])
