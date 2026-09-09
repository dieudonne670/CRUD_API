import os
from datetime import datetime, timezone

from app.celery_app import celery
from app.database import SessionLocal
from app import models


@celery.task
def delete_expired_stories():
    """
    Delete stories that have expired.
    """

    db = SessionLocal()

    try:

        expired_stories = (
            db.query(models.Story)
            .filter(models.Story.expires_at <= datetime.now(timezone.utc))
            .all()
        )

        for story in expired_stories:

            # Delete physical file
            if story.file_url and os.path.exists(story.file_url):
                os.remove(story.file_url)

            # Delete database record
            db.delete(story)

        db.commit()

        return f"{len(expired_stories)} expired stories deleted."

    finally:
        db.close()