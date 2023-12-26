from sqlalchemy import create_engine, text

uri = "mysql+mysqlconnector://accessuser:accesspwd@localhost:3306/authdb"

engine = create_engine(uri)

def get_user(username, pwd):
    with engine.connect() as connection:
        stmt = text("SELECT username FROM users WHERE username=:u and pwd=:p")
        result = connection.execute(stmt, {"u":username, "p": pwd}).one_or_none()
    if result is None:
        print({"message": "Authentication failed"}, 401)
    else:
        print({"message": result[0]}, 200)



get_user('Mập', 'Mập khùng')
