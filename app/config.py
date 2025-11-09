from pydantic_settings import BaseSettings
from pydantic import root_validator


class Settings(BaseSettings):
    POSTGRES_NAME: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_PORT: int
    POSTGRES_HOST: str

    
    @root_validator(skip_on_failure=True)
    def get_databese_url(cls, v):
        v["DATABASE_URL"] =  (
        f"postgresql+asyncpg://{v['POSTGRES_USER']}:"
        f"{v['POSTGRES_PASSWORD']}@{v['POSTGRES_HOST']}:{v['POSTGRES_PORT']}/{v['POSTGRES_NAME']}"
    )
        return v
    

    class Config:
        env_file = ".env"

settings = Settings()
print(settings.DATABASE_URL)