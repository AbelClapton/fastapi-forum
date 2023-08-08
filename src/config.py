from pydantic import BaseSettings


class Settings(BaseSettings):
    DB_HOSTNAME: str
    DB_PORT: int
    DB_HOST: str
    DB_USER: str
    DB_PASSWORD: str
    DB_SCHEMA: str

    SECRET_KEY :str
    ALGORITHM :str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = "./.env"


settings = Settings()  # type: ignore
