from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings


def setup_cors(app: FastAPI) -> None:
    """
    Configure CORS middleware for the FastAPI application.
    """

    if settings.is_production:
        origins = [settings.FRONTEND_URL]
    else:
        origins = ["*"]

        print("Running in development mode. Allowing CORS from all origins.")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
