import os
import time
import logging

from app.elastic import create_index, check_elasticsearch


# -------------------------------------------------
# USERS INDEX
# -------------------------------------------------

def create_users_index():

    """
    Creates the users index.
    """

    mapping = {
        "properties": {
            "username": {
                "type": "text",
            },
            "email": {
                "type": "keyword",
            },
            "bio": {
                "type": "text",
            },
            "profile_picture": {
                "type": "keyword",
            },
        }
    }

    create_index(
        index_name="users",
        mapping=mapping,
    )


# -------------------------------------------------
# POSTS INDEX
# -------------------------------------------------

def create_posts_index():

    """
    Creates the posts index.
    """

    mapping = {
        "properties": {
            "title": {
                "type": "text",
            },
            "content": {
                "type": "text",
            },
            "owner_id": {
                "type": "integer",
            },
            "created_at": {
                "type": "date",
            },
        }
    }

    create_index(
        index_name="posts",
        mapping=mapping,
    )


# -------------------------------------------------
# MESSAGES INDEX
# -------------------------------------------------

def create_messages_index():

    """
    Creates the messages index.
    """

    mapping = {
        "properties": {
            "sender_id": {
                "type": "integer",
            },
            "receiver_id": {
                "type": "integer",
            },
            "message": {
                "type": "text",
            },
            "created_at": {
                "type": "date",
            },
        }
    }

    create_index(
        index_name="messages",
        mapping=mapping,
    )


# -------------------------------------------------
# LIVESTREAMS INDEX
# -------------------------------------------------

def create_livestreams_index():

    """
    Creates the livestreams index.
    """

    mapping = {
        "properties": {
            "title": {
                "type": "text",
            },
            "description": {
                "type": "text",
            },
            "category": {
                "type": "keyword",
            },
            "status": {
                "type": "keyword",
            },
            "owner_id": {
                "type": "integer",
            },
        }
    }

    create_index(
        index_name="livestreams",
        mapping=mapping,
    )


# -------------------------------------------------
# CREATE ALL INDICES
# -------------------------------------------------

def create_all_indices():

    """
    Creates every Elasticsearch index.

    Retries briefly then gives up so startup never crashes or hangs if no
    Elasticsearch instance is configured (search will just be unavailable).
    Override via ES_INDEX_MAX_RETRIES / ES_INDEX_RETRY_DELAY env vars.
    """
    max_retries = int(os.getenv("ES_INDEX_MAX_RETRIES", "3"))
    delay_seconds = int(os.getenv("ES_INDEX_RETRY_DELAY", "1"))

    for attempt in range(1, max_retries + 1):
        try:
            if check_elasticsearch():
                create_users_index()
                create_posts_index()
                create_messages_index()
                create_livestreams_index()
                logging.info("✅ Elasticsearch indices are ready.")
                return
            else:
                logging.warning(
                    "Elasticsearch not ready (attempt %s/%s). Retrying in %s seconds...",
                    attempt,
                    max_retries,
                    delay_seconds,
                )
        except Exception as e:
            logging.warning(
                "Error while checking/creating indices (attempt %s/%s): %s",
                attempt,
                max_retries,
                e,
            )

        time.sleep(delay_seconds)

    logging.error(
        "Elasticsearch did not become available after %s attempts; skipping index creation.",
        max_retries,
    )