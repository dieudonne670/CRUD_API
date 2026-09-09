from app.elastic import es
from elasticsearch import NotFoundError

from app.elastic import es


def search_posts(
    query: str,
    size: int = 20,
):
    """
    Search posts using Elasticsearch.
    """

    response = es.search(
        index="posts",
        query={
            "multi_match": {
                "query": query,
                "fields": [
                    "title",
                    "content",
                ],
            }
        },
        size=size,
    )

    return response["hits"]["hits"]


def search_users(
    query: str,
    size: int = 20,
):
    """
    Search users.
    """

    response = es.search(
        index="users",
        query={
            "multi_match": {
                "query": query,
                "fields": [
                    "username",
                    "bio",
                ],
            }
        },
        size=size,
    )

    return response["hits"]["hits"]


def search_messages(
    query: str,
    size: int = 20,
):
    """
    Search private messages.
    """

    response = es.search(
        index="messages",
        query={
            "match": {
                "message": query,
            }
        },
        size=size,
    )

    return response["hits"]["hits"]

def search_streams(
    query: str,
    size: int = 20,
):
    """
    Search livestreams.
    """

    response = es.search(
        index="livestreams",
        query={
            "multi_match": {
                "query": query,
                "fields": [
                    "title",
                    "description",
                    "category",
                ],
            }
        },
        size=size,
    )

    return response["hits"]["hits"]