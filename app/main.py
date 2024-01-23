"""Import FastAPI and create an instance of the FastAPI class."""
import logging
from app.app import init_app
import uvicorn
logger = logging.getLogger(__name__)

app = init_app()

def start():
    """Launched with `poetry run start` at root level"""
    uvicorn.run(
        # app.main:app refers to the app variable in the main.py file in the app directory
        "app.main:app",
        # Host 0.0.0.0 means that other devices on the network can access the server
        host="0.0.0.0",  # noqa: S104
        # port 8000 is the default port for FastAPI
        port=8000,
        # reloads the server on code changes
        reload=True,
        # proxy headers for nginx
        proxy_headers=True,
    )
