from dataclasses import dataclass
from dtypes import api_response
import jwt
from datetime import datetime, timedelta
from config import config
@dataclass
class User:
    username = "Mập"
    pwd = "Mập ngu"
    is_admin = True

    def query(self, username):
        if username != self.username:
            raise Exception("Cannot found user")
        return self


db = User()


def createJWT(payload:User, secret):
    return jwt.encode({
        "username": payload.username,
        "is_admin": payload.is_admin,
        "exp": datetime.utcnow() + timedelta(minutes=1),
        "iat": datetime.utcnow()
    }, key=secret)

def sign_user(username, pwd) -> api_response:
    """
    Return a signed JWT or error
    """
    try:
        user = db.query(username)
        if pwd != user.pwd:
            return ({"message": "Wrong password"}, 401)
        
        
        return {"message": createJWT(user, config.get('JWT_SECRET'))}, 200
    except Exception as e:
        return ({"message": "User not found"}, 401)