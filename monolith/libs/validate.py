from dtypes import api_response
import jwt
from config import config

def validate_signature(sig) -> str | api_response:
    print('asfkjhasfkjhaksjfhk')
    # try:
    decoded=jwt.decode(sig, config.get("JWT_SECRET"), algorithms=["HS256"])
    print('decoded', decoded)
    return decoded
    # except Exception as e:
    #     return 'Error', 401
        # pass
    # if sig != 'signed JWT with user sth':