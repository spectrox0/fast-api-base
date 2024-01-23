from fastapi import FastAPI
import app.routes.user_routes as user_routes
import app.routes.profile_routes as profile_routes

list_of_routes = [
                user_routes.router,
                profile_routes.router
                ]

def include_router(app: FastAPI) -> None:
    """
    Includes the routers in the FastAPI application.

    Args:
        app (FastAPI): The FastAPI application.
    """
    for router in list_of_routes:
        app.include_router(
            router,
            prefix="/api",
        )
