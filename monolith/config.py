from dotenv import dotenv_values

config = dotenv_values('.env')

jwt_secret = config.get('JWT_SECRET', 'afgasfjhasfkjhsjkaf')
access_user = config.get('ACCESS_USR', 'accessuser')
access_pwd = config.get('ACCESS_PWD', 'accesspwd')
mariadb_host = config.get('MARIADB_HOST', 'localhost')
mongodb_host = config.get('MONGODB_HOST', 'localhost')