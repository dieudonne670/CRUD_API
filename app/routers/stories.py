import os
import uuid
from datetime import datetime, timedelta

from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
    File,
    HTTPException,
    status,
)

from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, schemas, oauth2


router = APIRouter(
    prefix="/stories",
    tags=["Stories"],
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.Story,
)
async def upload_story(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user),
):

    if file.content_type.startswith("image/"):
        folder = "uploads/stories/images"
        file_type = "image"

    elif file.content_type.startswith("video/"):
        folder = "uploads/stories/videos"
        file_type = "video"

    else:
        raise HTTPException(
            status_code=400,
            detail="Only images and videos are allowed."
        )

    os.makedirs(folder, exist_ok=True)
    contents = await file.read()
    from ..config import settings
    if settings.storage_backend == "cloudinary":
        public_id = f"stories/{uuid.uuid4()}"
        folder_name = "stories/images" if file_type == "image" else "stories/videos"
        from app.cloudinary_client import upload_bytes
        _, url = upload_bytes(contents, public_id=public_id, folder=folder_name, resource_type=("image" if file_type=="image" else "video"))
        file_url = url
        file_size = len(contents)
    else:
        os.makedirs(folder, exist_ok=True)
        extension = file.filename.split(".")[-1]
        filename = f"{uuid.uuid4()}.{extension}"
        filepath = os.path.join(folder, filename)
        with open(filepath, "wb") as buffer:
            buffer.write(contents)
        file_url = filepath
        file_size = os.path.getsize(filepath)

    story = models.Story(
        owner_id=current_user.id,
        file_url=file_url,
        file_type=file_type,
        mime_type=file.content_type,
        file_size=file_size,
        expires_at=datetime.utcnow() + timedelta(hours=24),
    )

    db.add(story)
    db.commit()
    db.refresh(story)

    return story

@router.get(
    "/",
    response_model=list[schemas.Story]
)
def get_active_stories(
    db: Session = Depends(get_db),
):

    stories = (
        db.query(models.Story)
        .filter(models.Story.expires_at > datetime.utcnow())
        .order_by(models.Story.created_at.desc())
        .all()
    )

    return stories

@router.delete(
    "/{story_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_story(
    story_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user),
):

    story = (
        db.query(models.Story)
        .filter(models.Story.id == story_id)
        .first()
    )

    if not story:
        raise HTTPException(
            status_code=404,
            detail="Story not found."
        )

    if story.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized."
        )

    if os.path.exists(story.file_url):
        # only remove local files; cloud uploads are managed externally
        os.remove(story.file_url)

    db.delete(story)
    db.commit()  