import os
import psycopg2
from flask import Flask

def get_db_connection():
    conn_string = os.getenv('POSTGRES_URL')
    if not conn_string:
        raise ValueError("Database connection string not found in environment variables")
    return psycopg2.connect(conn_string)

def create_app():
    app = Flask(__name__)
    return app
