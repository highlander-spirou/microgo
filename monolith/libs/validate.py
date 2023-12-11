from dtypes import api_response
import jwt
from config import config

def validate_signature(sig) -> str | api_response:
    try:
        decoded=jwt.decode(sig, config.get("JWT_SECRET"), algorithms=["HS256"])
        return decoded
    except Exception as e:
        return 'Error', 401