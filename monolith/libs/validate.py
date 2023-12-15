from dtypes import Error
import jwt
from config import config
from typing import TypedDict

class JWTPayload(TypedDict):
    username:str

def validate_signature(sig):
    try:
        decoded:JWTPayload = jwt.decode(sig, config.get("JWT_SECRET"), algorithms=["HS256"])
        return decoded
    except Exception:
        return Error()