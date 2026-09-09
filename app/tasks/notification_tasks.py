from app.celery_app import celery
from app.database import SessionLocal
from app import models
from app.tasks.email_tasks import send_notification_email


@celery.task
def process_notification(notification_id: int):
    """
    Background processing for notifications.
    """

    db = SessionLocal()

    try:

        notification = (
            db.query(models.Notification)
            .filter(models.Notification.id == notification_id)
            .first()
        )

        if not notification:
            return

        recipient = (
            db.query(models.User)
            .filter(models.User.id == notification.recipient_id)
            .first()
        )

        actor = (
            db.query(models.User)
            .filter(models.User.id == notification.actor_id)
            .first()
        )

        if not recipient or not actor:
            return

        # Send email in the background
        send_notification_email.delay(
            recipient.email,
            actor.email,
        )

    finally:
        db.close()