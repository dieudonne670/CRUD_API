from typing import List, Optional


from app import oauth2
from sqlalchemy import func 
from .. import models, schemas
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app.permission import verify_owner
from app.redis_cache import(get_cache, set_cache,
    delete_cache,
    make_key,)

from ..database import get_db
from app.elastic_sync import (
    sync_post,
    update_post,
    delete_post,
)

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]#tags are used to group the endpoints in the documentation
)




@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), 
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    cache_key = make_key("posts", limit, skip, search or "")

    cached_posts = get_cache(cache_key)

    if cached_posts:
        print("Returned from Redis")
        return cached_posts

    print("Returned from PostgreSQL")

    posts = (
        db.query(models.Post, func.count(models.Vote.post_id).label("vote"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.title.contains(search or ""))
        .limit(limit)
        .offset(skip)
        .all()
    )

    post_data = []
    for post, vote in posts:
        post_payload = schemas.Post.model_validate(post).model_dump(mode="json")
        post_data.append({"Post": post_payload, "vote": vote})

    set_cache(cache_key, post_data)
    return post_data

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
 
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    # -------------------------------
# Sync Elasticsearch
# -------------------------------

    sync_post(new_post)
    return new_post



@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    print(current_user.id)

    cache_key = make_key("post", id)

    cached_post = get_cache(cache_key)

    if cached_post:
        print("Returned from Redis")
        return cached_post

    print("Returned from PostgreSQL")

    post = (
        db.query(models.Post, func.count(models.Vote.post_id).label("vote"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.id == id)
        .first()
    )

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")

    post_obj, vote = post
    post_payload = schemas.Post.model_validate(post_obj).model_dump(mode="json")
    post_data = {"Post": post_payload, "vote": vote}

    set_cache(cache_key, post_data)
    return post_data

@router.delete("/{id}")
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    print(current_user.id)
    post_query = db.query(models.Post).filter(models.Post.id == id )
    post = post_query.first()
      
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} is deleted")
    #this is to make sure the owner  login as according to owner id 
    verify_owner(post.owner_id, current_user.id)

    post_query.delete(synchronize_session=False)
    db.commit()
    delete_post(post_query)
    return Response(status_code=status.HTTP_204_NO_CONTENT)





@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostUpdate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    print(current_user.id)
    post_query = db.query(models.Post).filter(models.Post.id == id)
    update_post = post_query.first()
    
    if update_post ==  None:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    verify_owner(update_post.owner_id, current_user)

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    update_post(post_query)
    return post_query.first()
    

    