# config.py

import os
# from dotenv import load_dotenv

# load_dotenv()

class Config:
    # Database configuration
    # HOST = os.getenv('HOST')
    # DATABASE = os.getenv('DATABASE')
    # USER_POSTGRES_DB = os.getenv('USER_POSTGRES_DB')
    # PASSWORD_POSTGRES_DB = os.getenv('PASSWORD_POSTGRES_DB')

    # HOST='localhost'
    # DATABASE='postgres'
    # USER_POSTGRES_DB='postgres'
    # PASSWORD_POSTGRES_DB='123456'
    HOST='localhost'
    DATABASE='jernsync_postgres'
    USER_POSTGRES_DB='jernsync_jer'
    PASSWORD_POSTGRES_DB='jerzend09'

    DATABASE_CONFIG = {
        'host': HOST,
        'database': DATABASE,
        'user': USER_POSTGRES_DB,
        'password': PASSWORD_POSTGRES_DB,
    }