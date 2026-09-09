from .. import models, schemas, utils, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from app.permission import verify_owner
from app.notifications import create_notification_for_follow

router = APIRouter(
    prefix="/followers",
    tags=["Followers"]
)   

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Follow)
def create_follow(
    follow: schemas.FollowCreate,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user)


):

    if follow.following_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot follow yourself."
        )

    existing_follow = db.query(models.Follows).filter(
        models.Follows.follower_id == current_user.id,
        models.Follows.following_id == follow.following_id
    ).first()

    if existing_follow:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Already following this user."
        )

    new_follow = models.Follows(
        follower_id=current_user.id,
        following_id=follow.following_id
    )

    db.add(new_follow)
    db.commit()
    db.refresh(new_follow)

    create_notification_for_follow(
        db=db,
        following_id=new_follow.following_id,
        actor_id=current_user.id,
    )

    return new_follow

@router.get("/{id}", response_model=schemas.Follow)
def get_follow(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user)
):

    follow = db.query(models.Follows).filter(
        models.Follows.id == id
    ).first()

    if not follow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Follow relationship not found."
        )

    return follow

@router.delete("/{following_id}", status_code=status.HTTP_204_NO_CONTENT)
def unfollow_user(
    following_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user)
):

    follow_query = db.query(models.Follows).filter(
        models.Follows.follower_id == current_user.id,
        models.Follows.following_id == following_id
    )

    follow = follow_query.first()

    if not follow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="You are not following this user."
        )

    follow_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
