from dtypes import api_response, internal_response
import jwt
from config import config

def validate_signature(sig) -> api_response | internal_response:
    try:
        decoded=jwt.decode(sig, config.get("JWT_SECRET"), algorithms=["HS256"])
        return decoded, 200
    except Exception as e:
        return {'message': 'Authentication failed'}, 401