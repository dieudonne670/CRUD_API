from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, oauth2
from app.permission import verify_owner
from app.notifications import create_notification
from app.redis_cache import get_cache, set_cache, make_key


router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)

# Get all notifications for the logged-in user
@router.get("/", response_model=list[schemas.Notification])
def get_notifications(
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user)
):
    cache_key = make_key("notifications", current_user.id)

    cached_notifications = get_cache(cache_key)

    if cached_notifications is not None:
        print("Returned from Redis")
        return cached_notifications

    print("Returned from PostgreSQL")

    notifications = (
        db.query(models.Notification)
        .filter(models.Notification.recipient_id == current_user.id)
        .all()
    )

    notification_data = [
        schemas.Notification.model_validate(notification).model_dump(mode="json")
        for notification in notifications
    ]

    set_cache(cache_key, notification_data)

    return notification_data


# Get a single notification
@router.get("/{id}", response_model=schemas.Notification)
def get_notification(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user)
):
    notification = (
        db.query(models.Notification)
        .filter(
            models.Notification.id == id,
            models.Notification.recipient_id == current_user.id
        )
        .first()
    )

    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )

    return notification


# Mark one notification as read
@router.put("/{id}/read", response_model=schemas.Notification)
def mark_notification_as_read(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user)
):
    notification = (
        db.query(models.Notification)
        .filter(
            models.Notification.id == id,
            models.Notification.recipient_id == current_user.id
        )
        .first()
    )

    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )

    notification.is_read = True

    db.commit()
    db.refresh(notification)

    return notification


# Mark all notifications as read
@router.put("/read-all", response_model=list[schemas.Notification])
def mark_all_notifications_as_read(
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user)
):
    notifications = (
        db.query(models.Notification)
        .filter(
            models.Notification.recipient_id == current_user.id,
            models.Notification.is_read == False
        )
        .all()
    )

    for notification in notifications:
        notification.is_read = True

    db.commit()

    return notifications


# Delete a notification
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_notification(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user)
):
    notification = (
        db.query(models.Notification)
        .filter(
            models.Notification.id == id,
            models.Notification.recipient_id == current_user.id
        )
        .first()
    )

    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )

    db.delete(notification)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)