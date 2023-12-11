from flask import Flask, request
from sqlalchemy import create_engine, text, TextClause
import jwt
from datetime import datetime, timedelta
from dotenv import dotenv_values


config = dotenv_values('./.env')


app = Flask(__name__)


connection_string = "mysql+mysqlconnector://user1:pscale_pw_abc123@us-east.connect.psdb.cloud:3306/sqlalchemy"
engine = create_engine(connection_string)




def createJWT(payload, secret, is_admin):
    return jwt.encode({
        "username": payload,
        "is_admin": is_admin,
        "exp": datetime.utcnow() + timedelta(minutes=1),
        "iat": datetime.utcnow()
    }, key=secret)


@app.route('/login', methods=['POST'])
def login_ctrl():
    auth = request.authorization
    if not auth:
        return "missing credentials", 401
    t = text("SELECT username, password FROM user WHERE username=:username")
    with engine.connect() as connection:
        cur = connection.execute(t, username=auth.username)
    result = cur.one_or_none()
    if auth.password != result[1]:
        return "Wrong password", 401
    else:
        return createJWT(auth.username, config.get('JWT_SECRET'), True)

@app.route('/validate', methods=['POST'])
def validate_ctrl():
    token = request.headers["Authorization"].split(" ")[1]
    if not token:
        return {
            "message": "Authentication Token is missing!",
            "data": None,
            "error": "Unauthorized"
            }, 401
    try:
        decoded=jwt.decode(token, config["JWT_SECRET"], algorithms=["HS256"])
        return decoded
    except Exception as e:
        return "Not authorized", 403

if __name__ == '__main__':
    app.run("0.0.0.0")