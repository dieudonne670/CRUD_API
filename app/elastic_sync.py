import logging

from app.elastic import (
    index_document,
    update_document,
    delete_document,
)

logger = logging.getLogger(__name__)


def _safe_index(action: str, func, *args, **kwargs):
    try:
        func(*args, **kwargs)
    except Exception:
        logger.warning("Elasticsearch %s sync failed; continuing without ES indexing.", action, exc_info=True)


# --------------------------------------------------
# USERS
# --------------------------------------------------

def sync_user(user):

    """
    Create or update a user document.
    """

    _safe_index(
        "user",
        index_document,
        index="users",
        document_id=user.id,
        document={
            "email": user.email,
            "profile_picture": user.profile_picture,
        },
    )


def update_user(user):

    """
    Update indexed user.
    """

    _safe_index(
        "user update",
        update_document,
        index="users",
        document_id=user.id,
        document={
            "email": user.email,
            "profile_picture": user.profile_picture,
        },
    )


def delete_user(user_id: int):

    """
    Remove user from Elasticsearch.
    """

    _safe_index(
        "user delete",
        delete_document,
        index="users",
        document_id=user_id,
    )


# --------------------------------------------------
# POSTS
# --------------------------------------------------

def sync_post(post):

    """
    Index a post.
    """

    _safe_index(
        "post",
        index_document,
        index="posts",
        document_id=post.id,
        document={
            "title": post.title,
            "content": post.content,
            "owner_id": post.owner_id,
            "created_at": post.created_at.isoformat(),
        },
    )


def update_post(post):

    """
    Update a post.
    """

    _safe_index(
        "post update",
        update_document,
        index="posts",
        document_id=post.id,
        document={
            "title": post.title,
            "content": post.content,
        },
    )


def delete_post(post_id: int):

    _safe_index(
        "post delete",
        delete_document,
        index="posts",
        document_id=post_id,
    )


# --------------------------------------------------
# MESSAGES
# --------------------------------------------------

def sync_message(message):

    """
    Index a private message.
    """

    _safe_index(
        "message",
        index_document,
        index="messages",
        document_id=message.id,
        document={
            "sender_id": message.sender_id,
            "receiver_id": message.receiver_id,
            "message": message.message,
            "created_at": message.created_at.isoformat(),
        },
    )


def delete_message(message_id: int):

    _safe_index(
        "message delete",
        delete_document,
        index="messages",
        document_id=message_id,
    )


# --------------------------------------------------
# LIVESTREAMS
# --------------------------------------------------

def sync_stream(stream):

    """
    Index livestream.
    """

    _safe_index(
        "stream",
        index_document,
        index="livestreams",
        document_id=stream.id,
        document={
            "title": stream.title,
            "description": stream.description,
            "category": stream.category,
            "status": stream.status,
            "owner_id": stream.owner_id,
        },
    )


def update_stream(stream):

    _safe_index(
        "stream update",
        update_document,
        index="livestreams",
        document_id=stream.id,
        document={
            "title": stream.title,
            "description": stream.description,
            "status": stream.status,
        },
    )


def delete_stream(stream_id: int):

    _safe_index(
        "stream delete",
        delete_document,
        index="livestreams",
        document_id=stream_id,
    )