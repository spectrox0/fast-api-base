from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def add_middleware_base(app: FastAPI):
    """
    Adds base middleware to the FastAPI application.

    Args:
        app (FastAPI): The FastAPI application instance.

    Returns:
        None
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
