from pathlib import Path

from pydantic import SecretStr
from pydantic.fields import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_PATH = Path(__file__).parent.parent.resolve() / ".env"


class PostgreSQLSettings(BaseSettings):
    mode: str
    database_name: str
    driver: str
    user: str
    password: SecretStr
    host: str
    port: int

    @property
    def dsn(self) -> str:
        return (
            f"postgresql+{self.driver}://{self.user}:{self.password.get_secret_value()}"
            f"@{self.host}:{self.port}/{self.database_name}"
        )

    model_config = SettingsConfigDict(
        env_file=ENV_PATH, env_file_encoding="utf-8", env_prefix="DB_"
    )


class Settings(BaseSettings):
    database: PostgreSQLSettings = Field(default_factory=PostgreSQLSettings)


settings = Settings()
