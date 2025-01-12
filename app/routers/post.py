from typing import Annotated, Any
from fastapi import APIRouter, Depends, status, HTTPException 
from .. import models, oauth2
from ..database import get_db
from sqlalchemy import func 
from sqlalchemy.orm import Session
from  ..schemas import Post, PostCreate, PostOut

router = APIRouter(
    prefix="/posts"
)


# the list will allow us to get all the post 
@router.get("/", response_model = list[PostOut])
async def get_posts(current_user: Annotated[list[dict[dict[str, Any]]], Depends(oauth2.get_current_user)], 
                    db: Annotated[Session, Depends(get_db)], 
                    limit: int = 10, 
                    skip: int = 0, 
                    search: str | None = ""):  
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    posts = db.query(models.Post, 
                       func.count(models.Vote.post_id)
                       .label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Post)
def create_posts(post: PostCreate, 
                 db: Annotated[Session, Depends(get_db)], 
                 current_user: Annotated[int, Depends(oauth2.get_current_user)]): 
    # This unpacking the dictonary
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/{id}", response_model = PostOut)
async def get_post(id: str, 
                   db: Annotated[Session, Depends(get_db)], 
                   current_user: Annotated[int, Depends(oauth2.get_current_user)]): 
    #post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, 
                       func.count(models.Vote.post_id)
                       .label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    
    if not post: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id: {id} was not found")
    
    return post

@router.delete("/{id}")
async def delete_post(id: int, 
                      db: Annotated[Session, Depends(get_db)], 
                      current_user: Annotated[int, Depends(oauth2.get_current_user)]): 
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id: {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to perform requested action")
    post.delete(synchronize_session=False)
    db.commit()

@router.put("/{id}")
async def update_post(id: int, 
                      updated_post: PostCreate, db: Annotated[Session, Depends(get_db)], 
                      current_user: Annotated[int, Depends(oauth2.get_current_user)]): 
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            details="Not authorized to perform requested action")
    
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit
    return post_query.first()