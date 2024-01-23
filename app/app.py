from app.routes import include_router
from fastapi import FastAPI
from config.database import init_db, disconnect_db

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
        swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"}
    )

    # app_instance.add_event_handler("startup", startup)
    # app_instance.add_event_handler("shutdown", shutdown)
    include_router(app_instance)

    @app_instance.on_event("startup")
    async def on_startup():
        """
        Connects to the database.
        """
        await init_db()


    @app_instance.on_event("shutdown")
    async def on_shutdown():
        """
        Performs the necessary cleanup operations before shutting down the application.
        """
        await disconnect_db()
    return app_instance