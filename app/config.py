from pydantic_settings import BaseSettings 


class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI CRUD App"
    PROJECT_VERSION: str = "1.0.0"
    MONGODB_URI: str
    DATABASE_NAME: str = "fastapi-crud"
    ITEMS_COLLECTION: str = "items"
    CLOCK_IN_COLLECTION: str = "clock_in"
    DEBUG: bool = False

    class Config:
        env_file = ".env"


settings = Settings()
