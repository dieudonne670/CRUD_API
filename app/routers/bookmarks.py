from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session  
from ..database import get_db
from .. import models, schemas, oauth2
from app.permission import verify_owner



router = APIRouter(
    prefix="/bookmarks",    
    tags=["Bookmarks"]
)

@router.post("/", status_code=status.HTTP_201_CREATED,
             response_model=schemas.Bookmark)
def create_bookmark(
        bookmark: schemas.BookmarkCreate,
        db: Session = Depends(get_db),
        current_user=Depends(oauth2.get_current_user)
):

    # Check the post exists
    post = db.query(models.Post).filter(
        models.Post.id == bookmark.post_id
    ).first()

    if not post:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )

    # Prevent duplicate bookmarks
    existing = db.query(models.Bookmark).filter(
        models.Bookmark.user_id == current_user.id,
        models.Bookmark.post_id == bookmark.post_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Post already bookmarked."
        )

    new_bookmark = models.Bookmark(
        user_id=current_user.id,
        post_id=bookmark.post_id
    )

    db.add(new_bookmark)
    db.commit()
    db.refresh(new_bookmark)

    return new_bookmark


@router.get("/", response_model=list[schemas.Bookmark])
def get_my_bookmarks(
        db: Session = Depends(get_db),
        current_user=Depends(oauth2.get_current_user)
):

    bookmarks = db.query(models.Bookmark).filter(
        models.Bookmark.user_id == current_user.id
    ).all()

    return bookmarks


@router.delete("/{post_id}",
               status_code=status.HTTP_204_NO_CONTENT)
def delete_bookmark(
        post_id: int,
        db: Session = Depends(get_db),
        current_user=Depends(oauth2.get_current_user)
):

    bookmark_query = db.query(models.Bookmark).filter(
        models.Bookmark.user_id == current_user.id,
        models.Bookmark.post_id == post_id
    )

    bookmark = bookmark_query.first()

    if not bookmark:
        raise HTTPException(
            status_code=404,
            detail="Bookmark not found."
        )

    bookmark_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)