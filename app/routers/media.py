import os
import uuid
from .. import models, schemas, utils, oauth2
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.orm import Session
from ..database import get_db
from app.tasks.media_tasks import (
    compress_image,
    generate_image_thumbnail,
    extract_video_metadata,
)

router = APIRouter(
    prefix="/media",
    tags=["Media"],
)


@router.post(
    "/upload",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.Media,
)
async def upload_media(
    post_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user),
):

    # 1. Check if the post exists
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # 2. Check ownership
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You don't own this post.")

    # 3. Detect file type
    if file.content_type.startswith("image/"):
        file_type = "image"
        folder = "uploads/images"

    elif file.content_type.startswith("video/"):
        file_type = "video"
        folder = "uploads/videos"

    else:
        raise HTTPException(status_code=400, detail="Only images and videos are allowed.")

    contents = await file.read()

    # If configured to use Cloudinary, upload and store remote URL
    from ..config import settings
    if settings.storage_backend == "cloudinary":
        public_id = f"media/{uuid.uuid4()}"
        folder_name = "media/images" if file_type == "image" else "media/videos"
        from app.cloudinary_client import upload_bytes
        _, url = upload_bytes(contents, public_id=public_id, folder=folder_name, resource_type=("image" if file_type == "image" else "video"))
        file_url = url
        file_size = len(contents)
    else:
        # disk fallback (existing behavior)
        os.makedirs(folder, exist_ok=True)
        extension = file.filename.split(".")[-1]
        filename = f"{uuid.uuid4()}.{extension}"
        filepath = os.path.join(folder, filename)
        with open(filepath, "wb") as buffer:
            buffer.write(contents)
        file_url = filepath
        file_size = os.path.getsize(filepath)

    media = models.Media(
        post_id=post.id,
        owner_id=current_user.id,
        file_url=file_url,
        file_type=file_type,
        mime_type=file.content_type,
        file_size=file_size,
    )

    db.add(media)
    db.commit()
    db.refresh(media)

    # For cloud uploads we rely on Cloudinary transformations; only run local tasks when using disk
    if settings.storage_backend == "disk":
        if file_type == "image":
            compress_image.delay(filepath)
            generate_image_thumbnail.delay(filepath)
        else:
            extract_video_metadata.delay(filepath)

    return media
