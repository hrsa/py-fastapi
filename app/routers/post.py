from typing import List, Optional

from fastapi import status, HTTPException, Depends, Response, APIRouter
from sqlalchemy.orm import Session

from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(prefix="/posts")


@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    posts = (db.query(models.Post)
             .filter(models.Post.title.contains(search) | models.Post.content.contains(search))
             .order_by(models.Post.id)
             .limit(limit)
             .offset(skip)
             .all())
    return posts

@router.get("/my_posts")
def get_my_posts(db: Session = Depends(get_db),
                 current_user: schemas.UserResponse = Depends(oauth2.get_current_user)
                 ):
    posts = db.query(models.Post).filter(models.Post.author_id == current_user.id).all()
    if posts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"You have no posts, {current_user.name}!")

    return posts


@router.get("/{post_id}", response_model=schemas.PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} not found")
    return post


@router.put("/{post_id}", response_model=schemas.PostResponse)
def update_post(post_id: int, post: schemas.PostUpdate, db: Session = Depends(get_db),
                current_user: schemas.UserResponse = Depends(oauth2.get_current_user)):
    existing_post = find_post_and_check_ownership(current_user, db, post_id)

    existing_post.update(post.dict(exclude_unset=True))

    db.commit()

    return existing_post.first()


def find_post_and_check_ownership(current_user, db, post_id):
    existing_post = db.query(models.Post).filter(models.Post.id == post_id)
    if existing_post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} not found")
    if existing_post.first().author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"That's not your post, {current_user.name}!")
    return existing_post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate,
                db: Session = Depends(get_db),
                current_user: schemas.UserResponse = Depends(oauth2.get_current_user)
                ):
    new_post = models.Post(title=post.title, author_id=current_user.id, content=post.content, published=post.published,
                           rating=post.rating)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.delete("/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db),
                current_user: schemas.UserResponse = Depends(oauth2.get_current_user)
                ):
    post = find_post_and_check_ownership(current_user=current_user, db=db, post_id=post_id)
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
