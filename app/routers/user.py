import os
import uuid

from pydantic import FilePath

from .. import models, schemas, utils, oauth2
from fastapi import FastAPI, File, Response, UploadFile, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app.redis_cache import ( get_cache,
    set_cache,
    delete_cache,
    make_key,
)
from app.tasks.email_tasks import send_welcome_email

from ..database import get_db

from app.elastic_sync import (
    sync_user as sync_user_index,
    update_user as update_user_index,
    delete_user as delete_user_index,
)

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/me", response_model=schemas.UserOut)
def get_current_user_profile(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    return current_user


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
     
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    send_welcome_email.delay(
    new_user.email
)
    sync_user_index(new_user)

    return new_user


@router.get("/{id}", response_model=schemas.UserOut)
def get_user(
    id: int,
    db: Session = Depends(get_db),
):

    # ----------------------------
    # Build cache key
    # ----------------------------

    cache_key = make_key("user", id)

    # ----------------------------
    # Try Redis first
    # ----------------------------

    cached_user = get_cache(cache_key)

    if cached_user:

        print("Returned from Redis")

        return cached_user

    # ----------------------------
    # Cache miss
    # Query PostgreSQL
    # ----------------------------

    print("Returned from PostgreSQL")

    user = (
        db.query(models.User)
        .filter(models.User.id == id)
        .first()
    )

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    # ----------------------------
    # Convert SQLAlchemy object
    # into dictionary
    # ----------------------------

    user_data = schemas.UserOut.model_validate(
        user
    ).model_dump(mode="json")

    # ----------------------------
    # Save into Redis
    # ----------------------------

    set_cache(
        cache_key,
        user_data,
    )

    return user_data


@router.put("/{id}", response_model=schemas.UserOut)
def update_user(
    id: int,
    user: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    user_to_update = db.query(models.User).filter(models.User.id == id).first()

    if not user_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id: {id} was not found",
        )

    if user_to_update.id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized",
        )

    for key, value in user.model_dump(exclude_unset=True).items():
        setattr(user_to_update, key, value)

    db.commit()
    db.refresh(user_to_update)
    update_user_index(user_to_update)
    return user_to_update


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user),
):
    user_query = db.query(models.User).filter(models.User.id == id)
    user = user_query.first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id: {id} was not found",
        )

    if user.id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized",
        )

    user_query.delete(synchronize_session=False)
    db.commit()

    delete_cache(make_key("user", id))
    delete_user_index(id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put(
    "/{id}/profile-picture",
    response_model=schemas.UserOut,
)
async def upload_profile_picture(
        id: int,
        file: UploadFile = File(...),
        db: Session = Depends(get_db),
        current_user=Depends(oauth2.get_current_user),
    ):

    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Only images are allowed."
        )

    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} was not found")

    uploads_dir = "uploads/profile"
    contents = await file.read()
    from ..config import settings
    if settings.storage_backend == "cloudinary":
        public_id = f"profile/{id}_{uuid.uuid4()}"
        from app.cloudinary_client import upload_bytes
        _, url = upload_bytes(contents, public_id=public_id, folder="profile/images", resource_type="image")
        user.profile_picture = url
        user.profile_picture_mime = file.content_type
        user.profile_picture_size = len(contents)
    else:
        os.makedirs(uploads_dir, exist_ok=True)
        file_name = f"{id}_{os.path.basename(file.filename)}"
        file_path = os.path.join(uploads_dir, file_name)
        with open(file_path, "wb") as buffer:
            buffer.write(contents)
        user.profile_picture = file_path
        user.profile_picture_mime = file.content_type
        user.profile_picture_size = len(contents)

    db.commit()
    db.refresh(user)
    return user






