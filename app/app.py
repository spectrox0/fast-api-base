from fastapi import FastAPI

from app.middlewares.base import add_middleware_base
from app.routes import include_router
from config.database import disconnect_db, init_db


async def on_startup():
    """
    Connects to the database.
    """
    await init_db()


async def on_shutdown():
    """
    Performs the necessary cleanup operations before shutting down the application.
    """
    await disconnect_db()


def init_app():
    """
    Initializes the FastAPI application.

    Returns:
        FastAPI: The initialized FastAPI instance.
    """
    app_instance = FastAPI(
        title="Fast API Test Project",
        description="This project is a test project for FastAPI.",
        version="1",
        swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"},
    )
    add_middleware_base(app_instance)

    app_instance.add_event_handler("startup", on_startup)
    app_instance.add_event_handler("shutdown", on_shutdown)
    include_router(app_instance)

    return app_instance
