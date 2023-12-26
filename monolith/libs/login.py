from dtypes import api_response
import jwt
from datetime import datetime, timedelta
from config import access_user, access_pwd, mariadb_host
from sqlalchemy import create_engine, text
from config import access_user, access_pwd, mariadb_host, jwt_secret

uri = f"mysql+mysqlconnector://{access_user}:{access_pwd}@{mariadb_host}:3306/authdb"

engine = create_engine(uri)

def get_user(username, pwd):
    with engine.connect() as connection:
        stmt = text("SELECT username FROM users WHERE username=:u and pwd=:p")
        result = connection.execute(stmt, {"u":username, "p": pwd}).one_or_none()
    
    return result
    


def createJWT(payload:str, secret):
    return jwt.encode({
        "username": payload,
        "exp": datetime.utcnow() + timedelta(minutes=100000),
        "iat": datetime.utcnow()
    }, key=secret)


def sign_user(username, pwd) -> api_response:
    """
    Return a signed JWT or error
    """
    result = get_user(username, pwd)
    if result is None:
        return ({"message": "Authentication failed"}, 401)
    return {"message": createJWT(result[0], jwt_secret)}, 200