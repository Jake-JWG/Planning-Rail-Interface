from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Railway Planning Proximity Monitor"
    database_url: str = "postgresql+psycopg://postgres:postgres@db:5432/rail_monitor"
    default_threshold_meters: float = 25.0
    default_buffer_meters: float = 15.0
    alert_daily_enabled: bool = True
    alert_weekly_enabled: bool = True
    planning_sources: str = "mock_planning"
    rail_sources: str = "mock_rail"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
