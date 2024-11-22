import psycopg2
import os

DATABASE_CONFIG = {
    'dbname': 'Employee',
    'user': 'postgres',
    'password': '123456',
    'host': 'localhost',
    'port': 5432
}

def get_db_connection():
    conn = psycopg2.connect(**DATABASE_CONFIG)
    return conn