from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MODELS_FILE_PATH: str
    WEBSITES_FILE_PATH: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        case_sensitive = True


@lru_cache
def get_settings() -> Settings:
    return Settings()
