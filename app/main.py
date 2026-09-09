import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import bookmarks, comments, followers
from .database import  engine
from . import models
from .routers import post, user, auth, vote, comments, followers, notifications, media, stories, livestream, message
from .config import settings
from fastapi.staticfiles import StaticFiles
from app import websocket
from app.routers import search
from app.elastic_indices import create_all_indices

from fastapi.middleware.cors import CORSMiddleware


#models.Base.metadata.create_all(bind=engine)

app = FastAPI()

allowed_origins = [
    origin.strip()
    for origin in settings.cors_origins.split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("uploads", exist_ok=True)
app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads"
)



@app.on_event("startup")
def startup_event():
    """
    Runs once when FastAPI starts.
    """

    create_all_indices()

    print("✅ Elasticsearch indices are ready.")


#schema for the post
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
app.include_router(comments.router)
app.include_router(followers.router)
app.include_router(bookmarks.router)
app.include_router(notifications.router)
app.include_router(media.router)
app.include_router(stories.router)
app.include_router(livestream.router)
app.include_router(message.router)
app.include_router(websocket.router)
app.include_router(search.router)
# get request to the point is "/"

@app.get("/")
def root():
    return {"welcome": "to our API!"}

