from sqlalchemy import create_engine, text

uri = "mysql+mysqlconnector://root:secret@localhost:3306/authdb"

engine = create_engine(uri)

# Test the connection
try:
    with engine.connect() as connection:
        re = connection.execute(text("SELECT * FROM user"))
        print(re.fetchall())
    
except Exception as e:
    print(f"Error connecting to MariaDB: {e}")
