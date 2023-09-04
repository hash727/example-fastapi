from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from . import schemas, database, models
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# SECRET_KEY = "4806fc9919e9b3691c81b048bb1090475fd02644484434c05d319b76515f522c"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

SECRET_KEY = settings.secrete_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    
    to_encode = data.copy()
    
    expiry = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expiry})
    
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encode_jwt

def very_access_token(token: str, credential_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = payload.get("user_id")
        id = str(id)
        #print(type(id))
        if id is None:
            raise credential_exception
    
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credential_exception
    
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db:Session = Depends(database.get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Unauthorized access !", headers={"WWW-Authenticate":"Bearer"})
    token = very_access_token(token, credential_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user