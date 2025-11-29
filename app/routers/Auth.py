from fastapi import APIRouter, Depends, HTTPException, Response, status, Body
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, Model, utils, oauth2

from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    tags=["Authentication"]
)

@router.post("/login", response_model=schemas.Token)
# implementing login with OAuth2 and JWT tokens
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(Model.User).filter(Model.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials"
        )   
    if not utils.verify_password(user_credentials.password, user.password): # type: ignore
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials"
        )
    
    
    # create a token and return it
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}

# General way to implement login (without OAuth2 and with JWT tokens)
# async def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
#     user = db.query(Model.User).filter(Model.User.email == user_credentials.email).first()
#     hashed_password_from_db: str = user.password  #ignore mypy warning
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Invalid Credentials"
#         )   
#     if not utils.verify_password(user_credentials.password, hashed_password_from_db):
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Invalid Credentials"
#         )
    
    
#     # create a token and return it
#     access_token = oauth2.create_access_token(data={"user_id": user.id})
#     return {"access_token": access_token, "token_type": "bearer"}
