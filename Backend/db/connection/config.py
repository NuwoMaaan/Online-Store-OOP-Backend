from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    HOST: str 
    USER: str
    PASSWORD: str 
    DATABASE: str
    POOL_SIZE: int

settings = Settings()
