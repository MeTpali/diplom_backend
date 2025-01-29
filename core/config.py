from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_url: str = (
        "postgresql+asyncpg://lalala:31lCmYhnXPrT@ep-dry-night-a2ty68gn.eu-central-1.aws.neon.tech/trail_exams"
    )
    db_echo: bool = True


settings = Settings()
# postgresql+asyncpg://trail_exams_owner:31lCmYhnXPrT@ep-dry-night-a2ty68gn.eu-central-1.aws.neon.tech/trail_exams
