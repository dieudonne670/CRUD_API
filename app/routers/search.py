from fastapi import APIRouter, Query

from app.search import (
    search_posts,
    search_users,
    search_messages,
    search_streams,
)

router = APIRouter(
    prefix="/search",
    tags=["Search"],
)

@router.get("/posts")
def search_posts_endpoint(
    q: str = Query(..., min_length=1),
):
    """
    Search posts.
    """

    return search_posts(q)

@router.get("/users")
def search_users_endpoint(
    q: str = Query(..., min_length=1),
):
    """
    Search users.
    """

    return search_users(q)

@router.get("/messages")
def search_messages_endpoint(
    q: str = Query(..., min_length=1),
):
    """
    Search messages.
    """

    return search_messages(q)

@router.get("/livestreams")
def search_streams_endpoint(
    q: str = Query(..., min_length=1),
):
    """
    Search livestreams.
    """

    return search_streams(q)