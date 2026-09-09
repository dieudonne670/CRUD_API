from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app import livestream
from .. import models, oauth2, schemas
from ..database import get_db

router = APIRouter(prefix="/livestreams", tags=["Livestream"])


@router.post("/create", response_model=schemas.LiveStream, status_code=status.HTTP_201_CREATED)
def create_live_stream(
    stream: schemas.LiveStreamCreate,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user),
):
    return livestream.create_stream(
        db=db,
        owner_id=current_user.id,
        title=stream.title,
        description=stream.description,
        category=stream.category,
    )


@router.get("/me", response_model=list[schemas.LiveStream])
def get_my_streams(
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user),
):
    return (
        db.query(models.LiveStream)
        .filter(models.LiveStream.owner_id == current_user.id)
        .order_by(models.LiveStream.created_at.desc())
        .all()
    )


@router.get("/live", response_model=list[schemas.LiveStream])
def get_live_streams(db: Session = Depends(get_db)):
    return (
        db.query(models.LiveStream)
        .filter(models.LiveStream.is_live.is_(True))
        .order_by(models.LiveStream.started_at.desc())
        .all()
    )


@router.get("/{stream_id}", response_model=schemas.LiveStream)
def get_stream(stream_id: int, db: Session = Depends(get_db)):
    stream = db.query(models.LiveStream).filter(models.LiveStream.id == stream_id).first()

    if not stream:
        raise HTTPException(status_code=404, detail="Stream not found")

    return stream


@router.put("/{stream_id}", response_model=schemas.LiveStream)
def update_stream(
    stream_id: int,
    updated_stream: schemas.LiveStreamUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user),
):
    stream = (
        db.query(models.LiveStream)
        .filter(
            models.LiveStream.id == stream_id,
            models.LiveStream.owner_id == current_user.id,
        )
        .first()
    )

    if not stream:
        raise HTTPException(status_code=404, detail="Stream not found")

    update_data = updated_stream.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(stream, key, value)

    db.commit()
    db.refresh(stream)

    return stream


@router.delete("/{stream_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_stream(
    stream_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user),
):
    stream = (
        db.query(models.LiveStream)
        .filter(
            models.LiveStream.id == stream_id,
            models.LiveStream.owner_id == current_user.id,
        )
        .first()
    )

    if not stream:
        raise HTTPException(status_code=404, detail="Stream not found")

    db.delete(stream)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{stream_id}/start", response_model=schemas.LiveStream)
def start_stream(
    stream_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user),
):
    stream = (
        db.query(models.LiveStream)
        .filter(
            models.LiveStream.id == stream_id,
            models.LiveStream.owner_id == current_user.id,
        )
        .first()
    )

    if not stream:
        raise HTTPException(status_code=404, detail="Stream not found")

    return livestream.start_stream(db, stream)


@router.post("/{stream_id}/stop", response_model=schemas.LiveStream)
def stop_stream(
    stream_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user),
):
    stream = (
        db.query(models.LiveStream)
        .filter(
            models.LiveStream.id == stream_id,
            models.LiveStream.owner_id == current_user.id,
        )
        .first()
    )

    if not stream:
        raise HTTPException(status_code=404, detail="Stream not found")

    return livestream.stop_stream(db, stream)


from fastapi import Query


@router.post("/on_publish")
def on_publish(
    stream_key: str = Query(...),
    db: Session = Depends(get_db),
):
    return livestream.start_stream_from_rtmp(
        db=db,
        stream_key=stream_key,
    )

@router.post("/on_done")
def on_done(
    stream_key: str = Query(...),
    db: Session = Depends(get_db),
):
    return livestream.stop_stream_from_rtmp(
        db=db,
        stream_key=stream_key,
    )

@router.get("/{stream_id}/watch", response_model=schemas.LiveStreamWatchResponse)
def watch_stream(stream_id: int, db: Session = Depends(get_db)):
    stream = db.query(models.LiveStream).filter(models.LiveStream.id == stream_id).first()

    if not stream:
        raise HTTPException(status_code=404, detail="Stream not found")

    return {
        "stream_id": stream.id,
        "playback_url": stream.playback_url,
        "is_live": stream.is_live,
        "stream": stream,
    }


@router.post("/{stream_id}/viewer/join", response_model=schemas.LiveStream)
def join_viewer(stream_id: int, db: Session = Depends(get_db)):
    stream = db.query(models.LiveStream).filter(models.LiveStream.id == stream_id).first()

    if not stream:
        raise HTTPException(status_code=404, detail="Stream not found")

    return livestream.increment_viewers(db, stream)


@router.post("/{stream_id}/viewer/leave", response_model=schemas.LiveStream)
def leave_viewer(stream_id: int, db: Session = Depends(get_db)):
    stream = db.query(models.LiveStream).filter(models.LiveStream.id == stream_id).first()

    if not stream:
        raise HTTPException(status_code=404, detail="Stream not found")

    return livestream.decrement_viewers(db, stream)


@router.post("/{stream_id}/chat", response_model=schemas.LiveStreamChatResponse)
def send_chat_message(stream_id: int, payload: schemas.LiveStreamChatMessage, db: Session = Depends(get_db)):
    stream = db.query(models.LiveStream).filter(models.LiveStream.id == stream_id).first()

    if not stream:
        raise HTTPException(status_code=404, detail="Stream not found")

    return {
        "stream_id": stream.id,
        "message": payload.message,
        "sender_id": None,
    }


@router.get("/{stream_id}/stats", response_model=schemas.LiveStreamStats)
def get_stream_stats(stream_id: int, db: Session = Depends(get_db)):
    stream = db.query(models.LiveStream).filter(models.LiveStream.id == stream_id).first()

    if not stream:
        raise HTTPException(status_code=404, detail="Stream not found")

    return {
        "stream_id": stream.id,
        "is_live": stream.is_live,
        "current_viewers": stream.current_viewers or 0,
        "peak_viewers": stream.peak_viewers or 0,
        "started_at": stream.started_at,
        "ended_at": stream.ended_at,
    }

