import os
from datetime import datetime, timezone

from app.celery_app import celery
from app.database import SessionLocal
from app import models


@celery.task
def cleanup_finished_streams():
    """
    Marks streams as finished if their end time has passed.
    """

    db = SessionLocal()

    try:

        finished_streams = (
            db.query(models.LiveStream)
            .filter(
                models.LiveStream.is_live == True,
                models.LiveStream.ends_at <= datetime.now(timezone.utc),
            )
            .all()
        )

        for stream in finished_streams:

            stream.is_live = False

        db.commit()

        return len(finished_streams)

    finally:

        db.close()

@celery.task
def delete_hls_segments():

    """
    Deletes old HLS video segments.
    """

    hls_folder = "hls"

    if not os.path.exists(hls_folder):
        return

    for file in os.listdir(hls_folder):

        if file.endswith(".ts"):

            os.remove(
                os.path.join(
                    hls_folder,
                    file,
                )
            )

        elif file.endswith(".m3u8"):

            os.remove(
                os.path.join(
                    hls_folder,
                    file,
                )
            )

    return True

@celery.task
def notify_stream_finished(stream_id):

    db = SessionLocal()

    try:

        stream = (
            db.query(models.LiveStream)
            .filter(
                models.LiveStream.id == stream_id
            )
            .first()
        )

        if not stream:

            return

        print(
            f"Notify followers that stream {stream.title} ended."
        )

    finally:

        db.close()

