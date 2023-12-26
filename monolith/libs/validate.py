from dtypes import Error
import jwt
from config import jwt_secret
from typing import TypedDict

class JWTPayload(TypedDict):
    username:str

def validate_signature(sig):
    try:
        decoded:JWTPayload = jwt.decode(sig, jwt_secret, algorithms=["HS256"])
        return decoded
    except Exception:
        return Error()
