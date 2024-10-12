from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api import items, clock_in
from app.config import settings
from app.database import connect_to_mongo, close_mongo_connection


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan of the FastAPI application.

    When the application is starting up, it will run the code
    before the yield statement. When the application is shutting
    down, it will run the code after the yield statement.

    This is used to connect to the database when the application
    starts and close the connection when the application
    stops.
    """

    # Startup: connect to the database
    await connect_to_mongo()
    yield
    # Shutdown: close database connection
    await close_mongo_connection()


app = FastAPI(
    title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION, lifespan=lifespan
)

app.include_router(items.router, prefix="/items", tags=["items"])
app.include_router(clock_in.router, prefix="/clock-in", tags=["clock-in"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=settings.DEBUG)
