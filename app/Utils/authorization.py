from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.Utils.config import settings, pwd_context
from app.Utils.database import get_database

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

PrivateKeyPath = "private_key.pem"  # Should be stored more securely
PublicKeyPath = "public_key.pem"  # Should be stored at Client's end


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    with open(PrivateKeyPath) as private_file:
        private_key = private_file.read()
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(hours=1)
    to_encode.update({"exp": expire.timestamp()})
    encoded_jwt = jwt.encode(to_encode, private_key, settings.algorithm)
    return encoded_jwt


async def authenticate_user(db, username: str, password: str):
    user = await db.get_collection("users").find_one({"username": username})
    if not user:
        return False
    if not verify_password(password, user["hashed_password"]):
        return False
    return user

async def get_current_user(token: str = Depends(oauth2_scheme), db=Depends(get_database)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username: str = payload.get("sub", "")
        if not username:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await db.get_collection("users").find_one({"username": username})
    if user is None:
        raise credentials_exception
    return user

async def verify_token(token: str = Depends(oauth2_scheme), db=Depends(get_database)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        with open(PublicKeyPath) as public_key:
            public_key = public_key.read()
        payload = jwt.decode(token, public_key, algorithms=[settings.algorithm])
    except jwt.ExpiredSignatureError:
        print("Token has expired.")
        raise credentials_exception
    except jwt.InvalidTokenError:
        print("Invalid token.")
        raise credentials_exception
    username: str = payload.get("sub")
    user = await db.get_collection("users").find_one({"username": username})
    if user is None:
        raise credentials_exception
    return user
