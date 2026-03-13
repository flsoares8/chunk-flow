import json
import logging
from typing import Optional

from scheduler.redis_client import TASK_QUEUE_KEY, get_client

logger = logging.getLogger(__name__)


def enqueue_task(task: dict) -> None:
    client = get_client()
    client.lpush(TASK_QUEUE_KEY, json.dumps(task))
    logger.info("Enqueued task %s", task.get("task_id"))


def dequeue_task() -> Optional[dict]:
    client = get_client()
    raw = client.rpop(TASK_QUEUE_KEY)
    if raw is None:
        return None
    task = json.loads(raw)
    logger.info("Dequeued task %s", task.get("task_id"))
    return task
