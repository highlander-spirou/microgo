from sqlalchemy import create_engine, text

uri = "mysql+mysqlconnector://root:secret@localhost:3306/authdb"

engine = create_engine(uri)

def get_user(username, pwd):
    with engine.connect() as connection:
        stmt = text("SELECT username FROM user WHERE username=:u and pwd=:p")
        result = connection.execute(stmt, {"u":username, "p": pwd}).one_or_none()
    if result is None:
        return {"message": "Authentication failed"}, 401
    else:
        return {"message": result[0]}, 200



get_user('Mập', 'Mập khùng')
