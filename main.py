"""Import FastAPI and create an instance of the FastAPI class."""
import logging

from fastapi import FastAPI

from app.routes import profile_routes, user_routes
from config.database import db

logger = logging.getLogger(__name__)


def init_app():
    app = FastAPI(
        title="Fast API Test Project",
        description="This project is a test project for FastAPI.",
        version="1",
    )

    @app.on_event("startup")
    def startup():
        db.connect()

    @app.on_event("shutdown")
    async def shutdown():
        await db.disconnect()

    for router in [user_routes.router, profile_routes.router]:
        app.include_router(
            router,
            prefix="/api/v1",
        )

    return app


app = init_app()
