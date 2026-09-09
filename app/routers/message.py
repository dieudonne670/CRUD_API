from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from .. import oauth2, schemas
from ..database import get_db
from ..messaging import create_message, delete_message, get_conversation, mark_read
from app.redis_cache import get_cache, set_cache, make_key

router = APIRouter(
    prefix="/messages",
    tags=["Messages"],
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.MessageOut)
def send_message(
    message: schemas.MessageCreate,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user),
):
    return create_message(db=db, sender_id=current_user.id, message_data=message)


@router.get("/conversation/{user_id}", response_model=list[schemas.MessageOut])
def get_messages(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user),
):
    cache_key = make_key("conversation", current_user.id, user_id)

    cached_messages = get_cache(cache_key)

    if cached_messages is not None:
        print("Returned from Redis")
        return cached_messages

    print("Returned from PostgreSQL")

    messages = get_conversation(
        db=db,
        current_user_id=current_user.id,
        other_user_id=user_id,
    )

    message_data = [
        schemas.MessageOut.model_validate(message).model_dump(mode="json")
        for message in messages
    ]

    set_cache(cache_key, message_data)

    return message_data


@router.put("/{message_id}/read", response_model=schemas.MessageOut)
def read_message(
    message_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user),
):
    return mark_read(db=db, message_id=message_id, current_user_id=current_user.id)


@router.delete("/{message_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_message(
    message_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user),
):
    return delete_message(db=db, message_id=message_id, current_user_id=current_user.id)
