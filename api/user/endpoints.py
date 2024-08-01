import os

from fastapi import APIRouter
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt


router = APIRouter(prefix="/user", tags=["User"])

crypt_context = CryptContext(schemes=["sha256_crypt"])


@router.post("/login")
async def login():
    exp = datetime.utcnow() + timedelta(days=23)

    payload = {"sub": os.getenv("SENHA"), "exp": exp}

    access_token = jwt.encode(payload, os.getenv("SECRET_KEY"), algorithm="HS256")
    return {"access_token": access_token, "exp": exp.isoformat(), "senha": os.getenv("SENHA")}
