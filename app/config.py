"""app/config.py

Configuration for the FastAPI CRUD app.

This module contains a class (`Settings`) which is used to load settings
from environment variables and a `.env` file. The settings are loaded using
the `pydantic_settings` library, which is based on the `pydantic` library.

The settings themselves are documented in the `Settings` class.

"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Settings for the FastAPI CRUD app.

    Loaded from environment variables and a `.env` file.
    """

    PROJECT_NAME: str = "FastAPI CRUD App"
    PROJECT_VERSION: str = "1.0.0"
    MONGODB_URI: str
    DATABASE_NAME: str = "fastapi-crud"
    ITEMS_COLLECTION: str = "items"
    CLOCK_IN_COLLECTION: str = "clock_in"
    DEBUG: bool = False

    class Config(object):
        """
        Configuration for the settings.

        This class is used to configure how the settings are loaded.
        """

        env_file = ".env"


settings = Settings()
