from sqlalchemy import create_engine, text

uri = "mysql+mysqlconnector://accessuser:accesspwd@localhost:3306/authdb"
engine = create_engine(uri)
print('Check for MariaDB connection ...')

with engine.connect() as conn:
    print('MariaDB connection success')

    print('test query')
    a = conn.execute(text('select * from user'))
    print(a.all())

    print('test drop')
    a = conn.execute(text('drop table user'))
# except Exception:
#     print('Cannot connect to MariaDB, closing the server ...')
#     exit()