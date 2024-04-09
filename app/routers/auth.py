from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from .. import models, oauth2, schemas
from app.schemas import UserLogin
from app.utils import verify

router = APIRouter(prefix="/auth")


@router.post("/login", status_code=status.HTTP_200_OK, response_model=schemas.Token)
def login(login_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == login_data.username).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not found")

    if verify(login_data.password, user.password) is False:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect password")

    # create a token
    token = oauth2.create_access_token(data={"user_id": user.id, "email": user.email})

    return {"access_token": token, "token_type": "bearer"}
