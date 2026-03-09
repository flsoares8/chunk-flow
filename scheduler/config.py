import os


class Config:
    host: str = os.getenv("SCHEDULER_HOST", "0.0.0.0")
    port: int = int(os.getenv("SCHEDULER_PORT", "8000"))
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379")


config = Config()
