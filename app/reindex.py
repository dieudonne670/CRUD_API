from sqlalchemy.orm import Session

from app import models
from app.elastic_sync import (
    sync_user,
    sync_post,
    sync_message,
    sync_stream,
)


# --------------------------------------------------
# Reindex Everything
# --------------------------------------------------

def reindex_all(
    db: Session,
):
    """
    Rebuilds every Elasticsearch index from PostgreSQL.
    """

    # -------------------------
    # Users
    # -------------------------

    users = db.query(models.User).all()

    for user in users:

        sync_user(user)

    print(f"Indexed {len(users)} users.")


    # -------------------------
    # Posts
    # -------------------------

    posts = db.query(models.Post).all()

    for post in posts:

        sync_post(post)

    print(f"Indexed {len(posts)} posts.")


    # -------------------------
    # Messages
    # -------------------------

    messages = db.query(models.Message).all()

    for message in messages:

        sync_message(message)

    print(f"Indexed {len(messages)} messages.")


    # -------------------------
    # Livestreams
    # -------------------------

    streams = db.query(models.LiveStream).all()

    for stream in streams:

        sync_stream(stream)

    print(f"Indexed {len(streams)} livestreams.")


    print("✅ Elasticsearch reindex completed.")