from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_swagger import patch_fastapi

from database import Base, engine
from routers import choices, play, players, scoreboard


def create_database() -> None:
    """Ensure all tables are created."""
    Base.metadata.create_all(bind=engine)


def create_app() -> FastAPI:
    """Create and configure a FastAPI application."""
    app = FastAPI()
    patch_fastapi(app)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(choices.router)
    app.include_router(play.router)
    app.include_router(scoreboard.router)
    app.include_router(players.router)

    return app


create_database()  # Create database tables
app = create_app()  # Assemble the application


if __name__ == "__main__":

    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
