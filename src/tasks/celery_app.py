from celery import Celery

from src.config import settings

celery_app = Celery(
    "tasks", broker=settings.REDIS_URL, include=["src.tasks.tasks_for_celery"]
)
