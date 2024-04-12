from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(prefix="/votes", tags=["Votes"])


@router.post("/", response_model=schemas.VoteResponse)
def create_vote(vote: schemas.Vote, db: Session = Depends(get_db),
                current_user: schemas.UserResponse = Depends(oauth2.get_current_user)):
    existing_vote = db.query(models.Vote).filter(
        (models.Vote.post_id == vote.post_id) & (models.Vote.user_id == current_user.id)).first()

    if vote.value == 1:
        if existing_vote is None:
            post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
            if post is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="That post was not found")

            db.add(models.Vote(user_id=current_user.id, post_id=vote.post_id))
            message = "Vote added"
            db.commit()
        else:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"You voted already, {current_user.name}!")
    else:
        if existing_vote is not None:
            db.delete(existing_vote)
            message = "Vote deleted"
            db.commit()
        else:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Your vote has already been deleted!")

    return {"status": message, "post_id": vote.post_id, "user_id": current_user.id}
