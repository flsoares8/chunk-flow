import logging

import uvicorn
from fastapi import FastAPI

from scheduler.config import config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(title="ChunkFlow Scheduler")


@app.get("/health")
def health() -> dict:
    logger.info("Health check requested")
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run("scheduler.main:app", host=config.host, port=config.port, reload=False)
