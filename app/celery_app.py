from celery import Celery

from app.config import settings

celery = Celery(
    "social_media",
    broker=settings.redis_url
    or f"redis://{settings.redis_host}:{settings.redis_port}/{settings.redis_db}",
    backend=settings.redis_url
    or f"redis://{settings.redis_host}:{settings.redis_port}/{settings.redis_db}",
)

celery.conf.update(
    timezone="Africa/Douala",
    enable_utc=True,
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    result_expires=3600,
)

celery.conf.imports = (
    "app.tasks",
    "app.tasks.email_tasks",
    "app.tasks.story_tasks",
    "app.tasks.media_tasks",
    "app.tasks.notification_tasks",
)