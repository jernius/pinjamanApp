# query.py

import psycopg2
from app.settings.config import Config

def get_db_connection():
    conn = psycopg2.connect(**Config.DATABASE_CONFIG)
    return conn
