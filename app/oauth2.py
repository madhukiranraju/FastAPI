from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from . import schemas, database, Model
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .database import get_db
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

#Secret key
# this can be "Hello World" but should be more complex and random in real applications
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm #algorithm used to hash the token 
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes  #token expiry time in minutes


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verifyaccesstoken(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        payload_id = payload.get("user_id")
        if payload_id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=payload_id)
        return payload_id
    except JWTError:
        raise credentials_exception
    
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = verifyaccesstoken(token, credentials_exception)
    user = db.query(Model.User).filter(Model.User.id == token).first()
    return user

    # user_id = verifyaccesstoken(token, credentials_exception)
    # return user_id
