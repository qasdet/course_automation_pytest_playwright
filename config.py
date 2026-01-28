from pydantic_settings import BaseSettings
from pydantic import ConfigDict, Field


class DBSettings(BaseSettings):
    model_config = ConfigDict(
        env_file = ".env",
        case_sensitive = False,
        env_file_encoding = "utf-8"
    )

    postgres_host: str = Field(default="localhost", validation_alias="HOST")
    postgres_db: str = Field(default="demo", validation_alias="DATABASE")
    postgres_port: int = Field(default=5432, validation_alias="PORT")
    postgres_user: str = Field(default="postgres", validation_alias="USER")
    postgres_password: str = Field(validation_alias="PASSWORD")
    
    @property
    def database_url(self) -> str:
        """Возвращает строку подключения к PostgreSQL базе данных"""
        return f"postgresql://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"



db = DBSettings()