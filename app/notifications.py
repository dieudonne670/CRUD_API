from sqlalchemy.orm import Session
from app.tasks.notification_tasks import process_notification
from app import models
from app.pubsub import publish_message

import asyncio

def create_notification(
    db: Session,
    recipient_id: int,
    actor_id: int,
    notification_type: str,
    post_id: int | None = None,
    comment_id: int | None = None,
):

    if recipient_id == actor_id:
        return None

    notification = models.Notification(
        recipient_id=recipient_id,
        actor_id=actor_id,
        type=notification_type,
        post_id=post_id,
        comment_id=comment_id,
    )

    db.add(notification)
    db.commit()
    db.refresh(notification)

    process_notification.delay(notification.id)

    # ------------------------------------
    # Publish realtime notification
    # ------------------------------------
    

    asyncio.create_task(
        publish_message(
            channel="notifications",
            data={
                "type": "notification",
                "notification_id": notification.id,
                "recipient": recipient_id,
                "actor": actor_id,
                "notification_type": notification.type,
                "post_id": post_id,
                "comment_id": comment_id,
                "is_read": notification.is_read,
                "created_at": str(notification.created_at),
            },
        )
    )

    return notification

def create_notification_for_follow(
    db: Session,
    following_id: int,
    actor_id: int,
):
    """
    User A follows User B.
    Notify User B.
    """
    return create_notification(
        db=db,
        recipient_id=following_id,
        actor_id=actor_id,
        notification_type="follow",
    )


def create_notification_for_like(
    db: Session,
    post_id: int,
    actor_id: int,
):
    """
    Someone liked a post.
    Notify the owner of the post.
    """

    post = (
        db.query(models.Post)
        .filter(models.Post.id == post_id)
        .first()
    )

    if not post:
        return None

    return create_notification(
        db=db,
        recipient_id=post.owner_id,
        actor_id=actor_id,
        notification_type="like",
        post_id=post.id,
    )


def create_notification_for_comment(
    db: Session,
    post_id: int,
    actor_id: int,
):
    """
    Someone commented on a post.
    Notify the owner of the post.
    """

    comment = (
        db.query(models.Comment)
        .filter(models.Comment.id == post_id)
        .first()
    )

    if not comment:
        return None

    post = (
        db.query(models.Post)
        .filter(models.Post.id == comment.post_id)
        .first()
    )

    if not post:
        return None

    return create_notification(
        db=db,
        recipient_id=post.owner_id,
        actor_id=actor_id,
        notification_type="comment",
        post_id=post.id
    )


def create_notification_for_reply(
    db: Session,
    comment_id: int,
    actor_id: int,
):
    """
    Someone replied to another user's comment.
    Notify the owner of the parent comment.
    """

    comment = (
        db.query(models.Comment)
        .filter(models.Comment.id == comment_id)
        .first()
    )

    if not comment:
        return None

    return create_notification(
        db=db,
        recipient_id=comment.owner_id,
        actor_id=actor_id,
        notification_type="reply",
        post_id=comment.post_id,
        comment_id=comment.id,
    )