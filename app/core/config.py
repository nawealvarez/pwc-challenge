from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    USER: str
    PASSWORD: str
    HOST: str
    PORT: str
    DBNAME: str
    DATABASE_URL: str

    class Config:
        env_file = ".env"

settings = Settings()