from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session  
from ..database import get_db
from .. import models, schemas, oauth2
from app.permission import verify_owner
from app.notifications import (
    create_notification_for_comment,
    create_notification_for_reply,
)


router = APIRouter(
    prefix="/comments",
    tags=["Comments"] 
)

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.Comment
)
def create_comment(
    comment: schemas.CommentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user)
):

    # Make sure the post exists
    post = db.query(models.Post).filter(
        models.Post.id == comment.post_id
    ).first()

    if not post:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )

    new_comment = models.Comment(
        content=comment.content,
        post_id=comment.post_id,
        parent_comment_id=comment.parent_comment_id,
        owner_id=current_user.id,
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    # -------------------------
    # Notification Logic
    # -------------------------

    if new_comment.parent_comment_id:
        create_notification_for_reply(
            db=db,
            comment_id=new_comment.parent_comment_id,
            actor_id=current_user.id,
        )

    else:
        create_notification_for_comment(
            db=db,
            post_id=new_comment.post_id,
            actor_id=current_user.id,
        )

    db.refresh(new_comment)

    return new_comment



@router.get("/{id}", response_model=schemas.Comment)
def get_comment(id: int, db: Session = Depends(get_db), current_user: int   = Depends(oauth2.get_current_user)):
    comment = db.query(models.Comment).filter(models.Comment.id == id).first()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Comment with id: {id} was not found")
    return comment  




@router.put("/{id}", response_model=schemas.Comment)
def update_comment(id: int, updated_comment: schemas.CommentCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    comment_query = db.query(models.Comment).filter(models.Comment.id == id)
    update_comment = comment_query.first()

    if update_comment == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Comment with id: {id} does not exist")

    verify_owner(update_comment.owner_id, current_user)
    comment_query.update(updated_comment.dict(), synchronize_session=False)
    db.commit()
    return comment_query.first()


@router.delete("/{id}")
def delete_comment(id: int, db: Session = Depends(get_db), current_user: int    = Depends(oauth2.get_current_user)):
    comment_query = db.query(models.Comment).filter(models.Comment.id == id)
    comment = comment_query.first()

    if comment == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Comment with id: {id} does not exist")

    verify_owner(comment.owner_id, current_user)
    comment_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
