from sqlalchemy import create_engine, text

uri = "mysql+mysqlconnector://root:secret@localhost:3306/authdb"
engine = create_engine(uri)
print('Check for MariaDB connection ...')

with engine.connect() as conn:
    print('MariaDB connection success')

    print('test query')
    a = conn.execute(text('show tables'))
    print(a.all())
# except Exception:
#     print('Cannot connect to MariaDB, closing the server ...')
#     exit()