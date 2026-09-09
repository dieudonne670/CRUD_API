from secrets import token_urlsafe

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from app.pubsub import publish_message
from app import models


# ============================================================
# Generate a secure stream key
# ============================================================

def generate_stream_key() -> str:
    """
    Generates a unique secret key for OBS.

    Example:
    X6P4xv8A5eVw7M2...
    """

    return token_urlsafe(32)


# ============================================================
# Create Livestream
# ============================================================

def create_stream(
    db: Session,
    owner_id: int,
    title: str,
    description: str | None,
    category: str | None,
) -> models.LiveStream:

    stream = models.LiveStream(

        owner_id=owner_id,

        title=title,

        description=description,

        category=category,

        stream_key=generate_stream_key(),

        playback_url="",

        thumbnail_url="",

        recording_url="",

        status="OFFLINE",

        is_live=False,

        current_viewers=0,

        peak_viewers=0,
    )

    db.add(stream)

    db.commit()

    db.refresh(stream)

    return stream


# ============================================================
# Get one stream
# ============================================================

def get_stream(
    db: Session,
    stream_id: int,
) -> models.LiveStream:

    stream = (
        db.query(models.LiveStream)
        .filter(models.LiveStream.id == stream_id)
        .first()
    )

    if not stream:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Livestream not found",
        )

    return stream


# ============================================================
# Get my streams
# ============================================================

def get_my_streams(
    db: Session,
    owner_id: int,
):

    return (
        db.query(models.LiveStream)
        .filter(models.LiveStream.owner_id == owner_id)
        .order_by(models.LiveStream.created_at.desc())
        .all()
    )


# ============================================================
# Get all active livestreams
# ============================================================

def get_live_streams(
    db: Session,
):

    return (
        db.query(models.LiveStream)
        .filter(models.LiveStream.is_live == True)
        .order_by(models.LiveStream.started_at.desc())
        .all()
    )


def start_stream_from_rtmp(
    db: Session,
    stream_key: str,
) -> models.LiveStream:
    """
    Called automatically by NGINX when OBS starts streaming.
    """

    stream = (
        db.query(models.LiveStream)
        .filter(models.LiveStream.stream_key == stream_key)
        .first()
    )

    if not stream:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid stream key",
        )

    stream.status = "LIVE"

    stream.is_live = True

    stream.started_at = datetime.utcnow()

    stream.ended_at = None

    stream.playback_url = (
        f"http://localhost/hls/{stream.stream_key}.m3u8"
    )

    db.commit()

    db.refresh(stream)

    publish_stream_started(stream)

    return stream



def stop_stream_from_rtmp(
    db: Session,
    stream_key: str,
) -> models.LiveStream:
    """
    Called automatically by NGINX
    when OBS disconnects.
    """

    stream = (
        db.query(models.LiveStream)
        .filter(models.LiveStream.stream_key == stream_key)
        .first()
    )

    if not stream:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid stream key",
        )

    stream.status = "ENDED"

    stream.is_live = False

    stream.ended_at = datetime.utcnow()

    db.commit()

    db.refresh(stream)

    publish_stream_stopped(stream)

    return stream

def publish_stream_started(
    stream: models.LiveStream,
):
    """
    Publish a livestream started event.
    """

    publish_message(
        channel="livestreams",
        data={
            "type": "stream_started",
            "stream_id": stream.id,
            "owner_id": stream.owner_id,
            "title": stream.title,
            "category": stream.category,
            "playback_url": stream.playback_url,
            "thumbnail": stream.thumbnail_url,
            "started_at": str(stream.started_at),
        },
    )

def publish_stream_stopped(
    stream: models.LiveStream,
):
    """
    Publish a livestream ended event.
    """

    publish_message(
        channel="livestreams",
        data={
            "type": "stream_stopped",
            "stream_id": stream.id,
            "owner_id": stream.owner_id,
            "ended_at": str(stream.ended_at),
        },
    )



# ============================================================
# Viewer joins livestream
# ============================================================

def increment_viewers(
    db: Session,
    stream: models.LiveStream,
) -> models.LiveStream:
    """
    Increase the number of active viewers.
    """

    stream.current_viewers += 1

    if stream.current_viewers > stream.peak_viewers:
        stream.peak_viewers = stream.current_viewers

    db.commit()

    db.refresh(stream)

    return stream


# ============================================================
# Viewer leaves livestream
# ============================================================

def decrement_viewers(
    db: Session,
    stream: models.LiveStream,
) -> models.LiveStream:
    """
    Decrease active viewers.
    """

    if stream.current_viewers > 0:
        stream.current_viewers -= 1

    db.commit()

    db.refresh(stream)

    return stream

def publish_viewer_update(
    stream: models.LiveStream,
):
    """
    Broadcast viewer statistics.
    """

    publish_message(
        channel="livestreams",
        data={
            "type": "viewer_update",
            "stream_id": stream.id,
            "current_viewers": stream.current_viewers,
            "peak_viewers": stream.peak_viewers,
        },
    )