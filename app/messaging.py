from fastapi import HTTPException, Response, status
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from app import models
from app.pubsub import publish_message


def create_message(
    db: Session,
    sender_id: int,
    message_data,
) -> models.Message:

    # Check if receiver exists
    receiver = (
        db.query(models.User)
        .filter(models.User.id == message_data.receiver_id)
        .first()
    )

    if not receiver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Receiver not found",
        )

    # Save message
    message = models.Message(
        sender_id=sender_id,
        receiver_id=message_data.receiver_id,
        message=message_data.message,
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    # ------------------------------------
    # Publish realtime event to Redis
    # ------------------------------------

    publish_message(
        channel="messages",
        data={
            "type": "message",
            "message_id": message.id,
            "sender": sender_id,
            "receiver": receiver.id,
            "message": message.message,
            "created_at": str(message.created_at),
        },
    )

    return message


def get_conversation(
    db: Session,
    current_user_id: int,
    other_user_id: int,
):

    receiver = (
        db.query(models.User)
        .filter(models.User.id == other_user_id)
        .first()
    )

    if not receiver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    messages = (
        db.query(models.Message)
        .filter(
            or_(
                and_(
                    models.Message.sender_id == current_user_id,
                    models.Message.receiver_id == other_user_id,
                ),
                and_(
                    models.Message.sender_id == other_user_id,
                    models.Message.receiver_id == current_user_id,
                ),
            )
        )
        .order_by(models.Message.created_at.asc())
        .all()
    )

    return messages


def mark_read(
    db: Session,
    message_id: int,
    current_user_id: int,
) -> models.Message:

    message = (
        db.query(models.Message)
        .filter(models.Message.id == message_id)
        .first()
    )

    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found",
        )

    if message.receiver_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot mark this message as read",
        )

    message.is_read = True
    db.commit()
    db.refresh(message)

    return message


def delete_message(
    db: Session,
    message_id: int,
    current_user_id: int,
) -> Response:

    message = (
        db.query(models.Message)
        .filter(models.Message.id == message_id)
        .first()
    )

    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found",
        )

    if (
        message.sender_id != current_user_id
        and message.receiver_id != current_user_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this message",
        )

    db.delete(message)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)