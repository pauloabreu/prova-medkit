import os

from fastapi import Request, HTTPException, status
from jose import jwt, JWTError

from dotenv import load_dotenv

load_dotenv()


async def auth_user(request: Request):
    authorization = request.headers.get("Authorization")
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You need pass access token")

    if not authorization.startswith("Bearer "):
        raise ValueError("Invalid token")

    return await verify_token(authorization[len("Bearer "):])


async def verify_token(access_token):
    try:
        data = jwt.decode(access_token, os.getenv("SECRET_KEY"), algorithms=["HS256"])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token")

    if data["sub"] != os.getenv("SENHA"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token")
