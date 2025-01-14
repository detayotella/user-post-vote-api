import os 
from dotenv import load_dotenv
from typing import Annotated
from fastapi import Depends, status, HTTPException 
from fastapi.security import OAuth2PasswordBearer
import jwt 
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, timezone
from . import schemas, database, models
from sqlalchemy.orm import Session

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict, expires_delta: timedelta | None = None): 
    to_encode = data.copy()

    if expires_delta: 
        expire = datetime.now(timezone.utc) + expires_delta
    else: 
        expire = datetime.now(timezone.utc) + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception): 
    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: int = payload.get("user_id")
        if id is None: 
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except InvalidTokenError: 
        raise credentials_exception
    
    return token_data
    
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], 
                           db: Annotated[Session, Depends(database.get_db)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail=f"Could not validate credentials", 
        headers={"WWW-Authenticate": "Bearer"}
    )
    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    
    return user 

